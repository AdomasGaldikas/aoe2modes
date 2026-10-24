"""Use XS for conditions whose native player selectors fail in sparse DE lobbies.

Live P1/P3/P5/P8 testing showed that native effects still address scenario colors,
but native Objects in Area and resource conditions do not recognize P5/P8. Keep
effects in their native domain and resolve condition owners in the XS domain.
"""

from AoE2ScenarioParser.datasets.buildings import BuildingInfo
from AoE2ScenarioParser.datasets.conditions import ConditionId


def configure_runtime_conditions(ctx, *, identity_resource, identity_tag):
    """Replace Castle, defeat and identity-token conditions; return embedded XS.

    Castle references are taken after map generation. They deliberately count only
    the four starting Castles, so a replacement building cannot revive a lost base.
    """
    rows = {}
    for color in range(1, 9):
        castles = [u for u in ctx.um.units[color] if u.unit_const == BuildingInfo.CASTLE.ID]
        if len(castles) != 4:
            raise RuntimeError(f"P{color}: expected four starting Castles, found {len(castles)}")
        area = (
            int(min(u.x for u in castles)), int(min(u.y for u in castles)),
            int(max(u.x for u in castles)), int(max(u.y for u in castles)),
        )
        if area in rows:
            raise RuntimeError(f"overlapping Castle row bounds: {area}")
        rows[area] = tuple(sorted(u.reference_id for u in castles))

    functions = {}
    replaced = 0
    for trigger in ctx.tm.triggers:
        conditions = []
        for condition in list(trigger.conditions):
            kind = condition.condition_type
            source = condition.source_player
            key = None
            body = None
            if kind == ConditionId.OBJECTS_IN_AREA and condition.object_list == BuildingInfo.CASTLE.ID:
                area = (condition.area_x1, condition.area_y1, condition.area_x2, condition.area_y2)
                refs = rows.get(area)
                if refs is not None:
                    key = ("castle", area, source, condition.quantity, condition.inverted)
                    lines = [f"int owner = xsGetWorldPlayerId({source});", "int count = 0;"]
                    for ref in refs:
                        lines.append(
                            f"if (owner > 0 && xsDoesUnitExist({ref}) && "
                            f"xsGetUnitHitpoints({ref}) > 0 && xsGetUnitOwner({ref}) == owner) "
                            "{ count = count + 1; }"
                        )
                    operator = "<" if condition.inverted == 1 else ">="
                    lines.append(f"return(count {operator} {condition.quantity});")
                    body = " ".join(lines)
            elif kind == ConditionId.PLAYER_DEFEATED and 1 <= source <= 8:
                key = ("defeated", source, condition.inverted)
                alive = "(owner > 0 && xsGetPlayerInGame(owner))"
                result = alive if condition.inverted == 1 else f"{alive} == false"
                body = f"int owner = xsGetWorldPlayerId({source}); return({result});"
            elif (
                kind == ConditionId.ACCUMULATE_ATTRIBUTE
                and condition.attribute == identity_resource
                and trigger.name.startswith("Color XS Identity ")
            ):
                if condition.quantity not in (identity_tag + 1, identity_tag + 9):
                    raise RuntimeError(f"unexpected identity boundary in {trigger.name}")
                key = ("identity", source, condition.quantity, condition.inverted)
                operator = "<" if condition.inverted == 1 else ">="
                body = (
                    f"int owner = xsGetWorldPlayerId({source}); "
                    f"return(owner > 0 && xsPlayerAttribute(owner, {identity_resource}) "
                    f"{operator} {condition.quantity});"
                )
            if key is None:
                conditions.append(condition)
                continue
            if key not in functions:
                functions[key] = (f"cbaRuntimeCondition{len(functions)}", body)
            replacement = trigger.new_condition.script_call(xs_function=functions[key][0])
            conditions.append(replacement)
            replaced += 1
        trigger.conditions = conditions
        # Parser 0.8.4 caches the previous condition hash. Explicit ordering avoids
        # an empty display-order array after rebuilding an unchanged condition list.
        trigger.condition_order = list(range(len(conditions)))
    _assert_sweep_is_complete(ctx, identity_resource)
    ctx.log(f"resolved {replaced} native conditions through {len(functions)} XS guards")
    return "\n".join(f"bool {name}() {{ {body} }}" for name, body in functions.values())


def _assert_sweep_is_complete(ctx, identity_resource) -> None:
    """Fail the build if a condition this pass owns survived in the native domain.

    Castle rows are matched by exact area bounds, so a one-tile geometry change would
    silently restore the live sparse-lobby defect (ASC-049) instead of raising here.
    GAIA selectors stay native on purpose: ``player_defeated`` on GAIA is the
    never-true condition that keeps an Objectives row displayed.
    """
    survivors = []
    for trigger in ctx.tm.triggers:
        for condition in trigger.conditions:
            kind = condition.condition_type
            source = condition.source_player
            if not 1 <= source <= 8:
                continue
            if kind == ConditionId.OBJECTS_IN_AREA and condition.object_list == BuildingInfo.CASTLE.ID:
                survivors.append(f"{trigger.name}: Castle row for P{source}")
            elif kind == ConditionId.PLAYER_DEFEATED:
                survivors.append(f"{trigger.name}: Player Defeated P{source}")
            elif (
                kind == ConditionId.ACCUMULATE_ATTRIBUTE
                and condition.attribute == identity_resource
                and trigger.name.startswith("Color XS Identity ")
            ):
                survivors.append(f"{trigger.name}: identity token for P{source}")
    if survivors:
        raise RuntimeError(
            f"{len(survivors)} native conditions escaped the sparse-lobby sweep: "
            + "; ".join(survivors[:5])
        )
