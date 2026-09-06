"""Regression checks for CBA Hero: Ascendants gameplay systems."""

from __future__ import annotations

import hashlib
import json
import re
import sys
from collections import Counter, defaultdict, deque

import pytest
from AoE2ScenarioParser.datasets.buildings import BuildingInfo
from AoE2ScenarioParser.datasets.conditions import ConditionId
from AoE2ScenarioParser.datasets.effects import EffectId
from AoE2ScenarioParser.datasets.heroes import HeroInfo
from AoE2ScenarioParser.datasets.other import OtherInfo
from AoE2ScenarioParser.datasets.players import PlayerId
from AoE2ScenarioParser.datasets.techs import TechInfo
from AoE2ScenarioParser.datasets.terrains import TerrainId
from AoE2ScenarioParser.datasets.trigger_lists import (
    ActionType,
    Attribute,
    Comparison,
    DiplomacyState,
    ObjectAttribute,
    ObjectClass,
    ObjectType,
    Operation,
    VictoryCondition,
)
from AoE2ScenarioParser.datasets.units import UnitInfo
from AoE2ScenarioParser.scenarios.aoe2_de_scenario import AoE2DEScenario

from aoe2modes import registry
from aoe2modes.builder import build_mode
from aoe2modes.lib import mapview
from aoe2modes.lib.audit import audit_scenario


def v2_cell_for_player(player, source_x, source_y):
    x, y = source_y, source_x
    return (
        (x, y),
        (143 - x, y),
        (y, x),
        (143 - y, x),
        (y, 143 - x),
        (143 - y, 143 - x),
        (x, 143 - y),
        (143 - x, 143 - y),
    )[int(player) - 1]


def v2_position_for_player(player, source_x, source_y):
    x, y = source_y, source_x
    return (
        (x, y),
        (144 - x, y),
        (y, x),
        (144 - y, x),
        (y, 144 - x),
        (144 - y, 144 - x),
        (x, 144 - y),
        (144 - x, 144 - y),
    )[int(player) - 1]


def castle_row_areas(scenario):
    """Derive each objective row from the serialized Castles, not build.py literals."""
    areas = {}
    for player in PlayerId.all(exclude_gaia=True):
        positions = [
            (int(unit.x), int(unit.y))
            for unit in scenario.unit_manager.units[player]
            if unit.unit_const == BuildingInfo.CASTLE.ID
        ]
        assert len(positions) == 4
        xs = {x for x, _y in positions}
        ys = {y for _x, y in positions}
        assert len(xs) == 1 or len(ys) == 1
        areas[int(player)] = (
            min(xs),
            min(ys),
            max(xs),
            max(ys),
        )
    return areas


VALID_COLOR_WORLD_PAIRS = {
    (color, world_player)
    for color in range(1, 9)
    for world_player in range(1, 9)
}


def test_evolution_alpha_training_rules_do_not_depend_on_color(evolution_alpha):
    players = evolution_alpha.player_manager.players[1:9]
    for field in ("disabled_units", "disabled_buildings", "disabled_techs"):
        restrictions = [getattr(player, field) for player in players]
        assert all(len(values) == len(set(values)) for values in restrictions)
        assert len({frozenset(values) for values in restrictions}) == 1
    # Specific inherited omissions: Green Genoese/Camel Archers, Yellow
    # Conquistadors and Outposts, and Orange's unique Trade Cart restriction.
    for player in players:
        assert {866, 868, 1009, 773, 128, 279, 542} <= set(player.disabled_units)
        assert {199, 598, 621} <= set(player.disabled_buildings)


def test_evolution_alpha_returned_units_are_not_deleted_or_rebuffed_by_rewards(evolution_alpha):
    checked = Counter()
    for trigger in evolution_alpha.trigger_manager.triggers:
        if not trigger.name.startswith(("Hero Milestone", "Hero Boost", "Center Trebuchet")):
            continue
        assert not any(
            effect.effect_type in {EffectId.REMOVE_OBJECT, EffectId.KILL_OBJECT}
            for effect in trigger.effects
        ), trigger.name
        buffs = [
            effect for effect in trigger.effects
            if effect.effect_type in {EffectId.CHANGE_OBJECT_HP, EffectId.CHANGE_OBJECT_ATTACK}
        ]
        for buff in buffs:
            guards = [
                condition for condition in trigger.conditions
                if condition.condition_type == ConditionId.OBJECTS_IN_AREA
                and condition.inverted and condition.quantity == 1
                and condition.source_player == buff.source_player
                and (
                    condition.object_list == buff.object_list_unit_id
                    or condition.object_group == buff.object_group != -1
                )
            ]
            guard, = guards
            assert (guard.area_x1, guard.area_y1, guard.area_x2, guard.area_y2) == (
                buff.area_x1, buff.area_y1, buff.area_x2, buff.area_y2,
            )
            # Evaluate the exclusion against parked copies: zero occupants
            # permits a new reward; one or more blocks both creation and buffs.
            assert [not (count >= guard.quantity) for count in (0, 1, 4)] == [True, False, False]
            checked["buffs"] += 1
        checked["producers"] += 1
    assert checked == {"buffs": 576, "producers": 640}


def test_evolution_alpha_hero_off_discards_a_pending_route(evolution_alpha):
    by_name = {trigger.name: trigger for trigger in evolution_alpha.trigger_manager.triggers}
    for player in range(1, 9):
        state = {96 + player: 1, 112 + player: 3}
        off = by_name[f"Hero Range Select L0 P{player}"]
        for effect in off.effects:
            assert effect.effect_type == EffectId.CHANGE_VARIABLE
            assert effect.operation == Operation.SET
            state[effect.variable] = effect.quantity
        assert state == {96 + player: 0, 112 + player: 0}
        # Switching back on without another birth cannot resurrect the old pulse.
        for effect in by_name[f"Hero Range Select L3 P{player}"].effects:
            state[effect.variable] = effect.quantity
        assert state == {96 + player: 0, 112 + player: 3}


def test_evolution_alpha_imperial_goths_cannot_lose_barracks_to_trigger_order(evolution_alpha):
    checked = 0
    for trigger in evolution_alpha.trigger_manager.triggers:
        if not trigger.name.startswith(("Goth Anarchy S", "Goth Barracks Restriction S")):
            continue
        owner = int(trigger.name[-1])
        guard, = [
            condition for condition in trigger.conditions
            if condition.condition_type == ConditionId.RESEARCH_TECHNOLOGY
            and condition.technology == TechInfo.IMPERIAL_AGE.ID
        ]
        assert guard.inverted and guard.source_player == owner
        checked += 1
    assert checked == 128


def test_evolution_alpha_vote_markers_allow_delete_but_not_combat_votes(evolution_alpha):
    triggers = evolution_alpha.trigger_manager.triggers
    by_name = {trigger.name: trigger for trigger in triggers}
    owners = {unit.reference_id: unit.player for unit in evolution_alpha.unit_manager.get_all_units()}
    markers = {
        reference
        for effect in by_name["Range And Vote Marker Labels"].effects
        if effect.effect_type == EffectId.CHANGE_OBJECT_NAME
        and effect.message.startswith("Delete Vote Kick ")
        for reference in effect.selected_object_ids
    }
    assert len(markers) == 24
    for reference in markers:
        assert any(
            effect.effect_type == EffectId.DISABLE_UNIT_ATTACKABLE
            and effect.source_player == -1 and reference in effect.selected_object_ids
            for effect in by_name["Range Controller Safety"].effects
        )
        for owner in range(1, 9):
            detector = by_name[f"Color Owner Detect S{int(owners[reference])} W{owner}"]
            assert any(
                effect.effect_type == EffectId.DISABLE_UNIT_ATTACKABLE
                and effect.source_player == owner and reference in effect.selected_object_ids
                for effect in detector.effects
            )
    assert not any(
        markers.intersection(effect.selected_object_ids)
        for trigger in triggers for effect in trigger.effects
        if effect.effect_type == EffectId.DISABLE_OBJECT_DELETION
    )


@pytest.fixture(scope="module")
def evolution_alpha(tmp_path_factory, repo):
    spec = registry.get("evolution_alpha", repo)
    result = build_mode(
        spec,
        out_dir=tmp_path_factory.mktemp("evolution-alpha"),
        xs_check=False,
    )
    return AoE2DEScenario.from_file(str(result.output))


def test_evolution_alpha_keeps_compact_trigger_count(evolution_alpha):
    triggers = evolution_alpha.trigger_manager.triggers
    assert len(triggers) == 3_783
    assert sum(len(units) for units in evolution_alpha.unit_manager.units) == 956
    assert all(trigger.conditions or trigger.effects for trigger in triggers)
    names = [trigger.name for trigger in triggers]
    assert len(names) == len(set(names))
    assert len(
        [
            trigger
            for trigger in triggers
            if re.fullmatch(
                r"\d+ kills \(p[1-8](?:, legacy variant [12])?\)",
                trigger.name,
            )
        ]
    ) == 99


def test_evolution_alpha_passes_parser_structural_audit(evolution_alpha):
    report = audit_scenario(evolution_alpha)
    assert report.errors == []
    assert report.warnings == []


def test_evolution_alpha_uses_v2_terrain_with_protected_team_routes(evolution_alpha):
    terrain = bytes(
        evolution_alpha.map_manager.get_tile(x=x, y=y).terrain_id
        for y in range(144)
        for x in range(144)
    )
    assert hashlib.sha256(terrain).hexdigest() == (
        "6cd911471fc98a7694539d9beac7947697ad3b038ab243d9ae59c834daf0b45f"
    )

    source_milestone_shore = {
        *((15, y) for y in range(38, 43)),
        (16, 39),
        (17, 38),
        (17, 39),
        *((x, 39) for x in range(18, 24)),
        *((24, y) for y in range(38, 44)),
    }
    assert len(source_milestone_shore) == 20
    milestone_shore = {
        v2_cell_for_player(player, source_x, source_y)
        for player in PlayerId.all(exclude_gaia=True)
        for source_x, source_y in source_milestone_shore
    }
    assert len(milestone_shore) == 160
    assert {
        (
            evolution_alpha.map_manager.get_tile(x=x, y=y).terrain_id,
            evolution_alpha.map_manager.get_tile(x=x, y=y).elevation,
            evolution_alpha.map_manager.get_tile(x=x, y=y).layer,
        )
        for x, y in milestone_shore
    } == {(TerrainId.GRASS_2, 1, -1)}

    transforms = (
        lambda x, y: (x, y),
        lambda x, y: (143 - x, y),
        lambda x, y: (y, x),
        lambda x, y: (143 - y, x),
        lambda x, y: (y, 143 - x),
        lambda x, y: (143 - y, 143 - x),
        lambda x, y: (x, 143 - y),
        lambda x, y: (143 - x, 143 - y),
    )
    route_orbits = set()
    for x1, y1, x2, y2 in ((65, 20, 78, 23), (65, 120, 78, 123)):
        for y in range(y1, y2 + 1):
            for x in range(x1, x2 + 1):
                route_orbits.update(transform(x, y) for transform in transforms)
    entrance_accent_tiles = {
        v2_cell_for_player(player, source_x, source_y)
        for player in PlayerId.all(exclude_gaia=True)
        for source_x in range(36, 39)
        for source_y in range(53, 56)
    }

    asymmetrical = set()
    for y in range(144):
        for x in range(144):
            tile = evolution_alpha.map_manager.get_tile(x=x, y=y)
            tile_values = (tile.terrain_id, tile.elevation, tile.layer)
            transformed_terrain = set()
            for transform in transforms:
                transformed_x, transformed_y = transform(x, y)
                transformed_tile = evolution_alpha.map_manager.get_tile(
                    x=transformed_x,
                    y=transformed_y,
                )
                transformed_terrain.add(
                    (
                        transformed_tile.terrain_id,
                        transformed_tile.elevation,
                        transformed_tile.layer,
                    )
                )
            if transformed_terrain != {tile_values}:
                asymmetrical.add((x, y))
    assert asymmetrical == route_orbits | entrance_accent_tiles

    for x1, y1, x2, y2 in ((65, 20, 78, 23), (65, 120, 78, 123)):
        assert {
            evolution_alpha.map_manager.get_tile(x=x, y=y).terrain_id
            for y in range(y1, y2 + 1)
            for x in range(x1, x2 + 1)
        } == {TerrainId.GRASS_2}
    for x1, y1, x2, y2 in ((20, 65, 23, 78), (120, 65, 123, 78)):
        assert {
            evolution_alpha.map_manager.get_tile(x=x, y=y).terrain_id
            for y in range(y1, y2 + 1)
            for x in range(x1, x2 + 1)
        } == {TerrainId.WATER_MEDIUM}

    winter_terrains = {
        TerrainId.FOREST_PINE_SNOW,
        TerrainId.ICE_NAVIGABLE,
        TerrainId.SNOW,
        TerrainId.OBSOLETE_SNOW_DIRT,
        TerrainId.OBSOLETE_SNOW_GRASS,
        TerrainId.ICE,
        TerrainId.SNOW_FOUNDATION,
        TerrainId.BEACH_ICE,
        TerrainId.OBSOLETE_ROAD_SNOW,
        TerrainId.UNDERBRUSH_SNOW,
        TerrainId.SNOW_LIGHT,
        TerrainId.SNOW_STRONG,
        TerrainId.FOREST_AUTUMN_SNOW,
        TerrainId.SNOW_SOFT,
        TerrainId.SNOW_SOFT_LIGHT,
        TerrainId.SNOW_SOFT_STRONG,
        TerrainId.ICE_SOFT,
    }
    winter_cells = {
        (x, y)
        for y in range(144)
        for x in range(144)
        if evolution_alpha.map_manager.get_tile(x=x, y=y).terrain_id in winter_terrains
    }
    expected_snow_cells = {
        v2_cell_for_player(player, source_x, source_y)
        for player in PlayerId.all(exclude_gaia=True)
        for source_x in range(1, 4)
        for source_y in (60, 61, 65, 66)
    }
    assert winter_cells == expected_snow_cells
    assert len(winter_cells) == 96
    assert {
        evolution_alpha.map_manager.get_tile(x=x, y=y).terrain_id
        for x, y in winter_cells
    } == {TerrainId.SNOW}

    entrance_terrains = {
        PlayerId.ONE: TerrainId.ROAD_GRAVEL,
        PlayerId.TWO: TerrainId.DIRT_4,
        PlayerId.THREE: TerrainId.GRASS_1,
        PlayerId.FOUR: TerrainId.DESERT_SAND,
        PlayerId.FIVE: TerrainId.GRASS_3,
        PlayerId.SIX: TerrainId.ROAD_FUNGUS,
        PlayerId.SEVEN: TerrainId.ROAD,
        PlayerId.EIGHT: TerrainId.DIRT_1,
    }
    for player, terrain_id in entrance_terrains.items():
        assert {
            evolution_alpha.map_manager.get_tile(
                x=v2_cell_for_player(player, source_x, source_y)[0],
                y=v2_cell_for_player(player, source_x, source_y)[1],
            ).terrain_id
            for source_x in range(36, 39)
            for source_y in range(53, 56)
        } == {terrain_id}


def test_evolution_alpha_trims_all_four_corner_team_routes(evolution_alpha):
    source_cut = {
        *((x, y) for x in range(15, 38) for y in range(15, 19)),
        *((x, y) for x in range(15, 19) for y in range(19, 38)),
    }
    cut_tiles = {
        v2_cell_for_player(player, source_x, source_y)
        for player in PlayerId.all(exclude_gaia=True)
        for source_x, source_y in source_cut
    }
    assert len(cut_tiles) == 672
    assert {
        evolution_alpha.map_manager.get_tile(x=x, y=y).terrain_id
        for x, y in cut_tiles
    } == {TerrainId.WATER_MEDIUM}

    occupied_tiles = {
        (int(unit.x), int(unit.y))
        for units in evolution_alpha.unit_manager.units
        for unit in units
    }
    assert cut_tiles.isdisjoint(occupied_tiles)

    for player in PlayerId.all(exclude_gaia=True):
        inner_route = {
            v2_cell_for_player(player, source_x, source_y)
            for source_x, source_y in (
                *((x, 19) for x in range(19, 38)),
                *((19, y) for y in range(19, 38)),
            )
        }
        assert {
            evolution_alpha.map_manager.get_tile(x=x, y=y).terrain_id
            for x, y in inner_route
        } == {TerrainId.GRASS_2}


def test_evolution_alpha_keeps_v2_objects_and_playable_gate_holes(evolution_alpha):
    original = []
    additions = []
    for player, units in enumerate(evolution_alpha.unit_manager.units):
        for unit in units:
            values = (
                int(unit.unit_const),
                float(unit.x),
                float(unit.y),
                float(unit.rotation),
                int(unit.status),
            )
            if unit.reference_id <= 109_906:
                original.append((int(unit.reference_id), *values))
            else:
                additions.append((player, *values))

    original_digest = hashlib.sha256(
        json.dumps(sorted(original), separators=(",", ":")).encode()
    ).hexdigest()
    additions_digest = hashlib.sha256(
        json.dumps(sorted(additions), separators=(",", ":")).encode()
    ).hexdigest()

    assert len(original) == 816
    assert original_digest == (
        "46db5fdc5165b1ea1ca13082d7d9d2d05081d61ebc44e04e7cd4fb4a46fe631d"
    )
    assert len(additions) == 140
    assert additions_digest == (
        "fdb8e4b15188e86c0d45725aff25842fd5201376525780579f874dfc6b06ae0b"
    )


def test_evolution_alpha_orients_every_v2_wall_and_gate_by_map_axis(
    evolution_alpha,
):
    unit_manager = evolution_alpha.unit_manager
    source_walls = [
        unit
        for unit in unit_manager.units[PlayerId.THREE]
        if unit.unit_const == BuildingInfo.STONE_WALL.ID
    ]
    source_gates = [
        unit
        for unit in unit_manager.units[PlayerId.THREE]
        if unit.unit_const in {64, 88}
    ]
    cuts = {
        PlayerId.ONE: {(64.5, y) for y in (20.5, 21.5, 22.5, 23.5)},
        PlayerId.TWO: {(79.5, y) for y in (20.5, 21.5, 22.5, 23.5)},
        PlayerId.SEVEN: {(64.5, y) for y in (120.5, 121.5, 122.5, 123.5)},
        PlayerId.EIGHT: {(79.5, y) for y in (120.5, 121.5, 122.5, 123.5)},
    }

    def transformed_axis(player, source, horizontal):
        first = v2_position_for_player(player, source.x, source.y)
        second = v2_position_for_player(
            player,
            source.x + int(horizontal),
            source.y + int(not horizontal),
        )
        return 0 if abs(second[0] - first[0]) > abs(second[1] - first[1]) else 1

    for player in PlayerId.all(exclude_gaia=True):
        walls_by_position = {
            (unit.x, unit.y): unit
            for unit in unit_manager.units[player]
            if unit.unit_const == BuildingInfo.STONE_WALL.ID
        }
        gates_by_position = {
            (unit.x, unit.y): unit
            for unit in unit_manager.units[player]
            if unit.unit_const in {64, 88}
        }
        for source in source_walls:
            position = v2_position_for_player(player, source.x, source.y)
            if position in cuts.get(player, set()):
                assert position not in walls_by_position
                continue
            target = walls_by_position[position]
            expected_rotation = (
                source.rotation
                if source.rotation == 2
                else transformed_axis(player, source, source.rotation == 0)
            )
            assert target.rotation == expected_rotation
        for source in source_gates:
            position = v2_position_for_player(player, source.x, source.y)
            target = gates_by_position[position]
            expected_axis = transformed_axis(
                player,
                source,
                source.unit_const == 64,
            )
            assert target.unit_const == (64 if expected_axis == 0 else 88)

    assert sum(
        unit.unit_const in {64, 88}
        for units in unit_manager.units
        for unit in units
    ) == 44


def test_evolution_alpha_keeps_allied_routes_open_and_enemy_sides_water(
    evolution_alpha,
):
    side_gates = {
        PlayerId.ONE: (109_743, 64.5, 22.0),
        PlayerId.TWO: (109_744, 79.5, 22.0),
        PlayerId.SEVEN: (109_745, 64.5, 122.0),
        PlayerId.EIGHT: (109_746, 79.5, 122.0),
    }
    wall_slots = {
        PlayerId.ONE: {(64.5, y) for y in (20.5, 21.5, 22.5, 23.5)},
        PlayerId.TWO: {(79.5, y) for y in (20.5, 21.5, 22.5, 23.5)},
        PlayerId.SEVEN: {(64.5, y) for y in (120.5, 121.5, 122.5, 123.5)},
        PlayerId.EIGHT: {(79.5, y) for y in (120.5, 121.5, 122.5, 123.5)},
    }
    water = {int(terrain) for terrain in TerrainId.water_terrains()}

    for player, (reference_id, x, y) in side_gates.items():
        gate = next(
            unit
            for unit in evolution_alpha.unit_manager.units[player]
            if unit.reference_id == reference_id
        )
        assert (gate.unit_const, gate.x, gate.y) == (88, x, y)
        assert evolution_alpha.map_manager.get_tile(
            x=int(gate.x),
            y=int(gate.y),
        ).terrain_id not in water
        player_walls = {
            (unit.x, unit.y)
            for unit in evolution_alpha.unit_manager.units[player]
            if unit.unit_const == BuildingInfo.STONE_WALL.ID
        }
        assert wall_slots[player].isdisjoint(player_walls)

    cliff_ids = {
        getattr(OtherInfo, f"CLIFF_DEFAULT_{index}").ID
        for index in range(1, 10)
    }
    gaia_cliffs = [
        unit
        for unit in evolution_alpha.unit_manager.units[PlayerId.GAIA]
        if unit.unit_const in cliff_ids
    ]
    all_units = [
        unit
        for units in evolution_alpha.unit_manager.units[1:]
        for unit in units
    ]
    for x1, y1, x2, y2 in ((65, 20, 78, 23), (65, 120, 78, 123)):
        assert not [
            cliff
            for cliff in gaia_cliffs
            if x1 <= cliff.x < x2 + 1 and y1 <= cliff.y < y2 + 1
        ]
        assert not [
            unit
            for unit in all_units
            if x1 <= int(unit.x) <= x2 and y1 <= int(unit.y) <= y2
        ]


def test_evolution_alpha_all_six_allied_links_have_clear_dry_centerlines(
    evolution_alpha,
):
    routes = {
        (1, 2): ({(x, 22) for x in range(64, 80)}, {109_743, 109_744}),
        (1, 3): (
            {(x, 23) for x in range(23, 44)}
            | {(23, y) for y in range(23, 44)},
            {65_500, 23_621},
        ),
        (2, 4): (
            {(x, 23) for x in range(100, 122)}
            | {(121, y) for y in range(23, 44)},
            {23_076, 23_205},
        ),
        (5, 7): (
            {(23, y) for y in range(100, 122)}
            | {(x, 121) for x in range(23, 44)},
            {23_618, 23_624},
        ),
        (6, 8): (
            {(121, y) for y in range(100, 122)}
            | {(x, 121) for x in range(100, 122)},
            {23_615, 23_627},
        ),
        (7, 8): ({(x, 122) for x in range(64, 80)}, {109_745, 109_746}),
    }
    water = {int(terrain) for terrain in TerrainId.water_terrains()}
    all_units = [
        unit
        for units in evolution_alpha.unit_manager.units
        for unit in units
    ]
    for (_first, _second), (tiles, expected_gates) in routes.items():
        assert all(
            evolution_alpha.map_manager.get_tile(x=x, y=y).terrain_id not in water
            for x, y in tiles
        )
        occupants = {
            unit.reference_id
            for unit in all_units
            if (int(unit.x), int(unit.y)) in tiles
        }
        assert occupants == expected_gates


def test_evolution_alpha_pins_king_and_relic_selector_roles(evolution_alpha):
    targets = {
        PlayerId.ONE: {95_792: (838, 39.5, 0.5), 48_301: (434, 45.5, 5.5)},
        PlayerId.TWO: {95_959: (434, 104.5, 0.5), 42_394: (434, 98.5, 5.5)},
        PlayerId.THREE: {95_961: (434, 0.5, 39.5), 42_395: (434, 5.5, 45.5)},
        PlayerId.FOUR: {95_962: (434, 143.5, 39.5), 42_396: (434, 138.5, 45.5)},
        PlayerId.FIVE: {95_963: (434, 0.5, 104.5), 42_397: (434, 5.5, 98.5)},
        PlayerId.SIX: {95_964: (434, 143.5, 104.5), 42_398: (434, 138.5, 98.5)},
        PlayerId.SEVEN: {95_965: (434, 39.5, 143.5), 42_399: (434, 45.5, 138.5)},
        PlayerId.EIGHT: {95_966: (434, 104.5, 143.5), 42_400: (434, 98.5, 138.5)},
    }
    for player, expected in targets.items():
        by_reference_id = {
            unit.reference_id: unit
            for unit in evolution_alpha.unit_manager.units[player]
        }
        for reference_id, values in expected.items():
            unit = by_reference_id[reference_id]
            assert (unit.unit_const, unit.x, unit.y) == values


def test_evolution_alpha_kings_use_symmetric_island_destinations(evolution_alpha):
    expected_references = {
        PlayerId.ONE: 95_792,
        PlayerId.TWO: 95_959,
        PlayerId.THREE: 95_961,
        PlayerId.FOUR: 95_962,
        PlayerId.FIVE: 95_963,
        PlayerId.SIX: 95_964,
        PlayerId.SEVEN: 95_965,
        PlayerId.EIGHT: 95_966,
    }
    source_area = (2, 38, 3, 40)
    pattern = re.compile(r"King Island S([1-8]) W([1-8])")
    triggers = {
        tuple(map(int, match.groups())): trigger
        for trigger in evolution_alpha.trigger_manager.triggers
        if (match := pattern.fullmatch(trigger.name))
    }
    assert set(triggers) == VALID_COLOR_WORLD_PAIRS
    for player, reference_id in expected_references.items():
        corners = (
            v2_cell_for_player(player, source_area[0], source_area[1]),
            v2_cell_for_player(player, source_area[0], source_area[3]),
            v2_cell_for_player(player, source_area[2], source_area[1]),
            v2_cell_for_player(player, source_area[2], source_area[3]),
        )
        expected_area = (
            min(x for x, _y in corners),
            min(y for _x, y in corners),
            max(x for x, _y in corners),
            max(y for _x, y in corners),
        )
        for world_player in range(1, 9):
            trigger = triggers[int(player), world_player]
            conditions = [
                condition
                for condition in trigger.conditions
                if condition.condition_type == ConditionId.BRING_OBJECT_TO_AREA
            ]
            assert len(conditions) == 1
            condition = conditions[0]
            assert condition.unit_object == reference_id
            assert (
                condition.area_x1,
                condition.area_y1,
                condition.area_x2,
                condition.area_y2,
            ) == expected_area
            assert {
                (item.variable, item.quantity, item.comparison)
                for item in trigger.conditions
                if item.condition_type == ConditionId.VARIABLE_VALUE
            } == {
                (31 + int(player), 1, Comparison.EQUAL),
                (39 + int(player), world_player, Comparison.EQUAL),
                (47 + int(player), 0, Comparison.EQUAL),
            }


