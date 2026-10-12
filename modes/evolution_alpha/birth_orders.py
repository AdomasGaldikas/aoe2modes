"""Issue orders by the reference returned by creation, never by a capture area.

DE 185872 supplies xsTaskUnits. A one-element array is reused for each immediate
birth order; no queues, scans, later movement pulse, or trigger/XS identity mixing
are needed. Returning units on a spawn cell keep their player-issued orders.
"""

import re

from AoE2ScenarioParser.datasets.effects import EffectId
from AoE2ScenarioParser.datasets.trigger_lists import Comparison


def configure_birth_orders(ctx, *, identity_base, identity_tag):
    """Convert Hero/builder creates and retire the old area-based movers."""
    converted = 0
    retired = 0
    wrappers = []
    for trigger in ctx.tm.triggers:
        changed = False
        hero = re.fullmatch(r"Hero (?:Milestone|Boost \S+) S([1-8]) W[1-8](?: .+)?", trigger.name)
        builder = re.fullmatch(r"Builder Reward S([1-8]) W[1-8]", trigger.name)
        birth = hero or builder
        if birth:
            changed = True
            color = int(birth.group(1))
            # Native rewards could previously run before the XS spawning owner
            # arrived. Wait rather than consume builder entitlement without a birth.
            for quantity, comparison in (
                (identity_tag + 1, Comparison.LARGER_OR_EQUAL),
                (identity_tag + 9, Comparison.LESS),
            ):
                trigger.new_condition.variable_value(
                    variable=identity_base + color - 1, quantity=quantity, comparison=comparison,
                )
            original = [trigger.effects[index] for index in trigger.effect_order]
            if builder:
                # Announce only a completed pair. The old mover now serves as its
                # owner-resolved notification and acknowledgement trigger.
                notice = next(t for t in ctx.tm.triggers
                              if t.name == trigger.name.replace("Builder Reward", "Builder Move"))
                notice.effects = [e for e in original if e.effect_type == EffectId.SEND_CHAT] + notice.effects
                notice.effect_order = list(range(len(notice.effects)))
                original = [e for e in original if e.effect_type not in
                            {EffectId.SEND_CHAT, EffectId.CHANGE_VARIABLE}]
            trigger.effects = []
            for effect in original:
                if effect.effect_type != EffectId.CREATE_OBJECT:
                    trigger.effects.append(effect)
                    continue
                family = "Hero" if hero else "Builder"
                # Recurring Hero births otherwise play a global creation cue,
                # even while the player's camera is elsewhere on the map.
                sound = "false" if hero or effect.disable_sound == 1 else "true"
                ctx_fn = f"cbaBirth{family}{converted}"
                wrappers.append(
                    f"void {ctx_fn}() {{ cba{'Create' if hero else 'Deliver'}{family}Birth({color}, "
                    f"{effect.object_list_unit_id}, {effect.location_x}, {effect.location_y}, {sound}); }}"
                )
                # DE effects call a zero-argument function by name. Define the
                # wrapper after its helpers in the shared embedded XS bundle.
                trigger.new_effect.script_call(message=ctx_fn)
                converted += 1
            if builder:
                commit = f"cbaCommitBuilderPair{color}W{trigger.name.rsplit('W', 1)[1]}"
                wrappers.append(f"void {commit}() {{ cbaCommitBuilderPair({color}); }}")
                trigger.new_effect.script_call(message=commit)
        if re.fullmatch(r"(?:Army|Hero) Range L\d S[1-8] W[1-8]|Builder Move S[1-8] W[1-8]", trigger.name):
            changed = True
            retired += sum(effect.effect_type == EffectId.TASK_OBJECT for effect in trigger.effects)
            trigger.effects = [
                trigger.effects[index] for index in trigger.effect_order
                if trigger.effects[index].effect_type != EffectId.TASK_OBJECT
            ]
        # The remaining movement triggers only acknowledge completed deliveries;
        # they never select or order units on a later game tick.
        if changed:
            trigger.effect_order = list(range(len(trigger.effects)))
    if converted != 1024 or retired != 1984:
        raise RuntimeError(f"birth-order migration drift: creates={converted}, area tasks={retired}")
    return "\n".join(wrappers)


