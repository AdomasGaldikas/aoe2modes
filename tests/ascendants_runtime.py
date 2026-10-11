"""Inspect and execute the small generated XS guard subset in regression tests.

This is a syntax translator with mocked XS API calls, not a DE emulator. The
logical descriptors are for structural assertions only; state-machine tests run
the emitted function bodies so broken owner conversion cannot pass unnoticed.
"""

import re
from functools import lru_cache
from types import SimpleNamespace

from AoE2ScenarioParser.datasets.buildings import BuildingInfo
from AoE2ScenarioParser.datasets.conditions import ConditionId
from AoE2ScenarioParser.datasets.effects import EffectId


@lru_cache(maxsize=4)
def xs_source(scenario):
    return next(t for t in scenario.trigger_manager.triggers if t.name == "XS SCRIPT").effects[0].message


@lru_cache(maxsize=4)
def guard_bodies(xs):
    return dict(re.findall(r"bool (cbaRuntimeCondition\d+)\(\) \{ ([^\n]+) \}", xs))


@lru_cache(maxsize=4)
def unit_index(scenario):
    return {u.reference_id: u for row in scenario.unit_manager.units for u in row}


def logical_conditions(scenario, trigger):
    """Decode emitted guards into their logical predicates for shape assertions."""
    bodies = guard_bodies(xs_source(scenario))
    units = unit_index(scenario)
    for condition in trigger.conditions:
        if condition.condition_type != ConditionId.SCRIPT_CALL:
            yield condition
            continue
        body = bodies.get(condition.xs_function)
        if body is None:
            yield condition
            continue
        owner = int(re.search(r"int owner = xsGetWorldPlayerId\((\d+)\)", body)[1])
        if "int count = 0;" in body:
            refs = [int(ref) for ref in re.findall(r"xsGetUnitOwner\((\d+)\)", body)]
            assert len(refs) == len(set(refs)) == 4
            castles = [units[ref] for ref in refs]
            operator, quantity = re.search(r"return\(count (<|>=) (\d+)\);", body).groups()
            yield SimpleNamespace(
                condition_type=ConditionId.OBJECTS_IN_AREA, source_player=owner,
                object_list=BuildingInfo.CASTLE.ID, object_group=-1, object_type=-1,
                quantity=int(quantity), inverted=int(operator == "<"),
                area_x1=int(min(u.x for u in castles)), area_y1=int(min(u.y for u in castles)),
                area_x2=int(max(u.x for u in castles)), area_y2=int(max(u.y for u in castles)),
            )
        elif "xsGetPlayerInGame" in body:
            yield SimpleNamespace(
                condition_type=ConditionId.PLAYER_DEFEATED, source_player=owner,
                inverted=int("== false" not in body),
            )
        else:
            resource, operator, quantity = re.search(
                r"xsPlayerAttribute\(owner, (\d+)\) (<|>=) (\d+)", body,
            ).groups()
            yield SimpleNamespace(
                condition_type=ConditionId.ACCUMULATE_ATTRIBUTE, source_player=owner,
                attribute=int(resource), quantity=int(quantity), inverted=int(operator == "<"),
            )


@lru_cache(maxsize=4)
def compiled_guards(xs):
    """Translate declarations, assignments, if blocks and return expressions."""
    lines = []
    for name, body in guard_bodies(xs).items():
        lines.append(f"def {name}():")
        indent = 1
        for token in re.split(r'([{};])(?=(?:[^"]*"[^"]*")*[^"]*$)', body):
            token = token.strip()
            if not token or token == ";":
                continue
            if token == "{":
                indent += 1
                continue
            if token == "}":
                indent -= 1
                continue
            token = token.replace("&&", "and").replace("||", "or")
            token = re.sub(r"\bfalse\b", "False", token)
            token = re.sub(r"\btrue\b", "True", token)
            if token.startswith("int "):
                token = token[4:]
            elif token.startswith("if (") and token.endswith(")"):
                token = f"if {token[4:-1]}:"
            else:
                assert token.startswith(("return(", "count = ")), token
            lines.append("    " * indent + token)
        assert indent == 1
    return compile("\n".join(lines), "<emitted XS runtime guards>", "exec")


def guard_runtime(scenario, **api):
    namespace = dict(api)
    exec(compiled_guards(xs_source(scenario)), namespace)
    return {name: namespace[name] for name in guard_bodies(xs_source(scenario))}


@lru_cache(maxsize=4)
def birth_descriptors(scenario):
    """Decode zero-argument wrappers for roster/geometry assertions only."""
    return {
        name: (family, int(color), int(unit), int(x), int(y), sound == "false")
        for name, family, color, unit, x, y, sound in re.findall(
            r"void (cbaBirth(?:Hero|Builder)\d+)\(\) \{ cbaCreate(Hero|Builder)Birth"
            r"\((\d+), (\d+), (\d+), (\d+), (true|false)\); \}", xs_source(scenario),
        )
    }


def logical_effects(scenario, trigger):
    """Represent converted births as logical creates, without inventing task effects.

    The source_player describes the trigger's selector. The runtime tests below
    execute the emitted code and verify creation uses the separate XS token.
    """
    descriptors = birth_descriptors(scenario)
    for effect in trigger.effects:
        descriptor = descriptors.get(effect.message) if effect.effect_type == EffectId.SCRIPT_CALL else None
        if descriptor is None:
            yield effect
        else:
            _, _, unit, x, y, disable_sound = descriptor
            owner = int(re.search(r" W([1-8])", trigger.name)[1])
            yield SimpleNamespace(
                effect_type=EffectId.CREATE_OBJECT, source_player=owner,
                object_list_unit_id=unit, location_x=x, location_y=y, disable_sound=int(disable_sound),
                area_x1=-1, area_y1=-1, area_x2=-1, area_y2=-1,
            )


