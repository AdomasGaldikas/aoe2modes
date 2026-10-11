"""A bounded, refreshable comeback boost; no imported Adrenaline trigger graph."""

import math
import re
import tomllib

from AoE2ScenarioParser.datasets.players import PlayerId
from AoE2ScenarioParser.datasets.units import UnitInfo


def load_settings(directory):
    with (directory / "mode.toml").open("rb") as handle:
        values = tomllib.load(handle)["speed_rush"]
    for name in ("delay_seconds", "duration_seconds"):
        if type(values[name]) is not int or values[name] < (0 if name == "delay_seconds" else 1):
            raise ValueError(f"speed_rush.{name} must be a valid integer duration")
    for name in ("movement_multiplier", "fire_rate_multiplier"):
        value = values[name]
        if isinstance(value, bool) or not isinstance(value, (float, int)):
            raise ValueError(f"speed_rush.{name} must be numeric")
        if not math.isfinite(value) or not 1 < value <= 4:
            raise ValueError(f"speed_rush.{name} must be finite and in (1, 4]")
    return values


def render_runtime(unit_ids, settings, *, occupied_base, eliminated_base, countdown_base):
    speed = float(settings["movement_multiplier"])
    fire_rate = float(settings["fire_rate_multiplier"])
    announcement = f"{speed:g}x move, {fire_rate:g}x fire, {settings['duration_seconds']}s (refreshed)."
    effects = []
    for unit_id in sorted(set(unit_ids)):
        for attribute, factor in (("cMovementSpeed", "movement"),
                                  ("cAttackReloadTime", "reload"), ("cAttackDelay", "reload")):
            effects.append(f"    xsEffectAmount(cMulAttribute, {unit_id}, {attribute}, {factor}, owner);")
    return f"""// RA Speed Rush: state transitions only, never a per-tick stat multiplier.
int gRaSpeedSeenLoss = -1;
int gRaSpeedUntil = -1;
int gRaSpeedApplied = -1;

void cbaSpeedInitialize() {{
    if (gRaSpeedSeenLoss >= 0) return;
    gRaSpeedSeenLoss = xsArrayCreateInt(9, 0, "raSpeedSeenLoss");
    gRaSpeedUntil = xsArrayCreateInt(3, 0, "raSpeedUntil");
    gRaSpeedApplied = xsArrayCreateInt(9, 0, "raSpeedApplied");
}}

int cbaSpeedTeam(int color = 0) {{
    if (color <= 4) return(1);
    return(2);
}}

bool cbaSpeedColorAlive(int color = 0) {{
    if (xsTriggerVariable({occupied_base} + color - 1) != 1) return(false);
    if (xsTriggerVariable({eliminated_base} + color - 1) == 1) return(false);
    return(true);
}}

bool cbaSpeedTeamHasSurvivor(int team = 0) {{
    for (color = 1; <= 8) {{
        if (cbaSpeedTeam(color) == team && cbaSpeedColorAlive(color)) return(true);
    }}
    return(false);
}}

void cbaSpeedSetOwner(int owner = 0, bool enabled = false) {{
    float movement = {1.0 / speed:.12g};
    float reload = {fire_rate:.12g};
    if (enabled) {{
        movement = {speed:.12g};
        reload = {1.0 / fire_rate:.12g};
    }}
{chr(10).join(effects)}
}}

void cbaSpeedTick() {{
    if (gRaSpeedSeenLoss < 0) return;
    int now = xsGetGameTime();
    // Observe losses throughout warm-up so early departures never pay out later.
    // Closed slots never entered persistent occupancy and cannot start a rush.
    for (color = 1; <= 8) {{
        if (xsTriggerVariable({occupied_base} + color - 1) == 1 &&
            xsTriggerVariable({eliminated_base} + color - 1) == 1 &&
            xsArrayGetInt(gRaSpeedSeenLoss, color) == 0) {{
            xsArraySetInt(gRaSpeedSeenLoss, color, 1);
            int team = cbaSpeedTeam(color);
            if (now >= {settings['delay_seconds']} && cbaSpeedTeamHasSurvivor(team)) {{
                // Extend the deadline only: another loss does not reapply the bonus.
                int deadline = now + {settings['duration_seconds']};
                if (xsArrayGetInt(gRaSpeedUntil, team) != deadline) {{
                    xsArraySetInt(gRaSpeedUntil, team, deadline);
                    if (team == 1) xsChatData("[RA Speed] Team 1: {announcement}");
                    else xsChatData("[RA Speed] Team 2: {announcement}");
                }}
            }}
        }}
    }}
    for (team = 1; <= 2) {{
        if (cbaSpeedTeamHasSurvivor(team) == false) xsArraySetInt(gRaSpeedUntil, team, 0);
        int remaining = xsArrayGetInt(gRaSpeedUntil, team) - now;
        if (remaining < 0) remaining = 0;
        xsSetTriggerVariable({countdown_base} + team - 1, remaining);
    }}
    // Resolve colors through RA's XS identity tokens. Never pass native selectors
    // to xsEffectAmount, and mutate each resolved owner at most once per transition.
    for (owner = 1; <= 8) {{
        bool wanted = false;
        for (color = 1; <= 8) {{
            if (cbaSpeedColorAlive(color) && cbaWorldPlayerForColor(color) == owner &&
                now < xsArrayGetInt(gRaSpeedUntil, cbaSpeedTeam(color))) wanted = true;
        }}
        int applied = xsArrayGetInt(gRaSpeedApplied, owner);
        int target = 0;
        if (wanted) target = 1;
        if (target != applied && xsGetPlayerInGame(owner)) {{
            cbaSpeedSetOwner(owner, wanted);
            xsArraySetInt(gRaSpeedApplied, owner, target);
        }}
    }}
}}
"""