def test_evolution_alpha_king_cannons_use_symmetric_ground_positions(evolution_alpha):
    source_positions = (
        (25, 61),
        (32, 61),
        (38, 61),
        (38, 45),
        (34, 45),
        (27, 45),
    )
    water = {int(terrain) for terrain in TerrainId.water_terrains()}
    occupied_fortifications = {
        (int(unit.x), int(unit.y))
        for player in PlayerId.all(exclude_gaia=True)
        for unit in evolution_alpha.unit_manager.units[player]
        if unit.unit_const
        in {
            BuildingInfo.STONE_WALL.ID,
            BuildingInfo.GATE_SOUTHWEST_TO_NORTHEAST.ID,
            BuildingInfo.GATE_NORTHWEST_TO_SOUTHEAST.ID,
        }
    }
    pattern = re.compile(r"King Island S([1-8]) W([1-8])")
    triggers = {
        tuple(map(int, match.groups())): trigger
        for trigger in evolution_alpha.trigger_manager.triggers
        if (match := pattern.fullmatch(trigger.name))
    }
    by_id = {
        trigger.trigger_id: trigger
        for trigger in evolution_alpha.trigger_manager.triggers
    }
    assert set(triggers) == VALID_COLOR_WORLD_PAIRS
    for player in PlayerId.all(exclude_gaia=True):
        expected_positions = tuple(
            v2_cell_for_player(player, x, y)
            for x, y in source_positions
        )
        for x, y in expected_positions:
            assert evolution_alpha.map_manager.get_tile(
                x=int(x),
                y=int(y),
            ).terrain_id not in water
            assert (x, y) not in occupied_fortifications
        for world_player in range(1, 9):
            trigger = triggers[int(player), world_player]
            creates = [
                effect
                for effect in trigger.effects
                if effect.effect_type == EffectId.CREATE_OBJECT
                and effect.object_list_unit_id == UnitInfo.SCORPION.ID
            ]
            assert len(creates) == 6
            assert tuple(
                (effect.location_x, effect.location_y)
                for effect in creates
            ) == expected_positions
            assert {effect.source_player for effect in creates} == {world_player}
            buffs = [
                effect
                for effect in trigger.effects
                if effect.effect_type
                in {EffectId.CHANGE_OBJECT_HP, EffectId.CHANGE_OBJECT_ATTACK}
                and effect.object_list_unit_id == UnitInfo.SCORPION.ID
            ]
            assert len(buffs) == 2
            assert {effect.source_player for effect in buffs} == {world_player}
            assert all(
                buff.area_x1 <= x <= buff.area_x2
                and buff.area_y1 <= y <= buff.area_y2
                for buff in buffs
                for x, y in expected_positions
            )
            cleanup_ids = {
                effect.trigger_id
                for effect in trigger.effects
                if effect.effect_type == EffectId.ACTIVATE_TRIGGER
            }
            assert {by_id[trigger_id].name for trigger_id in cleanup_ids} == {
                f"King Island Cleanup W{world_player}"
            }
            for trigger_id in cleanup_ids:
                cleanup = by_id[trigger_id]
                assert [
                    condition.timer for condition in cleanup.conditions
                    if condition.condition_type == ConditionId.TIMER
                ] == [50]  # Intentional reward lifetime; do not remove this rule.
                assert any(
                    effect.effect_type == EffectId.REMOVE_OBJECT
                    and effect.source_player == world_player
                    and effect.object_list_unit_id == UnitInfo.SCORPION.ID
                    for effect in cleanup.effects
                )


def test_evolution_alpha_builds_clear_two_lane_range_islands(evolution_alpha):
    gaia_units = evolution_alpha.unit_manager.units[PlayerId.GAIA]
    water = {int(terrain) for terrain in TerrainId.water_terrains()}
    assert not [
        unit
        for unit in gaia_units
        if unit.unit_const in {OtherInfo.RELIC.ID, OtherInfo.RUGS.ID}
    ]

    expected_signs = {
        v2_position_for_player(player, x, y)
        for player in PlayerId.all(exclude_gaia=True)
        for x, y in ((2.5, 60.5), (9.5, 60.5), (2.5, 66.5), (9.5, 66.5))
    }
    actual_signs = {
        (unit.x, unit.y)
        for unit in gaia_units
        if unit.unit_const == OtherInfo.SIGN.ID
    }
    assert actual_signs == expected_signs

    for player in PlayerId.all(exclude_gaia=True):
        island_cells = {
            v2_cell_for_player(player, source_x, source_y)
            for source_y in range(60, 67)
            for source_x in range(1, 10)
        }
        for source_y in range(60, 67):
            for source_x in range(1, 10):
                x, y = v2_cell_for_player(player, source_x, source_y)
                expected_terrain = (
                    TerrainId.WATER_DEEP
                    if source_y in {62, 63, 64}
                    else TerrainId.SNOW
                    if source_x <= 3
                    else TerrainId.ROAD
                    if source_y <= 61
                    else TerrainId.ROAD_GRAVEL
                )
                tile = evolution_alpha.map_manager.get_tile(x=x, y=y)
                assert (tile.terrain_id, tile.elevation, tile.layer) == (
                    expected_terrain,
                    1,
                    -1,
                )

        old_torches = {
            v2_position_for_player(player, x, y)
            for x, y in ((4, 63), (5, 63), (4, 64), (5, 64))
        }
        assert not [
            unit
            for unit in evolution_alpha.unit_manager.units[player]
            if unit.unit_const == OtherInfo.TORCH_A.ID
            and (unit.x, unit.y) in old_torches
        ]

        island_objects = []
        for owner, units in enumerate(evolution_alpha.unit_manager.units):
            for unit in units:
                footprint = mapview._footprint(unit.unit_const, unit.x, unit.y)
                occupied = set(footprint) or {(int(unit.x), int(unit.y))}
                if island_cells.intersection(occupied):
                    island_objects.append((owner, unit.unit_const))
        assert Counter(island_objects) == Counter(
            {
                (PlayerId.GAIA, OtherInfo.SIGN.ID): 4,
                (player, UnitInfo.SHEEP.ID): 1,
                (player, UnitInfo.WAR_PENGUIN.ID): 1,
            }
        )
        assert not [
            (trigger.name, effect.location_x, effect.location_y)
            for trigger in evolution_alpha.trigger_manager.triggers
            for effect in trigger.effects
            if effect.effect_type == EffectId.CREATE_OBJECT
            and island_cells.intersection(
                mapview._footprint(
                    effect.object_list_unit_id,
                    effect.location_x,
                    effect.location_y,
                )
                or [(effect.location_x, effect.location_y)]
            )
        ]
        moat = {
            (next_x, next_y)
            for x, y in island_cells
            for next_x, next_y in (
                (x - 1, y),
                (x + 1, y),
                (x, y - 1),
                (x, y + 1),
            )
            if 0 <= next_x < 144
            and 0 <= next_y < 144
            and (next_x, next_y) not in island_cells
        }
        assert len(moat) == 32
        assert all(
            evolution_alpha.map_manager.get_tile(x=x, y=y).terrain_id in water
            for x, y in moat
        )
        harmful_area_effects = {
            EffectId.CHANGE_OWNERSHIP,
            EffectId.DAMAGE_OBJECT,
            EffectId.DISABLE_OBJECT_SELECTION,
            EffectId.FREEZE_OBJECT,
            EffectId.KILL_OBJECT,
            EffectId.REMOVE_OBJECT,
            EffectId.REPLACE_OBJECT,
            EffectId.STOP_OBJECT,
            EffectId.TASK_OBJECT,
        }
        for trigger in evolution_alpha.trigger_manager.triggers:
            for effect in trigger.effects:
                if effect.effect_type not in harmful_area_effects or min(
                    effect.area_x1,
                    effect.area_y1,
                    effect.area_x2,
                    effect.area_y2,
                ) < 0:
                    continue
                if (
                    effect.object_list_unit_id >= 0
                    and effect.object_list_unit_id
                    not in {UnitInfo.SHEEP.ID, UnitInfo.WAR_PENGUIN.ID}
                ):
                    continue
                if effect.object_group == ObjectClass.WALL:
                    continue
                island_x1 = min(x for x, _y in island_cells)
                island_y1 = min(y for _x, y in island_cells)
                island_x2 = max(x for x, _y in island_cells)
                island_y2 = max(y for _x, y in island_cells)
                if (
                    effect.area_x2 < island_x1
                    or effect.area_x1 > island_x2
                    or effect.area_y2 < island_y1
                    or effect.area_y1 > island_y2
                ):
                    continue
                assert effect.effect_type == EffectId.REMOVE_OBJECT
                assert trigger.name.startswith(
                    (
                        "Color Defeat Resolve ",
                        "Color Runtime Defeated ",
                        "Color Elimination Cleanup ",
                        "Vote Kick Resolve ",
                    )
                )

    expected_ornaments = {
        v2_position_for_player(player, 2.5, 39.5)
        for player in PlayerId.all(exclude_gaia=True)
    }
    actual_ornaments = {
        (unit.x, unit.y)
        for units in evolution_alpha.unit_manager.units
        for unit in units
        if unit.unit_const == OtherInfo.NINE_BANDS.ID
    }
    assert actual_ornaments == expected_ornaments


def test_evolution_alpha_controllers_cannot_leave_their_trigger_tracks(evolution_alpha):
    """Conservative terrain and footprint checks, not a DE-engine path simulation."""
    by_name = {
        trigger.name: trigger
        for trigger in evolution_alpha.trigger_manager.triggers
    }
    all_units = [
        unit
        for units in evolution_alpha.unit_manager.units
        for unit in units
    ]
    controller_refs = {
        condition.unit_object
        for trigger in evolution_alpha.trigger_manager.triggers
        if re.fullmatch(r"(?:Army|Hero) Range Select L[0-5] P[1-8]", trigger.name)
        for condition in trigger.conditions
        if condition.condition_type == ConditionId.BRING_OBJECT_TO_AREA
    }
    unit_by_reference = {unit.reference_id: unit for unit in all_units}
    # Installed DE data: both controller types use land restriction 7. These
    # water types block it; SHALLOWS, ICE and WATER_2D_BRIDGE do not. Deliberately
    # treat every other terrain as passable so unknown/passable "water" cannot
    # accidentally prove that an escape route is sealed.
    blocked_terrain = {
        TerrainId.WATER_DEEP,
        TerrainId.WATER_MEDIUM,
        TerrainId.WATER_SHALLOW,
    }
    potentially_passable = {
        (x, y)
        for x in range(144)
        for y in range(144)
        if evolution_alpha.map_manager.get_tile(x=x, y=y).terrain_id not in blocked_terrain
    }
    prop_footprints = {
        cell
        for unit in all_units
        if unit.reference_id not in controller_refs
        for cell in mapview._footprint(unit.unit_const, unit.x, unit.y)
    }

    def reachable_from(start, passable, diagonal=False):
        assert start in passable
        reachable = {start}
        pending = deque([start])
        steps = ((1, 0), (-1, 0), (0, 1), (0, -1))
        if diagonal:
            # Unrestricted diagonal movement is intentionally stricter than
            # real corner collision: even this cannot escape the water moat.
            steps += ((1, 1), (1, -1), (-1, 1), (-1, -1))
        while pending:
            x, y = pending.popleft()
            for dx, dy in steps:
                neighbor = x + dx, y + dy
                if neighbor in passable and neighbor not in reachable:
                    reachable.add(neighbor)
                    pending.append(neighbor)
        return reachable

    all_tracks = []
    for player in PlayerId.all(exclude_gaia=True):
        for family, source_y1, source_y2 in (("Army", 60, 61), ("Hero", 65, 66)):
            bands = []
            reference_ids = set()
            for level in range(6):
                trigger = by_name[f"{family} Range Select L{level} P{int(player)}"]
                condition, = [
                    condition
                    for condition in trigger.conditions
                    if condition.condition_type == ConditionId.BRING_OBJECT_TO_AREA
                ]
                reference_ids.add(condition.unit_object)
                bands.append({
                    (x, y)
                    for x in range(condition.area_x1, condition.area_x2 + 1)
                    for y in range(condition.area_y1, condition.area_y2 + 1)
                })
            reference_id, = reference_ids
            controller = unit_by_reference[reference_id]
            start = int(controller.x), int(controller.y)
            track = {
                v2_cell_for_player(player, source_x, source_y)
                for source_x in range(1, 10)
                for source_y in range(source_y1, source_y2 + 1)
            }
            assert len(track) == 18
            assert set().union(*bands) == track
            assert sum(map(len, bands)) == len(track)
            assert start in bands[3]
            assert reachable_from(start, potentially_passable, diagonal=True) == track

            # Two half-tile-centred endpoint Signs may occupy the outside row,
            # but must never block both cells at any slider position.
            unblocked_track = track - prop_footprints
            assert len(unblocked_track) == 16
            assert reachable_from(start, unblocked_track) == unblocked_track
            assert all(band.intersection(unblocked_track) for band in bands)
            for source_x in range(1, 10):
                cross_section = {
                    v2_cell_for_player(player, source_x, source_y)
                    for source_y in range(source_y1, source_y2 + 1)
                }
                assert cross_section.intersection(unblocked_track)
            all_tracks.append(track)

    assert len(all_tracks) == 16
    assert sum(map(len, all_tracks)) == len(set().union(*all_tracks))


def test_evolution_alpha_places_vote_flags_beside_their_markers(evolution_alpha):
    offsets = {
        PlayerId.ONE: (2, 0),
        PlayerId.TWO: (-2, 0),
        PlayerId.THREE: (0, 2),
        PlayerId.FOUR: (0, 2),
        PlayerId.FIVE: (0, -2),
        PlayerId.SIX: (0, -2),
        PlayerId.SEVEN: (2, 0),
        PlayerId.EIGHT: (-2, 0),
    }
    color_by_name = {
        name: PlayerId(player)
        for player, name in {
            1: "BLUE",
            2: "RED",
            3: "GREEN",
            4: "YELLOW",
            5: "TEAL",
            6: "PURPLE",
            7: "GRAY",
            8: "ORANGE",
        }.items()
    }
    unit_by_reference = {
        unit.reference_id: (PlayerId(player), unit)
        for player, units in enumerate(evolution_alpha.unit_manager.units)
        for unit in units
    }
    expected_flags = set()
    for trigger in evolution_alpha.trigger_manager.triggers:
        if trigger.name != "Range And Vote Marker Labels":
            continue
        for effect in trigger.effects:
            if not (effect.message or "").startswith("Delete Vote Kick "):
                continue
            target = color_by_name[
                effect.message.removeprefix("Delete Vote Kick ")
            ]
            voter, marker = unit_by_reference[effect.selected_object_ids[0]]
            offset_x, offset_y = offsets[voter]
            expected_flags.add(
                (target, marker.x + offset_x, marker.y + offset_y)
            )
    assert len(expected_flags) == 24
    actual_flags = {
        (PlayerId(player), unit.x, unit.y)
        for player, units in enumerate(evolution_alpha.unit_manager.units)
        for unit in units
        if unit.unit_const == OtherInfo.CIV_FLAG_ACHAEMENIDS_2.ID
    }
    assert actual_flags == expected_flags


def test_evolution_alpha_removes_corner_staging_objects_and_submerged_clutter(
    evolution_alpha,
):
    water = {int(terrain) for terrain in TerrainId.water_terrains()}
    removed_types = {
        BuildingInfo.PALISADE_WALL.ID,
        HeroInfo.SABOTEUR.ID,
        OtherInfo.ICE_NAVIGABLE.ID,
    }
    all_units = [
        unit
        for units in evolution_alpha.unit_manager.units
        for unit in units
    ]
    assert all(unit.unit_const not in removed_types for unit in all_units)
    assert all(
        evolution_alpha.map_manager.get_tile(
            x=int(unit.x),
            y=int(unit.y),
        ).terrain_id
        not in water
        for unit in all_units
    )


def test_evolution_alpha_static_corner_clutter_is_not_referenced(evolution_alpha):
    removed_reference_ids = (
        set(range(67_515, 67_529))
        | set(range(67_593, 67_626))
        | set(range(67_627, 67_636))
        | set(range(67_700, 67_708))
    )
    assert all(
        not set(effect.selected_object_ids or ()) & removed_reference_ids
        for trigger in evolution_alpha.trigger_manager.triggers
        for effect in trigger.effects
    )
    assert all(
        condition.unit_object not in removed_reference_ids
        for trigger in evolution_alpha.trigger_manager.triggers
        for condition in trigger.conditions
        if condition.unit_object is not None
    )


def test_evolution_alpha_has_no_transport_ship_spawn_markers(evolution_alpha):
    assert all(
        unit.unit_const != UnitInfo.TRANSPORT_SHIP.ID
        for units in evolution_alpha.unit_manager.units
        for unit in units
    )


def test_evolution_alpha_uses_independent_sheep_and_penguin_range_sliders(
    evolution_alpha,
):
    by_name = {
        trigger.name: trigger
        for trigger in evolution_alpha.trigger_manager.triggers
    }
    unit_by_reference = {
        unit.reference_id: unit
        for units in evolution_alpha.unit_manager.units
        for unit in units
    }
    water = {int(terrain) for terrain in TerrainId.water_terrains()}
    forbidden_effects = {
        EffectId.CHANGE_OWNERSHIP,
        EffectId.DAMAGE_OBJECT,
        EffectId.DISABLE_OBJECT_SELECTION,
        EffectId.FREEZE_OBJECT,
        EffectId.STOP_OBJECT,
        EffectId.KILL_OBJECT,
        EffectId.REMOVE_OBJECT,
        EffectId.REPLACE_OBJECT,
        EffectId.TASK_OBJECT,
    }

    def transformed_area(player, source_area):
        source_x1, source_y1, source_x2, source_y2 = source_area
        corners = (
            v2_cell_for_player(player, source_x1, source_y1),
            v2_cell_for_player(player, source_x1, source_y2),
            v2_cell_for_player(player, source_x2, source_y1),
            v2_cell_for_player(player, source_x2, source_y2),
        )
        return (
            min(x for x, _y in corners),
            min(y for _x, y in corners),
            max(x for x, _y in corners),
            max(y for _x, y in corners),
        )

    controller_references = set()

    for player in PlayerId.all(exclude_gaia=True):
        controllers = {}
        all_lane_cells = []
        for family, unit_const, variable_id, start, lane_y1, lane_y2 in (
            ("Army", UnitInfo.SHEEP.ID, 88 + int(player), (6.5, 61.5), 60, 61),
            (
                "Hero",
                UnitInfo.WAR_PENGUIN.ID,
                112 + int(player),
                (6.5, 65.5),
                65,
                66,
            ),
        ):
            conditions = []
            for level in range(6):
                trigger = by_name[
                    f"{family} Range Select L{level} P{int(player)}"
                ]
                assert trigger.enabled and trigger.looping
                selectors = [
                    condition
                    for condition in trigger.conditions
                    if condition.condition_type == ConditionId.BRING_OBJECT_TO_AREA
                ]
                assert len(selectors) == 1
                condition = selectors[0]
                conditions.append(condition)
                source_area = (
                    (1, lane_y1, 3, lane_y2)
                    if level == 0
                    else (8, lane_y1, 9, lane_y2)
                    if level == 5
                    else (3 + level, lane_y1, 3 + level, lane_y2)
                )
                expected = transformed_area(player, source_area)
                assert (
                    condition.area_x1,
                    condition.area_y1,
                    condition.area_x2,
                    condition.area_y2,
                ) == expected
                writes = [
                    effect
                    for effect in trigger.effects
                    if effect.effect_type == EffectId.CHANGE_VARIABLE
                    and effect.variable == variable_id
                ]
                assert len(writes) == 1
                assert (
                    writes[0].variable,
                    writes[0].quantity,
                    writes[0].operation,
                ) == (variable_id, level, Operation.SET)

            assert len({condition.unit_object for condition in conditions}) == 1
            reference_id = conditions[0].unit_object
            controller_references.add(reference_id)
            controller = unit_by_reference[reference_id]
            controllers[family] = controller
            assert controller.player == player
            assert controller.unit_const == unit_const
            assert (controller.x, controller.y) == v2_position_for_player(
                player,
                *start,
            )
            assert evolution_alpha.map_manager.get_tile(
                x=int(controller.x), y=int(controller.y)
            ).terrain_id not in water

            lane_cells = [
                {
                    (x, y)
                    for x in range(condition.area_x1, condition.area_x2 + 1)
                    for y in range(condition.area_y1, condition.area_y2 + 1)
                }
                for condition in conditions
            ]
            assert [len(cells) for cells in lane_cells] == [6, 2, 2, 2, 2, 4]
            assert len(set().union(*lane_cells)) == sum(map(len, lane_cells))
            expected_lane = {
                v2_cell_for_player(player, source_x, source_y)
                for source_x in range(1, 10)
                for source_y in range(lane_y1, lane_y2 + 1)
            }
            assert set().union(*lane_cells) == expected_lane
            assert {
                (x, y)
                for x, y in expected_lane
                if evolution_alpha.map_manager.get_tile(x=x, y=y).terrain_id == TerrainId.SNOW
            } == lane_cells[0]
            assert all(
                evolution_alpha.map_manager.get_tile(x=x, y=y).terrain_id
                not in water
                for cells in lane_cells
                for x, y in cells
            )
            all_lane_cells.extend(lane_cells)

        assert controllers["Army"].reference_id != controllers["Hero"].reference_id
        assert set().union(*all_lane_cells[:6]).isdisjoint(
            set().union(*all_lane_cells[6:])
        )
        selected = {
            controllers["Army"].reference_id,
            controllers["Hero"].reference_id,
        }
        assert any(
            effect.effect_type == EffectId.DISABLE_OBJECT_DELETION
            and effect.source_player == -1
            and selected.issubset(effect.selected_object_ids or ())
            for effect in by_name[f"Antidelete P{int(player)}"].effects
        )
        assert any(
            effect.effect_type == EffectId.DISABLE_UNIT_ATTACKABLE
            and effect.source_player == -1
            and selected.issubset(effect.selected_object_ids or ())
            for effect in by_name["Range Controller Safety"].effects
        )
        assert any(
            effect.effect_type == EffectId.CHANGE_OBJECT_STANCE
            and effect.source_player == -1
            and controllers["Hero"].reference_id in (effect.selected_object_ids or ())
            and effect.attack_stance == 3
            for effect in by_name["Range Controller Safety"].effects
        )
        assert any(
            effect.effect_type == EffectId.CHANGE_OBJECT_ATTACK
            and effect.source_player == -1
            and controllers["Hero"].reference_id in (effect.selected_object_ids or ())
            and effect.armour_attack_quantity == 0
            and effect.operation == Operation.MULTIPLY
            for effect in by_name["Range Controller Safety"].effects
        )
        expected_controller_names = {
            controllers["Army"].reference_id: (
                "Army range - snow = HOLD"
            ),
            controllers["Hero"].reference_id: (
                "Hero range - snow = OFF"
            ),
        }
        for reference_id, message in expected_controller_names.items():
            assert any(
                effect.effect_type == EffectId.CHANGE_OBJECT_NAME
                and effect.source_player == -1
                and effect.message == message
                and effect.selected_object_ids == [reference_id]
                for effect in by_name["Range Controller Labels"].effects
            )

        for world_player in range(1, 9):
            detector = by_name[
                f"Color Owner Detect S{int(player)} W{world_player}"
            ]
            for reference_id in selected:
                assert any(
                    effect.effect_type == EffectId.CHANGE_OBJECT_NAME
                    and effect.source_player == world_player
                    and effect.message == expected_controller_names[reference_id]
                    and effect.selected_object_ids == [reference_id]
                    for effect in detector.effects
                )
            assert any(
                effect.effect_type == EffectId.DISABLE_OBJECT_DELETION
                and effect.source_player == world_player
                and selected.issubset(effect.selected_object_ids or ())
                for effect in detector.effects
            )
            assert any(
                effect.effect_type == EffectId.DISABLE_UNIT_ATTACKABLE
                and effect.source_player == world_player
                and selected.issubset(effect.selected_object_ids or ())
                for effect in detector.effects
            )
            assert any(
                effect.effect_type == EffectId.CHANGE_OBJECT_STANCE
                and effect.source_player == world_player
                and controllers["Hero"].reference_id
                in (effect.selected_object_ids or ())
                and effect.attack_stance == 3
                for effect in detector.effects
            )
            assert any(
                effect.effect_type == EffectId.CHANGE_OBJECT_ATTACK
                and effect.source_player == world_player
                and controllers["Hero"].reference_id
                in (effect.selected_object_ids or ())
                and effect.armour_attack_quantity == 0
                and effect.operation == Operation.MULTIPLY
                for effect in detector.effects
            )
            assert detector.effects[-1].effect_type == EffectId.DEACTIVATE_TRIGGER
            assert detector.effects[-1].trigger_id == detector.trigger_id

        for source_position, message in (
            ((2.5, 60.5), "HOLD - new armies stay home"),
            ((9.5, 60.5), "FAR - army range"),
            ((2.5, 66.5), "OFF - no new heroes"),
            ((9.5, 66.5), "FAR - hero range"),
        ):
            position = v2_position_for_player(player, *source_position)
            signs = [
                unit
                for unit in evolution_alpha.unit_manager.units[PlayerId.GAIA]
                if unit.unit_const == OtherInfo.SIGN.ID
                and (unit.x, unit.y) == position
            ]
            assert len(signs) == 1
            assert any(
                effect.effect_type == EffectId.CHANGE_OBJECT_NAME
                and effect.message == message
                and effect.selected_object_ids == [signs[0].reference_id]
                for effect in by_name["Range And Vote Marker Labels"].effects
            )
        assert not [
            (trigger.name, effect.effect_type)
            for trigger in evolution_alpha.trigger_manager.triggers
            for effect in trigger.effects
            if selected.intersection(effect.selected_object_ids or ())
            and effect.effect_type in forbidden_effects
        ]

    assert len(controller_references) == 16
    assert sum(
        unit.unit_const == UnitInfo.SHEEP.ID
        for units in evolution_alpha.unit_manager.units
        for unit in units
    ) == 8
    assert sum(
        unit.unit_const == UnitInfo.WAR_PENGUIN.ID
        for units in evolution_alpha.unit_manager.units
        for unit in units
    ) == 8
    assert {
        evolution_alpha.player_manager.players[player].population_cap
        for player in PlayerId.all(exclude_gaia=True)
    } == {251}
    assert not [
        trigger
        for trigger in evolution_alpha.trigger_manager.triggers
        if re.fullmatch(
            r"(?:short|med|long) \(p[1-8]\)|herospawn(?:open|close)(?: \(p[2-8]\))?",
            trigger.name,
        )
    ]
    assert not [
        effect
        for trigger in evolution_alpha.trigger_manager.triggers
        for effect in trigger.effects
        if effect.object_list_unit_id == OtherInfo.OLD_STONE_HEAD.ID
    ]
    assert not [
        effect
        for trigger in evolution_alpha.trigger_manager.triggers
        for effect in trigger.effects
        if effect.effect_type == EffectId.CHANGE_OBJECT_NAME
        and set(effect.selected_object_ids or ()) & controller_references
        and effect.message == "Move me to set spawn"
    ]


def test_evolution_alpha_protects_all_added_v2_walls(evolution_alpha):
    expected_counts = {
        PlayerId.ONE: 16,
        PlayerId.TWO: 16,
        PlayerId.THREE: 10,
        PlayerId.FOUR: 10,
        PlayerId.FIVE: 10,
        PlayerId.SIX: 10,
        PlayerId.SEVEN: 14,
        PlayerId.EIGHT: 14,
    }
    by_name = {
        trigger.name: trigger
        for trigger in evolution_alpha.trigger_manager.triggers
    }

    for player, expected_count in expected_counts.items():
        added_walls = {
            unit.reference_id
            for unit in evolution_alpha.unit_manager.units[player]
            if unit.reference_id > 109_906
            and unit.unit_const == BuildingInfo.STONE_WALL.ID
        }
        protected = {
            reference_id
            for effect in by_name[f"Antidelete P{int(player)}"].effects
            if effect.effect_type == EffectId.DISABLE_OBJECT_DELETION
            for reference_id in effect.selected_object_ids
        }
        assert len(added_walls) == expected_count
        assert added_walls <= protected


