"""Code-defined Last Caravan; all gameplay and ownership live in embedded XS."""

from __future__ import annotations

import math
import re
import tomllib

from AoE2ScenarioParser.datasets.buildings import BuildingInfo
from AoE2ScenarioParser.datasets.heroes import HeroInfo
from AoE2ScenarioParser.datasets.other import OtherInfo
from AoE2ScenarioParser.datasets.players import PlayerId
from AoE2ScenarioParser.datasets.techs import TechInfo
from AoE2ScenarioParser.datasets.terrains import TerrainId
from AoE2ScenarioParser.datasets.trigger_lists import VictoryCondition
from AoE2ScenarioParser.datasets.units import UnitInfo

from aoe2modes.context import BuildContext
from aoe2modes.lib import players, terrain, triggers

from .civilizations import CIV_SPAWN_RULES

FINAL_POINTS = tuple((x, y) for x in (80, 120, 160) for y in (80, 120, 160))
OUTPOST_POINTS = tuple((x, y) for x in (72, 168) for y in (72, 120, 168))
HUD_FIELDS = ("state", "kills", "deaths", "rank", "renown", "builders", "wood", "stone", "rescues")
GLOBAL_FIELDS = ("team_a", "team_b", "storm_seconds", "rescue_seconds", "end_seconds", "phase")
IDS = {
    "WAGON": UnitInfo.OX_WAGON.ID,
    "HERO": HeroInfo.KING_ARTHUR.ID,
    "CASTLE": BuildingInfo.CASTLE.ID,
    "BUILDER": UnitInfo.VILLAGER_MALE.ID,
    "TOWER": BuildingInfo.WATCH_TOWER.ID,
    "WALL": BuildingInfo.PALISADE_WALL.ID,
    "GATE": BuildingInfo.PALISADE_GATE.ID,
    "GATE_SW": BuildingInfo.PALISADE_GATE_SOUTHWEST_TO_NORTHEAST.ID,
    "GATE_NW": BuildingInfo.PALISADE_GATE_NORTHWEST_TO_SOUTHEAST.ID,
    "GATE_EW": BuildingInfo.PALISADE_GATE_WEST_TO_EAST.ID,
    "GATE_NS": BuildingInfo.PALISADE_GATE_NORTH_TO_SOUTH.ID,
    "BARRACKS": BuildingInfo.BARRACKS.ID,
    "RANGE": BuildingInfo.ARCHERY_RANGE.ID,
    "STABLE": BuildingInfo.STABLE.ID,
    "PIKE": UnitInfo.PIKEMAN.ID,
    "SKIRM": UnitInfo.ELITE_SKIRMISHER.ID,
    "CAV": UnitInfo.LIGHT_CAVALRY.ID,
    "CHAMPION": UnitInfo.CHAMPION.ID,
    "FIRE": OtherInfo.BONFIRE.ID,
    "WARNING": OtherInfo.FLAG_B.ID,
    "WRECK": OtherInfo.BROKEN_CART.ID,
    "OUTPOST": OtherInfo.FLAG_A.ID,
    "CHEST": OtherInfo.RELIC.ID,
}
BUILD_IDS = tuple(
    IDS[name]
    for name in (
        "TOWER",
        "WALL",
        "GATE",
        "BARRACKS",
        "RANGE",
        "STABLE",
        "GATE_SW",
        "GATE_NW",
        "GATE_EW",
        "GATE_NS",
    )
)


def _settings(ctx: BuildContext) -> dict:
    with (ctx.mode_dir / "mode.toml").open("rb") as handle:
        config = tomllib.load(handle)["royale"]
    if ctx.map_size != 240 or ctx.players.teams != (
        tuple(PlayerId(i) for i in range(1, 5)),
        tuple(PlayerId(i) for i in range(5, 9)),
    ):
        raise ValueError("Last Caravan requires its 240-tile, eight-color fixed 4v4 layout")
    for key, value in config.items():
        values = value if isinstance(value, list) else [value]
        if any(type(v) not in (int, float) or not math.isfinite(v) or v < 0 for v in values):
            raise ValueError(f"royale.{key} must contain finite nonnegative numbers")
        if isinstance(value, list) and key != "storm_radii" and values != sorted(set(values)):
            # Damage may repeat in the terminal stage.
            if key != "storm_damage_percent":
                raise ValueError(f"royale.{key} must be strictly increasing")
    if config["speed_factor"] != 2 or config["marker_limit"] != 256:
        raise ValueError("Hosting uses locked 2x speed and a fixed 256-marker budget")
    deadlines, radii, damage = (config[n] for n in ("storm_deadlines", "storm_radii", "storm_damage_percent"))
    if len(deadlines) != 9 or len(radii) != 9 or len(damage) != 9:
        raise ValueError("storm schedule requires nine stages")
    if radii != sorted(set(radii), reverse=True) or radii[-1] != 0 or radii[0] >= 112:
        raise ValueError("storm radii must decrease from below 112 to zero")
    if deadlines[-1] != config["deadline"] or config["rescue_cutoff"] >= config["deadline"]:
        raise ValueError("storm deadline and rescue cutoff are inconsistent")
    if len(config["rank_kills"]) != 3 or len(config["rank_floors"]) != 3 or len(config["builder_kills"]) != 4:
        raise ValueError("three ranks and four builder awards are required")
    if (
        config["combat_cap"] != 120
        or config["support_cap"] + max(v[1] for v in CIV_SPAWN_RULES.values()) > 119
    ):
        raise ValueError("population budgets must reserve room for the hero")
    return config


