"""A separate sea CBA, with RA's eight perimeter sectors and four lives per color."""

from __future__ import annotations

import tomllib

from AoE2ScenarioParser.datasets.buildings import BuildingInfo
from AoE2ScenarioParser.datasets.heroes import HeroInfo
from AoE2ScenarioParser.datasets.players import PlayerId
from AoE2ScenarioParser.datasets.techs import TechInfo
from AoE2ScenarioParser.datasets.terrains import TerrainId
from AoE2ScenarioParser.datasets.trigger_lists import (
    AttackStance,
    Attribute,
    ObjectAttribute,
    Operation,
    VictoryCondition,
)
from AoE2ScenarioParser.datasets.units import UnitInfo

from aoe2modes.context import BuildContext
from aoe2modes.lib import players, terrain, triggers

PORT_POINTS = ((18.5, 50.5), (18.5, 53.5), (18.5, 56.5), (18.5, 59.5))
HERO_POINT = (28.5, 50.5)
QUARTERS_POINT = (10.5, 47.5)
TOWER_POINTS = ((34.5, 49.5), (34.5, 60.5))
ARCHER_POINTS = ((34.5, 51.5), (34.5, 58.5))
BUILDER_POINT = (10.5, 54.5)
HUD_FIELDS = ("ports", "kills", "deaths", "razings", "rank", "waves", "builders")
SCORE_NEUTRAL_ATTRIBUTES = (
    Attribute.PERCENT_MAP_EXPLORED, Attribute.BUILDING_COST_SUM, Attribute.TECH_COST_SUM,
    Attribute.VALUE_CURRENT_UNITS, Attribute.VALUE_CURRENT_BUILDINGS, Attribute.TRIBUTE_SCORE,
    Attribute.VALUE_WONDERS_CASTLES, Attribute.FOOD_SCORE, Attribute.WOOD_SCORE,
    Attribute.STONE_SCORE, Attribute.GOLD_SCORE, Attribute.UNITS_VALUE_TOTAL, Attribute.BUILDINGS_VALUE_TOTAL,
)
NAVAL_IDS = {
    name: member.ID for name, member in (
        ("GALLEY", UnitInfo.GALLEY), ("WAR_GALLEY", UnitInfo.WAR_GALLEY),
        ("GALLEON", UnitInfo.GALLEON), ("FIRE_GALLEY", UnitInfo.FIRE_GALLEY),
        ("FIRE_SHIP", UnitInfo.FIRE_SHIP), ("FAST_FIRE_SHIP", UnitInfo.FAST_FIRE_SHIP),
        ("DEMOLITION_RAFT", UnitInfo.DEMOLITION_RAFT), ("DEMOLITION_SHIP", UnitInfo.DEMOLITION_SHIP),
        ("HEAVY_DEMOLITION_SHIP", UnitInfo.HEAVY_DEMOLITION_SHIP),
        ("LONGBOAT", UnitInfo.LONGBOAT), ("TURTLE_SHIP", UnitInfo.TURTLE_SHIP),
        ("ADMIRAL", HeroInfo.ADMIRAL_YI_SUN_SHIN), ("CANNON_GALLEON", UnitInfo.CANNON_GALLEON),
        ("VILLAGER", UnitInfo.VILLAGER_MALE), ("ARCHER", UnitInfo.ARCHER),
        ("DOCK", BuildingInfo.DOCK), ("WATCH_TOWER", BuildingInfo.WATCH_TOWER),
        ("GUARD_TOWER", BuildingInfo.GUARD_TOWER), ("ARCHERY_RANGE", BuildingInfo.ARCHERY_RANGE),
    )
}


def position(player: int, x: float, y: float, axis: float = 144) -> tuple[float, float]:
    """Same eight color sectors as RA, expressed independently of its build module.

    Object positions reflect across 144; tile indices reflect across 143.
    """
    return (
        (y, x), (axis - y, x), (x, y), (axis - x, y),
        (x, axis - y), (axis - x, axis - y), (y, axis - x), (axis - y, axis - x),
    )[player - 1]


def _settings(ctx: BuildContext) -> dict:
    with (ctx.mode_dir / "mode.toml").open("rb") as handle:
        settings = tomllib.load(handle)["naval"]
    if ctx.map_size != 144 or ctx.players.count != 8 or ctx.players.teams != (
        tuple(PlayerId(i) for i in range(1, 5)), tuple(PlayerId(i) for i in range(5, 9)),
    ):
        raise ValueError("naval harbor geometry requires the 144-tile, fixed-color 4v4 layout")
    for name, value in settings.items():
        if name != "rank_kills" and (type(value) is not int or value <= 0):
            raise ValueError(f"naval.{name} must be a positive integer")
    ranks = settings["rank_kills"]
    if len(ranks) != 3 or any(type(n) is not int or n <= 0 for n in ranks) or ranks != sorted(set(ranks)):
        raise ValueError("naval.rank_kills must contain three increasing positive integers")
    if settings["ships_per_port"] != 1:
        raise ValueError("naval.ships_per_port must be 1 for alternating fleet production")
    if not 8 <= settings["fleet_cap"] <= ctx.players.population_cap:
        raise ValueError("naval.fleet_cap must be 8..population_cap")
    if settings["extra_ports"] != 2:
        raise ValueError("naval.extra_ports must be 2 for the six-port harbor")
    return settings