def render_birth_orders(*, players, transform, army_destinations, hero_destinations,
                        builder_destinations, army_range_base, hero_range_base,
                        eliminated_base, occupied_base, pending_base, builder_notice_base):
    def branches(destinations, *, slot=False):
        lines = []
        for player in players:
            lines.append(f"if (scenarioPlayer == {int(player)}) {{")
            for level, points in destinations.items():
                lines.append(f"if (level == {level}) {{")
                if slot:
                    for index, point in enumerate(points):
                        x, y = transform(player, *point)
                        lines.append(
                            f"if (slot == {index}) cbaOrderBirth(unitRef, vector({x + 0.5}, {y + 0.5}, -1));"
                        )
                else:
                    x, y = transform(player, *points)
                    lines.append(f"cbaOrderBirth(unitRef, vector({x + 0.5}, {y + 0.5}, -1));")
                lines.append("}")
            lines.append("}")
        return "\n".join(lines)

    builder_lines = []
    for player in players:
        builder_lines.append(f"if (scenarioPlayer == {int(player)}) {{")
        for unit_id, (x, y) in builder_destinations[player].items():
            builder_lines.append(
                f"if (unitId == {unit_id}) cbaOrderBirth(unitRef, vector({x + 0.5}, {y + 0.5}, -1));"
            )
        builder_lines.append("}")
    return f"""
// Creation references and xsTaskUnits are documented in DE update 185872.
int gCbaBirthOrderUnit = -1;

void cbaOrderBirth(int unitRef = -1, vector destination = vector(-1, -1, -1)) {{
    if (unitRef < 0 || xsDoesUnitExist(unitRef) == false) return;
    xsArraySetInt(gCbaBirthOrderUnit, 0, unitRef);
    xsTaskUnits(gCbaBirthOrderUnit, 1, destination, -1, false, false, false, 0);
}}

void cbaOrderArmyBirth(int scenarioPlayer = 0, int slot = 0, int unitRef = -1) {{
int level = xsTriggerVariable({army_range_base} + scenarioPlayer - 1);
{branches(dict(enumerate(army_destinations)), slot=True)}
}}

void cbaCreateHeroBirth(int scenarioPlayer = 0, int unitId = -1, int x = 0, int y = 0, bool sound = false) {{
    if (xsTriggerVariable({eliminated_base} + scenarioPlayer - 1) == 1) return;
    if (xsTriggerVariable({occupied_base} + scenarioPlayer - 1) != 1) return;
    int worldPlayer = cbaWorldPlayerForColor(scenarioPlayer);
    if (worldPlayer < 1) return;
    if (cbaHasPopulationRoom(worldPlayer, unitId, 1) == false) return;
    int level = xsTriggerVariable({hero_range_base} + scenarioPlayer - 1);
    if (level < 1 || level > 5) return;
    int unitRef = xsCreateUnit(unitId, worldPlayer, xsVectorSet(0.5 + x, 0.5 + y, -1), false, sound, false);
{branches(hero_destinations)}
}}

int cbaCreateBuilderBirth(int scenarioPlayer = 0, int unitId = -1,
                          int x = 0, int y = 0, bool sound = true) {{
    if (xsTriggerVariable({eliminated_base} + scenarioPlayer - 1) == 1) return(-1);
    if (xsTriggerVariable({occupied_base} + scenarioPlayer - 1) != 1) return(-1);
    int worldPlayer = cbaWorldPlayerForColor(scenarioPlayer);
    if (worldPlayer < 1) return(-1);
    if (cbaHasPopulationRoom(worldPlayer, unitId, 1) == false) return(-1);
    int unitRef = xsCreateUnit(unitId, worldPlayer, xsVectorSet(0.5 + x, 0.5 + y, -1), false, sound, false);
{chr(10).join(builder_lines)}
    return(unitRef);
}}

void cbaDeliverBuilderBirth(int scenarioPlayer = 0, int unitId = -1,
                           int x = 0, int y = 0, bool sound = true) {{
    if (xsTriggerVariable({pending_base} + scenarioPlayer - 1) < 1) return;
    int delivered = gCbaBuilderMaleDelivered;
    if (unitId == 293) delivered = gCbaBuilderFemaleDelivered;
    if (xsArrayGetInt(delivered, scenarioPlayer) == 1) return;
    int unitRef = cbaCreateBuilderBirth(scenarioPlayer, unitId, x, y, sound);
    if (unitRef < 0) return;
    xsArraySetInt(delivered, scenarioPlayer, 1);
}}

void cbaCommitBuilderPair(int scenarioPlayer = 0) {{
    if (xsArrayGetInt(gCbaBuilderMaleDelivered, scenarioPlayer) != 1) return;
    if (xsArrayGetInt(gCbaBuilderFemaleDelivered, scenarioPlayer) != 1) return;
    int pending = xsTriggerVariable({pending_base} + scenarioPlayer - 1);
    if (pending < 1) return;
    xsSetTriggerVariable({pending_base} + scenarioPlayer - 1, pending - 1);
    xsSetTriggerVariable({builder_notice_base} + scenarioPlayer - 1, 1);
    xsArraySetInt(gCbaBuilderMaleDelivered, scenarioPlayer, 0);
    xsArraySetInt(gCbaBuilderFemaleDelivered, scenarioPlayer, 0);
}}
"""