def test_evolution_alpha_keeps_fixed_slot_teams(evolution_alpha):
    player_manager = evolution_alpha.player_manager

    assert player_manager.active_players == 8
    for player_id in PlayerId.all(exclude_gaia=True):
        player = player_manager.players[player_id]
        assert player.human
        assert player.allied_victory

        for target_id in PlayerId.all(exclude_gaia=True):
            if target_id == player_id:
                continue
            same_side = (player_id <= PlayerId.FOUR) == (target_id <= PlayerId.FOUR)
            expected = DiplomacyState.ALLY if same_side else DiplomacyState.ENEMY
            assert player.diplomacy[target_id - 1] == expected

    options = evolution_alpha.option_manager
    assert options.lock_teams
    assert options.lock_coop_alliances
    assert not options.allow_players_choose_teams

    # Player setup is color-aware when DE compacts a sparse lobby. A load-time
    # fixed-number diplomacy effect would overwrite teal-as-runtime-P2 back to
    # P1/P2 allies, so no such trigger may exist.
    assert all(
        trigger.name != "Enforce Color Teams"
        for trigger in evolution_alpha.trigger_manager.triggers
    )
    assert all(
        effect.effect_type != EffectId.CHANGE_DIPLOMACY
        for trigger in evolution_alpha.trigger_manager.triggers
        for effect in trigger.effects
    )


def test_evolution_alpha_removes_fixed_player_closed_slot_cleanup(evolution_alpha):
    expected_names = {f"remove (p{player})" for player in range(1, 9)}
    actual_names = {
        trigger.name for trigger in evolution_alpha.trigger_manager.triggers
    }
    assert expected_names.isdisjoint(actual_names)


def test_evolution_alpha_has_no_retired_cleanup_references(evolution_alpha):
    triggers = evolution_alpha.trigger_manager.triggers
    retired_names = {
        f"{family} (p{player})"
        for player in range(1, 9)
        for family in ("remove", "units", "walls", "units2", "units3", "warn", "remove walls")
    }
    assert retired_names.isdisjoint(trigger.name for trigger in triggers)

    valid_ids = set(range(len(triggers)))
    assert all(
        condition.trigger_id in valid_ids
        for trigger in triggers
        for condition in trigger.conditions
        if condition.condition_type == ConditionId.TRIGGER_ACTIVE
    )
    assert all(
        effect.trigger_id in valid_ids
        for trigger in triggers
        for effect in trigger.effects
        if effect.effect_type
        in {EffectId.ACTIVATE_TRIGGER, EffectId.DEACTIVATE_TRIGGER}
    )


def test_evolution_alpha_removes_legacy_no_wall_cleanup(evolution_alpha):
    cleanup = [
        trigger
        for trigger in evolution_alpha.trigger_manager.triggers
        if re.fullmatch(r"(?:re )?no wall \(p[1-8]\)", trigger.name)
    ]
    assert cleanup == []


def test_evolution_alpha_uses_ordered_right_side_combat_hud(evolution_alpha):
    full_objectives = [
        trigger
        for trigger in evolution_alpha.trigger_manager.triggers
        if trigger.display_as_objective and trigger.display_on_screen
    ]
    assert full_objectives == []

    trigger_manager = evolution_alpha.trigger_manager
    expected_variables = {
        (player - 1, f"pending_builders_p{player}") for player in range(1, 9)
    }
    expected_variables |= {
        (8 + ((player - 1) * 3) + offset, f"p{player}{suffix}")
        for player in range(1, 9)
        for offset, suffix in enumerate(("k", "d", "r"))
    }
    expected_variables |= {
        (31 + player, f"p{player}coloractive") for player in range(1, 9)
    }
    expected_variables |= {
        (39 + player, f"p{player}worldplayer") for player in range(1, 9)
    }
    expected_variables |= {
        (47 + player, f"p{player}coloreliminated") for player in range(1, 9)
    }
    expected_variables.add((56, "colorsidesready"))
    vote_keys = sorted(
        (
            (target, voter)
            for team in (range(1, 5), range(5, 9))
            for target in team
            for voter in team
            if voter != target
        ),
        key=lambda key: (key[0], key[1]),
    )
    expected_variables |= {
        (57 + index, f"votekickp{target}byp{voter}")
        for index, (target, voter) in enumerate(vote_keys)
    }
    expected_variables |= {
        (80 + player, f"army_move_pending_p{player}")
        for player in range(1, 9)
    }
    expected_variables |= {
        (88 + player, f"army_range_p{player}")
        for player in range(1, 9)
    }
    expected_variables |= {
        (96 + player, f"hero_move_pending_p{player}")
        for player in range(1, 9)
    }
    expected_variables |= {
        (104 + player, f"builder_move_pending_p{player}")
        for player in range(1, 9)
    }
    expected_variables |= {
        (112 + player, f"hero_range_p{player}")
        for player in range(1, 9)
    }
    expected_variables |= {
        (base + player, f"p{player}color{suffix}")
        for base, suffix in ((120, "occupied"), (128, "cleaned"))
        for player in range(1, 9)
    }
    assert {
        (variable.variable_id, variable.name) for variable in trigger_manager.variables
    } == expected_variables

    header = next(trigger for trigger in trigger_manager.triggers if trigger.name == "Combat HUD Header")
    assert header.enabled
    assert header.display_on_screen
    assert not header.display_as_objective
    assert header.header
    assert header.short_description == "P# | K | D | R"
    assert header.description_order == 19

    divider = next(
        trigger
        for trigger in trigger_manager.triggers
        if trigger.name == "Combat HUD Team Divider"
    )
    assert divider.enabled and divider.display_on_screen
    assert divider.short_description == "----------------"
    assert divider.description_order == 14

    for player in range(1, 9):
        empty = next(
            trigger for trigger in trigger_manager.triggers if trigger.name == f"Combat HUD Empty P{player}"
        )
        live = next(
            trigger for trigger in trigger_manager.triggers if trigger.name == f"Combat HUD Live P{player}"
        )
        assert empty.enabled
        assert not live.enabled
        assert empty.display_on_screen and live.display_on_screen
        assert not empty.display_as_objective and not live.display_as_objective
        expected_order = 19 - player if player <= 4 else 18 - player
        assert empty.description_order == live.description_order == expected_order
        assert empty.short_description == f"P{player} | - | - | -"
        assert live.short_description == (
            f"P{player} | <p{player}k> | <p{player}d> | <p{player}r>"
        )
        for row in (empty, live):
            assert len(row.conditions) == 1
            assert row.conditions[0].condition_type == ConditionId.PLAYER_DEFEATED
            assert row.conditions[0].source_player == PlayerId.GAIA

    xs_trigger = next(trigger for trigger in trigger_manager.triggers if trigger.name == "XS SCRIPT")
    xs_source = xs_trigger.effects[0].message
    assert "xsDisplayInstructions(" not in xs_source
    for color_tag in ("BLUE", "RED", "GREEN", "YELLOW", "AQUA", "PURPLE", "GREY", "ORANGE"):
        assert f"<{color_tag}>" not in xs_source
    assert "cAttributeKills" in xs_source
    assert "cAttributeKilledByOthers" in xs_source
    assert "cAttributeRazings" in xs_source
    assert "int owner = xsGetUnitOwner(reference);" in xs_source
    assert "return(xsTriggerVariable(" not in xs_source
    assert "40 + scenarioPlayer - 1" not in xs_source
    assert xs_source.count("cbaWorldPlayerForColor(scenarioPlayer)") == 4
    assert "int variableBase = 8 + ((scenarioPlayer - 1) * 3);" in xs_source
    assert "xsSetTriggerVariable(variableBase, kills);" in xs_source
    assert "xsSetTriggerVariable(variableBase + 1, deaths);" in xs_source
    assert "xsSetTriggerVariable(variableBase + 2, razings);" in xs_source
    for player in range(1, 9):
        assert f"cbaUpdateCombatRow({player})" in xs_source
    assert [xs_source.index(f"cbaUpdateCombatRow({player})") for player in range(1, 9)] == sorted(
        xs_source.index(f"cbaUpdateCombatRow({player})") for player in range(1, 9)
    )


def test_evolution_alpha_preserves_player_names(evolution_alpha):
    effects = (effect for trigger in evolution_alpha.trigger_manager.triggers for effect in trigger.effects)
    assert all(effect.effect_type != EffectId.CHANGE_PLAYER_NAME for effect in effects)


def test_evolution_alpha_shows_live_kills_on_every_white_king(evolution_alpha):
    references = (48_301, 42_394, 42_395, 42_396, 42_397, 42_398, 42_399, 42_400)
    by_name = {
        trigger.name: trigger
        for trigger in evolution_alpha.trigger_manager.triggers
    }
    counter_pattern = re.compile(r"White King Kills S([1-8]) W([1-8])")
    counters = {
        tuple(map(int, counter_pattern.fullmatch(name).groups())): trigger
        for name, trigger in by_name.items()
        if counter_pattern.fullmatch(name)
    }
    assert counters.keys() == VALID_COLOR_WORLD_PAIRS
    for (color, world_player), counter in counters.items():
        assert not counter.enabled and counter.looping
        assert len(counter.conditions) == 1
        assert counter.conditions[0].condition_type == ConditionId.TIMER
        assert counter.conditions[0].timer == 1
        assert len(counter.effects) == 2

        name_effect = next(
            effect
            for effect in counter.effects
            if effect.effect_type == EffectId.CHANGE_OBJECT_NAME
        )
        assert (
            name_effect.source_player,
            name_effect.message,
            tuple(name_effect.selected_object_ids or ()),
        ) == (
            world_player,
            f"P{color} Kills",
            (references[color - 1],),
        )

        value_effect = next(
            effect
            for effect in counter.effects
            if effect.effect_type == EffectId.MODIFY_OBJECT_ATTRIBUTE_BY_VARIABLE
        )
        assert (
            value_effect.source_player,
            value_effect.object_attributes,
            value_effect.operation,
            value_effect.variable,
            tuple(value_effect.selected_object_ids or ()),
        ) == (
            world_player,
            ObjectAttribute.SHOWN_ATTACK,
            Operation.SET,
            8 + ((color - 1) * 3),
            (references[color - 1],),
        )

        occupied = by_name[f"Occupied Slot S{color} W{world_player}"]
        assert counter.trigger_id in {
            effect.trigger_id
            for effect in occupied.effects
            if effect.effect_type == EffectId.ACTIVATE_TRIGGER
        }

    conflicting_labels = [
        effect
        for trigger in evolution_alpha.trigger_manager.triggers
        if trigger not in counters.values()
        for effect in trigger.effects
        if effect.effect_type == EffectId.CHANGE_OBJECT_NAME
        and set(effect.selected_object_ids or ()) & set(references)
    ]
    assert not conflicting_labels


def test_evolution_alpha_publishes_combat_only_score_values(evolution_alpha):
    xs_trigger = next(
        trigger for trigger in evolution_alpha.trigger_manager.triggers if trigger.name == "XS SCRIPT"
    )
    xs_source = xs_trigger.effects[0].message
    expected_values = {
        "cAttributeTotalValueOfKills": "kills * 100",
        "cAttributeValueKilledByOthers": "deaths * 100",
        "cAttributeTotalValueOfRazings": "razings * 500",
        "cAttributeValueRazedByOthers": "razed * 500",
    }
    for attribute, value in expected_values.items():
        assert f"xsSetPlayerAttribute(worldPlayer, {attribute}, {value});" in xs_source
    assert xs_source.count("xsSetPlayerAttribute(worldPlayer, cAttribute") == 4

    # Sparse lobbies compact selected colors into different runtime IDs. Clear
    # every non-combat score source through worldPlayer, not a fixed color slot.
    neutral_attributes = (
        Attribute.PERCENT_MAP_EXPLORED,
        Attribute.BUILDING_COST_SUM,
        Attribute.TECH_COST_SUM,
        Attribute.VALUE_CURRENT_UNITS,
        Attribute.VALUE_CURRENT_BUILDINGS,
        Attribute.TRIBUTE_SCORE,
        Attribute.VALUE_WONDERS_CASTLES,
        Attribute.FOOD_SCORE,
        Attribute.WOOD_SCORE,
        Attribute.STONE_SCORE,
        Attribute.GOLD_SCORE,
        Attribute.UNITS_VALUE_TOTAL,
        Attribute.BUILDINGS_VALUE_TOTAL,
    )
    for attribute in neutral_attributes:
        assert f"xsSetPlayerAttribute(worldPlayer, {int(attribute)}, 0);" in xs_source
    assert "cbaRefreshCombatValues(worldPlayer);" in xs_source


def test_evolution_alpha_equalizes_only_confirmed_occupied_slots(evolution_alpha):
    trigger_manager = evolution_alpha.trigger_manager
    equalizers = {
        trigger.name: trigger
        for trigger in trigger_manager.triggers
        if trigger.name.startswith("Resource Equalizer P")
    }
    gates = {
        trigger.name: trigger
        for trigger in trigger_manager.triggers
        if trigger.name.startswith("Occupied Slot S")
    }
    free_costs = {
        trigger.name: trigger
        for trigger in trigger_manager.triggers
        if trigger.name.startswith("Free Costs P")
    }
    empty_rows = {
        trigger.name: trigger
        for trigger in trigger_manager.triggers
        if trigger.name.startswith("Combat HUD Empty P")
    }
    live_rows = {
        trigger.name: trigger
        for trigger in trigger_manager.triggers
        if trigger.name.startswith("Combat HUD Live P")
    }
    king_counters = {
        trigger.name: trigger
        for trigger in trigger_manager.triggers
        if trigger.name.startswith("White King Kills S")
    }

    assert len(equalizers) == len(free_costs) == len(empty_rows) == len(live_rows) == 8
    assert len(gates) == len(VALID_COLOR_WORLD_PAIRS)
    assert {
        tuple(map(int, re.fullmatch(r"Occupied Slot S([1-8]) W([1-8])", name).groups()))
        for name in gates
    } == VALID_COLOR_WORLD_PAIRS
    for player in range(1, 9):
        equalizer = equalizers[f"Resource Equalizer P{player}"]
        assert not equalizer.enabled
        assert equalizer.looping

        defeated = [
            condition
            for condition in equalizer.conditions
            if condition.condition_type == ConditionId.PLAYER_DEFEATED
        ]
        assert len(defeated) == 1
        assert defeated[0].source_player == player
        assert defeated[0].inverted == 1

        resource_effects = [
            effect for effect in equalizer.effects if effect.effect_type == EffectId.MODIFY_RESOURCE
        ]
        assert {
            (effect.source_player, effect.tribute_list, effect.quantity, effect.operation)
            for effect in resource_effects
        } == {
            (player, resource, 0, 1)
            for resource in (
                0,
                1,
                2,
                3,
                Attribute.RESEARCH_COST_MODIFIER,
                Attribute.PERCENT_MAP_EXPLORED,
                Attribute.BUILDING_COST_SUM,
                Attribute.TECH_COST_SUM,
                Attribute.VALUE_CURRENT_UNITS,
                Attribute.VALUE_CURRENT_BUILDINGS,
                Attribute.TRIBUTE_SCORE,
                Attribute.VALUE_WONDERS_CASTLES,
                Attribute.FOOD_SCORE,
                Attribute.WOOD_SCORE,
                Attribute.STONE_SCORE,
                Attribute.GOLD_SCORE,
                Attribute.UNITS_VALUE_TOTAL,
                Attribute.BUILDINGS_VALUE_TOTAL,
            )
        }
    gate_pattern = re.compile(r"Occupied Slot S([1-8]) W([1-8])")
    for gate in gates.values():
        color, world_player = map(int, gate_pattern.fullmatch(gate.name).groups())
        assert gate.enabled and gate.looping
        gate_timers = [
            condition
            for condition in gate.conditions
            if condition.condition_type == ConditionId.TIMER
        ]
        gate_variables = [
            condition
            for condition in gate.conditions
            if condition.condition_type == ConditionId.VARIABLE_VALUE
        ]
        assert len(gate_timers) == 1 and gate_timers[0].timer == 3
        assert len(gate_variables) == 2
        assert {
            (condition.variable, condition.quantity, condition.comparison)
            for condition in gate_variables
        } == {
            (31 + color, 1, Comparison.EQUAL),
            (39 + color, world_player, Comparison.EQUAL),
        }
        activated = {
            effect.trigger_id for effect in gate.effects if effect.effect_type == EffectId.ACTIVATE_TRIGGER
        }
        assert activated == {
            equalizers[f"Resource Equalizer P{world_player}"].trigger_id,
            free_costs[f"Free Costs P{world_player}"].trigger_id,
            live_rows[f"Combat HUD Live P{color}"].trigger_id,
            king_counters[f"White King Kills S{color} W{world_player}"].trigger_id,
        }
        deactivated = {
            effect.trigger_id for effect in gate.effects if effect.effect_type == EffectId.DEACTIVATE_TRIGGER
        }
        assert deactivated == {
            empty_rows[f"Combat HUD Empty P{color}"].trigger_id,
            gate.trigger_id,
        }

    p1_p5_values = {
        **{31 + color: int(color in {1, 5}) for color in range(1, 9)},
        **{39 + color: {1: 1, 5: 2}.get(color, 0) for color in range(1, 9)},
    }
    matching_gates = {
        gate.name
        for gate in gates.values()
        if all(
            p1_p5_values[condition.variable] == condition.quantity
            for condition in gate.conditions
            if condition.condition_type == ConditionId.VARIABLE_VALUE
        )
    }
    assert matching_gates == {"Occupied Slot S1 W1", "Occupied Slot S5 W2"}


def test_evolution_alpha_has_zero_resources_and_free_purchases(evolution_alpha):
    by_name = {trigger.name: trigger for trigger in evolution_alpha.trigger_manager.triggers}
    for player in range(1, 9):
        settings = evolution_alpha.player_manager.players[PlayerId(player)]
        assert (settings.food, settings.wood, settings.stone, settings.gold) == (0, 0, 0, 0)

        assert f"res (p{player})" not in by_name

        free_costs = by_name[f"Free Costs P{player}"]
        assert not free_costs.enabled
        assert not free_costs.looping
        free_attributes = {
            effect.tribute_list
            for effect in free_costs.effects
            if effect.effect_type == EffectId.MODIFY_RESOURCE
        }
        assert free_attributes == {
            Attribute.RESEARCH_COST_MODIFIER,
            Attribute.UNIT_REPAIR_COST,
            Attribute.BUILDING_REPAIR_COST,
        }

        assert all(effect.effect_type != EffectId.CHANGE_OBJECT_COST for effect in free_costs.effects)


def test_evolution_alpha_keeps_all_research_free_at_runtime(evolution_alpha):
    xs_trigger = next(
        trigger for trigger in evolution_alpha.trigger_manager.triggers if trigger.name == "XS SCRIPT"
    )
    xs_source = xs_trigger.effects[0].message
    assert "for (worldPlayer = 1; <= xsGetNumPlayers())" in xs_source
    assert "int technologyCount = xsGetPlayerNumberOfTechs(worldPlayer);" in xs_source
    assert "for (technology = 0; < technologyCount)" in xs_source
    assert xs_source.count("xsEffectAmount(cModifyTech, technology, cAttrSet") == 4
    for cost_attribute in ("Food", "Wood", "Stone", "Gold"):
        assert (
            f"xsEffectAmount(cModifyTech, technology, cAttrSet{cost_attribute}Cost, 0, worldPlayer);"
        ) in xs_source
    assert "cAttrMulAllCosts" not in xs_source
    assert "rule cbaRuntimeEconomy" not in xs_source
    assert "gCbaFreeTechsApplied" not in xs_source
    assert "cAttrSetState" not in xs_source
    assert "cDisableTech" not in xs_source
    assert "xsResearchTechnology" not in xs_source


def test_evolution_alpha_keeps_every_object_free_at_runtime(evolution_alpha):
    xs_trigger = next(
        trigger for trigger in evolution_alpha.trigger_manager.triggers if trigger.name == "XS SCRIPT"
    )
    xs_source = xs_trigger.effects[0].message
    assert "int objectCount = xsGetPlayerNumberOfObjects(worldPlayer);" in xs_source
    assert "for (objectId = 0; < objectCount)" in xs_source
    assert xs_source.count("xsEffectAmount(cSetAttribute, objectId, c") == 4
    for cost_attribute in ("Food", "Wood", "Stone", "Gold"):
        assert (
            f"xsEffectAmount(cSetAttribute, objectId, c{cost_attribute}Cost, 0, worldPlayer);"
        ) in xs_source
    for state_mutation in ("cEnableObject", "cUpgradeUnit", "cAttributeEnable"):
        assert state_mutation not in xs_source


def test_evolution_alpha_disables_castle_trebuchet_training(evolution_alpha):
    for player in PlayerId.all(exclude_gaia=True):
        disabled = evolution_alpha.player_manager.players[player].disabled_units
        assert UnitInfo.TREBUCHET.ID in disabled
        assert UnitInfo.TREBUCHET_PACKED.ID in disabled


def test_evolution_alpha_forces_the_original_bombard_tower_unlock(evolution_alpha):
    assert all(
        trigger.name != "Legacy Bombard Tower Unlock Disabled"
        for trigger in evolution_alpha.trigger_manager.triggers
    )

    occupied_pattern = re.compile(r"Occupied Slot S([1-8]) W([1-8])")
    occupied = [
        trigger
        for trigger in evolution_alpha.trigger_manager.triggers
        if occupied_pattern.fullmatch(trigger.name)
    ]
    assert len(occupied) == 64
    for trigger in occupied:
        _color, world_player = map(
            int,
            occupied_pattern.fullmatch(trigger.name).groups(),
        )
        researches = [
            effect
            for effect in trigger.effects
            if effect.effect_type == EffectId.RESEARCH_TECHNOLOGY
            and effect.technology == TechInfo.BOMBARD_TOWER.ID
        ]
        enables = [
            effect
            for effect in trigger.effects
            if effect.effect_type == EffectId.ENABLE_DISABLE_OBJECT
            and effect.object_list_unit_id == BuildingInfo.BOMBARD_TOWER.ID
        ]
        assert {
            (
                effect.source_player,
                effect.technology,
                effect.force_research_technology,
            )
            for effect in researches
        } == {(world_player, TechInfo.BOMBARD_TOWER.ID, 1)}
        assert {
            (effect.source_player, effect.object_list_unit_id, effect.enabled)
            for effect in enables
        } == {(world_player, BuildingInfo.BOMBARD_TOWER.ID, 1)}


def test_evolution_alpha_remaps_sparse_feudal_upgrades(evolution_alpha):
    triggers = evolution_alpha.trigger_manager.triggers
    pattern = re.compile(r"Sparse Feudal S([1-8]) W([1-8])")
    sparse = {
        tuple(map(int, match.groups())): trigger
        for trigger in triggers
        if (match := pattern.fullmatch(trigger.name))
    }
    assert len(sparse) == 56
    assert set(sparse) == VALID_COLOR_WORLD_PAIRS - {
        (color, color) for color in range(1, 9)
    }

    areas = {}
    for color in range(1, 9):
        color_areas = set()
        own_blacksmiths = [
            (int(unit.x), int(unit.y))
            for unit in evolution_alpha.unit_manager.units[color]
            if unit.unit_const == BuildingInfo.BLACKSMITH.ID
        ]
        assert own_blacksmiths
        for world_player in range(1, 9):
            if world_player == color:
                continue
            trigger = sparse[color, world_player]
            conditions = [
                condition
                for condition in trigger.conditions
                if condition.condition_type == ConditionId.OBJECTS_IN_AREA
            ]
            assert len(conditions) == 1
            blacksmith = conditions[0]
            assert (
                blacksmith.source_player,
                blacksmith.object_list,
            ) == (world_player, BuildingInfo.BLACKSMITH.ID)
            bounds = (
                blacksmith.area_x1,
                blacksmith.area_y1,
                blacksmith.area_x2,
                blacksmith.area_y2,
            )
            color_areas.add(bounds)
            assert all(
                bounds[0] <= x <= bounds[2] and bounds[1] <= y <= bounds[3]
                for x, y in own_blacksmiths
            )
            assert {
                (condition.variable, condition.quantity, condition.comparison)
                for condition in trigger.conditions
                if condition.condition_type == ConditionId.VARIABLE_VALUE
            } == {
                (31 + color, 1, Comparison.EQUAL),
                (39 + color, world_player, Comparison.EQUAL),
            }
            assert {
                (effect.source_player, effect.technology)
                for effect in trigger.effects
                if effect.effect_type == EffectId.RESEARCH_TECHNOLOGY
            } == {
                (world_player, technology)
                for technology in (211, 199, 67, 81, 74, 1036, 1115, 1125)
            }
        assert len(color_areas) == 1
        areas[color] = color_areas.pop()

    source = areas[3]
    for color, bounds in areas.items():
        corner_a = v2_cell_for_player(color, source[0], source[1])
        corner_b = v2_cell_for_player(color, source[2], source[3])
        assert bounds == (
            min(corner_a[0], corner_b[0]),
            min(corner_a[1], corner_b[1]),
            max(corner_a[0], corner_b[0]),
            max(corner_a[1], corner_b[1]),
        )


def test_evolution_alpha_maps_center_rewards_to_runtime_players(evolution_alpha):
    triggers = evolution_alpha.trigger_manager.triggers
    patterns = {
        "Kills": re.compile(r"Center Kills S([1-8]) W([1-8])"),
        "Trebuchet": re.compile(r"Center Trebuchet S([1-8]) W([1-8])"),
    }
    families = {
        family: {
            tuple(map(int, match.groups())): trigger
            for trigger in triggers
            if (match := pattern.fullmatch(trigger.name))
        }
        for family, pattern in patterns.items()
    }
    assert all(set(family) == VALID_COLOR_WORLD_PAIRS for family in families.values())
    assert not any(
        trigger.name.startswith(("Middle kills", "Middle Trebuchet"))
        for trigger in triggers
    )
    marker_cells = {
        1: (69, 66),
        2: (74, 66),
        3: (66, 69),
        4: (77, 69),
        5: (66, 74),
        6: (77, 74),
        7: (69, 77),
        8: (74, 77),
    }
    water = {int(terrain) for terrain in TerrainId.water_terrains()}
    for family, mapped in families.items():
        for (color, world_player), trigger in mapped.items():
            assert trigger.enabled and trigger.looping
            control = next(
                condition
                for condition in trigger.conditions
                if condition.condition_type == ConditionId.OBJECTS_IN_AREA
            )
            assert (
                control.quantity,
                control.source_player,
                control.object_type,
                control.area_x1,
                control.area_y1,
                control.area_x2,
                control.area_y2,
            ) == (1, world_player, ObjectType.MILITARY, 65, 65, 78, 78)
            timers = [
                condition.timer
                for condition in trigger.conditions
                if condition.condition_type == ConditionId.TIMER
            ]
            assert timers == [180 if family == "Kills" else 1800]
            assert {
                (condition.variable, condition.quantity, condition.comparison)
                for condition in trigger.conditions
                if condition.condition_type == ConditionId.VARIABLE_VALUE
            } == {
                (31 + color, 1, Comparison.EQUAL),
                (39 + color, world_player, Comparison.EQUAL),
                *(() if family == "Kills" else ((47 + color, 0, Comparison.EQUAL),)),
            }
            if family == "Kills":
                tribute = next(
                    effect
                    for effect in trigger.effects
                    if effect.effect_type == EffectId.TRIBUTE
                )
                assert (
                    tribute.quantity,
                    tribute.tribute_list,
                    tribute.source_player,
                    tribute.target_player,
                ) == (10, Attribute.UNITS_KILLED, PlayerId.GAIA, world_player)
                continue
            marker = marker_cells[color]
            assert evolution_alpha.map_manager.get_tile(
                x=marker[0], y=marker[1]
            ).terrain_id not in water
            pad_guard = next(
                condition
                for condition in trigger.conditions
                if condition.condition_type == ConditionId.OBJECTS_IN_AREA
                and condition.object_group == ObjectClass.PACKED_UNIT
            )
            create = next(
                effect
                for effect in trigger.effects
                if effect.effect_type == EffectId.CREATE_OBJECT
            )
            hp = next(
                effect
                for effect in trigger.effects
                if effect.effect_type == EffectId.CHANGE_OBJECT_HP
            )
            assert (
                pad_guard.source_player,
                pad_guard.object_group,
                pad_guard.area_x1,
                pad_guard.area_y1,
                pad_guard.area_x2,
                pad_guard.area_y2,
            ) == (world_player, ObjectClass.PACKED_UNIT, *marker, *marker)
            assert pad_guard.inverted and pad_guard.quantity == 1
            assert not any(effect.effect_type == EffectId.REMOVE_OBJECT for effect in trigger.effects)
            assert (
                create.source_player,
                create.object_list_unit_id,
                create.location_x,
                create.location_y,
            ) == (world_player, UnitInfo.TREBUCHET_PACKED.ID, *marker)
            assert (
                hp.source_player,
                hp.object_list_unit_id,
                hp.quantity,
                hp.operation,
                hp.area_x1,
                hp.area_y1,
                hp.area_x2,
                hp.area_y2,
            ) == (
                world_player,
                UnitInfo.TREBUCHET_PACKED.ID,
                200,
                Operation.ADD,
                *marker,
                *marker,
            )