def build(ctx: BuildContext) -> None:
    settings = _settings(ctx)
    ctx.xm.xs_check.additional_args.extend([
        "--extra-prelude-path", str(ctx.mode_dir / "xs-check-prelude.xs"),
    ])
    _map(ctx)
    initializers = []
    references = {}
    for player in ctx.players.ids:
        color = int(player)
        refs = []
        for slot, point in enumerate(PORT_POINTS):
            x, y = position(color, *point)
            port = ctx.um.add_unit(player=player, unit_const=BuildingInfo.DOCK.ID, x=x, y=y)
            refs.append(port.reference_id)
            initializers.append(f"xsArraySetInt(gPorts, {color * 4 + slot}, {port.reference_id});")
        x, y = position(color, *HERO_POINT)
        hero = ctx.um.add_unit(player=player, unit_const=UnitInfo.LONGBOAT.ID, x=x, y=y)
        refs.append(hero.reference_id)
        initializers.extend((
            f"xsArraySetInt(gShips, {color * settings['fleet_cap']}, {hero.reference_id});",
            f"xsArraySetInt(gFlagship, {color}, {hero.reference_id});",
            f"xsArraySetVector(gHeroPads, {color}, vector({x}, {y}, -1));",
        ))
        x, y = position(color, *QUARTERS_POINT)
        quarters = ctx.um.add_unit(player=player, unit_const=BuildingInfo.BARRACKS.ID, x=x, y=y)
        refs.append(quarters.reference_id)
        for point in TOWER_POINTS:
            x, y = position(color, *point)
            tower = ctx.um.add_unit(player=player, unit_const=BuildingInfo.GUARD_TOWER.ID, x=x, y=y)
            refs.append(tower.reference_id)
        for point in ARCHER_POINTS:
            x, y = position(color, *point)
            archer = ctx.um.add_unit(player=player, unit_const=UnitInfo.ARCHER.ID, x=x, y=y)
            refs.append(archer.reference_id)
        x, y = position(color, *BUILDER_POINT)
        initializers.append(f"xsArraySetVector(gBuilderPads, {color}, vector({x}, {y}, -1));")
        references[color] = refs
        players.set_camera(ctx.pm, player, *position(color, 26, 55))
        # Only native Archer production and three construction choices are available.
        # Workers are earned in XS; water isolates each harbor's entire land component.
        participant = ctx.pm.players[player]
        participant.disabled_units = sorted({u.ID for u in UnitInfo if u != UnitInfo.ARCHER})
        allowed_buildings = {BuildingInfo.DOCK, BuildingInfo.WATCH_TOWER, BuildingInfo.ARCHERY_RANGE}
        participant.disabled_buildings = sorted({b.ID for b in BuildingInfo if b not in allowed_buildings})
        participant.disabled_techs = sorted({t.ID for t in TechInfo if t != TechInfo.CARTOGRAPHY})
        participant.allied_victory = True
        for index, field in enumerate(HUD_FIELDS):
            ctx.tm.add_variable(f"p{color}_{field}", (color - 1) * len(HUD_FIELDS) + index)

    options = ctx.scenario.option_manager
    options.victory_condition = VictoryCondition.CUSTOM
    options.victory_custom_conditions_required = False
    ctx.scenario.sections["GlobalVictory"].retriever_map["conquest_required"].set_data(0)
    options.lock_teams = True
    options.allow_players_choose_teams = False
    options.random_start_points = False
    start = triggers.on_start(ctx.tm, "Harbor setup")
    start.new_condition.timer(timer=1)
    triggers.announce(
        start, f"CBA Naval v{ctx.spec.version} — one ship per port every {settings['wave_interval']}s; "
        "sink every completed enemy port!", seconds=10,
    )
    for player in ctx.players.ids:
        # Scenario hard cap alone does not supply housing for native Archer queues.
        start.new_effect.modify_resource(
            source_player=player, tribute_list=Attribute.POPULATION_HEADROOM,
            quantity=ctx.players.population_cap, operation=Operation.SET,
        )
        start.new_effect.research_technology(
            source_player=player, technology=TechInfo.CARTOGRAPHY.ID, force_research_technology=True,
        )
        # The native Archery Range prerequisite is a completed Barracks. Keep its
        # construction and infantry disabled, but supply one harmless prerequisite.
        start.new_effect.change_object_name(
            source_player=player, object_list_unit_id=BuildingInfo.BARRACKS.ID,
            message="Harbor Quarters — unlocks Archery Range; no infantry training",
        )
        start.new_effect.change_object_name(
            source_player=player, object_list_unit_id=UnitInfo.LONGBOAT.ID,
            message="Hero Flagship — one at a time; returns to its berth after sinking",
        )
        for hero_type in (UnitInfo.LONGBOAT.ID, UnitInfo.TURTLE_SHIP.ID, HeroInfo.ADMIRAL_YI_SUN_SHIN.ID):
            start.new_effect.change_object_stance(
                source_player=player, object_list_unit_id=hero_type,
                attack_stance=AttackStance.STAND_GROUND,
            )
        start.new_effect.change_object_hp(
            source_player=player, object_list_unit_id=BuildingInfo.DOCK.ID,
            quantity=settings["port_hp"], operation=Operation.SET,
        )
        start.new_effect.change_object_name(
            source_player=player, object_list_unit_id=BuildingInfo.DOCK.ID,
            message="Fleet Port — a life, one ship per wave and harbor repair",
        )
        start.new_effect.change_object_hp(
            source_player=player, object_list_unit_id=BuildingInfo.GUARD_TOWER.ID,
            quantity=settings["tower_hp"], operation=Operation.SET,
        )
        start.new_effect.change_object_name(
            source_player=player, object_list_unit_id=BuildingInfo.GUARD_TOWER.ID,
            message="Harbor Battery — defend the fleet ports",
        )
        for building, hp in ((BuildingInfo.DOCK, settings["port_hp"]),
                             (BuildingInfo.WATCH_TOWER, settings["tower_hp"])):
            start.new_effect.modify_attribute(
                source_player=player, object_list_unit_id=building.ID,
                object_attributes=ObjectAttribute.HIT_POINTS, quantity=hp, operation=Operation.SET,
            )
        for unit, wood, stone in (
            (BuildingInfo.DOCK, settings["port_wood"], 0),
            (BuildingInfo.WATCH_TOWER, settings["tower_wood"], settings["tower_stone"]),
            (BuildingInfo.ARCHERY_RANGE, settings["range_wood"], 0),
            (UnitInfo.ARCHER, settings["archer_wood"], 0),
        ):
            start.new_effect.change_object_cost(
                source_player=player, object_list_unit_id=unit.ID,
                resource_1=Attribute.WOOD_STORAGE, resource_1_quantity=wood,
                resource_2=Attribute.STONE_STORAGE, resource_2_quantity=stone,
                resource_3=Attribute.FOOD_STORAGE, resource_3_quantity=0,
            )
        start.new_effect.change_object_stance(
            source_player=player, object_list_unit_id=UnitInfo.ARCHER.ID,
            attack_stance=AttackStance.STAND_GROUND,
        )

    rules = (
        f"Naval v{ctx.spec.version}: sink every completed enemy port "
        f"(4 starting + up to {settings['extra_ports']} built). "
        f"Mixed fleets every {settings['wave_interval']}s; "
        f"{settings['ships_per_port']} ships per surviving port; cap {settings['fleet_cap']}.",
        "Kills + control unlock tiers at " + "/".join(map(str, settings["rank_kills"]))
        + f". Towers defend; nearby ships heal {settings['repair_hp']} HP/s, including during combat.",
        f"Hold the azure center uncontested: +{settings['center_bonus']} prestige every "
        f"{settings['center_bonus_interval']}s; siege every {settings['center_cannon_interval']}s. "
        f"Also earn siege every {settings['siege_interval']}s and for each razing. "
        "Siege replaces one ship on the next port wave; never extra fast spawns.",
        f"Every {settings['builder_kills']} real kills: builder + {settings['builder_wood']} wood/"
        f"{settings['builder_stone']} stone, up to {settings['builder_rewards']} rewards. "
        "Build ports, Watch Towers or one Archery Range. "
        "Harbor Quarters unlock the Range; no further kills required. "
        "Archers/civilians stay on your island; no transports.",
        f"One hero flagship starts at its own berth. After sinking, it returns there in "
        f"{settings['flagship_interval']}s at your current tier; control it manually.",
    )
    for order, text in enumerate(rules):
        objective = triggers.objective(ctx.tm, f"Naval rule {order + 1}", text, order=order)
        objective.new_condition.timer(timer=2_000_000_000)
    _resolvers(ctx, references)
    ctx.message_manager.instructions = "\n".join(rules)
    ctx.message_manager.hints = (
        "Galley range, fire-ship pressure, demolition ambushes; keep siege ships screened."
    )
    ctx.message_manager.victory = "The enemy harbors have fallen. Your navy rules the sea."
    ctx.message_manager.loss = "Your last fleet port has fallen."
    constants = {name.upper(): value for name, value in settings.items() if name != "rank_kills"}
    constants.update({f"RANK_{i}": value for i, value in enumerate(settings["rank_kills"], start=1)})
    constants.update(NAVAL_IDS)
    neutralize = "\n    ".join(
        f"xsSetPlayerAttribute(owner, {int(attr)}, 0);" for attr in SCORE_NEUTRAL_ATTRIBUTES
    )
    ctx.set_xs_vars(
        **constants, INITIALIZERS="\n    ".join(initializers), HUD_STRIDE=len(HUD_FIELDS),
        SCORE_NEUTRALIZE=neutralize,
    )


