"""Native lobby/engine population admission; no in-game population selector."""

import re

from AoE2ScenarioParser.datasets.conditions import ConditionId
from AoE2ScenarioParser.datasets.effects import EffectId
from AoE2ScenarioParser.datasets.players import PlayerId


def configure_population_setup(ctx):
    # The stock 200 fallback does not introduce a custom 501/251 scenario ceiling.
    # Multiplayer's population choice is owned by DE; all scenario colors match.
    for player in PlayerId.all(exclude_gaia=True):
        ctx.pm.players[player].population_cap = ctx.spec.players.population_cap
    # Replace old integer military counts with native free population checks.
    # This also supports fractional population costs and complete reward batches.
    gates = []
    for trigger in ctx.tm.triggers:
        hero = re.fullmatch(r"Hero (?:Milestone|Boost \S+) S([1-8]) W[1-8](?: .+)?", trigger.name)
        builder = re.fullmatch(r"Builder Reward S([1-8]) W[1-8]", trigger.name)
        backup = re.fullmatch(r"King Island S([1-8]) W[1-8]", trigger.name)
        if not (hero or builder or backup):
            continue
        if hero:
            trigger.conditions = [c for c in trigger.conditions
                                  if c.condition_type != ConditionId.OWN_FEWER_OBJECTS]
        creates = [e for e in trigger.effects if e.effect_type == EffectId.CREATE_OBJECT]
        if not creates:
            raise RuntimeError(f"Population setup ran after birth conversion: {trigger.name}")
        color = int((hero or builder or backup).group(1))
        name = f"cbaPopulationGate{len(gates)}"
        costs = " + ".join(
            f"cbaPopulationCost(owner, {e.object_list_unit_id})" for e in creates
        )
        if builder:
            costs = f"cbaBuilderPopulationCost({color}, owner)"
        # DE rejected the compound bool/float return in cbaPopulationGate0
        # even though xs-check accepted it. Separate the arithmetic and owner
        # guard, and return literals after the comparison.
        gates.append(
            f"bool {name}() {{\n"
            f"    int owner = cbaWorldPlayerForColor({color});\n"
            "    if (owner < 1) return(false);\n"
            f"    float cost = {costs};\n"
            "    float room = xsPlayerAttribute(owner, cAttributePopulationCap);\n"
            "    if (cost > room) return(false);\n"
            "    return(true);\n"
            "}"
        )
        trigger.new_condition.script_call(xs_function=name)
    return f"""
float cbaPopulationCost(int worldPlayer = 0, int unitId = -1) {{
    float cost = 0.0 - xsGetObjectAttribute(worldPlayer, unitId, cPopulation);
    if (cost < 0) cost = 1;
    return(cost);
}}

bool cbaHasPopulationRoom(int worldPlayer = 0, int unitId = -1, int count = 1) {{
    if (worldPlayer < 1 || unitId < 0 || count < 1) return(false);
    float cost = cbaPopulationCost(worldPlayer, unitId) * count;
    float room = xsPlayerAttribute(worldPlayer, cAttributePopulationCap);
    if (cost > room) return(false);
    return(true);
}}
int gCbaBuilderMaleDelivered = -1;
int gCbaBuilderFemaleDelivered = -1;

float cbaBuilderPopulationCost(int scenarioPlayer = 0, int owner = 0) {{
    float cost = 0;
    if (xsArrayGetInt(gCbaBuilderMaleDelivered, scenarioPlayer) == 0) {{
        cost = cost + cbaPopulationCost(owner, 83);
    }}
    if (xsArrayGetInt(gCbaBuilderFemaleDelivered, scenarioPlayer) == 0) {{
        cost = cost + cbaPopulationCost(owner, 293);
    }}
    return(cost);
}}
{chr(10).join(gates)}
"""