@lru_cache(maxsize=4)
def compiled_births(xs):
    """Translate the emitted birth subset, rejecting unsupported syntax.

    API mocks supply creation references and capture actual xsTaskUnits arguments.
    This does not simulate pathfinding or DE's scheduling.
    """
    names = (r"cba(?:WorldPlayerForColor|OrderBirth|OrderArmyBirth|CreateHeroBirth|"
             r"CreateBuilderBirth|CreateWave|BirthHero\d+|BirthBuilder\d+|PopulationCost|PopulationUsed|"
             r"HasPopulationRoom|PopulationColorActive|ClaimPopulationChooser|UpdatePopulationSetup|PopulationGate\d+)")
    lines = []
    for match in re.finditer(r"(?:void|int|bool|float) (" + names + r")\((.*?)\) \{", xs, re.S):
        name, parameters = match.groups()
        args = re.findall(r"(?:int|bool|vector|float) (\w+)\s*=", parameters)
        lines.append(f"def {name}({', '.join(args)}):")
        start = match.end()
        depth, end = 1, start
        while depth:
            depth += (xs[end] == "{") - (xs[end] == "}")
            end += 1
        body = re.sub(r"//[^\n]*", "", xs[start:end - 1])
        lines.append("    global gCbaPopulationLimit, gCbaPopulationOwner, gCbaPopulationLocked")
        indent = 1
        for token in re.split(r'([{};])(?=(?:[^"]*"[^"]*")*[^"]*$)', body):
            token = " ".join(token.split())
            if not token or token == ";":
                continue
            if token == "{":
                indent += 1
                continue
            if token == "}":
                indent -= 1
                continue
            token = token.replace("&&", "and").replace("||", "or")
            token = re.sub(r"\bfalse\b", "False", token)
            token = re.sub(r"\btrue\b", "True", token)
            if token.startswith("else if (") and token.endswith(")"):
                token = f"elif {token[9:-1]}:"
            elif token.startswith("if ("):
                depth, close = 1, 4
                while depth:
                    depth += (token[close] == "(") - (token[close] == ")")
                    close += 1
                expression, statement = token[4:close - 1], token[close:].strip()
                token = f"if {expression}:" + (f" {statement}" if statement else "")
            else:
                token = re.sub(r"^(int|bool|float|vector) ", "", token)
                assert token.startswith((
                    "return", "worldPlayer =", "level =", "unitRef =", "created =",
                    "owner =", "used =", "cost =", "candidate =", "position =", "x =", "y =",
                    "reserve =", "room =", "previous =", "gCbaPopulation", "xsSetUnitProperty(",
                    "xsRemoveUnit(", "xsDisplayInstructions(", "xsSetPlayerAttribute(", "xsChatData(",
                    "cbaClaimPopulationChooser(",
                    "xsArraySetInt(", "xsTaskUnits(", "xsSetTriggerVariable(",
                    "cbaOrderBirth(", "cbaOrderArmyBirth(", "cbaCreateHeroBirth(", "cbaCreateBuilderBirth(",
                )), token
            token = token.replace(' + gCbaPopulationLimit,', ' + str(gCbaPopulationLimit),')
            lines.append("    " * indent + token)
        assert indent == 1
    return compile("\n".join(lines), "<emitted XS birth orders>", "exec")


def birth_runtime(scenario, **api):
    namespace = {
        "gCbaBirthOrderUnit": 70000, "gCbaPopulationLimit": 250,
        "gCbaPopulationOwner": 0, "gCbaPopulationLocked": False,
        "cAttributePopulation": 11, "cPopulation": 21, "cAttributeUnitLimit": 32,
        "xsGetObjectAttribute": lambda *args: -1,
        "xsPlayerAttribute": lambda *args: 1, **api,
    }
    namespace.update({name: int(value) for name, value in
                      re.findall(r"const int (CBA_UNIT_\w+) = (\d+);", xs_source(scenario))})
    exec(compiled_births(xs_source(scenario)), namespace)
    return namespace



def birth_destination(scenario, family, color, level=1, slot=0, unit_id=83):
    """Execute an emitted order and return its integer destination cell."""
    from collections import defaultdict

    variables = defaultdict(int, {137 + color - 1: 1007, 121 + color - 1: 1,
                                 89 + color - 1: level, 113 + color - 1: level})
    selected, orders = {}, []
    runtime = birth_runtime(
        scenario, xsTriggerVariable=lambda var: variables[var],
        xsCreateUnit=lambda *args: 91234, xsDoesUnitExist=lambda ref: ref == 91234,
        xsArraySetInt=lambda array, index, ref: selected.update({index: ref}),
        xsTaskUnits=lambda *args: orders.append(args),
        xsVectorSet=lambda x, y, z: (x, y), vector=lambda x, y, z: (x, y),
    )
    if family == "Army":
        runtime["cbaOrderArmyBirth"](color, slot, 91234)
    else:
        runtime[f"cbaCreate{family}Birth"](color, unit_id, 1, 1, False)
    assert len(orders) == 1 and selected == {0: 91234}
    assert orders[0][1] == 1  # Move, per DE's ActionType enum.
    x, y = orders[0][2]
    assert x % 1 == y % 1 == 0.5
    return int(x), int(y)