def test_evolution_alpha_removes_palisade_bonus_and_maps_other_goth_rules(
    evolution_alpha,
):
    triggers = evolution_alpha.trigger_manager.triggers
    assert all("Palisade Bonus" not in trigger.name for trigger in triggers)
    assert all(
        condition.object_list != BuildingInfo.PALISADE_WALL.ID
        for trigger in triggers
        for condition in trigger.conditions
    )
    assert all(
        effect.object_list_unit_id != BuildingInfo.PALISADE_WALL.ID
        for trigger in triggers
        for effect in trigger.effects
    )

    family_patterns = {
        "Restriction": re.compile(
            r"Goth Barracks Restriction S([1-8]) W([1-8])"
        ),
        "Anarchy": re.compile(r"Goth Anarchy S([1-8]) W([1-8])"),
        "Imperial": re.compile(r"Goth Imperial S([1-8]) W([1-8])"),
    }
    families = {
        family: {
            tuple(map(int, match.groups())): trigger
            for trigger in triggers
            if (match := pattern.fullmatch(trigger.name))
        }
        for family, pattern in family_patterns.items()
    }
    assert all(set(family) == VALID_COLOR_WORLD_PAIRS for family in families.values())
    for pair in VALID_COLOR_WORLD_PAIRS:
        color, world_player = pair
        restriction = families["Restriction"][pair]
        anarchy = families["Anarchy"][pair]
        imperial = families["Imperial"][pair]
        assert not restriction.enabled and restriction.looping
        assert any(
            condition.condition_type == ConditionId.TIMER
            and condition.timer == 1
            for condition in restriction.conditions
        )
        barracks = next(
            condition
            for condition in restriction.conditions
            if condition.condition_type == ConditionId.OBJECTS_IN_AREA
        )
        assert (barracks.object_list, barracks.source_player) == (
            BuildingInfo.BARRACKS.ID,
            world_player,
        )
        kill = next(
            effect
            for effect in restriction.effects
            if effect.effect_type == EffectId.KILL_OBJECT
        )
        assert (kill.object_list_unit_id, kill.source_player) == (
            BuildingInfo.BARRACKS.ID,
            world_player,
        )
        for trigger, technology in (
            (anarchy, TechInfo.ANARCHY.ID),
            (imperial, TechInfo.IMPERIAL_AGE.ID),
        ):
            assert {
                (condition.variable, condition.quantity, condition.comparison)
                for condition in trigger.conditions
                if condition.condition_type == ConditionId.VARIABLE_VALUE
            } == {
                (31 + color, 1, Comparison.EQUAL),
                (39 + color, world_player, Comparison.EQUAL),
            }
            research = next(
                condition
                for condition in trigger.conditions
                if condition.condition_type == ConditionId.RESEARCH_TECHNOLOGY
            )
            assert (research.source_player, research.technology) == (
                world_player,
                technology,
            )
        assert {
            effect.trigger_id
            for effect in anarchy.effects
            if effect.effect_type == EffectId.ACTIVATE_TRIGGER
        } == {restriction.trigger_id}
        assert {
            effect.trigger_id
            for effect in imperial.effects
            if effect.effect_type == EffectId.DEACTIVATE_TRIGGER
        } == {restriction.trigger_id, anarchy.trigger_id}

    legacy_barracks = [
        trigger
        for trigger in triggers
        if re.fullmatch(
            r"Legacy Goth (?:Barracks|Anarchy|Imp) Disabled #[0-9]+",
            trigger.name,
        )
    ]
    assert legacy_barracks == []


def test_evolution_alpha_spawns_sparse_raze_builders_in_their_color_base(evolution_alpha):
    triggers = evolution_alpha.trigger_manager.triggers
    rewards = {
        trigger.name: trigger
        for trigger in triggers
        if trigger.name.startswith("Builder Reward S")
    }
    movers = {
        trigger.name: trigger
        for trigger in triggers
        if trigger.name.startswith("Builder Move S")
    }
    legacy_stages = [
        trigger for trigger in triggers if trigger.name.startswith("Legacy Raze Reward Disabled #")
    ]
    assert len(rewards) == len(VALID_COLOR_WORLD_PAIRS)
    assert len(movers) == len(VALID_COLOR_WORLD_PAIRS)
    assert legacy_stages == []

    areas = castle_row_areas(evolution_alpha)
    source_points = {
        UnitInfo.VILLAGER_MALE.ID: (10, 54),
        UnitInfo.VILLAGER_FEMALE.ID: (11, 54),
    }
    destination_points = {
        UnitInfo.VILLAGER_MALE.ID: (17, 45),
        UnitInfo.VILLAGER_FEMALE.ID: (17, 63),
    }
    occupied_tiles = {
        (int(unit.x), int(unit.y))
        for units in evolution_alpha.unit_manager.units
        for unit in units
    }
    source_flag_positions = ((22.5, 40.5), (23.5, 40.5))
    target_flag_positions = ((10.5, 53.5), (10.5, 55.5))
    for color in range(1, 9):
        spawns = {
            unit_id: v2_cell_for_player(color, *point)
            for unit_id, point in source_points.items()
        }
        destinations = {
            unit_id: v2_cell_for_player(color, *point)
            for unit_id, point in destination_points.items()
        }
        for point in (*spawns.values(), *destinations.values()):
            assert evolution_alpha.map_manager.get_tile(x=point[0], y=point[1]).terrain_id == (
                TerrainId.GRASS_2
            )
            assert point not in occupied_tiles

        flags = {
            (unit.x, unit.y)
            for unit in evolution_alpha.unit_manager.units[color]
            if unit.unit_const == OtherInfo.FLAG_A.ID
        }
        assert {
            v2_position_for_player(color, *point)
            for point in target_flag_positions
        } <= flags
        assert {
            v2_position_for_player(color, *point)
            for point in source_flag_positions
        }.isdisjoint(flags)

        for world_player in range(1, 9):
            reward = rewards[f"Builder Reward S{color} W{world_player}"]
            assert reward.enabled and reward.looping
            assert len(reward.conditions) == 6

            variable_conditions = {
                (
                    condition.variable,
                    condition.comparison,
                    condition.quantity,
                )
                for condition in reward.conditions
                if condition.condition_type == ConditionId.VARIABLE_VALUE
            }
            assert {
                (color - 1, Comparison.LARGER_OR_EQUAL, 1),
                (31 + color, Comparison.EQUAL, 1),
                (39 + color, Comparison.EQUAL, world_player),
                (47 + color, Comparison.EQUAL, 0),
            } == variable_conditions

            castle = next(
                condition
                for condition in reward.conditions
                if condition.condition_type == ConditionId.OBJECTS_IN_AREA
            )
            assert castle.source_player == PlayerId(world_player)
            assert castle.object_list == BuildingInfo.CASTLE.ID
            assert (
                castle.area_x1,
                castle.area_y1,
                castle.area_x2,
                castle.area_y2,
            ) == areas[color]

            builders = {
                (
                    effect.object_list_unit_id,
                    effect.location_x,
                    effect.location_y,
                )
                for effect in reward.effects
                if effect.effect_type == EffectId.CREATE_OBJECT
            }
            assert builders == {
                (unit_id, *point) for unit_id, point in spawns.items()
            }
            assert all(
                effect.source_player == PlayerId(world_player)
                for effect in reward.effects
                if effect.effect_type in {EffectId.CREATE_OBJECT, EffectId.SEND_CHAT}
            )
            chats = [
                effect
                for effect in reward.effects
                if effect.effect_type == EffectId.SEND_CHAT
            ]
            assert len(chats) == 1
            assert chats[0].message == "Villager Created"

            variable_effects = [
                effect
                for effect in reward.effects
                if effect.effect_type == EffectId.CHANGE_VARIABLE
            ]
            assert len(variable_effects) == 2
            consume_pending = next(
                effect for effect in variable_effects if effect.variable == color - 1
            )
            assert (
                consume_pending.variable,
                consume_pending.operation,
                consume_pending.quantity,
            ) == (color - 1, Operation.SUBTRACT, 1)
            arm_movement = next(
                effect for effect in variable_effects if effect.variable == 104 + color
            )
            assert (
                arm_movement.operation,
                arm_movement.quantity,
            ) == (Operation.SET, 1)

            mover = movers[f"Builder Move S{color} W{world_player}"]
            assert mover.enabled and mover.looping
            assert any(
                condition.condition_type == ConditionId.TIMER
                and condition.timer == 1
                for condition in mover.conditions
            )
            assert {
                (condition.variable, condition.quantity, condition.comparison)
                for condition in mover.conditions
                if condition.condition_type == ConditionId.VARIABLE_VALUE
            } == {
                (104 + color, 1, Comparison.EQUAL),
                (31 + color, 1, Comparison.EQUAL),
                (39 + color, world_player, Comparison.EQUAL),
            }
            tasks = {
                (
                    effect.object_list_unit_id,
                    effect.source_player,
                    effect.area_x1,
                    effect.area_y1,
                    effect.area_x2,
                    effect.area_y2,
                    effect.location_x,
                    effect.location_y,
                )
                for effect in mover.effects
                if effect.effect_type == EffectId.TASK_OBJECT
            }
            assert all(
                effect.action_type == ActionType.MOVE
                for effect in mover.effects
                if effect.effect_type == EffectId.TASK_OBJECT
            )
            assert tasks == {
                (
                    unit_id,
                    world_player,
                    spawn[0] - 1,
                    spawn[1] - 1,
                    spawn[0] + 1,
                    spawn[1] + 1,
                    *destinations[unit_id],
                )
                for unit_id, spawn in spawns.items()
            }
            movement_resets = [
                effect
                for effect in mover.effects
                if effect.effect_type == EffectId.CHANGE_VARIABLE
                and effect.variable == 104 + color
            ]
            assert len(movement_resets) == 1
            assert (
                movement_resets[0].operation,
                movement_resets[0].quantity,
            ) == (Operation.SET, 0)

    xs_trigger = next(trigger for trigger in triggers if trigger.name == "XS SCRIPT")
    xs_source = xs_trigger.effects[0].message
    assert "int currentRazings = xsCeilToInt(xsPlayerAttribute(" in xs_source
    assert "int earnedPairs = currentRazings - threshold + 1;" in xs_source
    # The builder-pair block is addressed from PENDING_BUILDER_VARIABLE_BASE, which is
    # interpolated into the XS so the Python and XS sides cannot drift apart.
    assert re.search(
        r"int pendingPairs = xsTriggerVariable\(\s*\d+ \+ scenarioPlayer - 1\);", xs_source
    ), "builder-pair variable read is no longer derived from the shared base"
    assert "pendingPairs + earnedPairs - previousEarnedPairs" in xs_source
    assert "xsArraySetInt(gCbaBuilderThresholdByCiv, 8, 4);" in xs_source
    assert 'xsArraySetString(gCbaNameByCiv, 8, "Persians");' in xs_source
    assert "xsGetLocalPlayerId()" in xs_source
    assert "xsGetPlayerCivilization(localPlayer)" in xs_source
    assert "first builder pair after" in xs_source
    assert "if (xsGetGameTime() >= 4)" in xs_source
    # Two mutually exclusive builder messages, plus the one-shot identity diagnostic.
    # The dedicated identity test pins its timer and self-disable to prevent spam.
    assert xs_source.count("xsChatData(") == 3
    assert "Unsupported civilization (id " in xs_source
    assert "xsDisableSelf();" in xs_source
    assert xs_source.count("cbaQueueColorBuilders(") == 9
    assert "xsSetTriggerVariable(worldPlayer - 1" not in xs_source

    thresholds = {
        int(civilization): int(threshold)
        for civilization, threshold in re.findall(
            r"xsArraySetInt\(gCbaBuilderThresholdByCiv, (\d+), (\d+)\);",
            xs_source,
        )
    }
    expected_thresholds = dict(
        enumerate(
            (
                1,
                3,
                2,
                3,
                3,
                2,
                2,
                4,
                2,
                3,
                2,
                2,
                2,
                3,
                2,
                1,
                4,
                3,
                1,
                3,
                2,
                1,
                2,
                3,
                2,
                3,
                1,
                4,
                1,
                3,
                1,
                2,
                2,
                2,
                2,
                2,
                2,
                2,
                2,
                2,
                2,
                3,
                2,
                2,
                1,
                1,
                1,
                1,
                2,
                2,
                2,
                2,
                2,
                1,
                1,
                1,
                1,
                1,
                1,
            ),
            start=1,
        )
    )
    assert thresholds == expected_thresholds
    assert Counter(thresholds.values()) == {1: 17, 2: 28, 3: 11, 4: 3}
    assert {civilization for civilization, threshold in thresholds.items() if threshold == 4} == {
        8,
        17,
        28,
    }
    assert 9 - thresholds[8] + 1 == 6
    assert all(
        not (effect.effect_type == EffectId.TRIBUTE and effect.tribute_list == Attribute.RAZINGS)
        for trigger in triggers
        for effect in trigger.effects
    )


def test_evolution_alpha_uses_sparse_safe_two_teammate_vote_kick(evolution_alpha):
    triggers = evolution_alpha.trigger_manager.triggers
    detector_pattern = re.compile(r"VoteKickP([1-8])-P([1-8])-P([1-8])")
    resolver_pattern = re.compile(r"Vote Kick Resolve P([1-8]) W([1-8])")
    detectors = [trigger for trigger in triggers if detector_pattern.fullmatch(trigger.name)]
    resolvers = [trigger for trigger in triggers if resolver_pattern.fullmatch(trigger.name)]
    assert len(detectors) == 24
    assert len(resolvers) == len(VALID_COLOR_WORLD_PAIRS)
    assert {
        tuple(map(int, resolver_pattern.fullmatch(trigger.name).groups()))
        for trigger in resolvers
    } == VALID_COLOR_WORLD_PAIRS

    resolver_ids = {
        int(match.group(1)): trigger.trigger_id
        for trigger in resolvers
        for match in [resolver_pattern.fullmatch(trigger.name)]
    }
    resolver_ids_by_target = {
        target: {
            trigger.trigger_id
            for trigger in resolvers
            if int(resolver_pattern.fullmatch(trigger.name).group(1)) == target
        }
        for target in range(1, 9)
    }
    assert len(resolver_ids) == 8
    assert all(len(ids) == 8 for ids in resolver_ids_by_target.values())

    castle_areas = castle_row_areas(evolution_alpha)
    marker_units = [
        unit
        for units in evolution_alpha.unit_manager.units
        for unit in units
        if unit.unit_const == BuildingInfo.OUTPOST.ID
    ]
    vote_keys = sorted(
        (
            (target, voter)
            for team in (range(1, 5), range(5, 9))
            for target in team
            for voter in team
            if voter != target
        ),
        key=lambda key: (key[0], key[1]),
    )
    vote_variable = {
        key: 57 + index for index, key in enumerate(vote_keys)
    }
    marker_pattern = re.compile(r"Vote Marker Deleted P([1-8]) V([1-8]) W([1-8])")
    marker_detectors = [
        trigger for trigger in triggers if marker_pattern.fullmatch(trigger.name)
    ]
    assert len(marker_detectors) == len(vote_keys) * 8 == 192
    assert all(
        condition.source_player != -1
        for trigger in triggers
        for condition in trigger.conditions
        if condition.condition_type == ConditionId.OBJECTS_IN_AREA
        and condition.object_list == BuildingInfo.OUTPOST.ID
    )
    for marker_detector in marker_detectors:
        target, voter, world_player = map(
            int, marker_pattern.fullmatch(marker_detector.name).groups()
        )
        assert (target, voter) in vote_variable
        assert 1 <= world_player <= 8
        timers = [
            condition
            for condition in marker_detector.conditions
            if condition.condition_type == ConditionId.TIMER
        ]
        variables = [
            condition
            for condition in marker_detector.conditions
            if condition.condition_type == ConditionId.VARIABLE_VALUE
        ]
        deleted_markers = [
            condition
            for condition in marker_detector.conditions
            if condition.condition_type == ConditionId.OBJECTS_IN_AREA
        ]
        assert len(timers) == 1 and timers[0].timer == 4
        assert {
            (condition.variable, condition.quantity) for condition in variables
        } == {
            (56, 1),
            (31 + voter, 1),
            (39 + voter, world_player),
        }
        assert len(deleted_markers) == 1
        marker = deleted_markers[0]
        assert marker.object_list == BuildingInfo.OUTPOST.ID
        assert marker.source_player == world_player
        assert marker.inverted == 1
        assert any(
            int(unit.x) == marker.area_x1
            and int(unit.y) == marker.area_y1
            and int(unit.x) == marker.area_x2
            and int(unit.y) == marker.area_y2
            for unit in marker_units
        )
        changes = [
            effect
            for effect in marker_detector.effects
            if effect.effect_type == EffectId.CHANGE_VARIABLE
        ]
        assert len(changes) == 1
        assert (
            changes[0].variable,
            changes[0].quantity,
            changes[0].operation,
        ) == (vote_variable[target, voter], 1, Operation.SET)

    for detector in detectors:
        match = detector_pattern.fullmatch(detector.name)
        target, first_voter, second_voter = map(int, match.groups())
        expected_team = set(range(1, 5) if target <= 4 else range(5, 9))
        assert {target, first_voter, second_voter} <= expected_team
        assert len({target, first_voter, second_voter}) == 3
        assert detector.enabled
        assert not detector.looping

        timers = [
            condition
            for condition in detector.conditions
            if condition.condition_type == ConditionId.TIMER
        ]
        variables = [
            condition
            for condition in detector.conditions
            if condition.condition_type == ConditionId.VARIABLE_VALUE
        ]
        assert len(detector.conditions) == 7
        assert len(timers) == 1 and timers[0].timer == 4
        assert {
            (condition.variable, condition.quantity) for condition in variables
        } == {
            (56, 1),
            *((31 + player, 1) for player in (target, first_voter, second_voter)),
            (vote_variable[target, first_voter], 1),
            (vote_variable[target, second_voter], 1),
        }
        assert all(condition.comparison == Comparison.EQUAL for condition in variables)

        activations = [
            effect
            for effect in detector.effects
            if effect.effect_type == EffectId.ACTIVATE_TRIGGER
        ]
        assert {effect.trigger_id for effect in activations} == (
            resolver_ids_by_target[target]
        )

    for resolver in resolvers:
        match = resolver_pattern.fullmatch(resolver.name)
        target, world_player = map(int, match.groups())
        assert not resolver.enabled
        assert len(resolver.conditions) == 4
        castle = next(
            condition
            for condition in resolver.conditions
            if condition.condition_type == ConditionId.OBJECTS_IN_AREA
        )
        assert castle.condition_type == ConditionId.OBJECTS_IN_AREA
        assert castle.object_list == BuildingInfo.CASTLE.ID
        assert castle.source_player == world_player
        assert (castle.area_x1, castle.area_y1, castle.area_x2, castle.area_y2) == (
            castle_areas[target]
        )
        assert {
            (condition.variable, condition.quantity, condition.comparison)
            for condition in resolver.conditions
            if condition.condition_type == ConditionId.VARIABLE_VALUE
        } == {
            (56, 1, Comparison.EQUAL),
            (31 + target, 1, Comparison.EQUAL),
            (39 + target, world_player, Comparison.EQUAL),
        }

        chats = [
            effect for effect in resolver.effects if effect.effect_type == EffectId.SEND_CHAT
        ]
        clears = [
            effect
            for effect in resolver.effects
            if effect.effect_type == EffectId.CHANGE_VARIABLE
        ]
        defeats = [
            effect
            for effect in resolver.effects
            if effect.effect_type == EffectId.DECLARE_VICTORY
        ]
        purges = [
            effect
            for effect in resolver.effects
            if effect.effect_type == EffectId.REMOVE_OBJECT
        ]
        assert len(chats) == len(defeats) == 1
        assert len(purges) == 1
        assert purges[0].source_player == world_player
        assert (
            purges[0].area_x1,
            purges[0].area_y1,
            purges[0].area_x2,
            purges[0].area_y2,
        ) == (-1, -1, -1, -1)
        # Only the elimination bit: XS owns p#coloractive and derives it from this.
        assert len(clears) == 1
        assert chats[0].source_player == -1
        assert "vote-kicked" in chats[0].message
        assert {
            (effect.variable, effect.quantity, effect.operation)
            for effect in clears
        } == {
            (47 + target, 1, Operation.SET),
        }
        assert defeats[0].source_player == world_player
        assert not defeats[0].enabled

    xs_trigger = next(trigger for trigger in triggers if trigger.name == "XS SCRIPT")
    xs_source = xs_trigger.effects[0].message
    assert "void cbaUpdateColorRuntime(int scenarioPlayer = 0)" in xs_source
    assert "int owner = xsGetUnitOwner(reference);" in xs_source
    assert "int worldPlayer = cbaWorldPlayerForColor(scenarioPlayer);" in xs_source
    assert "rule cbaColorRuntimeState" in xs_source
    assert xs_source.count("cbaUpdateColorRuntime(") == 9
    assert "40 + scenarioPlayer - 1" not in xs_source
    assert "48 + scenarioPlayer - 1" in xs_source


def test_evolution_alpha_detects_every_color_owner_from_its_castles(
    evolution_alpha,
):
    pattern = re.compile(r"Color Owner Detect S([1-8]) W([1-8])")
    detectors = {
        tuple(map(int, match.groups())): trigger
        for trigger in evolution_alpha.trigger_manager.triggers
        if (match := pattern.fullmatch(trigger.name))
    }
    assert set(detectors) == VALID_COLOR_WORLD_PAIRS
    castle_areas = castle_row_areas(evolution_alpha)
    for (color, world_player), detector in detectors.items():
        assert detector.enabled and detector.looping
        assert len(detector.conditions) == 3
        castle = next(
            condition
            for condition in detector.conditions
            if condition.condition_type == ConditionId.OBJECTS_IN_AREA
        )
        assert (
            castle.object_list,
            castle.source_player,
            castle.area_x1,
            castle.area_y1,
            castle.area_x2,
            castle.area_y2,
        ) == (BuildingInfo.CASTLE.ID, world_player, *castle_areas[color])
        variables = [
            effect
            for effect in detector.effects
            if effect.effect_type == EffectId.CHANGE_VARIABLE
        ]
        # p#coloractive is deliberately absent: XS is its only writer.
        assert {
            (effect.variable, effect.quantity, effect.operation)
            for effect in variables
        } == {
            (39 + color, world_player, Operation.SET),
            (88 + color, 3, Operation.SET),
            (112 + color, 3, Operation.SET),
        }
        # The detector arms exactly the one victory trigger that can match its latch.
        activations = [
            effect
            for effect in detector.effects
            if effect.effect_type == EffectId.ACTIVATE_TRIGGER
        ]
        assert len(activations) == 1
        armed = next(
            trigger
            for trigger in evolution_alpha.trigger_manager.triggers
            if trigger.trigger_id == activations[0].trigger_id
        )
        assert armed.name == f"Color Team Victory S{color} W{world_player}"
        assert not armed.enabled
        deactivations = [
            effect
            for effect in detector.effects
            if effect.effect_type == EffectId.DEACTIVATE_TRIGGER
        ]
        assert len(deactivations) == 1
        assert deactivations[0].trigger_id == detector.trigger_id
        assert detector.effects[-1] is deactivations[0]

    # This proves complete trigger-side candidate coverage only. XS lobby-slot
    # ownership is a different identity domain and is guarded separately by the
    # Castle-reference binding tests; the converter is diagnostic only.
    assert detectors[3, 4].name == "Color Owner Detect S3 W4"
    assert detectors[4, 3].name == "Color Owner Detect S4 W3"


def test_evolution_alpha_removes_invisible_edge_deletion_strips(evolution_alpha):
    disabled = [
        trigger
        for trigger in evolution_alpha.trigger_manager.triggers
        if trigger.name.startswith("Legacy Edge Delete Disabled (uk")
    ]
    assert disabled == []


def test_evolution_alpha_anti_treb_zones_are_mirrored_and_cover_their_castles(
    evolution_alpha,
):
    """The anti-treb kill zones must be one mirror orbit, and each must reach its Castles.

    This deliberately asserts the *property*, not the eight rectangles. The previous
    version of this test restated the same literal table that build.py used, so it could
    not fail for a wrong-but-consistent value — and it did not: only one of the eight
    zones matched any mirror of another, and P4/P6/P7/P8's zones stopped at 123 while
    their Castle rows sit at 125, leaving a Trebuchet parked beside those four players'
    Castles alive while the mirror-image position in P1/P2/P3/P5's base was cleared.
    """
    triggers = evolution_alpha.trigger_manager.triggers
    zones = {}
    for base_player in range(1, 9):
        matches = [
            trigger
            for trigger in triggers
            if trigger.name == f"No trebs in p{base_player} base"
            or trigger.name.startswith(f"No trebs in p{base_player} base (p")
        ]
        assert len(matches) == 8
        areas = set()
        for trigger in matches:
            effects = [
                effect for effect in trigger.effects if effect.effect_type == EffectId.KILL_OBJECT
            ]
            assert len(effects) == 1
            effect = effects[0]
            areas.add((effect.area_x1, effect.area_y1, effect.area_x2, effect.area_y2))
        assert len(areas) == 1, f"P{base_player} anti-treb zones disagree: {areas}"
        zones[base_player] = areas.pop()

    # Every zone is the P3 zone reflected into that player's sector.
    source = zones[3]
    for base_player, bounds in zones.items():
        corner_a = v2_cell_for_player(base_player, source[0], source[1])
        corner_b = v2_cell_for_player(base_player, source[2], source[3])
        x1, x2 = sorted((corner_a[0], corner_b[0]))
        y1, y2 = sorted((corner_a[1], corner_b[1]))
        assert bounds == (x1, y1, x2, y2), (
            f"P{base_player} anti-treb zone {bounds} is not the mirror of P3's {source}"
        )

    # And each zone actually reaches the Castles it is supposed to protect.
    castles = defaultdict(list)
    for player in range(1, 9):
        for unit in evolution_alpha.unit_manager.units[player]:
            if unit.unit_const == BuildingInfo.CASTLE.ID:
                castles[player].append((int(unit.x), int(unit.y)))
    for base_player, (x1, y1, x2, y2) in zones.items():
        owned = castles[base_player]
        assert len(owned) == 4
        covered = [c for c in owned if x1 <= c[0] <= x2 and y1 <= c[1] <= y2]
        assert len(covered) == 4, (
            f"P{base_player} zone {(x1, y1, x2, y2)} misses Castles "
            f"{sorted(set(owned) - set(covered))}"
        )


