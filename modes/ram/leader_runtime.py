"""Keep the eight original leader references while using civilization-specific units."""

import json

from AoE2ScenarioParser.datasets.effects import EffectId
from AoE2ScenarioParser.datasets.heroes import HeroInfo
from AoE2ScenarioParser.datasets.players import PlayerId

from .civilization_leaders import leader_unit_id, leaders_enabled, load_leader_catalog


def configure_civilization_leaders(ctx):
    if not leaders_enabled(ctx.mode_dir):
        return
    catalog = load_leader_catalog(ctx.mode_dir)
    unit_id = leader_unit_id(ctx.mode_dir)
    leaders = {}
    for color in PlayerId.all(exclude_gaia=True):
        leader, = [u for u in ctx.um.units[color] if u.unit_const == HeroInfo.GENGHIS_KHAN.ID]
        leaders[int(color)] = leader.reference_id
        # The Data Mod defines this ID separately in each civilization. Everything
        # else, including exact-reference growth and owner detection, stays intact.
        leader.unit_const = unit_id

    growth, = [t for t in ctx.tm.triggers if t.name == "ge kan"]
    growth.effects = [e for e in growth.effects if e.effect_type != EffectId.CHANGE_OBJECT_ATTACK]
    for reference in leaders.values():
        # Native Script Call snippets precede the bundled script. Keep each
        # parameterless entry point self-contained; forward calls fail in DE.
        growth.new_effect.script_call(
            message=f"""void ramGrowLeader{reference}() {{
    int reference = {reference};
    if (xsDoesUnitExist(reference) == false) return;
    if (xsGetUnitHitpoints(reference) <= 0) return;
    int damageClass = 3;
    if (xsGetUnitAttribute(reference, 9, 4) > 0) damageClass = 4;
    xsEffectAmount(cAddUnitAttribute, reference, 9, damageClass * 256 + 3, 0);
}}""",
        )
    growth.effect_order = list(range(len(growth.effects)))

    names = "\n".join(
        f"    if (civilization == {row['civilization']}) return({json.dumps(row['leader_name'])});"
        for row in catalog
    )
    bindings = "\n".join(
        f"    ramNameLeader({color}, {reference});" for color, reference in leaders.items()
    )
    ctx.add_xs(f"""// Civilization-specific starting leaders; no replacement or new births.
int gRamNamedLeaders = -1;

string ramCivilizationLeaderName(int civilization = 0) {{
{names}
    return("Commander");
}}

void ramNameLeader(int color = 0, int reference = -1) {{
    if (xsArrayGetInt(gRamNamedLeaders, color) == 1) return;
    if (xsTriggerVariable(31 + color) != 1) return;
    int owner = cbaWorldPlayerForColor(color);
    if (owner < 1) return;
    if (xsDoesUnitExist(reference) == false) return;
    if (xsGetUnitHitpoints(reference) <= 0) return;
    if (xsGetUnitOwner(reference) != owner) return;
    if (xsSetUnitName(reference, ramCivilizationLeaderName(xsGetPlayerCivilization(owner)))) {{
        xsArraySetInt(gRamNamedLeaders, color, 1);
    }}
}}

rule ramCivilizationLeaderNames
    active
    minInterval 1
{{
    if (gRamNamedLeaders < 0) gRamNamedLeaders = xsArrayCreateInt(9, 0, "ramNamedLeaders");
{bindings}
}}
""", label="civilization-specific starting leaders")