def configure_speed_rush(ctx, unit_ids, shared):
    settings = load_settings(ctx.mode_dir)
    matches = [(index, source) for index, (label, source) in enumerate(ctx.xs_chunks)
               if label == "color-aware army spawning"]
    index, source = matches[0] if len(matches) == 1 else (-1, "")
    if index < 0 or source.count("void main() {") != 1:
        raise RuntimeError("Speed expects RA's single maintained XS runtime")
    for _label, chunk in ctx.xs_chunks:
        unit_ids.update(int(value) for value in re.findall(r"cbaCreateHeroBirth\(\d+, (\d+),", chunk))
    unit_ids.update((UnitInfo.SCORPION.ID, UnitInfo.HEAVY_SCORPION.ID,
                     UnitInfo.VILLAGER_MALE.ID, UnitInfo.VILLAGER_FEMALE.ID))
    if UnitInfo.WAR_PENGUIN.ID in unit_ids or UnitInfo.SHEEP.ID in unit_ids or UnitInfo.KING.ID in unit_ids:
        raise RuntimeError("Speed roster must not include controllers")
    countdown_base = len(ctx.tm.variables)
    for team in (1, 2):
        ctx.tm.add_variable(f"speed_t{team}seconds", variable_id=countdown_base + team - 1)
        row = ctx.tm.add_trigger(
            f"Speed Rush HUD Team {team}", enabled=1, display_on_screen=1,
            description_order=9 - team, header=0, mute_objectives=1,
            description_stid=0, short_description_stid=0,
            short_description=f"rush t{team}: <speed_t{team}seconds>s (0 = off)",
        )
        row.new_condition.player_defeated(source_player=PlayerId.GAIA)
    shared._assert_variable_ids_are_contiguous(ctx)
    runtime = render_runtime(unit_ids, settings, occupied_base=shared.COLOR_OCCUPIED_VARIABLE_BASE,
                             eliminated_base=shared.COLOR_ELIMINATED_VARIABLE_BASE,
                             countdown_base=countdown_base)
    # Define helpers after RA's resolver and before main; allocate arrays in main.
    if source.count("void cbaCreateWave(") != 1:
        raise RuntimeError("Speed expects exactly one shared RA wave helper")
    source = source.replace("void cbaCreateWave(", runtime + "\nvoid cbaCreateWave(", 1)
    source = source.replace("void main() {", "void main() {\n    cbaSpeedInitialize();", 1)
    source += "\nrule cbaSpeedRush\n    active\n    minInterval 1\n{\n    cbaSpeedTick();\n}\n"
    ctx.xs_chunks[index] = ("color-aware army spawning", source)
    ctx.scenario.message_manager.instructions += (
        f"\r\rSPEED RUSH\rAfter {settings['delay_seconds']} seconds, "
        "losing a started teammate gives survivors "
        f"{settings['movement_multiplier']:g}x movement and "
        f"{settings['fire_rate_multiplier']:g}x attack rate "
        f"for {settings['duration_seconds']} seconds. Another loss refreshes the "
        "time without stacking. Closed slots and earlier departures give no rush. "
        "Castle armies, Heroes, Scorpions and builders receive the boost; controllers "
        "and buildings do not. All other normal RA rules remain in effect."
    )
    ctx.log(f"Speed Rush roster: {len(unit_ids)} unit types; normal RA geometry/rules preserved")