def test_evolution_alpha_wall_breach_removes_side_walls_but_keeps_front_and_uni(evolution_alpha):
    triggers = evolution_alpha.trigger_manager.triggers
    wall_pattern = re.compile(r"Wall Breach S([1-8]) W([1-8])")
    wall_breaches = {
        tuple(map(int, match.groups())): trigger
        for trigger in triggers
        if (match := wall_pattern.fullmatch(trigger.name))
    }
    assert set(wall_breaches) == VALID_COLOR_WORLD_PAIRS

    by_name = {trigger.name: trigger for trigger in triggers}
    structural_types = {
        BuildingInfo.STONE_WALL.ID,
        BuildingInfo.FORTIFIED_WALL.ID,
        *mapview.GATE_IDS,
    }
    for player in range(1, 9):
        owned_units = evolution_alpha.unit_manager.units[player]
        yard_positions = {
            v2_position_for_player(player, x, y)
            for x, y in (
                *((x + 0.5, y) for x in range(17, 25) for y in (43.5, 64.5)),
                *((24.5, y + 0.5) for y in (*range(44, 47), *range(61, 64))),
                *((x + 0.5, y) for x in range(24, 39) for y in (47.5, 60.5)),
            )
        }
        expected_removals = {
            unit.reference_id
            for unit in owned_units
            if unit.unit_const in {BuildingInfo.STONE_WALL.ID, BuildingInfo.FORTIFIED_WALL.ID}
            and (unit.x, unit.y) in yard_positions
        }
        assert len(expected_removals) == (44 if player in {1, 2, 7, 8} else 48)
        switch, = [
            unit for unit in owned_units
            if (unit.x, unit.y) == v2_position_for_player(player, 23.0, 43.5)
            and unit.unit_const in mapview.GATE_IDS
        ]
        permanent = {
            unit.reference_id
            for unit in owned_units
            if unit.unit_const in structural_types
        } - expected_removals - {switch.reference_id}
        assert permanent
        uni_gate, = [
            unit for unit in owned_units
            if (unit.x, unit.y) == v2_position_for_player(player, 14.5, 54.0)
            and unit.unit_const in mapview.GATE_IDS
        ]
        assert uni_gate.reference_id in permanent
        side_walls = {
            unit.reference_id
            for unit in owned_units
            if unit.unit_const in {BuildingInfo.STONE_WALL.ID, BuildingInfo.FORTIFIED_WALL.ID}
            and (unit.x, unit.y) in {
                v2_position_for_player(player, x + 0.5, y)
                for x in range(24, 39)
                for y in (47.5, 60.5)
            }
        }
        assert len(side_walls) == 30
        assert side_walls <= expected_removals
        front_row = {
            unit.reference_id
            for unit in owned_units
            if (unit.x, unit.y) in {
                v2_position_for_player(player, 39.5, y)
                for y in (45.5, 46.5, 47.5, 50.0, 54.0, 58.0, 60.5, 61.5, 62.5)
            }
            and unit.unit_const in structural_types
        }
        assert len(front_row) == 9
        assert front_row <= permanent
        front_endcaps = {
            unit.reference_id
            for unit in owned_units
            if (unit.x, unit.y) in {
                v2_position_for_player(player, 39.5, y)
                for y in (45.5, 46.5, 61.5, 62.5)
            }
        }
        assert len(front_endcaps) == 4
        assert front_endcaps <= permanent
        removal_footprints = {
            cell
            for unit in owned_units
            if unit.reference_id in expected_removals
            for cell in mapview._footprint(unit.unit_const, unit.x, unit.y)
        }
        rear_route = {
            v2_cell_for_player(player, source_x, source_y)
            for source_x in range(7, 17)
            for source_y in (53, 54, 55)
        }
        assert removal_footprints.isdisjoint(rear_route)
        assert any(
            effect.effect_type == EffectId.DISABLE_OBJECT_DELETION
            and effect.source_player == -1
            and permanent.issubset(effect.selected_object_ids or ())
            for effect in by_name[f"Antidelete P{player}"].effects
        )
        assert all(
            switch.reference_id not in (effect.selected_object_ids or ())
            for effect in by_name[f"Antidelete P{player}"].effects
            if effect.effect_type == EffectId.DISABLE_OBJECT_DELETION
        )

        for world_player in range(1, 9):
            trigger = wall_breaches[player, world_player]
            assert trigger.enabled and not trigger.looping
            effects = [
                effect
                for effect in trigger.effects
                if effect.effect_type == EffectId.REMOVE_OBJECT
            ]
            assert len(effects) == len(trigger.effects) == 1
            effect = effects[0]
            assert effect.source_player == world_player
            assert set(effect.selected_object_ids) == expected_removals
            assert effect.object_list_unit_id == -1
            assert (effect.area_x1, effect.area_y1, effect.area_x2, effect.area_y2) == (-1,) * 4
            gate_condition, = [
                condition
                for condition in trigger.conditions
                if condition.condition_type == ConditionId.DESTROY_OBJECT
            ]
            assert gate_condition.unit_object == switch.reference_id
            assert {
                (condition.variable, condition.quantity, condition.comparison)
                for condition in trigger.conditions
                if condition.condition_type == ConditionId.VARIABLE_VALUE
            } == {
                (31 + player, 1, Comparison.EQUAL),
                (39 + player, world_player, Comparison.EQUAL),
            }
            detector = by_name[f"Color Owner Detect S{player} W{world_player}"]
            assert any(
                effect.effect_type == EffectId.DISABLE_OBJECT_DELETION
                and effect.source_player == world_player
                and set(effect.selected_object_ids or ()) == permanent
                for effect in detector.effects
            )
            assert detector.effects[-1].effect_type == EffectId.DEACTIVATE_TRIGGER
            assert detector.effects[-1].trigger_id == detector.trigger_id


def test_evolution_alpha_gate_breach_keeps_front_and_university_enclosures_sealed(evolution_alpha):
    """Simulate serialized deletions with closed gates, including diagonal squeeze paths."""
    by_name = {
        trigger.name: trigger
        for trigger in evolution_alpha.trigger_manager.triggers
    }
    all_units = [unit for units in evolution_alpha.unit_manager.units for unit in units]
    terrain = [
        evolution_alpha.map_manager.get_tile(x=x, y=y).terrain_id
        for y in range(144)
        for x in range(144)
    ]
    all_opened_sides = {
        reference_id
        for player in range(1, 9)
        for effect in by_name[f"Wall Breach S{player} W{player}"].effects
        if effect.effect_type == EffectId.REMOVE_OBJECT
        for reference_id in effect.selected_object_ids
    } | {
        condition.unit_object
        for player in range(1, 9)
        for condition in by_name[f"Wall Breach S{player} W{player}"].conditions
        if condition.condition_type == ConditionId.DESTROY_OBJECT
    }

    def reachable_after_removing(player, deleted):
        placements = [
            mapview.Placement(unit.unit_const, unit.x, unit.y, int(unit.player))
            for unit in all_units
            if unit.reference_id not in deleted
        ]
        walkable = mapview._walkable(
            144, terrain, mapview._blocked(144, placements, gates_block=True)
        )
        start = v2_cell_for_player(player, 22, 54)
        assert walkable[start[1]][start[0]]  # Do not allow _bfs's fallback to hide a bad anchor.
        return mapview._bfs(144, walkable, start)

    for player in range(1, 9):
        trigger = by_name[f"Wall Breach S{player} W{player}"]
        switches = {
            condition.unit_object
            for condition in trigger.conditions
            if condition.condition_type == ConditionId.DESTROY_OBJECT
        }
        assert len(switches) == 1
        removals = {
            reference_id
            for effect in trigger.effects
            if effect.effect_type == EffectId.REMOVE_OBJECT
            for reference_id in effect.selected_object_ids
        }
        assert len(removals) == (44 if player in {1, 2, 7, 8} else 48)
        arena = v2_cell_for_player(player, 42, 54)
        university = v2_cell_for_player(player, 10, 54)
        opened_side = v2_cell_for_player(player, 30, 47)
        assert opened_side not in reachable_after_removing(player, set())
        after_breach = reachable_after_removing(player, removals | switches)
        assert opened_side in after_breach
        assert arena not in after_breach
        assert university not in after_breach
        # Stress all eight switches at once: neighboring openings must not
        # create a route around someone else's preserved gate barrier either.
        after_all_breaches = reachable_after_removing(player, all_opened_sides)
        assert opened_side in after_all_breaches
        assert arena not in after_all_breaches
        assert university not in after_all_breaches

        # A surviving, opened University gate still provides the intended access;
        # the fix must not turn the rear enclosure into an inaccessible island.
        uni_gate, = [
            unit for unit in evolution_alpha.unit_manager.units[player]
            if unit.unit_const in mapview.GATE_IDS
            and (unit.x, unit.y) == v2_position_for_player(player, 14.5, 54.0)
        ]
        assert uni_gate.reference_id not in removals | switches
        opened_uni = reachable_after_removing(
            player, removals | switches | {uni_gate.reference_id}
        )
        assert university in opened_uni
        assert arena not in opened_uni

        # Sensitivity check: only opening the surviving front gates permits the
        # intended front route. An unreachable arena anchor cannot hide bypasses.
        front_gates = {
            unit.reference_id
            for unit in evolution_alpha.unit_manager.units[player]
            if unit.unit_const in mapview.GATE_IDS
            and (unit.x, unit.y) in {
                v2_position_for_player(player, 39.5, y)
                for y in (50.0, 54.0, 58.0)
            }
        }
        assert len(front_gates) == 3
        assert front_gates.isdisjoint(removals | switches)
        opened_front = reachable_after_removing(player, removals | switches | front_gates)
        assert arena in opened_front
        assert university not in opened_front


def _permanent_wall_and_gate_cells(scenario):
    """Independent spatial role contract; do not trust the deletion effects themselves."""
    structural_types = {
        BuildingInfo.STONE_WALL.ID,
        BuildingInfo.FORTIFIED_WALL.ID,
        *mapview.GATE_IDS,
    }
    protected = set()
    for player in range(1, 9):
        side_positions = {
            v2_position_for_player(player, x, y)
            for x, y in (
                *((x + 0.5, y) for x in range(17, 25) for y in (43.5, 64.5)),
                *((24.5, y + 0.5) for y in (*range(44, 47), *range(61, 64))),
                *((x + 0.5, y) for x in range(24, 39) for y in (47.5, 60.5)),
                (23.0, 43.5),  # The deletable switch, not a permanent barrier.
            )
        }
        for unit in scenario.unit_manager.units[player]:
            if unit.unit_const in structural_types and (unit.x, unit.y) not in side_positions:
                footprint = mapview._footprint(unit.unit_const, unit.x, unit.y)
                assert len(footprint) == (4 if unit.unit_const in mapview.GATE_IDS else 1)
                protected.update(footprint)
    assert len(protected) == 368
    return protected


def test_evolution_alpha_wall_cap_warns_then_wipes_for_every_resolved_owner(evolution_alpha):
    triggers = evolution_alpha.trigger_manager.triggers
    families = {}
    for family in ("Warn", "Wipe"):
        pattern = re.compile(rf"Wall Cap {family} S([1-8]) W([1-8])")
        families[family] = {
            tuple(map(int, match.groups())): trigger
            for trigger in triggers
            if (match := pattern.fullmatch(trigger.name))
        }
        assert set(families[family]) == VALID_COLOR_WORLD_PAIRS

    wipe_ids = {trigger.trigger_id for trigger in families["Wipe"].values()}
    activation_edges = Counter(
        (trigger.trigger_id, effect.trigger_id)
        for trigger in triggers
        for effect in trigger.effects
        if effect.effect_type == EffectId.ACTIVATE_TRIGGER and effect.trigger_id in wipe_ids
    )
    assert activation_edges == Counter({
        (families["Warn"][pair].trigger_id, families["Wipe"][pair].trigger_id): 1
        for pair in VALID_COLOR_WORLD_PAIRS
    })

    for (color, world_player), warning in families["Warn"].items():
        wipe = families["Wipe"][color, world_player]
        assert warning.enabled and not warning.looping
        assert not wipe.enabled and not wipe.looping
        for trigger, threshold in ((warning, 200), (wipe, 220)):
            assert len(trigger.conditions) == 4
            timer, = [
                condition for condition in trigger.conditions
                if condition.condition_type == ConditionId.TIMER
            ]
            assert timer.timer == 1 and not timer.inverted
            count, = [
                condition for condition in trigger.conditions
                if condition.condition_type == ConditionId.OWN_OBJECTS
            ]
            # Keep the original count basis: all owned WALL-class objects, not
            # just side walls, one wall unit ID, or fixed scenario-player slots.
            assert count.quantity == threshold
            assert count.source_player == world_player
            assert count.object_group == ObjectClass.WALL
            assert count.object_list == -1
            assert not count.inverted
            assert {
                (condition.variable, condition.quantity, condition.comparison)
                for condition in trigger.conditions
                if condition.condition_type == ConditionId.VARIABLE_VALUE
            } == {
                (31 + color, 1, Comparison.EQUAL),
                (39 + color, world_player, Comparison.EQUAL),
            }
        assert len(warning.effects) == 2
        chat, activation = warning.effects
        assert chat.effect_type == EffectId.SEND_CHAT
        assert chat.source_player == world_player and chat.message
        assert activation.effect_type == EffectId.ACTIVATE_TRIGGER
        assert activation.trigger_id == wipe.trigger_id
        assert wipe.effects[-1].effect_type == EffectId.SEND_CHAT
        assert wipe.effects[-1].source_player == world_player


def test_evolution_alpha_wall_cap_clears_every_nonstructural_cell_once(evolution_alpha):
    protected = _permanent_wall_and_gate_cells(evolution_alpha)
    permitted = {(x, y) for x in range(144) for y in range(144)} - protected
    patterns = set()
    for trigger in evolution_alpha.trigger_manager.triggers:
        match = re.fullmatch(r"Wall Cap Wipe S([1-8]) W([1-8])", trigger.name)
        if match is None:
            continue
        color, world_player = map(int, match.groups())
        removals = [effect for effect in trigger.effects if effect.effect_type == EffectId.REMOVE_OBJECT]
        assert len(removals) == len(trigger.effects) - 1
        assert removals
        coverage = Counter()
        rectangles = []
        for effect in removals:
            assert effect.source_player == world_player
            assert effect.object_group == ObjectClass.WALL
            assert effect.object_list_unit_id == -1
            assert not effect.selected_object_ids
            rectangle = (effect.area_x1, effect.area_y1, effect.area_x2, effect.area_y2)
            x1, y1, x2, y2 = rectangle
            assert 0 <= x1 <= x2 < 144 and 0 <= y1 <= y2 < 144
            cells = {(x, y) for x in range(x1, x2 + 1) for y in range(y1, y2 + 1)}
            assert cells.isdisjoint(protected), (trigger.name, rectangle)
            coverage.update(cells)
            rectangles.append(rectangle)
        assert set(coverage) == permitted
        assert set(coverage.values()) == {1}
        patterns.add(tuple(rectangles))

        # Every removable side segment is inside the cap's spatial mask, while
        # the complete front gate row and rear University barrier are outside it.
        side_cells = {
            v2_cell_for_player(color, x, y)
            for x in range(24, 39)
            for y in (47, 60)
        }
        assert side_cells <= permitted
        assert {
            v2_cell_for_player(color, 39, y)
            for y in range(45, 63)
        } <= protected
        assert {
            v2_cell_for_player(color, 14, y)
            for y in range(44, 64)
        } <= protected
    assert len(patterns) == 1


def test_evolution_alpha_has_no_unauthorized_wall_or_gate_destruction(evolution_alpha):
    structural_types = {
        BuildingInfo.STONE_WALL.ID,
        BuildingInfo.FORTIFIED_WALL.ID,
        *mapview.GATE_IDS,
    }
    protected_cells = _permanent_wall_and_gate_cells(evolution_alpha)
    structural_refs = {
        unit.reference_id
        for units in evolution_alpha.unit_manager.units
        for unit in units
        if unit.unit_const in structural_types
    }
    destructive_types = {
        EffectId.REMOVE_OBJECT,
        EffectId.KILL_OBJECT,
        EffectId.DAMAGE_OBJECT,
        EffectId.CHANGE_OBJECT_HP,
        EffectId.REPLACE_OBJECT,
        EffectId.CHANGE_OWNERSHIP,
    }
    found = Counter()
    for trigger in evolution_alpha.trigger_manager.triggers:
        for effect in trigger.effects:
            if effect.effect_type not in destructive_types:
                continue
            selected = set(effect.selected_object_ids or ())
            if selected:
                if not selected.intersection(structural_refs):
                    continue
                assert effect.effect_type == EffectId.REMOVE_OBJECT, (trigger.name, effect.effect_type)
                assert re.fullmatch(r"Wall Breach S[1-8] W[1-8]", trigger.name), trigger.name
                assert selected <= structural_refs
                assert (effect.area_x1, effect.area_y1, effect.area_x2, effect.area_y2) == (-1,) * 4
                found["exact_breach"] += 1
                continue
            if effect.object_list_unit_id >= 0 and effect.object_list_unit_id not in structural_types:
                continue
            if effect.object_group >= 0 and effect.object_group not in {ObjectClass.WALL, ObjectClass.GATE}:
                continue
            if effect.object_type >= 0 and effect.object_type != ObjectType.BUILDING:
                continue
            assert effect.effect_type == EffectId.REMOVE_OBJECT, (trigger.name, effect.effect_type)
            cap_match = re.fullmatch(r"Wall Cap Wipe S([1-8]) W([1-8])", trigger.name)
            if cap_match:
                assert effect.source_player == int(cap_match.group(2))
                assert effect.object_group == ObjectClass.WALL
                assert effect.object_list_unit_id == -1
                x1, y1, x2, y2 = effect.area_x1, effect.area_y1, effect.area_x2, effect.area_y2
                assert 0 <= x1 <= x2 < 144 and 0 <= y1 <= y2 < 144
                assert protected_cells.isdisjoint(
                    (x, y) for x in range(x1, x2 + 1) for y in range(y1, y2 + 1)
                )
                found["bounded_wall_cap"] += 1
                continue
            assert re.fullmatch(
                r"(?:(?:Color Defeat Resolve|Color Runtime Defeated|Color Elimination Cleanup) "
                r"S[1-8]|Vote Kick Resolve P[1-8]) W[1-8]",
                trigger.name,
            ), trigger.name
            assert (effect.area_x1, effect.area_y1, effect.area_x2, effect.area_y2) == (-1, -1, -1, -1)
            found["player_elimination"] += 1
    assert found["exact_breach"] == 64
    assert found["player_elimination"] == 256
    assert found["bounded_wall_cap"] > 64
    assert set(found) == {"exact_breach", "player_elimination", "bounded_wall_cap"}


def test_evolution_alpha_uses_color_side_custom_victory(evolution_alpha):
    assert evolution_alpha.option_manager.victory_condition == VictoryCondition.CUSTOM
    assert not evolution_alpha.option_manager.victory_custom_conditions_required
    assert evolution_alpha.sections["GlobalVictory"].retriever_map["conquest_required"].data == 0

    triggers = evolution_alpha.trigger_manager.triggers
    defeat_pattern = re.compile(r"Color Defeat Resolve S([1-8]) W([1-8])")
    resigned_pattern = re.compile(r"Color Runtime Defeated S([1-8]) W([1-8])")
    victory_pattern = re.compile(r"Color Team Victory S([1-8]) W([1-8])")
    ready_pattern = re.compile(r"Color Match Ready L([1-4]) R([5-8])")
    defeat_triggers = [
        trigger for trigger in triggers if defeat_pattern.fullmatch(trigger.name)
    ]
    victory_triggers = [
        trigger for trigger in triggers if victory_pattern.fullmatch(trigger.name)
    ]
    resigned_triggers = [
        trigger for trigger in triggers if resigned_pattern.fullmatch(trigger.name)
    ]
    ready_triggers = [
        trigger for trigger in triggers if ready_pattern.fullmatch(trigger.name)
    ]
    assert (
        len(defeat_triggers)
        == len(resigned_triggers)
        == len(victory_triggers)
        == len(VALID_COLOR_WORLD_PAIRS)
    )
    for pattern, family in (
        (defeat_pattern, defeat_triggers),
        (resigned_pattern, resigned_triggers),
        (victory_pattern, victory_triggers),
    ):
        assert {
            tuple(map(int, pattern.fullmatch(trigger.name).groups()))
            for trigger in family
        } == VALID_COLOR_WORLD_PAIRS
    assert len(ready_triggers) == 16

    defeat_ids_by_color = {
        color: {
            trigger.trigger_id
            for trigger in defeat_triggers
            if int(defeat_pattern.fullmatch(trigger.name).group(1)) == color
        }
        for color in range(1, 9)
    }
    defeat_effects = []
    for color in range(1, 9):
        castle_loss = next(
            trigger for trigger in triggers if trigger.name == f"castle (p{color})"
        )
        assert all(
            effect.effect_type != EffectId.DECLARE_VICTORY
            for effect in castle_loss.effects
        )
        activated = {
            effect.trigger_id
            for effect in castle_loss.effects
            if effect.effect_type == EffectId.ACTIVATE_TRIGGER
        }
        assert activated == defeat_ids_by_color[color]

    for trigger in defeat_triggers:
        color, world_player = map(int, defeat_pattern.fullmatch(trigger.name).groups())
        # Defeat is a map state, not a one-shot Destroy Object event: the resolver has
        # to be live from the start so any way the Castles leave the row resolves it.
        assert trigger.enabled
        assert len(trigger.conditions) == 4
        variable_conditions = [
            condition
            for condition in trigger.conditions
            if condition.condition_type == ConditionId.VARIABLE_VALUE
        ]
        castle_guards = [
            condition
            for condition in trigger.conditions
            if condition.condition_type == ConditionId.OBJECTS_IN_AREA
        ]
        assert len(variable_conditions) == 3
        assert all(
            condition.condition_type == ConditionId.VARIABLE_VALUE
            and condition.comparison == Comparison.EQUAL
            for condition in variable_conditions
        )
        assert {
            (condition.variable, condition.quantity)
            for condition in variable_conditions
        } == {
            (120 + color, 1),
            (39 + color, world_player),
            (56, 1),
        }
        assert len(castle_guards) == 1
        castle_guard = castle_guards[0]
        assert castle_guard.object_list == BuildingInfo.CASTLE.ID
        assert castle_guard.source_player == world_player
        assert castle_guard.inverted == 1
        effects = [
            effect
            for effect in trigger.effects
            if effect.effect_type == EffectId.DECLARE_VICTORY
        ]
        assert len(effects) == 1
        assert effects[0].source_player == world_player
        assert not effects[0].enabled
        defeat_effects.extend(effects)
        variable_changes = [
            effect
            for effect in trigger.effects
            if effect.effect_type == EffectId.CHANGE_VARIABLE
        ]
        assert {
            (effect.variable, effect.quantity, effect.operation)
            for effect in variable_changes
        } == {
            (47 + color, 1, Operation.SET),
        }
        removals = [
            effect
            for effect in trigger.effects
            if effect.effect_type == EffectId.REMOVE_OBJECT
        ]
        assert len(removals) == 1
        assert removals[0].source_player == world_player
        assert (
            removals[0].area_x1,
            removals[0].area_y1,
            removals[0].area_x2,
            removals[0].area_y2,
        ) == (-1, -1, -1, -1)

    legacy_cleanup = [
        trigger
        for trigger in triggers
        if re.fullmatch(r"(?:units|walls|units2|units3) \(p[1-8]\)", trigger.name)
    ]
    assert legacy_cleanup == []

    for trigger in resigned_triggers:
        color, world_player = map(int, resigned_pattern.fullmatch(trigger.name).groups())
        variables = [
            condition
            for condition in trigger.conditions
            if condition.condition_type == ConditionId.VARIABLE_VALUE
        ]
        defeated = [
            condition
            for condition in trigger.conditions
            if condition.condition_type == ConditionId.PLAYER_DEFEATED
        ]
        assert len(variables) == 3
        assert len(defeated) == 1
        assert {
            (condition.variable, condition.quantity) for condition in variables
        } == {
            (39 + color, world_player),
            (56, 1),
            (120 + color, 1),
        }
        assert defeated[0].source_player == world_player
        changes = [
            effect
            for effect in trigger.effects
            if effect.effect_type == EffectId.CHANGE_VARIABLE
        ]
        assert {
            (effect.variable, effect.quantity, effect.operation)
            for effect in changes
        } == {
            (47 + color, 1, Operation.SET),
        }
        removals = [
            effect
            for effect in trigger.effects
            if effect.effect_type == EffectId.REMOVE_OBJECT
        ]
        assert len(removals) == 1
        assert removals[0].source_player == world_player
        assert (
            removals[0].area_x1,
            removals[0].area_y1,
            removals[0].area_x2,
            removals[0].area_y2,
        ) == (-1, -1, -1, -1)

    for trigger in ready_triggers:
        left_color, right_color = map(
            int, ready_pattern.fullmatch(trigger.name).groups()
        )
        timers = [
            condition
            for condition in trigger.conditions
            if condition.condition_type == ConditionId.TIMER
        ]
        variables = [
            condition
            for condition in trigger.conditions
            if condition.condition_type == ConditionId.VARIABLE_VALUE
        ]
        assert trigger.looping
        assert len(timers) == 1 and timers[0].timer == 3
        assert {
            (condition.variable, condition.quantity, condition.comparison)
            for condition in variables
        } == {
            (39 + left_color, 1, Comparison.LARGER_OR_EQUAL),
            (39 + right_color, 1, Comparison.LARGER_OR_EQUAL),
        }
        changes = [
            effect
            for effect in trigger.effects
            if effect.effect_type == EffectId.CHANGE_VARIABLE
        ]
        assert len(changes) == 1
        assert (
            changes[0].variable,
            changes[0].quantity,
            changes[0].operation,
        ) == (56, 1, Operation.SET)
        assert {
            effect.trigger_id
            for effect in trigger.effects
            if effect.effect_type == EffectId.DEACTIVATE_TRIGGER
        } == {trigger.trigger_id}

    # Fallback elimination: independent of both the trigger-side p#worldplayer latch
    # and the XS lobby-slot domain, so a disagreement between them cannot deadlock.
    castle_areas = castle_row_areas(evolution_alpha)
    row_empty = {
        int(match.group(1)): trigger
        for trigger in triggers
        if (match := re.fullmatch(r"Color Castle Row Empty S([1-8])", trigger.name))
    }
    assert set(row_empty) == set(range(1, 9))
    for color, trigger in row_empty.items():
        assert trigger.enabled and not trigger.looping
        timers = [
            condition
            for condition in trigger.conditions
            if condition.condition_type == ConditionId.TIMER
        ]
        guards = [
            condition
            for condition in trigger.conditions
            if condition.condition_type == ConditionId.OBJECTS_IN_AREA
        ]
        assert len(trigger.conditions) == len(timers) + len(guards)
        assert len(timers) == 1 and timers[0].timer == 3
        # One inverted guard per candidate owner: the row is empty for everyone.
        assert {condition.source_player for condition in guards} == set(range(1, 9))
        for condition in guards:
            assert condition.object_list == BuildingInfo.CASTLE.ID
            assert condition.inverted == 1
            assert (
                condition.area_x1,
                condition.area_y1,
                condition.area_x2,
                condition.area_y2,
            ) == castle_areas[color]
        assert [
            (effect.effect_type, effect.variable, effect.quantity, effect.operation)
            for effect in trigger.effects
        ] == [(EffectId.CHANGE_VARIABLE, 47 + color, 1, Operation.SET)]

    victory_effects = []
    for trigger in victory_triggers:
        color, world_player = map(int, victory_pattern.fullmatch(trigger.name).groups())
        opponents = set(range(5, 9) if color <= 4 else range(1, 5))
        # Armed by the matching owner detector, never live on its own.
        assert not trigger.enabled
        timers = [
            condition
            for condition in trigger.conditions
            if condition.condition_type == ConditionId.TIMER
        ]
        variables = [
            condition
            for condition in trigger.conditions
            if condition.condition_type == ConditionId.VARIABLE_VALUE
        ]
        assert len(timers) == 1 and timers[0].timer == 5
        assert len(variables) == 11
        assert all(condition.comparison == Comparison.EQUAL for condition in variables)
        assert {(condition.variable, condition.quantity) for condition in variables} == {
            (31 + color, 1),
            (39 + color, world_player),
            (56, 1),
            *((31 + opponent, 0) for opponent in opponents),
            *((128 + opponent, 1) for opponent in opponents),
        }
        effects = [
            effect
            for effect in trigger.effects
            if effect.effect_type == EffectId.DECLARE_VICTORY
        ]
        assert len(effects) == 1
        assert effects[0].source_player == world_player
        assert effects[0].enabled
        victory_effects.extend(effects)

    def runtime_variables(
        occupied_colors,
        alive_colors=None,
        match_ready=None,
        mapping_override=None,
    ):
        if alive_colors is None:
            alive_colors = occupied_colors
        mapping = mapping_override or {
            color: world_player
            for world_player, color in enumerate(sorted(occupied_colors), start=1)
        }
        assert set(mapping) == set(occupied_colors)
        assert len(set(mapping.values())) == len(mapping)
        values = {}
        for color in range(1, 9):
            values[31 + color] = int(color in alive_colors)
            values[39 + color] = mapping.get(color, 0)
            values[47 + color] = int(color in mapping and color not in alive_colors)
            values[120 + color] = int(color in mapping)
            # These older truth-table cases represent fully cleaned eliminations.
            values[128 + color] = int(color not in alive_colors)
        if match_ready is None:
            match_ready = bool(
                occupied_colors.intersection(range(1, 5))
                and occupied_colors.intersection(range(5, 9))
            )
        values[56] = int(match_ready)
        return mapping, values

    def variable_conditions_match(trigger, values):
        return all(
            values[condition.variable] == condition.quantity
            for condition in trigger.conditions
            if condition.condition_type == ConditionId.VARIABLE_VALUE
        )

    # A one-sided launch is useful for map inspection and must never resolve as
    # a defeat or victory. The readiness latch remains clear until both color
    # sides have had at least one occupied slot.
    one_sided_starts = (
        {1},
        {4},
        {5},
        {8},
        set(range(1, 5)),
        set(range(5, 9)),
    )
    for occupied_colors in one_sided_starts:
        _mapping, values = runtime_variables(occupied_colors)
        assert values[56] == 0
        assert not any(
            variable_conditions_match(trigger, values)
            for trigger in victory_triggers
        )
        assert not any(
            variable_conditions_match(trigger, values)
            for trigger in defeat_triggers
        )

    # Even a full 4v4 cannot reach any declaration during the startup window.
    _mapping, full_before_ready = runtime_variables(
        set(range(1, 9)),
        match_ready=False,
    )
    assert not any(
        variable_conditions_match(trigger, full_before_ready)
        for trigger in victory_triggers
    )
    assert not any(
        variable_conditions_match(trigger, full_before_ready)
        for trigger in defeat_triggers
    )

    # These are the sparse starts that previously ended at the three-second
    # victory timer. Both color sides are present, so no victory trigger may fire.
    startup_sets = [
        {left, right}
        for left in range(1, 5)
        for right in range(5, 9)
    ]
    startup_sets.extend(
        (
            {1, 2, 5, 6},
            {2, 4, 5, 8},
            set(range(1, 9)),
        )
    )
    for occupied_colors in startup_sets:
        mapping, values = runtime_variables(occupied_colors)
        assert not any(
            variable_conditions_match(trigger, values)
            for trigger in victory_triggers
        )

        for color in range(1, 9):
            matching_defeats = [
                trigger
                for trigger in defeat_triggers
                if int(defeat_pattern.fullmatch(trigger.name).group(1)) == color
                and variable_conditions_match(trigger, values)
            ]
            if color in occupied_colors:
                assert len(matching_defeats) == 1
                assert int(defeat_pattern.fullmatch(matching_defeats[0].name).group(2)) == (
                    mapping[color]
                )
            else:
                assert matching_defeats == []

    full_colors = set(range(1, 9))
    for mapping in (
        {1: 1, 2: 2, 3: 4, 4: 3, 5: 5, 6: 6, 7: 7, 8: 8},
        {color: 9 - color for color in range(1, 9)},
    ):
        _, values = runtime_variables(
            full_colors,
            mapping_override=mapping,
        )
        assert not any(
            variable_conditions_match(trigger, values)
            for trigger in victory_triggers
        )
        _, left_values = runtime_variables(
            full_colors,
            set(range(1, 5)),
            mapping_override=mapping,
        )
        assert {
            trigger.name
            for trigger in victory_triggers
            if variable_conditions_match(trigger, left_values)
        } == {
            f"Color Team Victory S{color} W{mapping[color]}"
            for color in range(1, 5)
        }

    for left in range(1, 5):
        for right in range(5, 9):
            occupied = {left, right}
            mapping, left_values = runtime_variables(occupied, {left})
            left_winning = [
                trigger
                for trigger in victory_triggers
                if variable_conditions_match(trigger, left_values)
            ]
            assert [trigger.name for trigger in left_winning] == [
                f"Color Team Victory S{left} W{mapping[left]}"
            ]

            _, right_values = runtime_variables(occupied, {right})
            right_winning = [
                trigger
                for trigger in victory_triggers
                if variable_conditions_match(trigger, right_values)
            ]
            assert [trigger.name for trigger in right_winning] == [
                f"Color Team Victory S{right} W{mapping[right]}"
            ]

    _, left_team_values = runtime_variables(full_colors, set(range(1, 5)))
    assert {
        trigger.name
        for trigger in victory_triggers
        if variable_conditions_match(trigger, left_team_values)
    } == {f"Color Team Victory S{color} W{color}" for color in range(1, 5)}
    _, right_team_values = runtime_variables(full_colors, set(range(5, 9)))
    assert {
        trigger.name
        for trigger in victory_triggers
        if variable_conditions_match(trigger, right_team_values)
    } == {f"Color Team Victory S{color} W{color}" for color in range(5, 9)}

    compact_colors = {2, 4, 5, 8}
    _, one_enemy_left = runtime_variables(compact_colors, {2, 4, 8})
    assert not any(
        variable_conditions_match(trigger, one_enemy_left)
        for trigger in victory_triggers
    )
    compact_mapping, left_only = runtime_variables(compact_colors, {2, 4})
    assert {
        trigger.name
        for trigger in victory_triggers
        if variable_conditions_match(trigger, left_only)
    } == {
        f"Color Team Victory S{color} W{compact_mapping[color]}"
        for color in (2, 4)
    }

    # Exhaust every occupied/alive combination (3^8 - 1 states). This proves
    # sparse-lobby compaction cannot produce a false declaration for any color
    # subset, not only the representative examples above.
    all_colors = set(range(1, 9))
    left_colors = set(range(1, 5))
    right_colors = set(range(5, 9))
    for occupied_mask in range(1, 1 << 8):
        occupied = {
            color
            for color in all_colors
            if occupied_mask & (1 << (color - 1))
        }
        alive_mask = occupied_mask
        while True:
            alive = {
                color
                for color in occupied
                if alive_mask & (1 << (color - 1))
            }
            mapping, values = runtime_variables(occupied, alive)
            actual_winners = {
                trigger.name
                for trigger in victory_triggers
                if variable_conditions_match(trigger, values)
            }
            left_alive = alive & left_colors
            right_alive = alive & right_colors
            if not values[56] or (left_alive and right_alive) or not alive:
                expected_winners = set()
            elif left_alive:
                expected_winners = {
                    f"Color Team Victory S{color} W{mapping[color]}"
                    for color in left_alive
                }
            else:
                expected_winners = {
                    f"Color Team Victory S{color} W{mapping[color]}"
                    for color in right_alive
                }
            assert actual_winners == expected_winners

            variable_eligible_defeats = {
                trigger.name
                for trigger in defeat_triggers
                if variable_conditions_match(trigger, values)
            }
            expected_defeats = (
                {
                    f"Color Defeat Resolve S{color} W{mapping[color]}"
                    for color in occupied
                }
                if values[56]
                else set()
            )
            assert variable_eligible_defeats == expected_defeats

            if alive_mask == 0:
                break
            alive_mask = (alive_mask - 1) & occupied_mask

    all_declarations = [
        effect
        for trigger in triggers
        for effect in trigger.effects
        if effect.effect_type == EffectId.DECLARE_VICTORY
    ]
    vote_kick_effects = [
        effect
        for trigger in triggers
        if trigger.name.startswith("Vote Kick Resolve P")
        for effect in trigger.effects
        if effect.effect_type == EffectId.DECLARE_VICTORY
    ]
    assert len(vote_kick_effects) == len(VALID_COLOR_WORLD_PAIRS)
    assert {id(effect) for effect in all_declarations} == {
        id(effect)
        for effect in defeat_effects + victory_effects + vote_kick_effects
    }