def _map(ctx: BuildContext) -> None:
    def disc(cx: int, cy: int, radius: int, kind: TerrainId, elevation: int) -> None:
        # Units/circles use map coordinates; tiles have centers at x/y + 0.5.
        # This preserves exact east/west symmetry around coordinate 120.
        for x in range(cx - radius, cx + radius):
            for y in range(cy - radius, cy + radius):
                if (x + 0.5 - cx) ** 2 + (y + 0.5 - cy) ** 2 <= radius**2:
                    tile = ctx.mm.get_tile(x, y)
                    tile.terrain_id = kind
                    tile.elevation = elevation

    terrain.border(ctx.mm, 4, TerrainId.WATER_DEEP)
    for x in (100, 140):
        for y in (100, 140):
            terrain.rect(ctx.mm, x - 4, y - 4, x + 3, y + 3, TerrainId.WATER_MEDIUM, elevation=0)
    for x in (100, 140):
        for y in (60, 180):
            disc(x, y, 10, TerrainId.GRASS_2, 2)
    for x, y in FINAL_POINTS:
        disc(x, y, 14, TerrainId.DIRT_3, 1)
    # Three clear east-west approaches. They do not cross the ponds or hills.
    for y in (84, 120, 156):
        terrain.rect(ctx.mm, 32, y - 6, 207, y + 5, TerrainId.ROAD)


def _native(ctx: BuildContext, refs: dict[int, list[int]]) -> None:
    wrappers = []
    for color in range(1, 9):
        guard = f"royaleClosed{color}"
        wrappers.append(
            f"bool {guard}() {{ if (gReady == false) return (false); "
            f"return (xsArrayGetInt(gOccupied, {color}) == 0); }}"
        )
        clean = ctx.tm.add_trigger(f"Closed start cleanup — P{color}")
        clean.new_condition.script_call(xs_function=guard)
        clean.new_effect.remove_object(selected_object_ids=refs[color])
        base = len(GLOBAL_FIELDS) + (color - 1) * len(HUD_FIELDS)
        text = (
            f"P{color} | Wagon <Variable {base}> | K/D <Variable {base + 1}>/<Variable {base + 2}> "
            f"| Rank <Variable {base + 3}> | Renown <Variable {base + 4}> "
            f"| Builders owed <Variable {base + 5}> | W/S <Variable {base + 6}>/<Variable {base + 7}> "
            f"| Rescues <Variable {base + 8}>"
        )
        hud = triggers.objective(ctx.tm, f"Caravan status — P{color}", text, order=10 + color, enabled=False)
        hud.new_condition.timer(timer=2_000_000_000)
        for selector in range(1, 9):
            guard = f"royaleShow{color}W{selector}"
            wrappers.append(f"bool {guard}() {{ return (royaleOwner({color}, {selector})); }}")
            show = ctx.tm.add_trigger(f"Show caravan — P{color} W{selector}")
            show.new_condition.script_call(xs_function=guard)
            show.new_effect.activate_trigger(trigger_id=hud.trigger_id)
            guard = f"royaleResult{color}W{selector}"
            wrappers.append(f"bool {guard}() {{ return (royaleResult({color}, {selector})); }}")
            result = ctx.tm.add_trigger(f"Caravan victory — P{color} W{selector}")
            result.new_condition.script_call(xs_function=guard)
            result.new_effect.declare_victory(source_player=selector, enabled=True)
        for rank in range(1, 4):
            guard = f"royalePromotionSound{color}R{rank}"
            wrappers.append(
                f"bool {guard}() {{ if (gReady == false) return (false); "
                f"return (xsArrayGetInt(gOccupied, {color}) == 1 "
                f"&& xsArrayGetInt(gRank, {color}) >= {rank}); }}"
            )
            cue = ctx.tm.add_trigger(f"Promotion sound — P{color} rank {rank}")
            cue.new_condition.script_call(xs_function=guard)
            cue.new_effect.play_sound(source_player=-1, global_sound=True, sound_name="Play_Age_Up")
        guard = f"royaleRescueSound{color}"
        wrappers.append(
            f"bool {guard}() {{ if (gReady == false) return (false); "
            f"return (xsArrayGetInt(gRescued, {color}) == 1); }}"
        )
        cue = ctx.tm.add_trigger(f"Rescue sound — P{color}")
        cue.new_condition.script_call(xs_function=guard)
        cue.new_effect.play_sound(
            source_player=-1, global_sound=True, sound_name="Play_Technology_Researched"
        )
    for stage in range(1, 10):
        guard = f"royaleClosureSound{stage}"
        wrappers.append(f"bool {guard}() {{ return (gReady && gStage >= {stage}); }}")
        cue = ctx.tm.add_trigger(f"Closure sound — phase {stage}")
        cue.new_condition.script_call(xs_function=guard)
        cue.new_effect.play_sound(source_player=-1, global_sound=True, sound_name="Play_Under_Attack")
    wrappers.append("bool royaleFinalSound() { return (gReady && gStage >= 6); }")
    cue = ctx.tm.add_trigger("Final phase sound")
    cue.new_condition.script_call(xs_function="royaleFinalSound")
    cue.new_effect.play_sound(source_player=-1, global_sound=True, sound_name="Play_Town_Under_Attack")
    ctx.add_xs("\n".join(wrappers), label="royale owner-resolved native effects")


