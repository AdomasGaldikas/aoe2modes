"""One shared match-start population choice, owned by the first occupied color."""

import re

from AoE2ScenarioParser.datasets.conditions import ConditionId
from AoE2ScenarioParser.datasets.effects import EffectId
from AoE2ScenarioParser.datasets.heroes import HeroInfo
from AoE2ScenarioParser.datasets.other import OtherInfo
from AoE2ScenarioParser.datasets.players import PlayerId
from AoE2ScenarioParser.datasets.terrains import TerrainId

CHOICES = (200, 250, 300, 500)
PADS = ((68, 4), (70, 4), (72, 4), (74, 4))
DEFAULT_LIMIT = 250
ENGINE_LIMIT = 501  # One additional real population slot for the Penguin.


def configure_population_setup(ctx, *, occupied_base, eliminated_base):
    if ctx.spec.players.population_cap != ENGINE_LIMIT:
        raise ValueError("Population setup expects the declared 501 engine ceiling")
    # Isolated from all controller islands, army pads and protected routes.
    for x in range(68, 76):
        for y in range(2, 8):
            tile = ctx.mm.get_tile(x=x, y=y)
            tile.terrain_id, tile.elevation, tile.layer = TerrainId.GRASS_2, 1, -1
    chooser = ctx.um.add_unit(player=PlayerId.GAIA, unit_const=HeroInfo.KING_ALFONSO.ID, x=70.5, y=4.5)
    labels = ctx.tm.add_trigger("Population Setup Labels")
    labels.new_condition.timer(timer=1)
    labels.new_effect.change_object_name(
        source_player=PlayerId.GAIA,
        selected_object_ids=[chooser.reference_id],
        message="Population chooser - move to 200 / 250 / 300 / 500",
    )
    labels.new_effect.disable_object_deletion(
        source_player=PlayerId.GAIA, selected_object_ids=[chooser.reference_id]
    )
    for limit, (x, y) in zip(CHOICES, PADS, strict=True):
        sign = ctx.um.add_unit(player=PlayerId.GAIA, unit_const=OtherInfo.SIGN.ID, x=x + 0.5, y=y - 0.5)
        labels.new_effect.change_object_name(
            source_player=PlayerId.GAIA,
            selected_object_ids=[sign.reference_id],
            message=f"{limit} population - choose within first 60 seconds",
        )
    for player in PlayerId.all(exclude_gaia=True):
        ctx.pm.players[player].population_cap = ctx.spec.players.population_cap
    # Replace old integer military counts with the selected real population budget.
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
        # DE rejected the compound bool/float return in cbaPopulationGate0
        # even though xs-check accepted it. Separate the arithmetic and owner
        # guard, and return literals after the comparison.
        gates.append(
            f"bool {name}() {{\n"
            f"    int owner = cbaWorldPlayerForColor({color});\n"
            "    if (owner < 1) return(false);\n"
            f"    float cost = {costs};\n"
            "    float used = cbaPopulationUsed(owner);\n"
            "    float room = gCbaPopulationLimit;\n"
            "    room = room - used;\n"
            "    if (cost > room) return(false);\n"
            "    return(true);\n"
            "}"
        )
        trigger.new_condition.script_call(xs_function=name)
    ref = chooser.reference_id
    owners = []
    updates = []
    for color in range(1, 9):
        # Stop at the first occupied color, even if its XS identity arrives late.
        owners.append(f"""if (cbaPopulationColorActive({color})) {{
            candidate = cbaWorldPlayerForColor({color});
            if (candidate < 1) return;
            if (xsSetUnitOwner({ref}, candidate, false) == false) return;
            if (xsSetUnitProperty({ref}, CBA_UNIT_ATTACKABLE, 0.0) == false) return;
            if (xsSetUnitProperty({ref}, CBA_UNIT_TARGETABLE, 0.0) == false) return;
            if (xsSetUnitProperty({ref}, CBA_UNIT_DELETABLE, 0.0) == false) return;
            gCbaPopulationOwner = candidate;
            xsDisplayInstructions(
                "Host: move Population chooser on north island to 200 / 250 / 300 / 500. "
                + "Locks at 60 seconds. Default 250.",
                50, candidate, {HeroInfo.KING_ALFONSO.ID}, cPanelTop, false, false, "", candidate);
            return;
        }}""")
        updates.append(f"""if (cbaPopulationColorActive({color})) {{
            owner = cbaWorldPlayerForColor({color});
            if (owner > 0) {{
                reserve = 1.0;
                if (owner == gCbaPopulationOwner && xsDoesUnitExist({ref}))
                    reserve = reserve + cbaPopulationCost(owner, {HeroInfo.KING_ALFONSO.ID});
                xsSetPlayerAttribute(owner, cAttributeUnitLimit,
                    reserve + gCbaPopulationLimit - {ENGINE_LIMIT}.0);
                room = reserve + gCbaPopulationLimit - xsPlayerAttribute(owner, cAttributePopulation);
                if (room < 0) room = 0;
                xsSetPlayerAttribute(owner, 4, room); // Population Headroom, not maximum cap.
            }}
        }}""")
    choices = []
    for limit, (x, y) in zip(CHOICES, PADS, strict=True):
        choices.append(
            f"if (x >= {x} && x < {x + 2} && y >= {y} && y < {y + 2}) gCbaPopulationLimit = {limit};"
        )
    return f"""
// Property ids documented at ugc.aoe2.rocks/general/xs/constants/constants/.
// The validator bundled with parser 0.8.4 predates these property enum names.
const int CBA_UNIT_DELETABLE = 7;
const int CBA_UNIT_TARGETABLE = 8;
const int CBA_UNIT_ATTACKABLE = 9;
const int CBA_UNIT_SELECTABLE = 10;
int gCbaPopulationLimit = {DEFAULT_LIMIT};
int gCbaPopulationOwner = 0;
bool gCbaPopulationLocked = false;

float cbaPopulationCost(int worldPlayer = 0, int unitId = -1) {{
    float cost = 0.0 - xsGetObjectAttribute(worldPlayer, unitId, cPopulation);
    if (cost < 0) cost = 1;
    return(cost);
}}

float cbaPopulationUsed(int worldPlayer = 0) {{
    float used = xsPlayerAttribute(worldPlayer, cAttributePopulation) - 1.0;
    if (worldPlayer == gCbaPopulationOwner && xsDoesUnitExist({ref}))
        used = used - cbaPopulationCost(worldPlayer, {HeroInfo.KING_ALFONSO.ID});
    if (used < 0) used = 0;
    return(used);
}}

bool cbaHasPopulationRoom(int worldPlayer = 0, int unitId = -1, int count = 1) {{
    if (worldPlayer < 1 || unitId < 0 || count < 1) return(false);
    float cost = cbaPopulationCost(worldPlayer, unitId) * count;
    float used = cbaPopulationUsed(worldPlayer);
    float room = gCbaPopulationLimit;
    room = room - used;
    if (cost > room) return(false);
    return(true);
}}

bool cbaPopulationColorActive(int scenarioPlayer = 0) {{
    return(xsTriggerVariable({occupied_base} + scenarioPlayer - 1) == 1 &&
        xsTriggerVariable({eliminated_base} + scenarioPlayer - 1) == 0);
}}

void cbaClaimPopulationChooser() {{
    if (gCbaPopulationOwner > 0 || xsGetGameTime() < 4 || gCbaPopulationLocked) return;
    if (xsDoesUnitExist({ref}) == false) return;
    int candidate = 0;
{chr(10).join(owners)}
}}

void cbaUpdatePopulationSetup() {{
    if (xsGetGameTime() < 60) cbaClaimPopulationChooser();
    int previous = gCbaPopulationLimit;
    int owner = 0;
    float reserve = 1.0;
    float room = 0.0;
    if (gCbaPopulationLocked == false) {{
        if (xsGetGameTime() >= 60) {{
            gCbaPopulationLocked = true;
            if (xsDoesUnitExist({ref}) && xsRemoveUnit({ref}) == false)
                xsChatData("[CBA] Population choice is locked; chooser cleanup will need a check.");
            xsDisplayInstructions("Population limit locked: " + gCbaPopulationLimit,
                8, -1, -1, cPanelTop, false, false);
        }} else if (gCbaPopulationOwner > 0 && xsDoesUnitExist({ref}) &&
            xsGetUnitOwner({ref}) == gCbaPopulationOwner) {{
            vector position = xsGetUnitPosition({ref});
            float x = xsVectorGetX(position);
            float y = xsVectorGetY(position);
{chr(10).join(choices)}
        }}
    }}
    if (previous != gCbaPopulationLimit)
        xsDisplayInstructions("Population selected: " + gCbaPopulationLimit,
            5, -1, -1, cPanelTop, false, false);
{chr(10).join(updates)}
}}

rule cbaPopulationSetup
    active
    minInterval 1
{{
    cbaUpdatePopulationSetup();
}}
{chr(10).join(gates)}
"""