def test_evolution_alpha_keeps_xs_spawn_and_trigger_routes_in_separate_identity_domains(
    evolution_alpha,
):
    """A shuffled lobby must keep one color's complete control chain together.

    Parser tests cannot execute DE's lobby mapping. They can prove that XS reads
    actual Castle owners, while every trigger-side candidate uses one consistent
    owner for milestone creation and normal/hero movement in the color's own geometry.
    """
    triggers = evolution_alpha.trigger_manager.triggers
    by_name = {trigger.name: trigger for trigger in triggers}
    xs_source = by_name["XS SCRIPT"].effects[0].message
    assert xs_source.count("xsGetWorldPlayerId(scenarioPlayer)") == 1
    assert "40 + scenarioPlayer - 1" not in xs_source

    army_destinations = (
        ((21, 48), (21, 52), (21, 55), (21, 59)),
        ((25, 49), (25, 50), (25, 54), (25, 55)),
        ((30, 50), (30, 51), (30, 54), (30, 55)),
        ((34, 51), (34, 52), (34, 54), (34, 54)),
        ((38, 52), (38, 52), (38, 54), (38, 54)),
        ((43, 53), (43, 53), (43, 54), (43, 54)),
    )
    hero_destinations = {
        1: (21, 54),
        2: (30, 52),
        3: (34, 52),
        4: (38, 53),
        5: (43, 53),
    }
    mappings = (
        {color: color for color in range(1, 9)},
        {1: 1, 2: 3, 3: 2, 4: 4, 5: 5, 6: 6, 7: 7, 8: 8},
        {color: (color % 8) + 1 for color in range(1, 9)},
    )

    for mapping in mappings:
        assert set(mapping) == set(range(1, 9))
        assert set(mapping.values()) == set(range(1, 9))
        for color, trigger_player in mapping.items():
            spawn_areas = {
                (x, y, x, y)
                for x, y in (
                    v2_cell_for_player(color, x, y)
                    for x, y in ((22, 48), (22, 52), (22, 55), (22, 59))
                )
            }
            hero_x, hero_y = v2_cell_for_player(color, 16, 38)
            milestone = by_name[
                f"Hero Milestone S{color} W{trigger_player} K200"
            ]
            milestone_create = next(
                effect
                for effect in milestone.effects
                if effect.effect_type == EffectId.CREATE_OBJECT
            )
            assert (
                milestone_create.source_player,
                milestone_create.location_x,
                milestone_create.location_y,
            ) == (trigger_player, hero_x, hero_y)

            for level, source_destinations in enumerate(army_destinations):
                selector = by_name[f"Army Range Select L{level} P{color}"]
                assert any(
                    effect.effect_type == EffectId.CHANGE_VARIABLE
                    and effect.variable == 88 + color
                    and effect.quantity == level
                    and effect.operation == Operation.SET
                    for effect in selector.effects
                )
                normal = by_name[
                    f"Army Range L{level} S{color} W{trigger_player}"
                ]
                normal_tasks = [
                    effect
                    for effect in normal.effects
                    if effect.effect_type == EffectId.TASK_OBJECT
                ]
                assert len(normal_tasks) == 4
                assert {effect.source_player for effect in normal_tasks} == {
                    trigger_player
                }
                assert {
                    (effect.area_x1, effect.area_y1, effect.area_x2, effect.area_y2)
                    for effect in normal_tasks
                } == spawn_areas
                assert [
                    (effect.location_x, effect.location_y)
                    for effect in normal_tasks
                ] == [
                    v2_cell_for_player(color, *destination)
                    for destination in source_destinations
                ]
                assert {
                    (condition.variable, condition.quantity)
                    for condition in normal.conditions
                    if condition.condition_type == ConditionId.VARIABLE_VALUE
                } >= {
                    (39 + color, trigger_player),
                    (88 + color, level),
                }

            for level, source_destination in hero_destinations.items():
                selector = by_name[f"Hero Range Select L{level} P{color}"]
                assert any(
                    effect.effect_type == EffectId.CHANGE_VARIABLE
                    and effect.variable == 112 + color
                    and effect.quantity == level
                    and effect.operation == Operation.SET
                    for effect in selector.effects
                )
                hero = by_name[
                    f"Hero Range L{level} S{color} W{trigger_player}"
                ]
                hero_task = next(
                    effect
                    for effect in hero.effects
                    if effect.effect_type == EffectId.TASK_OBJECT
                )
                assert hero_task.source_player == trigger_player
                assert (
                    hero_task.area_x1,
                    hero_task.area_y1,
                    hero_task.area_x2,
                    hero_task.area_y2,
                ) == (hero_x - 1, hero_y - 1, hero_x + 1, hero_y + 1)
                assert (hero_task.location_x, hero_task.location_y) == (
                    v2_cell_for_player(color, *source_destination)
                )
                assert {
                    (condition.variable, condition.quantity)
                    for condition in hero.conditions
                    if condition.condition_type == ConditionId.VARIABLE_VALUE
                } >= {
                    (39 + color, trigger_player),
                    (112 + color, level),
                }


def test_evolution_alpha_spawns_for_compacted_color_slots(evolution_alpha):
    triggers = evolution_alpha.trigger_manager.triggers
    disabled_spawners = [
        trigger for trigger in triggers if trigger.name.startswith("Legacy Army Spawn Disabled #")
    ]
    assert disabled_spawners == []

    xs_trigger = next(trigger for trigger in triggers if trigger.name == "XS SCRIPT")
    assert not xs_trigger.enabled
    assert len(xs_trigger.effects) == 1
    assert xs_trigger.effects[0].effect_type == EffectId.SCRIPT_CALL
    xs_source = xs_trigger.effects[0].message
    assert "int owner = xsGetUnitOwner(reference);" in xs_source
    assert "int worldPlayer = cbaWorldPlayerForColor(scenarioPlayer);" in xs_source
    assert "xsGetPlayerCivilization(worldPlayer)" in xs_source
    assert "xsPlayerAttribute(worldPlayer, cAttributeMilitaryPopulation)" in xs_source
    assert (
        "xsPlayerAttribute(worldPlayer, cAttributeMilitaryPopulation) - 1"
        in xs_source
    )
    assert xs_source.count("81 + scenarioPlayer - 1") == 1
    assert xs_source.count("xsArraySetInt(gCbaUnitByCiv") == 59
    assert xs_source.count("cbaSpawnColor(") == 9  # declaration plus all eight colors
    assert "vector(22.5, 95.5, -1)" in xs_source
    assert "vector(22.5, 84.5, -1)" in xs_source

    movement_pattern = re.compile(r"Army Range L([0-5]) S([1-8]) W([1-8])")
    movements = {
        tuple(map(int, match.groups())): trigger
        for trigger in triggers
        if (match := movement_pattern.fullmatch(trigger.name))
    }
    assert len(movements) == 6 * len(VALID_COLOR_WORLD_PAIRS)
    assert all(trigger.enabled and trigger.looping for trigger in movements.values())
    teal_for_compacted_p2 = movements[3, 5, 2]
    assert teal_for_compacted_p2.looping
    assert len(teal_for_compacted_p2.conditions) == 6
    owner = next(
        condition
        for condition in teal_for_compacted_p2.conditions
        if condition.condition_type == ConditionId.OBJECTS_IN_AREA
    )
    assert owner.condition_type == ConditionId.OBJECTS_IN_AREA
    assert owner.source_player == PlayerId.TWO
    assert owner.object_list == BuildingInfo.CASTLE.ID
    assert (
        owner.area_x1,
        owner.area_y1,
        owner.area_x2,
        owner.area_y2,
    ) == castle_row_areas(evolution_alpha)[5]

    tasks = [effect for effect in teal_for_compacted_p2.effects if effect.effect_type == EffectId.TASK_OBJECT]
    assert len(tasks) == 4
    assert {effect.source_player for effect in tasks} == {PlayerId.TWO}
    assert {effect.action_type for effect in tasks} == {ActionType.MOVE}
    assert {
        (effect.area_x1, effect.area_y1, effect.area_x2, effect.area_y2)
        for effect in tasks
    } == {
        (22, 95, 22, 95),
        (22, 91, 22, 91),
        (22, 88, 22, 88),
        (22, 84, 22, 84),
    }

    source_spawn_points = ((22, 48), (22, 52), (22, 55), (22, 59))
    spawn_points = {
        player: tuple(
            v2_cell_for_player(player, x, y)
            for x, y in source_spawn_points
        )
        for player in range(1, 9)
    }
    all_spawn_points = {
        point
        for points in spawn_points.values()
        for point in points
    }
    assert len(all_spawn_points) == 32

    static_cells = {
        (int(unit.x), int(unit.y))
        for units in evolution_alpha.unit_manager.units
        for unit in units
    }
    assert all_spawn_points.isdisjoint(static_cells)
    assert not [
        (trigger.name, effect.location_x, effect.location_y)
        for trigger in triggers
        for effect in trigger.effects
        if effect.effect_type == EffectId.CREATE_OBJECT
        and (effect.location_x, effect.location_y) in all_spawn_points
    ]

    castles = {
        player: [
            unit
            for unit in evolution_alpha.unit_manager.units[player]
            if unit.unit_const == BuildingInfo.CASTLE.ID
        ]
        for player in range(1, 9)
    }
    assert all(len(player_castles) == 4 for player_castles in castles.values())
    for player, points in spawn_points.items():
        own_castles = castles[player]
        other_castles = [
            castle
            for other_player, player_castles in castles.items()
            if other_player != player
            for castle in player_castles
        ]
        for x, y in points:
            own_distance = min(
                (castle.x - x) ** 2 + (castle.y - y) ** 2
                for castle in own_castles
            )
            other_distance = min(
                (castle.x - x) ** 2 + (castle.y - y) ** 2
                for castle in other_castles
            )
            assert own_distance < other_distance
    source_destinations = (
        ((21, 48), (21, 52), (21, 55), (21, 59)),
        ((25, 49), (25, 50), (25, 54), (25, 55)),
        ((30, 50), (30, 51), (30, 54), (30, 55)),
        ((34, 51), (34, 52), (34, 54), (34, 54)),
        ((38, 52), (38, 52), (38, 54), (38, 54)),
        ((43, 53), (43, 53), (43, 54), (43, 54)),
    )
    route_cells = all_spawn_points | {
        v2_cell_for_player(player, *destination)
        for player in range(1, 9)
        for destinations in source_destinations
        for destination in destinations
    } | {
        v2_cell_for_player(player, *destination)
        for player in range(1, 9)
        for destination in (
            (15, 38),
            (16, 38),
            (17, 38),
            (21, 54),
            (30, 52),
            (34, 52),
            (38, 53),
            (43, 53),
        )
    }
    water = {int(terrain) for terrain in TerrainId.water_terrains()}
    assert all(
        evolution_alpha.map_manager.get_tile(x=x, y=y).terrain_id not in water
        for x, y in route_cells
    )
    static_blocked_cells = {
        cell
        for units in evolution_alpha.unit_manager.units
        for unit in units
        for cell in mapview._footprint(unit.unit_const, unit.x, unit.y)
    }
    assert route_cells.isdisjoint(static_blocked_cells)
    created_blocked_cells = {
        cell
        for trigger in triggers
        for effect in trigger.effects
        if effect.effect_type == EffectId.CREATE_OBJECT
        and effect.object_list_unit_id
        not in {
            HeroInfo.ROBIN_HOOD.ID,
            HeroInfo.THEODORIC_THE_GOTH.ID,
            HeroInfo.CHARLES_MARTEL.ID,
            HeroInfo.SUBOTAI.ID,
            HeroInfo.GENGHIS_KHAN.ID,
        }
        and effect.location_x >= 0
        and effect.location_y >= 0
        for cell in mapview._footprint(
            effect.object_list_unit_id,
            effect.location_x,
            effect.location_y,
        )
    }
    assert route_cells.isdisjoint(created_blocked_cells)

    for scenario_player, expected_spawns in spawn_points.items():
        for spawn_index, (spawn_x, spawn_y) in enumerate(expected_spawns):
            transformed_destinations = [
                v2_cell_for_player(
                    scenario_player,
                    *destinations[spawn_index],
                )
                for destinations in source_destinations
            ]
            travel_distances = [
                abs(destination_x - spawn_x) + abs(destination_y - spawn_y)
                for destination_x, destination_y in transformed_destinations
            ]
            assert travel_distances == sorted(set(travel_distances))

            spawn_castle_distance = min(
                abs(castle.x - spawn_x) + abs(castle.y - spawn_y)
                for castle in castles[scenario_player]
            )
            hold_x, hold_y = transformed_destinations[0]
            hold_castle_distance = min(
                abs(castle.x - hold_x) + abs(castle.y - hold_y)
                for castle in castles[scenario_player]
            )
            assert hold_castle_distance == spawn_castle_distance - 1

        for world_player in range(1, 9):
            for level, destinations in enumerate(source_destinations):
                movement = movements[level, scenario_player, world_player]
                tasks = [
                    effect
                    for effect in movement.effects
                    if effect.effect_type == EffectId.TASK_OBJECT
                ]
                assert len(tasks) == 4
                assert {effect.source_player for effect in tasks} == {world_player}
                assert {effect.action_type for effect in tasks} == {
                    ActionType.MOVE
                }
                assert [
                    (effect.area_x1, effect.area_y1, effect.area_x2, effect.area_y2)
                    for effect in tasks
                ] == [
                    (x, y, x, y)
                    for x, y in expected_spawns
                ]
                hold_destinations = [
                    v2_cell_for_player(scenario_player, *destination)
                    for destination in source_destinations[0]
                ]
                assert all(
                    not (
                        task.area_x1 <= hold_x <= task.area_x2
                        and task.area_y1 <= hold_y <= task.area_y2
                    )
                    for task in tasks
                    for hold_x, hold_y in hold_destinations
                )
                assert [
                    (effect.location_x, effect.location_y)
                    for effect in tasks
                ] == [
                    v2_cell_for_player(scenario_player, *destination)
                    for destination in destinations
                ]
                assert {
                    (condition.variable, condition.quantity)
                    for condition in movement.conditions
                    if condition.condition_type == ConditionId.VARIABLE_VALUE
                } == {
                    (80 + scenario_player, 1),
                    (31 + scenario_player, 1),
                    (39 + scenario_player, world_player),
                    (88 + scenario_player, level),
                }
                resets = [
                    effect
                    for effect in movement.effects
                    if effect.effect_type == EffectId.CHANGE_VARIABLE
                    and effect.variable == 80 + scenario_player
                ]
                assert len(resets) == 1
                assert (resets[0].operation, resets[0].quantity) == (
                    Operation.SET,
                    0,
                )

    movement_ids = {trigger.trigger_id for trigger in movements.values()}
    assert not [
        effect
        for trigger in triggers
        for effect in trigger.effects
        if effect.effect_type
        in {EffectId.ACTIVATE_TRIGGER, EffectId.DEACTIVATE_TRIGGER}
        and effect.trigger_id in movement_ids
    ]


def test_evolution_alpha_closest_heroes_share_the_castle_front_line(evolution_alpha):
    """Read actual orders and footprints, across all 64 color/owner mappings."""
    by_name = {trigger.name: trigger for trigger in evolution_alpha.trigger_manager.triggers}
    water = {int(terrain) for terrain in TerrainId.water_terrains()}
    blocked = {
        cell
        for units in evolution_alpha.unit_manager.units
        for unit in units
        if unit.unit_const not in mapview.GATE_IDS  # Friendly gates can open.
        for cell in mapview._footprint(unit.unit_const, unit.x, unit.y)
    }
    for color in range(1, 9):
        castles = [
            unit for unit in evolution_alpha.unit_manager.units[color]
            if unit.unit_const == BuildingInfo.CASTLE.ID
        ]
        castle_cells = {
            cell for castle in castles
            for cell in mapview._footprint(castle.unit_const, castle.x, castle.y)
        }
        # Identify the Castle row's normal from placed buildings, not a color table.
        normal_axis = 0 if len({castle.x for castle in castles}) == 1 else 1
        for owner in range(1, 9):
            orders = [
                effect for effect in by_name[f"Hero Range L1 S{color} W{owner}"].effects
                if effect.effect_type == EffectId.TASK_OBJECT
            ]
            assert len(orders) == 1
            order = orders[0]
            target = (order.location_x, order.location_y)
            assert order.source_player == owner
            hold = [
                (effect.location_x, effect.location_y)
                for effect in by_name[f"Army Range L0 S{color} W{owner}"].effects
                if effect.effect_type == EffectId.TASK_OBJECT
            ]
            assert len(hold) == 4
            assert {point[normal_axis] for point in hold} == {target[normal_axis]}
            assert min(abs(x - target[0]) + abs(y - target[1]) for x, y in castle_cells) == 1
            assert target not in blocked

        # Conservative tile connectivity, not a DE-unit collision simulation.
        allowed = {v2_cell_for_player(color, x, y) for x in range(15, 45) for y in range(37, 66)}
        passable = {
            (x, y) for x, y in allowed - blocked
            if evolution_alpha.map_manager.get_tile(x=x, y=y).terrain_id not in water
        }
        start = v2_cell_for_player(color, 16, 38)
        assert start in passable and target in passable
        reached = {start}
        pending = deque([start])
        while pending:
            x, y = pending.popleft()
            for neighbor in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
                if neighbor in passable and neighbor not in reached:
                    reached.add(neighbor)
                    pending.append(neighbor)
        assert target in reached