def build(ctx: BuildContext) -> None:
    settings = _settings(ctx)
    ctx.xm.xs_check.additional_args.extend(
        ["--extra-prelude-path", str(ctx.mode_dir / "xs-check-prelude.xs")]
    )
    _map(ctx)
    init = []
    refs = {}
    for player in ctx.players.ids:
        color = int(player)
        x = 32 if color <= 4 else 208
        y = 84 + ((color - 1) % 4) * 24
        castle_x = x - 8 if color <= 4 else x + 8
        objects = (
            ("gWagons", IDS["WAGON"], x, y),
            ("gCastles", IDS["CASTLE"], castle_x, y),
            ("gHeroes", IDS["HERO"], x + (3 if color <= 4 else -3), y + 3),
        )
        refs[color] = []
        for array, unit_id, px, py in objects:
            unit = ctx.um.add_unit(player=player, unit_const=unit_id, x=px, y=py)
            init.append(f"xsArraySetInt({array}, {color}, {unit.reference_id});")
            refs[color].append(unit.reference_id)
        players.set_camera(ctx.pm, player, x, y)
        participant = ctx.pm.players[player]
        participant.disabled_units = sorted({u.ID for u in UnitInfo})
        participant.disabled_buildings = sorted({b.ID for b in BuildingInfo} - set(BUILD_IDS))
        participant.disabled_techs = sorted({t.ID for t in TechInfo} - {TechInfo.CARTOGRAPHY.ID})
        participant.allied_victory = True
    for x, y in OUTPOST_POINTS:
        ctx.um.add_unit(player=PlayerId.GAIA, unit_const=IDS["OUTPOST"], x=x, y=y)
    options = ctx.scenario.option_manager
    options.victory_condition = VictoryCondition.CUSTOM
    options.victory_custom_conditions_required = False
    options.lock_teams = True
    options.allow_players_choose_teams = False
    options.random_start_points = False
    ctx.scenario.sections["GlobalVictory"].retriever_map["conquest_required"].set_data(0)
    # Universal camp construction, including meso civilizations. Production is scripted.
    ctx.scenario.sections["Options"].retriever_map["all_techs"].set_data(0)
    for variable, name in enumerate(GLOBAL_FIELDS):
        ctx.tm.add_variable(name, variable)
    for color in range(1, 9):
        for offset, name in enumerate(HUD_FIELDS):
            ctx.tm.add_variable(
                f"p{color}_{name}", len(GLOBAL_FIELDS) + (color - 1) * len(HUD_FIELDS) + offset
            )
    rules = (
        "Protect your command wagon. Enter the announced safe zone. Destroy all enemy wagons.",
        "HOST: Faster (2x), Lock Speed ON, fixed P1-P4 / P5-P8 teams; 70:00 "
        "game clock is ~35 active minutes.",
        "Wagon state: 1 active, 2 rescue window, 3 stranded, 4 resigned. One "
        "rescue each before 58:00 game time.",
        "A teammate Hero rescues a safe wreck in 15 real seconds; nearby "
        "enemies interrupt. Last wagon lost = defeat.",
        "Builders at 40/100/200/350 combat kills. Two towers, 12 palisades, one "
        "gate and one counter camp per player.",
        "Outposts need five combat population. Storm damage and scripted deaths "
        "earn no Renown or builder rewards.",
    )
    for order, rule in enumerate(rules):
        objective = triggers.objective(ctx.tm, f"Royale rule {order + 1}", rule, order=order)
        objective.new_condition.timer(timer=2_000_000_000)
    hud = triggers.objective(
        ctx.tm,
        "Storm and teams",
        "Wagons A/B <Variable 0>/<Variable 1> "
        "| Storm in <Variable 2>s | Rescues close in <Variable 3>s "
        "| Finale in <Variable 4>s | Phase <Variable 5>",
        order=9,
    )
    hud.new_condition.timer(timer=2_000_000_000)
    ctx.message_manager.instructions = "\n".join(rules)
    ctx.message_manager.hints = (
        "Contest supplies, screen the caravan, rotate early and escort Heroes to rescue wrecks."
    )
    ctx.message_manager.victory = "Your caravan survived the Last Fire."
    ctx.message_manager.loss = "The last command wagon has fallen."
    _native(ctx, refs)
    constants = {key.upper(): value for key, value in settings.items() if not isinstance(value, list)}
    constants.update(IDS)
    data = []
    for key, value in settings.items():
        if isinstance(value, list):
            array = "g" + "".join(word.title() for word in key.split("_"))
            for index, entry in enumerate(value):
                data.append(f"xsArraySetInt({array}, {index}, {entry});")
    for index, (x, y) in enumerate(FINAL_POINTS):
        data.append(f"xsArraySetVector(gFinals, {index}, vector({x}, {y}, -1));")
    for index, (x, y) in enumerate(OUTPOST_POINTS):
        data.append(f"xsArraySetVector(gOutposts, {index}, vector({x}, {y}, -1));")
    for civilization, (unit, cap, interval) in CIV_SPAWN_RULES.items():
        data.extend(
            (
                f"xsArraySetInt(gCivUnits, {civilization}, {unit});",
                f"xsArraySetInt(gCivCaps, {civilization}, {cap});",
                f"xsArraySetInt(gCivIntervals, {civilization}, {interval});",
            )
        )
    # Dense, mode-local type flags include buildings missing from the parser enums.
    ctx.set_xs_vars(
        **constants,
        INITIALIZERS="\n    ".join(init + data),
        HUD_BASE=len(GLOBAL_FIELDS),
        HUD_STRIDE=len(HUD_FIELDS),
        CIV_COUNT=max(CIV_SPAWN_RULES) + 1,
    )
    # One allocation ledger. Every global array is initialized before rules/guards run.
    vectors = {"gLastWagon": 9, "gFinals": 9, "gOutposts": 6, "gZones": 9}
    floats = {"gBaseHp": 9, "gBaseAttack": 9, "gRankHealth": 2048}
    special_sizes = {
        "gBuildings": 144,
        "gCivUnits": max(CIV_SPAWN_RULES) + 1,
        "gCivCaps": max(CIV_SPAWN_RULES) + 1,
        "gCivIntervals": max(CIV_SPAWN_RULES) + 1,
        "gRankKills": 3,
        "gRankFloors": 3,
        "gBuilderKills": 4,
        "gChestTimes": 7,
        "gStormDeadlines": 9,
        "gStormRadii": 9,
        "gStormDamagePercent": 9,
        "gPostTeam": 6,
        "gPostCandidate": 6,
        "gPostSince": 6,
        "gPostDue": 6,
        "gPostXp": 18,
        "gMarkers": 256,
        "gSurvey": 1,
        "gWorld": 1,
        "gOrder": 1,
    }
    invalid_defaults = {
        "gOwners",
        "gWagons",
        "gCastles",
        "gHeroes",
        "gWrecks",
        "gRescueSince",
        "gHeroDue",
        "gBuildings",
        "gMarkers",
        "gPostSince",
        "gSurvey",
        "gWorld",
        "gOrder",
    }
    source = (ctx.mode_dir / "xs/main.xs").read_text(encoding="utf-8")
    allocations = []
    for name in re.findall(r"^int (g\w+) = -1;", source, flags=re.MULTILINE):
        if name in {"gLastTick", "gAnnounced", "gChestRef", "gChestSince", "gChestExpires"}:
            continue
        if name in vectors:
            allocations.append(
                f'{name} = xsArrayCreateVector({vectors[name]}, vector(-1, -1, -1), "{name}");'
            )
        elif name in floats:
            allocations.append(f'{name} = xsArrayCreateFloat({floats[name]}, 0.0, "{name}");')
        else:
            allocations.append(
                f"{name} = xsArrayCreateInt({special_sizes.get(name, 9)}, "
                f'{-1 if name in invalid_defaults else 0}, "{name}");'
            )
    ctx.set_xs_vars(ALLOCATIONS="\n    ".join(allocations))