def _map(ctx: BuildContext) -> None:
    """Isolated ring-shaped harbor islands; one four-tile entrance per lagoon."""
    terrain.border(ctx.mm, 3, TerrainId.WATER_DEEP)
    for color in range(1, 9):
        for x in range(3, 38):
            for y in range(43, 67):
                if 17 <= x <= 31 and 46 <= y <= 63:
                    continue
                if x >= 32 and 53 <= y <= 56:
                    continue
                if x == 16 and 46 <= y <= 63:
                    kind = TerrainId.BEACH
                else:
                    kind = TerrainId.GRASS_1
                tx, ty = position(color, x, y, 143)
                ctx.mm.get_tile(int(tx), int(ty)).terrain_id = kind
    terrain.rect(ctx.mm, 64, 64, 79, 79, TerrainId.WATER_AZURE)
    for cx, cy in ((52, 52), (91, 52), (52, 91), (91, 91)):
        terrain.disc(ctx.mm, cx, cy, 5, TerrainId.BEACH)
        terrain.disc(ctx.mm, cx, cy, 3, TerrainId.GRASS_1)


def _resolvers(ctx: BuildContext, references: dict[int, list[int]]) -> None:
    """Owner-resolved native cleanup/results; never use an XS owner as an effect selector."""
    wrappers = []
    for color in range(1, 9):
        closed = ctx.tm.add_trigger(f"Closed harbor cleanup — P{color}")
        guard = f"navalClosed{color}"
        wrappers.append(
            f"bool {guard}() {{ if (gReady == false) return (false); "
            f"return (xsArrayGetInt(gOccupied, {color}) == 0); }}"
        )
        closed.new_condition.script_call(xs_function=guard)
        closed.new_effect.remove_object(selected_object_ids=references[color])
        base = (color - 1) * len(HUD_FIELDS)
        hud = triggers.objective(
            ctx.tm, f"Fleet status — P{color}",
            f"P{color} | Ports <Variable {base}> | K <Variable {base + 1}> "
            f"| D <Variable {base + 2}> | R <Variable {base + 3}> "
            f"| Tier <Variable {base + 4}> | Waves <Variable {base + 5}> | Builders <Variable {base + 6}>",
            order=10 + color, enabled=False,
        )
        hud.new_condition.timer(timer=2_000_000_000)
        show = ctx.tm.add_trigger(f"Show fleet status — P{color}")
        guard = f"navalOccupied{color}"
        wrappers.append(
            f"bool {guard}() {{ if (gReady == false) return (false); "
            f"return (xsArrayGetInt(gOccupied, {color}) == 1); }}"
        )
        show.new_condition.script_call(xs_function=guard)
        show.new_effect.activate_trigger(trigger_id=hud.trigger_id)
        for selector in range(1, 9):
            guard = f"navalDefeat{color}W{selector}"
            wrappers.append(f"bool {guard}() {{ return (navalNeedsCleanup({color}, {selector})); }}")
            defeat = triggers.every(ctx.tm, f"Harbor defeat — P{color} W{selector}", 1)
            defeat.new_condition.script_call(xs_function=guard)
            defeat.new_effect.remove_object(source_player=selector)
            defeat.new_effect.declare_victory(source_player=selector, enabled=False)
            mark = f"navalCleaned{color}W{selector}"
            wrappers.append(f"void {mark}() {{ xsArraySetInt(gCleaned, {color}, 1); }}")
            defeat.new_effect.script_call(message=mark)
            guard = f"navalWin{color}W{selector}"
            wrappers.append(f"bool {guard}() {{ return (navalWins({color}, {selector})); }}")
            win = ctx.tm.add_trigger(f"Sea victory — P{color} W{selector}")
            win.new_condition.script_call(xs_function=guard)
            win.new_effect.declare_victory(source_player=selector, enabled=True)
    # Definitions follow main.xs, whose helpers and state they reference.
    ctx.add_xs("\n".join(wrappers), label="naval native-effect guards")