def test_evolution_alpha_hero_milestones_work_for_every_color_and_runtime_owner(
    evolution_alpha,
):
    triggers = evolution_alpha.trigger_manager.triggers
    milestone_pattern = re.compile(
        r"Hero Milestone S([1-8]) W([1-8]) K(200|400|600|800|1000|2000)"
    )
    order_pattern = re.compile(r"Hero Range L([1-5]) S([1-8]) W([1-8])")
    milestone_units = {
        200: HeroInfo.ROBIN_HOOD.ID,
        400: HeroInfo.THEODORIC_THE_GOTH.ID,
        600: HeroInfo.CHARLES_MARTEL.ID,
        800: HeroInfo.SUBOTAI.ID,
        1_000: HeroInfo.GENGHIS_KHAN.ID,
        2_000: HeroInfo.GENGHIS_KHAN.ID,
    }
    milestone_triggers = {
        tuple(map(int, match.groups())): trigger
        for trigger in triggers
        if (match := milestone_pattern.fullmatch(trigger.name))
    }
    assert len(milestone_triggers) == len(VALID_COLOR_WORLD_PAIRS) * len(
        milestone_units
    )

    occupied_tiles = {
        (int(unit.x), int(unit.y))
        for units in evolution_alpha.unit_manager.units
        for unit in units
    }
    for color in range(1, 9):
        spawn = v2_cell_for_player(color, 16, 38)
        tile = evolution_alpha.map_manager.get_tile(x=spawn[0], y=spawn[1])
        assert tile.terrain_id == TerrainId.GRASS_2
        assert spawn not in occupied_tiles
        for world_player in range(1, 9):
            for threshold, unit_id in milestone_units.items():
                trigger = milestone_triggers[color, world_player, threshold]
                assert trigger.enabled and trigger.looping

                kill_conditions = [
                    condition
                    for condition in trigger.conditions
                    if condition.condition_type == ConditionId.ACCUMULATE_ATTRIBUTE
                    and condition.attribute == Attribute.UNITS_KILLED
                ]
                assert len(kill_conditions) == 2
                assert {
                    (
                        condition.source_player,
                        condition.quantity,
                        bool(condition.inverted),
                    )
                    for condition in kill_conditions
                } == {
                    (world_player, threshold, False),
                    (
                        world_player,
                        {
                            200: 400,
                            400: 600,
                            600: 800,
                            800: 1_000,
                            1_000: 2_000,
                            2_000: 3_500,
                        }[threshold],
                        True,
                    ),
                }
                assert any(
                    condition.condition_type == ConditionId.OWN_FEWER_OBJECTS
                    and condition.source_player == world_player
                    and condition.quantity == 251
                    for condition in trigger.conditions
                )
                variable_conditions = {
                    (condition.variable, condition.quantity, condition.comparison)
                    for condition in trigger.conditions
                    if condition.condition_type == ConditionId.VARIABLE_VALUE
                }
                assert {
                    (31 + color, 1, Comparison.EQUAL),
                    (39 + color, world_player, Comparison.EQUAL),
                    (112 + color, 1, Comparison.LARGER_OR_EQUAL),
                } <= variable_conditions
                assert all(variable != 56 for variable, _quantity, _comparison in variable_conditions)

                creates = [
                    effect
                    for effect in trigger.effects
                    if effect.effect_type == EffectId.CREATE_OBJECT
                ]
                assert len(creates) == 1
                assert (
                    creates[0].source_player,
                    creates[0].object_list_unit_id,
                    creates[0].location_x,
                    creates[0].location_y,
                ) == (world_player, unit_id, *spawn)
                movement_arms = [
                    effect
                    for effect in trigger.effects
                    if effect.effect_type == EffectId.CHANGE_VARIABLE
                    and effect.variable == 96 + color
                ]
                assert len(movement_arms) == 1
                assert (
                    movement_arms[0].operation,
                    movement_arms[0].quantity,
                ) == (Operation.SET, 1)

                deactivations = [
                    effect
                    for effect in trigger.effects
                    if effect.effect_type == EffectId.DEACTIVATE_TRIGGER
                ]
                assert not deactivations

                for effect in trigger.effects:
                    if min(
                        effect.area_x1,
                        effect.area_y1,
                        effect.area_x2,
                        effect.area_y2,
                    ) >= 0:
                        assert (
                            effect.area_x1,
                            effect.area_y1,
                            effect.area_x2,
                            effect.area_y2,
                        ) == (*spawn, *spawn)

    canonical_orders = {
        1: (21, 54),
        2: (30, 52),
        3: (34, 52),
        4: (38, 53),
        5: (43, 53),
    }
    order_triggers = {
        tuple(map(int, match.groups())): trigger
        for trigger in triggers
        if (match := order_pattern.fullmatch(trigger.name))
    }
    assert len(order_triggers) == len(canonical_orders) * len(
        VALID_COLOR_WORLD_PAIRS
    )
    assert not any(trigger.name.startswith("Hero Orders ") for trigger in triggers)
    for level, source_destination in canonical_orders.items():
        for color in range(1, 9):
            spawn_x, spawn_y = v2_cell_for_player(color, 16, 38)
            destination = v2_cell_for_player(color, *source_destination)
            for world_player in range(1, 9):
                trigger = order_triggers[level, color, world_player]
                assert trigger.enabled and trigger.looping
                assert any(
                    condition.condition_type == ConditionId.TIMER
                    and condition.timer == 1
                    for condition in trigger.conditions
                )
                selector_conditions = [
                    condition
                    for condition in trigger.conditions
                    if condition.condition_type == ConditionId.BRING_OBJECT_TO_AREA
                ]
                assert selector_conditions == []
                assert {
                    (condition.variable, condition.quantity, condition.comparison)
                    for condition in trigger.conditions
                    if condition.condition_type == ConditionId.VARIABLE_VALUE
                } == {
                    (31 + color, 1, Comparison.EQUAL),
                    (39 + color, world_player, Comparison.EQUAL),
                    (112 + color, level, Comparison.EQUAL),
                    (96 + color, 1, Comparison.EQUAL),
                }
                tasks = [
                    effect
                    for effect in trigger.effects
                    if effect.effect_type == EffectId.TASK_OBJECT
                ]
                assert len(tasks) == 1
                task = tasks[0]
                assert task.source_player == world_player
                assert (
                    task.area_x1,
                    task.area_y1,
                    task.area_x2,
                    task.area_y2,
                ) == (spawn_x - 1, spawn_y - 1, spawn_x + 1, spawn_y + 1)
                assert (task.location_x, task.location_y) == destination
                assert task.action_type == ActionType.MOVE
                movement_resets = [
                    effect
                    for effect in trigger.effects
                    if effect.effect_type == EffectId.CHANGE_VARIABLE
                    and effect.variable == 96 + color
                ]
                assert len(movement_resets) == 1
                assert (
                    movement_resets[0].operation,
                    movement_resets[0].quantity,
                ) == (Operation.SET, 0)

    for color in range(1, 9):
        spawn_x, spawn_y = v2_cell_for_player(color, 16, 38)
        travel_distances = [
            abs(destination_x - spawn_x) + abs(destination_y - spawn_y)
            for destination_x, destination_y in (
                v2_cell_for_player(color, *canonical_orders[level])
                for level in sorted(canonical_orders)
            )
        ]
        assert travel_distances == sorted(set(travel_distances))


def test_evolution_alpha_late_heroes_arm_one_shot_route_orders(evolution_alpha):
    pattern = re.compile(r"Hero Boost (K3500|K5000A|K5000B) S([1-8]) W([1-8])")
    boosts = {
        (match.group(1), int(match.group(2)), int(match.group(3))): trigger
        for trigger in evolution_alpha.trigger_manager.triggers
        if (match := pattern.fullmatch(trigger.name))
    }
    assert len(boosts) == 3 * len(VALID_COLOR_WORLD_PAIRS)

    source_locations = {
        "K3500": (16, 38),
        "K5000A": (15, 38),
        "K5000B": (17, 38),
    }
    for label, source_location in source_locations.items():
        for color, world_player in VALID_COLOR_WORLD_PAIRS:
            trigger = boosts[label, color, world_player]
            assert trigger.enabled and trigger.looping
            kill_conditions = [
                condition
                for condition in trigger.conditions
                if condition.condition_type == ConditionId.ACCUMULATE_ATTRIBUTE
                and condition.attribute == Attribute.UNITS_KILLED
            ]
            expected_kills = (
                {(world_player, 3_500, False), (world_player, 5_000, True)}
                if label == "K3500"
                else {(world_player, 5_000, False)}
            )
            assert {
                (
                    condition.source_player,
                    condition.quantity,
                    bool(condition.inverted),
                )
                for condition in kill_conditions
            } == expected_kills
            assert {
                (condition.variable, condition.quantity, condition.comparison)
                for condition in trigger.conditions
                if condition.condition_type == ConditionId.VARIABLE_VALUE
            } == {
                (31 + color, 1, Comparison.EQUAL),
                (39 + color, world_player, Comparison.EQUAL),
                (112 + color, 1, Comparison.LARGER_OR_EQUAL),
                (47 + color, 0, Comparison.EQUAL),
            }
            own_fewer = [
                condition
                for condition in trigger.conditions
                if condition.condition_type == ConditionId.OWN_FEWER_OBJECTS
            ]
            assert len(own_fewer) == 1
            assert (
                own_fewer[0].source_player,
                own_fewer[0].object_type,
                own_fewer[0].quantity,
            ) == (world_player, ObjectType.MILITARY, 301)
            creates = [
                effect
                for effect in trigger.effects
                if effect.effect_type == EffectId.CREATE_OBJECT
            ]
            assert len(creates) == 1
            assert (
                creates[0].object_list_unit_id,
                creates[0].source_player,
                creates[0].location_x,
                creates[0].location_y,
            ) == (
                HeroInfo.GENGHIS_KHAN.ID,
                world_player,
                *v2_cell_for_player(color, *source_location),
            )
            movement_arms = [
                effect
                for effect in trigger.effects
                if effect.effect_type == EffectId.CHANGE_VARIABLE
                and effect.variable == 96 + color
            ]
            assert len(movement_arms) == 1
            assert (
                movement_arms[0].operation,
                movement_arms[0].quantity,
            ) == (Operation.SET, 1)

    assert not any(
        trigger.name.startswith("Hero Boost Unlock")
        for trigger in evolution_alpha.trigger_manager.triggers
    )

    hero_ids = {
        HeroInfo.ROBIN_HOOD.ID,
        HeroInfo.THEODORIC_THE_GOTH.ID,
        HeroInfo.CHARLES_MARTEL.ID,
        HeroInfo.SUBOTAI.ID,
        HeroInfo.GENGHIS_KHAN.ID,
    }
    live_hero_creates = [
        (trigger, effect)
        for trigger in evolution_alpha.trigger_manager.triggers
        for effect in trigger.effects
        if effect.effect_type == EffectId.CREATE_OBJECT
        and effect.object_list_unit_id in hero_ids
    ]
    assert len(live_hero_creates) == 576
    for trigger, _effect in live_hero_creates:
        match = re.fullmatch(
            r"Hero (?:Milestone S([1-8]) W[1-8] K(?:200|400|600|800|1000|2000)"
            r"|Boost (?:K3500|K5000A|K5000B) S([1-8]) W[1-8])",
            trigger.name,
        )
        assert match is not None, trigger.name
        color = int(match.group(1) or match.group(2))
        assert any(
            condition.condition_type == ConditionId.VARIABLE_VALUE
            and condition.variable == 112 + color
            and condition.quantity == 1
            and condition.comparison == Comparison.LARGER_OR_EQUAL
            for condition in trigger.conditions
        ), trigger.name


def test_evolution_alpha_all_looping_move_orders_consume_one_spawn_pulse(
    evolution_alpha,
):
    """No periodic task may reclaim a unit after the player gives it a new order."""
    triggers = evolution_alpha.trigger_manager.triggers
    referenced_trigger_ids = {
        effect.trigger_id
        for trigger in triggers
        for effect in trigger.effects
        if effect.effect_type
        in {EffectId.ACTIVATE_TRIGGER, EffectId.DEACTIVATE_TRIGGER}
    }
    move_loops = [
        trigger
        for trigger in triggers
        if trigger.looping
        and (trigger.enabled or trigger.trigger_id in referenced_trigger_ids)
        and any(
            effect.effect_type == EffectId.TASK_OBJECT
            for effect in trigger.effects
        )
    ]
    assert len(move_loops) == 768

    for trigger in move_loops:
        armed_variables = {
            condition.variable
            for condition in trigger.conditions
            if condition.condition_type == ConditionId.VARIABLE_VALUE
            and condition.quantity == 1
            and condition.comparison == Comparison.EQUAL
        }
        consumed_variables = {
            effect.variable
            for effect in trigger.effects
            if effect.effect_type == EffectId.CHANGE_VARIABLE
            and effect.operation == Operation.SET
            and effect.quantity == 0
        }
        assert len(armed_variables & consumed_variables) == 1, trigger.name
        assert any(
            condition.condition_type == ConditionId.TIMER
            and condition.timer == 1
            for condition in trigger.conditions
        ), trigger.name
        assert all(
            effect.action_type == ActionType.MOVE
            for effect in trigger.effects
            if effect.effect_type == EffectId.TASK_OBJECT
        ), trigger.name


def test_evolution_alpha_removes_blocking_castle_hay_markers(evolution_alpha):
    assert not [
        (trigger.name, effect.location_x, effect.location_y)
        for trigger in evolution_alpha.trigger_manager.triggers
        for effect in trigger.effects
        if effect.effect_type == EffectId.CREATE_OBJECT
        and effect.object_list_unit_id == OtherInfo.HAY_STACK.ID
    ]
    assert not [
        trigger.name
        for trigger in evolution_alpha.trigger_manager.triggers
        if re.fullmatch(r"hay[1-4] \(p[1-8]\)", trigger.name)
    ]



def test_evolution_alpha_uses_complete_rear_walls_without_cliffs(evolution_alpha):
    cliff_constants = {getattr(OtherInfo, f"CLIFF_DEFAULT_{index}").ID for index in range(1, 10)}
    assert not [
        unit
        for unit in evolution_alpha.unit_manager.units[PlayerId.GAIA]
        if unit.unit_const in cliff_constants
    ]

    source_wall_slots = {
        (14.5, position + 0.5)
        for position in (*range(43, 52), *range(56, 65))
    }
    water = {int(terrain) for terrain in TerrainId.water_terrains()}
    for player in PlayerId.all(exclude_gaia=True):
        expected_walls = {
            v2_position_for_player(player, x, y)
            for x, y in source_wall_slots
        }
        actual_walls = {
            (unit.x, unit.y)
            for unit in evolution_alpha.unit_manager.units[player]
            if unit.unit_const == BuildingInfo.STONE_WALL.ID
            and (unit.x, unit.y) in expected_walls
        }
        assert actual_walls == expected_walls

        gate_position = v2_position_for_player(player, 14.5, 54.0)
        gates = [
            unit
            for unit in evolution_alpha.unit_manager.units[player]
            if unit.unit_const in {64, 88}
            and (unit.x, unit.y) == gate_position
        ]
        assert len(gates) == 1

        for x, y in (*expected_walls, gate_position):
            assert evolution_alpha.map_manager.get_tile(
                x=int(x), y=int(y)
            ).terrain_id not in water

        for source_x in range(8, 14):
            for source_y in range(43, 65):
                if source_x in {8, 9} and source_y >= 60:
                    # The two six-level controller lanes deliberately occupy
                    # this former rear-water corner of every color sector.
                    continue
                x, y = v2_cell_for_player(player, source_x, source_y)
                expected = (
                    TerrainId.GRASS_2
                    if source_y in {53, 54, 55}
                    else TerrainId.WATER_MEDIUM
                )
                assert evolution_alpha.map_manager.get_tile(x=x, y=y).terrain_id == expected

        side_joins = {
            v2_position_for_player(player, source_x, source_y)
            for source_y in (43.5, 64.5)
            for source_x in (14.5, 15.5, 16.5)
        }
        assert side_joins <= {
            (unit.x, unit.y)
            for unit in evolution_alpha.unit_manager.units[player]
            if unit.unit_const == BuildingInfo.STONE_WALL.ID
        }
        obsolete_overhangs = {
            v2_position_for_player(player, source_x, source_y)
            for source_y in (43.5, 64.5)
            for source_x in (10.5, 11.5, 12.5, 13.5)
        }
        assert obsolete_overhangs.isdisjoint(
            {
                (unit.x, unit.y)
                for unit in evolution_alpha.unit_manager.units[player]
                if unit.unit_const == BuildingInfo.STONE_WALL.ID
            }
        )

        expected_gate_towers = {
            v2_position_for_player(player, 15.5, source_y)
            for source_y in (52.5, 55.5)
        }
        assert expected_gate_towers <= {
            (unit.x, unit.y)
            for unit in evolution_alpha.unit_manager.units[player]
            if unit.unit_const == BuildingInfo.BOMBARD_TOWER.ID
        }

        for source_x in (15, 16):
            for source_y in range(43, 65):
                x, y = v2_cell_for_player(player, source_x, source_y)
                tile = evolution_alpha.map_manager.get_tile(x=x, y=y)
                assert (tile.terrain_id, tile.elevation, tile.layer) == (
                    TerrainId.GRASS_2,
                    1,
                    -1,
                )


def test_evolution_alpha_keeps_all_rear_technology_paths_dry(evolution_alpha):
    path_rectangles = {
        PlayerId.ONE: (53, 7, 55, 16),
        PlayerId.TWO: (88, 7, 90, 16),
        PlayerId.THREE: (7, 53, 16, 55),
        PlayerId.FOUR: (127, 53, 136, 55),
        PlayerId.FIVE: (7, 88, 16, 90),
        PlayerId.SIX: (127, 88, 136, 90),
        PlayerId.SEVEN: (53, 127, 55, 136),
        PlayerId.EIGHT: (88, 127, 90, 136),
    }
    for x1, y1, x2, y2 in path_rectangles.values():
        assert {
            (
                evolution_alpha.map_manager.get_tile(x=x, y=y).terrain_id,
                evolution_alpha.map_manager.get_tile(x=x, y=y).elevation,
                evolution_alpha.map_manager.get_tile(x=x, y=y).layer,
            )
            for y in range(y1, y2 + 1)
            for x in range(x1, x2 + 1)
        } == {(TerrainId.GRASS_2, 1, -1)}

    critical_buildings = {
        BuildingInfo.CASTLE.ID,
        BuildingInfo.STONE_WALL.ID,
        BuildingInfo.GATE_SOUTHWEST_TO_NORTHEAST.ID,
        BuildingInfo.GATE_NORTHWEST_TO_SOUTHEAST.ID,
        BuildingInfo.BOMBARD_TOWER.ID,
        BuildingInfo.BLACKSMITH.ID,
        BuildingInfo.UNIVERSITY.ID,
    }
    water = {int(terrain) for terrain in TerrainId.water_terrains()}
    assert not [
        unit
        for player in PlayerId.all(exclude_gaia=True)
        for unit in evolution_alpha.unit_manager.units[player]
        if unit.unit_const in critical_buildings
        and evolution_alpha.map_manager.get_tile(
            x=int(unit.x), y=int(unit.y)
        ).terrain_id in water
    ]

    cliff_ids = {
        getattr(OtherInfo, f"CLIFF_DEFAULT_{index}").ID
        for index in range(1, 10)
    }
    blocking_ids = {
        BuildingInfo.CASTLE.ID,
        BuildingInfo.STONE_WALL.ID,
        BuildingInfo.BOMBARD_TOWER.ID,
        *cliff_ids,
    }
    blocked = {
        (int(unit.x), int(unit.y))
        for units in evolution_alpha.unit_manager.units
        for unit in units
        if unit.unit_const in blocking_ids
    }
    for player in PlayerId.all(exclude_gaia=True):
        allowed = {
            v2_cell_for_player(player, source_x, source_y)
            for source_x in range(3, 18)
            for source_y in range(48, 61)
        }
        start = v2_cell_for_player(player, 16, 54)
        targets = {
            (int(unit.x), int(unit.y))
            for unit in evolution_alpha.unit_manager.units[player]
            if unit.unit_const
            in {BuildingInfo.BLACKSMITH.ID, BuildingInfo.UNIVERSITY.ID}
        }
        assert len(targets) == 2
        passable = {
            point
            for point in allowed
            if point not in blocked
            and evolution_alpha.map_manager.get_tile(
                x=point[0],
                y=point[1],
            ).terrain_id
            not in water
        } | targets | {start}
        reachable = {start}
        pending = deque([start])
        while pending:
            x, y = pending.popleft()
            for neighbor in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
                if neighbor in passable and neighbor not in reachable:
                    reachable.add(neighbor)
                    pending.append(neighbor)
        assert targets <= reachable


def test_evolution_alpha_messages_are_public_facing(evolution_alpha):
    messages = evolution_alpha.message_manager
    assert "Units spawn automatically" in messages.instructions
    assert "eight equal mirrored fortified territories" in messages.instructions
    assert "Guarded rear team routes" in messages.instructions
    assert "Blue, Red, Green, and Yellow" in messages.instructions
    assert "Two occupied teammates must vote" in messages.instructions
    assert "closed slots never count as votes" in messages.instructions
    assert "right-side Kills / Deaths / Razings list" in messages.instructions
    assert "Resources stay at zero" in messages.instructions
    assert "units, buildings, upgrades, and repairs are free" in messages.instructions
    assert "Sheep = Castle army range. Penguin = Hero range." in messages.instructions
    assert "snow = HOLD (new armies stay by your Castles)" in messages.instructions
    assert "Penguin on snow = OFF (no new Heroes)" in messages.instructions
    assert "The road begins exactly where HOLD/OFF ends." in messages.instructions
    assert "Water keeps each controller on its own track." in messages.instructions
    assert (
        "first ON position sends Heroes right in front of your Castles, like Army HOLD"
        in messages.instructions
    )
    assert "untouched player nicknames" not in messages.instructions
    assert "sparse-lobby-safe" not in messages.instructions
    public_text = [
        messages.instructions,
        messages.hints,
        messages.scouts,
        messages.victory,
        messages.loss,
        messages.history,
        *(
            effect.message
            for trigger in evolution_alpha.trigger_manager.triggers
            for effect in trigger.effects
            if effect.effect_type != EffectId.SCRIPT_CALL and effect.message
        ),
    ]
    serialized_labels = [
        label
        for trigger in evolution_alpha.trigger_manager.triggers
        for label in (
            trigger.name,
            trigger.description,
            trigger.short_description,
        )
    ]
    forbidden_authorship = re.compile(
        r"(?:\b(?:Codex|OpenAI|ChatGPT|GPT|AI[- ]generated|Reforged|Big_Ytri)\b|By:\s*System)",
        re.IGNORECASE,
    )
    forbidden_color_tag = re.compile(
        r"<(?:BLUE|RED|GREEN|YELLOW|AQUA|PURPLE|GREY|ORANGE)>",
        re.IGNORECASE,
    )
    assert not any(forbidden_authorship.search(text or "") for text in public_text)
    assert not any(
        forbidden_authorship.search(text or "") for text in serialized_labels
    )
    assert messages.instructions.startswith("CBA HERO: ASCENDANTS")
    assert not any(forbidden_color_tag.search(text or "") for text in public_text)
    assert not any(
        legacy in (text or "")
        for text in public_text
        for legacy in ("Mova-me", "Médio", "Longo", "Move me to set spawn")
    )


def test_evolution_alpha_has_valid_runtime_references_and_throttled_loops(
    evolution_alpha,
):
    triggers = evolution_alpha.trigger_manager.triggers
    trigger_ids = [trigger.trigger_id for trigger in triggers]
    assert trigger_ids == list(range(len(triggers)))
    valid_trigger_ids = set(trigger_ids)
    referenced_trigger_ids = {
        effect.trigger_id
        for trigger in triggers
        for effect in trigger.effects
        if effect.effect_type
        in {EffectId.ACTIVATE_TRIGGER, EffectId.DEACTIVATE_TRIGGER}
    }
    assert referenced_trigger_ids <= valid_trigger_ids

    potentially_running_loops = [
        trigger
        for trigger in triggers
        if trigger.looping
        and (trigger.enabled or trigger.trigger_id in referenced_trigger_ids)
    ]
    assert potentially_running_loops
    assert all(
        any(
            condition.condition_type == ConditionId.TIMER
            and condition.timer >= 1
            for condition in trigger.conditions
        )
        for trigger in potentially_running_loops
    )

    valid_unit_references = {
        unit.reference_id
        for units in evolution_alpha.unit_manager.units
        for unit in units
    }
    for trigger in triggers:
        if not trigger.enabled and trigger.trigger_id not in referenced_trigger_ids:
            continue
        assert all(
            condition.unit_object < 0
            or condition.unit_object in valid_unit_references
            for condition in trigger.conditions
        )
        assert all(
            not effect.selected_object_ids
            or set(effect.selected_object_ids) <= valid_unit_references
            for effect in trigger.effects
        )
        assert all(
            effect.location_object_reference < 0
            or effect.location_object_reference in valid_unit_references
            for effect in trigger.effects
        )


def test_evolution_alpha_has_no_unconditional_all_slot_resource_loop(evolution_alpha):
    unsafe_equalizers = [
        trigger
        for trigger in evolution_alpha.trigger_manager.triggers
        if trigger.looping
        and any(
            effect.effect_type == EffectId.MODIFY_RESOURCE and effect.tribute_list in range(4)
            for effect in trigger.effects
        )
        and not any(
            condition.condition_type == ConditionId.PLAYER_DEFEATED for condition in trigger.conditions
        )
    ]
    assert unsafe_equalizers == []

    nonzero_stockpile_effects = [
        (trigger.name, effect)
        for trigger in evolution_alpha.trigger_manager.triggers
        for effect in trigger.effects
        if effect.effect_type in (EffectId.MODIFY_RESOURCE, EffectId.TRIBUTE)
        and effect.tribute_list in range(4)
        and effect.quantity != 0
    ]
    assert nonzero_stockpile_effects == []


def test_free_costs_are_activated_only_for_occupied_slots(evolution_alpha):
    by_name = {trigger.name: trigger for trigger in evolution_alpha.trigger_manager.triggers}
    for player in range(1, 9):
        free_costs = by_name[f"Free Costs P{player}"]
        activators = {
            trigger.name
            for trigger in evolution_alpha.trigger_manager.triggers
            for effect in trigger.effects
            if effect.effect_type == EffectId.ACTIVATE_TRIGGER and effect.trigger_id == free_costs.trigger_id
        }
        assert activators == {
            f"Occupied Slot S{color} W{player}"
            for color in range(1, 9)
        }


def ascendants_build_module():
    """The mode's own build.py, as the builder imported it for the fixture."""
    return sys.modules["aoe2modes._modes.evolution_alpha"]


COLOR_ACTIVE_VARIABLES = {color: 31 + color for color in range(1, 9)}
COLOR_WORLD_VARIABLES = {color: 39 + color for color in range(1, 9)}
COLOR_ELIMINATED_VARIABLES = {color: 47 + color for color in range(1, 9)}
COLOR_OCCUPIED_VARIABLES = {color: 120 + color for color in range(1, 9)}
COLOR_CLEANED_VARIABLES = {color: 128 + color for color in range(1, 9)}
MATCH_READY_VARIABLE = 56
VICTORY_STATE_VARIABLES = (
    set(COLOR_ACTIVE_VARIABLES.values())
    | set(COLOR_WORLD_VARIABLES.values())
    | set(COLOR_ELIMINATED_VARIABLES.values())
    | set(COLOR_OCCUPIED_VARIABLES.values())
    | set(COLOR_CLEANED_VARIABLES.values())
    | {MATCH_READY_VARIABLE}
)


def _victory_subsystem(scenario):
    """Every trigger that can move victory state, plus whatever activates it.

    Selected from the serialized data, never by name: a trigger belongs if it writes a
    variable in the victory block, purges an eliminated owner, or declares a result;
    the set is then
    closed over incoming Activate Trigger edges so nothing that gates the subsystem is
    left outside the model.
    """
    triggers = scenario.trigger_manager.triggers
    by_id = {trigger.trigger_id: trigger for trigger in triggers}
    selected = {
        trigger.trigger_id
        for trigger in triggers
        if any(
            (
                effect.effect_type == EffectId.CHANGE_VARIABLE
                and effect.variable in VICTORY_STATE_VARIABLES
            )
            or effect.effect_type == EffectId.DECLARE_VICTORY
            or (
                effect.effect_type == EffectId.REMOVE_OBJECT
                and any(
                    c.condition_type == ConditionId.VARIABLE_VALUE
                    and c.variable in COLOR_ELIMINATED_VARIABLES.values()
                    and c.quantity == 1 and c.comparison == Comparison.EQUAL
                    for c in trigger.conditions
                )
            )
            for effect in trigger.effects
        )
    }
    frontier = set(selected)
    while frontier:
        pending = set()
        for trigger in triggers:
            if trigger.trigger_id in selected:
                continue
            if any(
                effect.effect_type == EffectId.ACTIVATE_TRIGGER
                and effect.trigger_id in frontier
                for effect in trigger.effects
            ):
                pending.add(trigger.trigger_id)
        selected |= pending
        frontier = pending
    return [by_id[trigger_id] for trigger_id in sorted(selected)]


