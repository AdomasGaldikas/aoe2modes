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
        for token in re.split(r"([{};])", body):
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