def _run_victory_subsystem(
    subsystem, castle_areas, seats, phases, *, objects=(), pre_eliminate=(), report=None,
):
    """Run the subsystem to a fixpoint per phase and return every declared winner.

    ``seats`` maps a colour to the lobby slot XS resolves for it; a colour absent from
    it is a closed slot. Each phase is a ``(trigger_owner, castles)`` pair describing
    the map at that point: ``trigger_owner`` is the trigger-side player number holding
    a row's Castles — a separate identity domain from ``seats``, which may disagree —
    and ``castles`` says whether each row still has Castles at all.

    Phases exist because start-up ordering is part of the contract: owner detection and
    the two-sided readiness latch run while every base is still standing, and only then
    do Castles start falling. Collapsing that into one state would test a map that no
    match ever passes through.

    Timers are treated as elapsed, because the question is eventual reachability.
    ``Destroy Object`` conditions evaluate to false on purpose: an object can leave the
    map by being removed rather than destroyed, so nothing that resolves a match may
    depend on that condition ever becoming true.
    """
    row_color = {area: color for color, area in castle_areas.items()}
    variables = defaultdict(int)
    # main() starts empty slots clean; the first in-game XS observation latches
    # occupancy and resets cleanliness. Neither is derived from current aliveness.
    for color in range(1, 9):
        variables[COLOR_OCCUPIED_VARIABLES[color]] = int(color in seats)
        variables[COLOR_CLEANED_VARIABLES[color]] = int(color not in seats)
    remaining = [dict(item) for item in objects]
    victory_snapshots = []
    enabled = {trigger.trigger_id: bool(trigger.enabled) for trigger in subsystem}
    winners = set()
    seated_slots = set(seats.values())
    trigger_owner, castles = {}, {}

    def refresh_active():
        # cbaUpdateColorRuntime: XS is the only writer of p#coloractive.
        for color in range(1, 9):
            eliminated = variables[COLOR_ELIMINATED_VARIABLES[color]] == 1
            variables[COLOR_ACTIVE_VARIABLES[color]] = int(
                color in seats and not eliminated
            )

    def castle_present(condition):
        area = (
            condition.area_x1,
            condition.area_y1,
            condition.area_x2,
            condition.area_y2,
        )
        color = row_color[area]
        return castles[color] and trigger_owner.get(color) == condition.source_player

    def holds(condition):
        kind = condition.condition_type
        if kind == ConditionId.TIMER:
            return True
        if kind == ConditionId.DESTROY_OBJECT:
            return False
        if kind == ConditionId.VARIABLE_VALUE:
            value = variables[condition.variable]
            if condition.comparison == Comparison.EQUAL:
                return value == condition.quantity
            assert condition.comparison == Comparison.LARGER_OR_EQUAL, (
                condition.comparison
            )
            return value >= condition.quantity
        if kind == ConditionId.OBJECTS_IN_AREA:
            assert condition.object_list == BuildingInfo.CASTLE.ID
            present = castle_present(condition)
            return not present if condition.inverted == 1 else present
        if kind in {ConditionId.OWN_OBJECTS, ConditionId.OWN_FEWER_OBJECTS}:
            assert condition.object_list == condition.object_type == condition.object_group == -1
            count = sum(item["owner"] == condition.source_player for item in remaining)
            count += sum(
                present and trigger_owner.get(color) == condition.source_player
                for color, present in castles.items()
            )
            return (
                count < condition.quantity if kind == ConditionId.OWN_FEWER_OBJECTS
                else count >= condition.quantity
            )
        assert kind == ConditionId.PLAYER_DEFEATED, ConditionId(kind).name
        return condition.source_player not in seated_slots

    for phase, (phase_owner, phase_castles) in enumerate(phases):
        trigger_owner, castles = dict(phase_owner), dict(phase_castles)
        if phase > 0:
            # Reproduce fallback/XS pre-emption BEFORE the normal resolver runs.
            for color in pre_eliminate:
                variables[COLOR_ELIMINATED_VARIABLES[color]] = 1
        for _pass in range(64):
            changed = False
            refresh_active()
            for trigger in subsystem:
                if not enabled[trigger.trigger_id]:
                    continue
                if not all(holds(condition) for condition in trigger.conditions):
                    continue
                if not trigger.looping:
                    enabled[trigger.trigger_id] = False
                    changed = True
                for effect in trigger.effects:
                    if effect.effect_type == EffectId.CHANGE_VARIABLE:
                        if effect.variable not in VICTORY_STATE_VARIABLES:
                            continue
                        assert effect.operation == Operation.SET
                        if variables[effect.variable] != effect.quantity:
                            variables[effect.variable] = effect.quantity
                            changed = True
                    elif effect.effect_type == EffectId.ACTIVATE_TRIGGER:
                        if (
                            effect.trigger_id in enabled
                            and not enabled[effect.trigger_id]
                        ):
                            enabled[effect.trigger_id] = True
                            changed = True
                    elif effect.effect_type == EffectId.DEACTIVATE_TRIGGER:
                        if enabled.get(effect.trigger_id):
                            enabled[effect.trigger_id] = False
                            changed = True
                    elif effect.effect_type == EffectId.REMOVE_OBJECT:
                        assert effect.source_player in range(1, 9)
                        assert effect.object_list_unit_id == effect.object_type == effect.object_group == -1
                        assert effect.object_state == effect.max_units_affected == -1
                        assert (
                            effect.area_x1, effect.area_y1, effect.area_x2, effect.area_y2
                        ) == (-1, -1, -1, -1)
                        kept = [item for item in remaining if item["owner"] != effect.source_player]
                        changed |= len(kept) != len(remaining)
                        remaining = kept
                        for color in castles:
                            if castles[color] and trigger_owner.get(color) == effect.source_player:
                                castles[color] = False
                                changed = True
                    elif (
                        effect.effect_type == EffectId.DECLARE_VICTORY and effect.enabled
                    ):
                        victory_snapshots.append([dict(item) for item in remaining])
                        if effect.source_player not in winners:
                            winners.add(effect.source_player)
                            changed = True
                refresh_active()
            if not changed:
                break
        else:  # pragma: no cover - a fixpoint always exists here
            raise AssertionError("victory subsystem did not settle")
    if report is not None:
        report.update(remaining=remaining, victory_snapshots=victory_snapshots, variables=dict(variables))
    return winners


#: Colour -> lobby slot XS resolves for it. Unlisted colours are closed slots.
LOBBY_SHAPES = {
    "full 4v4": {color: color for color in range(1, 9)},
    "solo vs four": {1: 1, 5: 2, 6: 3, 7: 4, 8: 5},
    "reported 2v4 with two closed slots": {1: 1, 3: 2, 5: 3, 6: 4, 7: 5, 8: 6},
    "four vs solo": {1: 1, 2: 2, 3: 3, 4: 4, 5: 5},
    "minimum 1v1": {1: 1, 5: 2},
    "non-adjacent 2v2": {2: 1, 4: 2, 5: 3, 8: 4},
    "shuffled full": {1: 3, 2: 1, 3: 2, 4: 4, 5: 6, 6: 5, 7: 8, 8: 7},
}


def _starting_rows(seats, closed_slots_cleaned):
    """Trigger-side owner and Castle presence for every row at match start."""
    owners = {}
    castles = {}
    for color in range(1, 9):
        if color in seats:
            owners[color] = seats[color]
            castles[color] = True
        elif closed_slots_cleaned:
            owners[color] = None
            castles[color] = False
        else:
            owners[color] = color
            castles[color] = True
    return owners, castles


def test_evolution_alpha_victory_resolves_for_every_lobby_shape(evolution_alpha):
    """A side that has actually lost its Castles must always end the match.

    This is the liveness counterpart to the structural victory test. It walks the
    serialized victory subsystem as a state machine rather than checking trigger
    shapes, so a match that can never resolve fails here even though every trigger is
    individually well formed and the strict structural audit is clean.
    """
    subsystem = _victory_subsystem(evolution_alpha)
    castle_areas = castle_row_areas(evolution_alpha)

    for shape, seats in LOBBY_SHAPES.items():
        for closed_slots_cleaned in (False, True):
            for side in (range(1, 5), range(5, 9)):
                losers = [color for color in side if color in seats]
                survivors = [color for color in seats if color not in set(side)]
                if not losers or not survivors:
                    continue
                start = _starting_rows(seats, closed_slots_cleaned)
                owners, castles = _starting_rows(seats, closed_slots_cleaned)
                # The winning side razes exactly the occupied enemy bases. It must
                # never have to raze a colour nobody is playing.
                for color in losers:
                    castles[color] = False
                    owners[color] = None
                winners = _run_victory_subsystem(
                    subsystem, castle_areas, seats, [start, (owners, castles)]
                )
                assert winners == {seats[color] for color in survivors}, (
                    f"{shape}, closed slots cleaned={closed_slots_cleaned}, "
                    f"side {tuple(side)} eliminated"
                )

    for shape, seats in LOBBY_SHAPES.items():
        for closed_slots_cleaned in (False, True):
            start = _starting_rows(seats, closed_slots_cleaned)
            assert (
                _run_victory_subsystem(subsystem, castle_areas, seats, [start])
                == set()
            ), f"{shape} declared a winner while both sides still hold Castles"


def test_evolution_alpha_victory_survives_split_player_identity(evolution_alpha):
    """The two player-identity domains may disagree without deadlocking the match.

    ``p#worldplayer`` is latched from the trigger-side Castle owner; ``p#coloractive``
    comes from cached XS Castle ownership. A sparse lobby can make the two differ. When they
    do, every owner-resolved defeat trigger for that colour is unsatisfiable, so the
    match can only end because elimination also has a path needing neither latch.
    """
    subsystem = _victory_subsystem(evolution_alpha)
    castle_areas = castle_row_areas(evolution_alpha)
    seats = {1: 1, 5: 2, 6: 3, 7: 4, 8: 5}

    # Start-up: every occupied row resolves to a live lobby slot on the trigger side,
    # but a different one from the seat XS resolves for that colour.
    skewed = {1: 5, 5: 1, 6: 2, 7: 3, 8: 4}
    assert set(skewed.values()) == set(seats.values())
    assert all(skewed[color] != seats[color] for color in (1, 5, 6, 7))
    start_owners, start_castles = _starting_rows(seats, False)
    start_owners.update(skewed)
    start = (start_owners, start_castles)

    for losing_side in ((5, 6, 7, 8), (1,)):
        surviving = [color for color in seats if color not in losing_side]
        owners = dict(start_owners)
        castles = dict(start_castles)
        for color in losing_side:
            # Worst case: the rows do not merely empty, the trigger layer also stops
            # resolving an owner for them, so no Color Defeat Resolve can ever match
            # and only the row-empty fallback can clear the victory gate.
            owners[color] = None
            castles[color] = False
        # The match resolves through the trigger-side owner of each surviving colour.
        # Which lobby slot that names is the pre-existing property of trigger player
        # fields; that it resolves at all is what this test pins.
        assert (
            _run_victory_subsystem(
                subsystem, castle_areas, seats, [start, (owners, castles)]
            )
            == {start_owners[color] for color in surviving}
        ), losing_side


def test_evolution_alpha_elimination_purges_objects_before_any_winner(evolution_alpha):
    """Exercise the serialized effects, including XS pre-emption and spent resolvers.

    This is a trigger-state model, not an engine test of garrison/collision behavior.
    Geometry/filter coverage is independently checked for all 64 mappings below.
    """
    subsystem = _victory_subsystem(evolution_alpha)
    castle_areas = castle_row_areas(evolution_alpha)
    for seats in LOBBY_SHAPES.values():
        objects = [
            {"owner": seats[color], "id": unit.reference_id, "state": unit.status}
            for color in seats
            for unit in evolution_alpha.unit_manager.units[color]
            if unit.unit_const != BuildingInfo.CASTLE.ID
        ]
        objects += [
            {"owner": owner, "id": f"{owner}-{kind}", "state": state}
            for owner in seats.values()
            for kind, state in (("foundation", 0), ("unfinished", 1), ("garrisoned", 2), ("dying", 4))
        ]
        objects.append({"owner": 0, "id": "gaia", "state": 2})
        start = _starting_rows(seats, True)
        for side in (range(1, 5), range(5, 9)):
            losing_colors = set(side) & seats.keys()
            losing_owners = {seats[color] for color in losing_colors}
            owners, castles = _starting_rows(seats, True)
            for color in losing_colors:
                castles[color] = False
                owners[color] = None
            for immediate_resolvers, castles_still_present in (
                (True, False), (False, False), (True, True), (False, True),
            ):
                # Once a one-shot resolver has fired, only durable cleanup can
                # catch delayed objects. Remove those resolvers from this case.
                selected = subsystem if immediate_resolvers else [
                    trigger for trigger in subsystem
                    if not trigger.name.startswith(("Color Defeat Resolve ", "Color Runtime Defeated "))
                ]
                phase_owners, phase_castles = dict(owners), dict(castles)
                if castles_still_present:
                    # Resignation/XS loss can latch elimination with Castles intact.
                    for color in losing_colors:
                        phase_owners[color], phase_castles[color] = seats[color], True
                report = {}
                winners = _run_victory_subsystem(
                    selected, castle_areas, seats, [start, (phase_owners, phase_castles)],
                    objects=objects, pre_eliminate=losing_colors, report=report,
                )
                assert winners == set(seats.values()) - losing_owners
                assert {item["id"] for item in report["remaining"]} == {
                    item["id"] for item in objects if item["owner"] not in losing_owners
                }
                assert report["victory_snapshots"]
                assert all(
                    item["owner"] not in losing_owners
                    for snapshot in report["victory_snapshots"] for item in snapshot
                ), "victory fired while defeated owners still had objects"


def test_evolution_alpha_cleanup_is_owner_wide_and_inactive_safe(evolution_alpha):
    by_name = {trigger.name: trigger for trigger in evolution_alpha.trigger_manager.triggers}
    for color in range(1, 9):
        for owner in range(1, 9):
            cleanup = by_name[f"Color Elimination Cleanup S{color} W{owner}"]
            complete = by_name[f"Color Cleanup Complete S{color} W{owner}"]
            for trigger in (cleanup, complete):
                assert trigger.enabled and trigger.looping
                assert {
                    (condition.variable, condition.quantity)
                    for condition in trigger.conditions
                    if condition.condition_type == ConditionId.VARIABLE_VALUE
                } == {(39 + color, owner), (120 + color, 1), (47 + color, 1), (56, 1)}
                assert any(c.condition_type == ConditionId.TIMER and c.timer == 1 for c in trigger.conditions)
            for family in ("Color Defeat Resolve", "Color Runtime Defeated", "Color Elimination Cleanup"):
                trigger = by_name[f"{family} S{color} W{owner}"]
                removal, = [e for e in trigger.effects if e.effect_type == EffectId.REMOVE_OBJECT]
                enable, = [e for e in trigger.effects if e.effect_type == EffectId.ENABLE_OBJECT_DELETION]
                assert trigger.effects.index(enable) < trigger.effects.index(removal)
                for effect in (enable, removal):
                    assert effect.source_player == owner
                    assert (
                        effect.area_x1, effect.area_y1, effect.area_x2, effect.area_y2
                    ) == (-1, -1, -1, -1)
                    assert not effect.selected_object_ids and effect.object_list_unit_id == -1
                assert removal.object_type == removal.object_group == removal.object_state == -1
                assert removal.max_units_affected == -1
            empty, = [c for c in complete.conditions if c.condition_type == ConditionId.OWN_FEWER_OBJECTS]
            assert empty.source_player == owner and empty.quantity == 1
            assert empty.object_list == empty.object_type == empty.object_group == -1
            assert (empty.area_x1, empty.area_y1, empty.area_x2, empty.area_y2) == (-1, -1, -1, -1)
            assert [(e.variable, e.quantity) for e in complete.effects] == [(128 + color, 1)]


def test_evolution_alpha_cannot_produce_after_elimination(evolution_alpha):
    checked = 0
    for trigger in evolution_alpha.trigger_manager.triggers:
        if not any(e.effect_type in {
            EffectId.CREATE_OBJECT, EffectId.CREATE_GARRISONED_OBJECT,
            EffectId.TRAIN_UNIT, EffectId.PLACE_FOUNDATION,
        } for e in trigger.effects):
            continue
        active = [
            c for c in trigger.conditions if c.condition_type == ConditionId.VARIABLE_VALUE
            and 32 <= c.variable <= 39 and c.quantity == 1
        ]
        for condition in active:
            assert any(
                c.condition_type == ConditionId.VARIABLE_VALUE and c.variable == condition.variable + 16
                and c.quantity == 0 and c.comparison == Comparison.EQUAL
                for c in trigger.conditions
            ), trigger.name
            checked += 1
    assert checked >= 640  # All milestone/late Heroes and builder producers, plus rewards.
    xs = next(t for t in evolution_alpha.trigger_manager.triggers if t.name == "XS SCRIPT").effects[0].message
    for name in ("cbaSpawnColor", "cbaQueueColorBuilders"):
        body = xs.split(f"void {name}(int scenarioPlayer = 0) {{", 1)[1]
        assert body.lstrip().startswith("if (xsTriggerVariable(48 + scenarioPlayer - 1) == 1) return;")


def test_evolution_alpha_color_active_has_exactly_one_writer(evolution_alpha):
    """Only XS writes p#coloractive; triggers read it and write elimination instead.

    Two writers with different semantics used to agree only by convention: every
    trigger path that cleared the active bit also had to set the elimination bit, or
    XS put the active bit straight back within a second.
    """
    trigger_writes = [
        (trigger.name, effect.variable)
        for trigger in evolution_alpha.trigger_manager.triggers
        for effect in trigger.effects
        if effect.effect_type == EffectId.CHANGE_VARIABLE
        and effect.variable in set(COLOR_ACTIVE_VARIABLES.values())
    ]
    assert trigger_writes == []

    readers = {
        trigger.name
        for trigger in evolution_alpha.trigger_manager.triggers
        for condition in trigger.conditions
        if condition.condition_type == ConditionId.VARIABLE_VALUE
        and condition.variable in set(COLOR_ACTIVE_VARIABLES.values())
    }
    assert len(readers) > 100

    xs_source = next(
        effect.message
        for trigger in evolution_alpha.trigger_manager.triggers
        for effect in trigger.effects
        if effect.effect_type == EffectId.SCRIPT_CALL and effect.message
    )
    assert "void cbaUpdateColorRuntime(int scenarioPlayer = 0)" in xs_source
    assert "gCbaSeenInGameByColor" in xs_source


def _castle_identity_runtime(scenario, owners, in_game):
    """Execute the emitted resolver's small C-like subset with mocked engine reads.

    This tests its actual branch/loop/cache code, not a separately reimplemented
    mapping algorithm. It does NOT emulate DE or prove that engine unit ids survive
    lobby loading. Unknown syntax fails translation rather than being skipped.
    """
    xs = next(t for t in scenario.trigger_manager.triggers if t.name == "XS SCRIPT").effects[0].message
    body = xs.split("int cbaWorldPlayerForColor(int scenarioPlayer = 0) {\n", 1)[1].split("\n}\n", 1)[0]
    lines = ["def resolve(scenarioPlayer=0):"]
    indent = 1
    for raw in body.splitlines():
        line = raw.split("//", 1)[0].strip()
        if not line:
            continue
        if line == "}":
            indent -= 1
            continue
        line = line.replace("||", "or").replace("&&", "and").replace("false", "False")
        if loop := re.fullmatch(r"for \((\w+) = (\d+); (<|<=) (\d+)\) \{", line):
            name, start, operator, stop = loop.groups()
            line = f"for {name} in range({start}, {int(stop) + (operator == '<=')}):"
        elif line.startswith("if ("):
            condition, action = line[4:].rsplit(") ", 1)
            line = f"if {condition}:" + ("" if action == "{" else " " + action.removesuffix(";"))
        else:
            assert line.endswith(";"), line
            line = line.removeprefix("int ").removesuffix(";")
        lines.append("    " * indent + line)
        if line.endswith(":"):
            indent += 1
    assert indent == 1
    refs = [-1] * 32
    for index, reference in re.findall(r"xsArraySetInt\(gCbaCastleRefs, (\d+), (\d+)\);", xs):
        assert refs[int(index)] == -1
        refs[int(index)] = int(reference)
    assert -1 not in refs and len(set(refs)) == 32
    for color in range(1, 9):
        actual = {u.reference_id for u in scenario.unit_manager.units[color] if u.unit_const == 82}
        assert set(refs[(color - 1) * 4:color * 4]) == actual
    cache = [0] * 9
    namespace = {
        "gCbaWorldByColor": cache, "gCbaCastleRefs": refs,
        "xsArrayGetInt": lambda array, index: array[index],
        "xsArraySetInt": lambda array, index, value: array.__setitem__(index, value),
        "xsDoesUnitExist": lambda reference: reference in owners,
        "xsGetUnitOwner": lambda reference: owners[reference],
        "xsGetPlayerInGame": lambda player: player in in_game,
    }
    # No converter or trigger-variable mock: accidentally consulting either fails.
    exec("\n".join(lines), namespace)
    return namespace["resolve"], refs, cache


def test_evolution_alpha_identity_handles_explicitly_closed_slots(evolution_alpha):
    """All nonempty subsets, including P1/P3 versus P5/P6/P7/P8 with P2/P4 closed."""
    for mask in range(1, 256):
        colors = [c for c in range(1, 9) if mask & (1 << (c - 1))]
        # Exercise compacted lobby seats in both ascending and shuffled order.
        for order in (colors, list(reversed(colors))):
            seats = {color: index + 1 for index, color in enumerate(order)}
            owners = {
                u.reference_id: seats[color]
                for color in colors for u in evolution_alpha.unit_manager.units[color]
                if u.unit_const == 82
            }
            resolve, _refs, cache = _castle_identity_runtime(evolution_alpha, owners, set(seats.values()))
            assert {c: resolve(c) for c in range(1, 9)} == {c: seats.get(c, 0) for c in range(1, 9)}
            assert cache[1:] == [seats.get(c, 0) for c in range(1, 9)]
            assert resolve(0) == resolve(9) == 0


def test_evolution_alpha_identity_persists_after_castle_loss_and_resignation(evolution_alpha):
    seats = {1: 2, 3: 1, 5: 4, 6: 3, 7: 6, 8: 5}
    owners = {}
    live = set(seats.values())
    resolve, refs, _cache = _castle_identity_runtime(evolution_alpha, owners, live)
    for color, owner in seats.items():
        # A delayed engine load must be retried, not cached as permanently closed.
        assert resolve(color) == 0
        owners[refs[(color - 1) * 4]] = owner
        assert resolve(color) == owner
    owners.clear()
    live.clear()
    assert {color: resolve(color) for color in seats} == seats


def test_evolution_alpha_identity_refuses_ambiguous_or_inactive_owners(evolution_alpha):
    owners, live = {}, {1, 2, 7, 8}
    resolve, refs, _cache = _castle_identity_runtime(evolution_alpha, owners, live)
    for invalid in (0, -1, 9, 3):
        owners[refs[0]] = invalid
        assert resolve(1) == 0
    owners[refs[0]], owners[refs[1]] = 1, 2
    assert resolve(1) == 0  # mixed ownership must not choose the first Castle
    owners[refs[1]] = 1
    assert resolve(1) == 1
    owners[refs[4]] = 1
    assert resolve(2) == 0  # duplicate territory binding
    owners[refs[24]], owners[refs[28]] = 7, 8
    assert resolve(7) == 7 and resolve(8) == 8  # never bound by a six-player count


def test_evolution_alpha_identity_converter_is_diagnostic_only(evolution_alpha):
    xs = next(t for t in evolution_alpha.trigger_manager.triggers if t.name == "XS SCRIPT").effects[0].message
    resolver = xs.split("int cbaWorldPlayerForColor", 1)[1].split("void cbaCreateWave", 1)[0]
    assert "xsGetWorldPlayerId" not in resolver and "xsTriggerVariable" not in resolver
    diagnostic = xs.split("rule cbaIdentityDiagnostic", 1)[1].split("rule ", 1)[0]
    assert "minInterval 10" in diagnostic and "xsDisableSelf();" in diagnostic
    assert "xsGetWorldPlayerId(scenarioPlayer)" in diagnostic


def test_evolution_alpha_xs_addresses_trigger_variables_through_named_bases(
    evolution_alpha,
):
    """No XS variable access may hard-code a block base as a bare literal.

    The read and the write of the pending-builder variable sat next to each other, one
    using the interpolated base and one using ``scenarioPlayer - 1``. They agreed only
    because that base happens to be zero.
    """
    xs_source = next(
        effect.message
        for trigger in evolution_alpha.trigger_manager.triggers
        for effect in trigger.effects
        if effect.effect_type == EffectId.SCRIPT_CALL and effect.message
    )
    accesses = re.findall(
        r"xs(?:Set)?TriggerVariable\(\s*([^,)]+)",
        xs_source,
    )
    assert accesses
    for expression in accesses:
        expression = " ".join(expression.split())
        if expression.startswith("variableBase"):
            continue
        assert re.fullmatch(r"\d+ \+ scenarioPlayer - 1", expression), expression


def test_evolution_alpha_bans_every_auto_spawned_unique_unit(evolution_alpha):
    """Nobody may hand-train the unit their own Castles already produce for free.

    The ban is derived from CIV_SPAWN_RULES rather than the imported per-colour lists,
    so a civilization added to that table cannot be left trainable by omission.
    """
    build_module = ascendants_build_module()
    banned = set()
    CIV_SPAWN_RULES = build_module.CIV_SPAWN_RULES
    _unit_family = build_module._unit_family
    for unit_id, _cap, _interval in CIV_SPAWN_RULES.values():
        banned |= _unit_family(unit_id)
    assert len(banned) >= len(CIV_SPAWN_RULES)

    for player in range(1, 9):
        disabled = set(evolution_alpha.player_manager.players[player].disabled_units)
        assert banned <= disabled, sorted(banned - disabled)

    # Every Elite unit the mode spawns also has its non-Elite form covered.
    assert UnitInfo.ELITE_HUSKARL_BARRACKS.ID in banned
    assert UnitInfo.HUSKARL_BARRACKS.ID in banned


def test_evolution_alpha_bans_every_castle_class_building(evolution_alpha):
    """Krepost and Donjon are Castles by another name and follow the same rule."""
    castle_class = {
        BuildingInfo.CASTLE.ID,
        BuildingInfo.KREPOST.ID,
        BuildingInfo.DONJON.ID,
    }
    for player in range(1, 9):
        disabled = set(evolution_alpha.player_manager.players[player].disabled_buildings)
        assert castle_class <= disabled, sorted(castle_class - disabled)


def test_evolution_alpha_has_no_imported_language_dependencies(evolution_alpha):
    """The hand-maintained scenario layer no longer carries its source's language."""
    assert ascendants_build_module().HERO_ORDER_FAMILIES == ("Short", "Medium", "Long")
    leftovers = [
        trigger.name
        for trigger in evolution_alpha.trigger_manager.triggers
        if any(word in trigger.name for word in ("Curto", "Médio", "Longo"))
    ]
    assert leftovers == []


def test_evolution_alpha_readme_tracks_the_built_version(repo):
    """The mode README states the version mode.toml actually builds."""
    spec = registry.get("evolution_alpha", repo)
    readme = (repo.modes / "evolution_alpha" / "README.md").read_text(encoding="utf-8")
    assert readme.splitlines()[0] == f"# CBA Hero: Ascendants v{spec.version}"
    assert f"v{spec.version}.aoe2scenario" in readme


def test_ascendants_docs_civilization_table_matches_the_source(repo, evolution_alpha):
    """docs/ascendants-data-tables.md reproduces CIV_SPAWN_RULES row for row.

    The table is the runbook's reference for adding a civilization. A silently stale
    row there is worse than no table: it reads as authoritative.
    """
    build_module = ascendants_build_module()
    doc = (repo.root / "docs" / "ascendants-data-tables.md").read_text(encoding="utf-8")
    documented = {
        int(civilization): (int(unit), int(cap), int(interval), int(threshold))
        for civilization, unit, cap, interval, threshold in re.findall(
            r"^\| (\d+) \| [^|]+ \| [^|]*\((\d+)\) \| (\d+) \| (\d+) \| (\d+) \|$",
            doc,
            re.M,
        )
    }
    expected = {
        civilization: (unit, cap, interval, build_module.CIV_BUILDER_RULES[civilization][1])
        for civilization, (unit, cap, interval) in build_module.CIV_SPAWN_RULES.items()
    }
    assert documented == expected


def test_ascendants_docs_variable_registry_matches_the_source(repo, evolution_alpha):
    """Every variable block in the docs has the base id build.py actually uses."""
    build_module = ascendants_build_module()
    doc = (repo.root / "docs" / "ascendants-data-tables.md").read_text(encoding="utf-8")
    rows = re.findall(r"^\| (\d+)(?:–(\d+))? \| `([A-Z_]+)`", doc, re.M)
    documented_bases = {constant: int(first) for first, _last, constant in rows}
    expected_bases = {
        name: getattr(build_module, name)
        for name in dir(build_module)
        if name.endswith(("_VARIABLE_BASE", "_VARIABLE_ID"))
    }
    assert documented_bases == expected_bases

    # The documented ranges must also account for every serialized variable, so a new
    # block cannot be added to build.py and left out of the registry.
    documented_ids = {
        variable_id
        for first, last, _constant in rows
        for variable_id in range(int(first), int(last or first) + 1)
    }
    assert documented_ids == {
        variable.variable_id
        for variable in evolution_alpha.trigger_manager.variables
    }
