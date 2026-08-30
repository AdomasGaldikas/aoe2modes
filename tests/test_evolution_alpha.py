"""Regression checks for CBA Hero: Ascendants gameplay systems."""

from __future__ import annotations

import hashlib
import json
import re
from collections import Counter, deque

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


VALID_COLOR_WORLD_PAIRS = {
    (color, world_player)
    for color in range(1, 9)
    for world_player in range(1, color + 1)
}


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
    assert len(triggers) == 2_291
    assert sum(len(units) for units in evolution_alpha.unit_manager.units) == 1_076
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
        "a5fea90f87225aad16d1096ea88996cf5a97cac9d2162668f880ab2c27fa1ce6"
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
    assert not {
        evolution_alpha.map_manager.get_tile(x=x, y=y).terrain_id
        for y in range(144)
        for x in range(144)
    } & winter_terrains

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

    assert len(original) == 992
    assert original_digest == (
        "253ac71abcdab09f490905f74bbf03f6f10230312551f1425fe12f15799e5b5e"
    )
    assert len(additions) == 84
    assert additions_digest == (
        "37797678d99545b5ff07adb9e987ea50a7768dabf269a3b01c79ca3fb3df4cb3"
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
        for world_player in range(1, int(player) + 1):
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
        for world_player in range(1, int(player) + 1):
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


def test_evolution_alpha_aligns_edge_selector_props_to_ground(evolution_alpha):
    source_slots = {
        OtherInfo.RELIC.ID: {
            (1.5, 61.5),
            (1.5, 63.5),
            (1.5, 65.5),
            (7.5, 61.5),
            (7.5, 65.5),
        },
        OtherInfo.RUGS.ID: {
            (2.5, 61.5),
            (2.5, 63.5),
            (2.5, 65.5),
            (6.5, 61.5),
            (6.5, 65.5),
        },
    }
    gaia_units = evolution_alpha.unit_manager.units[PlayerId.GAIA]
    for unit_const, source_positions in source_slots.items():
        expected = {
            v2_position_for_player(player, x, y)
            for player in PlayerId.all(exclude_gaia=True)
            for x, y in source_positions
        }
        actual = {
            (unit.x, unit.y)
            for unit in gaia_units
            if unit.unit_const == unit_const
        }
        assert actual == expected

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
        if trigger.name != "==Rename======":
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


def test_evolution_alpha_keeps_visible_land_objects_out_of_water(evolution_alpha):
    water = {int(terrain) for terrain in TerrainId.water_terrains()}
    intentional_submerged = {
        BuildingInfo.PALISADE_WALL.ID,
        HeroInfo.SABOTEUR.ID,
    }
    submerged = [
        unit
        for units in evolution_alpha.unit_manager.units
        for unit in units
        if evolution_alpha.map_manager.get_tile(
            x=int(unit.x),
            y=int(unit.y),
        ).terrain_id in water
    ]
    assert Counter(unit.unit_const for unit in submerged) == Counter(
        {
            BuildingInfo.PALISADE_WALL.ID: 56,
            HeroInfo.SABOTEUR.ID: 8,
        }
    )
    assert all(unit.unit_const in intentional_submerged for unit in submerged)
    assert all(
        unit.unit_const != OtherInfo.ICE_NAVIGABLE.ID
        for units in evolution_alpha.unit_manager.units
        for unit in units
    )


def test_evolution_alpha_has_no_transport_ship_spawn_markers(evolution_alpha):
    assert all(
        unit.unit_const != UnitInfo.TRANSPORT_SHIP.ID
        for units in evolution_alpha.unit_manager.units
        for unit in units
    )


def test_evolution_alpha_distance_movers_are_mobile_and_use_all_five_selectors(
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
        EffectId.DISABLE_OBJECT_SELECTION,
        EffectId.FREEZE_OBJECT,
        EffectId.STOP_OBJECT,
    }
    source_selector_areas = (
        (1, 60, 3, 62),
        (1, 63, 3, 63),
        (1, 64, 3, 66),
        (4, 64, 8, 66),
        (4, 60, 8, 62),
    )

    for player in PlayerId.all(exclude_gaia=True):
        suffix = "" if player == PlayerId.ONE else f" (p{int(player)})"
        selector_names = (
            f"short (p{int(player)})",
            f"med (p{int(player)})",
            f"long (p{int(player)})",
            f"herospawnclose{suffix}",
            f"herospawnopen{suffix}",
        )
        selector_conditions = [
            condition
            for name in selector_names
            for condition in by_name[name].conditions
            if condition.condition_type == ConditionId.BRING_OBJECT_TO_AREA
        ]
        assert len(selector_conditions) == 5
        assert len({condition.unit_object for condition in selector_conditions}) == 1
        reference_id = selector_conditions[0].unit_object
        mover = unit_by_reference[reference_id]
        assert mover.player == player
        assert mover.unit_const == UnitInfo.SHEEP.ID
        assert evolution_alpha.map_manager.get_tile(
            x=int(mover.x),
            y=int(mover.y),
        ).terrain_id not in water
        assert len(
            {
                (
                    condition.area_x1,
                    condition.area_y1,
                    condition.area_x2,
                    condition.area_y2,
                )
                for condition in selector_conditions
            }
        ) == 5
        expected_areas = []
        for source_x1, source_y1, source_x2, source_y2 in source_selector_areas:
            corners = (
                v2_cell_for_player(player, source_x1, source_y1),
                v2_cell_for_player(player, source_x1, source_y2),
                v2_cell_for_player(player, source_x2, source_y1),
                v2_cell_for_player(player, source_x2, source_y2),
            )
            expected_areas.append(
                (
                    min(x for x, _y in corners),
                    min(y for _x, y in corners),
                    max(x for x, _y in corners),
                    max(y for _x, y in corners),
                )
            )
        assert [
            (
                condition.area_x1,
                condition.area_y1,
                condition.area_x2,
                condition.area_y2,
            )
            for condition in selector_conditions
        ] == expected_areas
        route_cells = [
            {
                (x, y)
                for x in range(condition.area_x1, condition.area_x2 + 1)
                for y in range(condition.area_y1, condition.area_y2 + 1)
            }
            for condition in selector_conditions[:3]
        ]
        assert [len(cells) for cells in route_cells] == [9, 3, 9]
        assert len(set().union(*route_cells)) == sum(map(len, route_cells))
        spawn_cells = [
            {
                (x, y)
                for x in range(condition.area_x1, condition.area_x2 + 1)
                for y in range(condition.area_y1, condition.area_y2 + 1)
            }
            for condition in selector_conditions[3:]
        ]
        assert [len(cells) for cells in spawn_cells] == [15, 15]
        assert spawn_cells[0].isdisjoint(spawn_cells[1])
        all_control_cells = route_cells + spawn_cells
        assert len(set().union(*all_control_cells)) == sum(
            map(len, all_control_cells)
        )
        mover_cell = (int(mover.x), int(mover.y))
        assert mover_cell not in set().union(*route_cells)
        assert mover_cell not in spawn_cells[0] | spawn_cells[1]

        protections = {
            effect.effect_type
            for effect in by_name[f"Antidelete P{int(player)}"].effects
            if reference_id in effect.selected_object_ids
        }
        assert protections == {EffectId.DISABLE_OBJECT_DELETION}
        conflicts = [
            (trigger.name, effect.effect_type)
            for trigger in evolution_alpha.trigger_manager.triggers
            for effect in trigger.effects
            if reference_id in effect.selected_object_ids
            and effect.effect_type in forbidden_effects
        ]
        assert not conflicts

        close_trigger = by_name[f"herospawnclose{suffix}"]
        open_trigger = by_name[f"herospawnopen{suffix}"]
        blocker_x, blocker_y = v2_cell_for_player(player, 16, 38)
        close_creates = [
            effect
            for effect in close_trigger.effects
            if effect.effect_type == EffectId.CREATE_OBJECT
            and effect.object_list_unit_id == OtherInfo.OLD_STONE_HEAD.ID
        ]
        assert len(close_creates) == 1
        assert (
            close_creates[0].source_player,
            close_creates[0].location_x,
            close_creates[0].location_y,
        ) == (PlayerId.GAIA, blocker_x, blocker_y)
        close_blocker_conditions = [
            condition
            for condition in close_trigger.conditions
            if condition.condition_type == ConditionId.OBJECTS_IN_AREA
            and condition.object_list == OtherInfo.OLD_STONE_HEAD.ID
        ]
        assert len(close_blocker_conditions) == 1
        assert close_blocker_conditions[0].inverted
        assert not any(
            effect.effect_type == EffectId.TASK_OBJECT
            and reference_id in effect.selected_object_ids
            for effect in open_trigger.effects
        )
        blocker_conditions = [
            condition
            for condition in open_trigger.conditions
            if condition.condition_type == ConditionId.OBJECTS_IN_AREA
            and condition.object_list == OtherInfo.OLD_STONE_HEAD.ID
        ]
        assert len(blocker_conditions) == 1
        assert not blocker_conditions[0].inverted
        open_removals = [
            effect
            for effect in open_trigger.effects
            if effect.effect_type == EffectId.REMOVE_OBJECT
            and effect.object_list_unit_id == OtherInfo.OLD_STONE_HEAD.ID
        ]
        assert len(open_removals) == 1
        assert (
            open_removals[0].area_x1,
            open_removals[0].area_y1,
            open_removals[0].area_x2,
            open_removals[0].area_y2,
        ) == (blocker_x, blocker_y, blocker_x, blocker_y)


def test_evolution_alpha_protects_all_added_v2_walls(evolution_alpha):
    expected_counts = {
        PlayerId.ONE: 14,
        PlayerId.TWO: 14,
        PlayerId.THREE: 8,
        PlayerId.FOUR: 8,
        PlayerId.FIVE: 8,
        PlayerId.SIX: 8,
        PlayerId.SEVEN: 12,
        PlayerId.EIGHT: 12,
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
        for family in ("remove", "units", "walls", "units2", "units3")
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
        (88 + player, f"army_route_p{player}")
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
    assert "xsGetWorldPlayerId(" not in xs_source
    assert "return(xsTriggerVariable(" in xs_source
    assert "40 + scenarioPlayer - 1" in xs_source
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
    assert len(occupied) == 36
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
    sparse = {trigger.name: trigger for trigger in triggers if trigger.name.startswith("Sparse Feudal S")}
    assert len(sparse) == 28
    assert {
        tuple(map(int, re.fullmatch(r"Sparse Feudal S([1-8]) W([1-8])", name).groups()))
        for name in sparse
    } == VALID_COLOR_WORLD_PAIRS - {(color, color) for color in range(1, 9)}

    teal_for_compacted_p2 = sparse["Sparse Feudal S5 W2"]
    blacksmith = next(
        condition
        for condition in teal_for_compacted_p2.conditions
        if condition.condition_type == ConditionId.OBJECTS_IN_AREA
    )
    assert blacksmith.source_player == PlayerId.TWO
    assert blacksmith.object_list == BuildingInfo.BLACKSMITH.ID
    assert (blacksmith.area_x1, blacksmith.area_y1, blacksmith.area_x2, blacksmith.area_y2) == (
        1,
        85,
        6,
        93,
    )
    assert {
        (effect.source_player, effect.technology)
        for effect in teal_for_compacted_p2.effects
        if effect.effect_type == EffectId.RESEARCH_TECHNOLOGY
    } == {(PlayerId.TWO, technology) for technology in (211, 199, 67, 81, 74, 1036, 1115, 1125)}


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
            remove = next(
                effect
                for effect in trigger.effects
                if effect.effect_type == EffectId.REMOVE_OBJECT
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
                remove.source_player,
                remove.object_group,
                remove.area_x1,
                remove.area_y1,
                remove.area_x2,
                remove.area_y2,
            ) == (world_player, ObjectClass.PACKED_UNIT, *marker, *marker)
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


def test_evolution_alpha_maps_goth_rules_to_runtime_players(evolution_alpha):
    triggers = evolution_alpha.trigger_manager.triggers
    palisade_pattern = re.compile(r"Goth Palisade Bonus S([1-8]) W([1-8])")
    palisades = {
        tuple(map(int, match.groups())): trigger
        for trigger in triggers
        if (match := palisade_pattern.fullmatch(trigger.name))
    }
    assert set(palisades) == VALID_COLOR_WORLD_PAIRS
    occupied = {
        (int(unit.x), int(unit.y))
        for units in evolution_alpha.unit_manager.units
        for unit in units
    }
    for (color, world_player), trigger in palisades.items():
        x1, y1 = v2_cell_for_player(color, 24, 48)
        x2, y2 = v2_cell_for_player(color, 24, 59)
        area = (min(x1, x2), min(y1, y2), max(x1, x2), max(y1, y2))
        row = {
            (x, y)
            for x in range(area[0], area[2] + 1)
            for y in range(area[1], area[3] + 1)
        }
        assert len(row) == 12
        assert all(
            evolution_alpha.map_manager.get_tile(x=x, y=y).terrain_id
            == TerrainId.GRASS_2
            for x, y in row
        )
        assert row.isdisjoint(occupied)
        wall = next(
            condition
            for condition in trigger.conditions
            if condition.condition_type == ConditionId.OBJECTS_IN_AREA
        )
        tech = next(
            condition
            for condition in trigger.conditions
            if condition.condition_type == ConditionId.RESEARCH_TECHNOLOGY
        )
        assert (
            wall.quantity,
            wall.object_list,
            wall.source_player,
            wall.area_x1,
            wall.area_y1,
            wall.area_x2,
            wall.area_y2,
        ) == (12, BuildingInfo.PALISADE_WALL.ID, world_player, *area)
        assert (tech.source_player, tech.technology) == (
            world_player,
            TechInfo.ELITE_HUSKARL.ID,
        )
        assert {
            (condition.variable, condition.quantity, condition.comparison)
            for condition in trigger.conditions
            if condition.condition_type == ConditionId.VARIABLE_VALUE
        } == {
            (31 + color, 1, Comparison.EQUAL),
            (39 + color, world_player, Comparison.EQUAL),
        }
        hp = next(
            effect
            for effect in trigger.effects
            if effect.effect_type == EffectId.CHANGE_OBJECT_HP
        )
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
            BuildingInfo.PALISADE_WALL.ID,
            2750,
            Operation.ADD,
            *area,
        )

    legacy_palisades = [
        trigger
        for trigger in triggers
        if trigger.name.startswith("Legacy Goth Palisade Bonus Disabled #")
    ]
    assert legacy_palisades == []

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

    areas = {
        1: (48, 19, 60, 19),
        2: (84, 19, 96, 19),
        3: (19, 48, 19, 60),
        4: (125, 48, 125, 60),
        5: (19, 84, 19, 96),
        6: (125, 84, 125, 96),
        7: (48, 125, 60, 125),
        8: (84, 125, 96, 125),
    }
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

        for world_player in range(1, color + 1):
            reward = rewards[f"Builder Reward S{color} W{world_player}"]
            assert reward.enabled and reward.looping
            assert len(reward.conditions) == 5

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
            assert len(variable_effects) == 1
            consume_pending = variable_effects[0]
            assert (
                consume_pending.variable,
                consume_pending.operation,
                consume_pending.quantity,
            ) == (color - 1, Operation.SUBTRACT, 1)

            mover = movers[f"Builder Move S{color} W{world_player}"]
            assert mover.enabled and mover.looping
            assert any(
                condition.condition_type == ConditionId.TIMER
                and condition.timer == 1
                for condition in mover.conditions
            )
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

    xs_trigger = next(trigger for trigger in triggers if trigger.name == "XS SCRIPT")
    xs_source = xs_trigger.effects[0].message
    assert "int currentRazings = xsCeilToInt(xsPlayerAttribute(" in xs_source
    assert "int earnedPairs = currentRazings - threshold + 1;" in xs_source
    assert "int pendingPairs = xsTriggerVariable(scenarioPlayer - 1);" in xs_source
    assert "pendingPairs + earnedPairs - previousEarnedPairs" in xs_source
    assert "xsArraySetInt(gCbaBuilderThresholdByCiv, 8, 4);" in xs_source
    assert 'xsArraySetString(gCbaNameByCiv, 8, "Persians");' in xs_source
    assert "xsGetLocalPlayerId()" in xs_source
    assert "xsGetPlayerCivilization(localPlayer)" in xs_source
    assert "first builder pair after" in xs_source
    assert "if (xsGetGameTime() >= 4)" in xs_source
    assert xs_source.count("xsChatData(") == 1
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
    assert all(len(ids) == target for target, ids in resolver_ids_by_target.items())

    castle_areas = {
        1: (48, 19, 60, 19),
        2: (84, 19, 96, 19),
        3: (19, 48, 19, 60),
        4: (125, 48, 125, 60),
        5: (19, 84, 19, 96),
        6: (125, 84, 125, 96),
        7: (48, 125, 60, 125),
        8: (84, 125, 96, 125),
    }
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
    assert len(marker_detectors) == sum(voter for _target, voter in vote_keys) == 108
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
        assert 1 <= world_player <= voter
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
        ) == (0, 0, 143, 143)
        assert len(clears) == 2
        assert chats[0].source_player == -1
        assert "vote-kicked" in chats[0].message
        assert {
            (effect.variable, effect.quantity, effect.operation)
            for effect in clears
        } == {
            (31 + target, 0, Operation.SET),
            (47 + target, 1, Operation.SET),
        }
        assert defeats[0].source_player == world_player
        assert not defeats[0].enabled

    xs_trigger = next(trigger for trigger in triggers if trigger.name == "XS SCRIPT")
    xs_source = xs_trigger.effects[0].message
    assert "void cbaUpdateColorRuntime(int scenarioPlayer = 0)" in xs_source
    assert "xsGetWorldPlayerId(" not in xs_source
    assert "int worldPlayer = cbaWorldPlayerForColor(scenarioPlayer);" in xs_source
    assert "rule cbaColorRuntimeState" in xs_source
    assert xs_source.count("cbaUpdateColorRuntime(") == 9
    assert "40 + scenarioPlayer - 1" in xs_source
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
    castle_areas = {
        1: (48, 19, 60, 19),
        2: (84, 19, 96, 19),
        3: (19, 48, 19, 60),
        4: (125, 48, 125, 60),
        5: (19, 84, 19, 96),
        6: (125, 84, 125, 96),
        7: (48, 125, 60, 125),
        8: (84, 125, 96, 125),
    }
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
        assert {
            (effect.variable, effect.quantity, effect.operation)
            for effect in variables
        } == {
            (39 + color, world_player, Operation.SET),
            (31 + color, 1, Operation.SET),
        }
        deactivations = [
            effect
            for effect in detector.effects
            if effect.effect_type == EffectId.DEACTIVATE_TRIGGER
        ]
        assert len(deactivations) == 1
        assert deactivations[0].trigger_id == detector.trigger_id


def test_evolution_alpha_removes_invisible_edge_deletion_strips(evolution_alpha):
    disabled = [
        trigger
        for trigger in evolution_alpha.trigger_manager.triggers
        if trigger.name.startswith("Legacy Edge Delete Disabled (uk")
    ]
    assert disabled == []


def test_evolution_alpha_keeps_legacy_cleanup_off_rear_routes(evolution_alpha):
    anti_treb_bounds = {
        1: (39, 19, 66, 25),
        2: (75, 19, 102, 26),
        3: (18, 38, 25, 64),
        4: (114, 38, 123, 65),
        5: (18, 74, 24, 101),
        6: (114, 74, 123, 101),
        7: (39, 116, 66, 123),
        8: (74, 116, 102, 123),
    }
    triggers = evolution_alpha.trigger_manager.triggers
    for base_player, bounds in anti_treb_bounds.items():
        matches = [
            trigger
            for trigger in triggers
            if trigger.name == f"No trebs in p{base_player} base"
            or trigger.name.startswith(f"No trebs in p{base_player} base (p")
        ]
        assert len(matches) == 8
        for trigger in matches:
            effects = [effect for effect in trigger.effects if effect.effect_type == EffectId.KILL_OBJECT]
            assert len(effects) == 1
            effect = effects[0]
            assert (effect.area_x1, effect.area_y1, effect.area_x2, effect.area_y2) == bounds

    wall_cleanup_bounds = {
        1: (43, 17, 64, 38),
        2: (79, 17, 100, 38),
        3: (17, 43, 38, 64),
        4: (105, 43, 126, 64),
        5: (17, 79, 38, 100),
        6: (105, 79, 126, 100),
        7: (43, 105, 64, 126),
        8: (79, 105, 100, 126),
    }
    wall_pattern = re.compile(r"Wall Breach S([1-8]) W([1-8])")
    wall_breaches = {
        tuple(map(int, match.groups())): trigger
        for trigger in triggers
        if (match := wall_pattern.fullmatch(trigger.name))
    }
    assert set(wall_breaches) == VALID_COLOR_WORLD_PAIRS
    for player, bounds in wall_cleanup_bounds.items():
        for world_player in range(1, player + 1):
            trigger = wall_breaches[player, world_player]
            effects = [
                effect
                for effect in trigger.effects
                if effect.effect_type == EffectId.REMOVE_OBJECT
            ]
            assert len(effects) == 2
            assert {
                (effect.area_x1, effect.area_y1, effect.area_x2, effect.area_y2)
                for effect in effects
            } == {bounds}
            assert {effect.source_player for effect in effects} == {world_player}
            gate_condition = next(
                condition
                for condition in trigger.conditions
                if condition.condition_type == ConditionId.DESTROY_OBJECT
            )
            gate = next(
                unit
                for units in evolution_alpha.unit_manager.units
                for unit in units
                if unit.reference_id == gate_condition.unit_object
            )
            x1, y1, x2, y2 = bounds
            assert x1 <= int(gate.x) <= x2
            assert y1 <= int(gate.y) <= y2
            assert {
                (condition.variable, condition.quantity, condition.comparison)
                for condition in trigger.conditions
                if condition.condition_type == ConditionId.VARIABLE_VALUE
            } == {
                (31 + player, 1, Comparison.EQUAL),
                (39 + player, world_player, Comparison.EQUAL),
            }


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
        assert not trigger.enabled
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
            (31 + color, 1),
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
            (31 + color, 0, Operation.SET),
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
        ) == (0, 0, 143, 143)

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
        assert len(variables) == 2
        assert len(defeated) == 1
        assert {
            (condition.variable, condition.quantity) for condition in variables
        } == {
            (39 + color, world_player),
            (56, 1),
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
            (31 + color, 0, Operation.SET),
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
        ) == (0, 0, 143, 143)

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

    victory_effects = []
    for trigger in victory_triggers:
        color, world_player = map(int, victory_pattern.fullmatch(trigger.name).groups())
        opponents = set(range(5, 9) if color <= 4 else range(1, 5))
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
        assert len(variables) == 7
        assert all(condition.comparison == Comparison.EQUAL for condition in variables)
        assert {(condition.variable, condition.quantity) for condition in variables} == {
            (31 + color, 1),
            (39 + color, world_player),
            (56, 1),
            *((31 + opponent, 0) for opponent in opponents),
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

    def runtime_variables(occupied_colors, alive_colors=None, match_ready=None):
        if alive_colors is None:
            alive_colors = occupied_colors
        mapping = {
            color: world_player
            for world_player, color in enumerate(sorted(occupied_colors), start=1)
        }
        values = {}
        for color in range(1, 9):
            values[31 + color] = int(color in alive_colors)
            values[39 + color] = mapping.get(color, 0)
            values[47 + color] = int(color in mapping and color not in alive_colors)
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

    full_colors = set(range(1, 9))
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
                    for color in alive
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
    assert "xsGetWorldPlayerId(" not in xs_source
    assert "int worldPlayer = cbaWorldPlayerForColor(scenarioPlayer);" in xs_source
    assert "xsGetPlayerCivilization(worldPlayer)" in xs_source
    assert "xsPlayerAttribute(worldPlayer, cAttributeMilitaryPopulation)" in xs_source
    assert xs_source.count("81 + scenarioPlayer - 1") == 1
    assert xs_source.count("xsArraySetInt(gCbaUnitByCiv") == 59
    assert xs_source.count("cbaSpawnColor(") == 9  # declaration plus all eight colors
    assert "vector(22, 96, -1)" in xs_source
    assert "vector(22, 85, -1)" in xs_source

    movements = {
        trigger.name: trigger
        for trigger in triggers
        if trigger.name.startswith("Sparse Move S")
        and not trigger.name.startswith(("Sparse Move Short S", "Sparse Move Long S"))
    }
    short_movements = {
        trigger.name: trigger
        for trigger in triggers
        if trigger.name.startswith("Sparse Move Short S")
    }
    long_movements = {
        trigger.name: trigger
        for trigger in triggers
        if trigger.name.startswith("Sparse Move Long S")
    }
    assert len(movements) == 28
    assert len(short_movements) == 28
    assert len(long_movements) == 28
    assert all(trigger.enabled for trigger in movements.values())
    assert all(trigger.enabled for trigger in short_movements.values())
    assert all(trigger.enabled for trigger in long_movements.values())
    teal_for_compacted_p2 = movements["Sparse Move S5 W2"]
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
    assert (owner.area_x1, owner.area_y1, owner.area_x2, owner.area_y2) == (19, 84, 19, 96)

    tasks = [effect for effect in teal_for_compacted_p2.effects if effect.effect_type == EffectId.TASK_OBJECT]
    assert len(tasks) == 4
    assert {effect.source_player for effect in tasks} == {PlayerId.TWO}
    assert {effect.action_type for effect in tasks} == {ActionType.MOVE}
    assert {
        (effect.area_x1, effect.area_y1, effect.area_x2, effect.area_y2)
        for effect in tasks
    } == {
        (21, 95, 23, 97),
        (21, 91, 23, 93),
        (21, 88, 23, 90),
        (21, 84, 23, 86),
    }

    spawn_points = {
        1: ((48, 22), (52, 22), (55, 22), (59, 22)),
        2: ((96, 22), (92, 22), (89, 22), (85, 22)),
        3: ((22, 48), (22, 52), (22, 55), (22, 59)),
        4: ((122, 48), (122, 52), (122, 55), (122, 59)),
        5: ((22, 96), (22, 92), (22, 89), (22, 85)),
        6: ((122, 96), (122, 92), (122, 89), (122, 85)),
        7: ((48, 122), (52, 122), (55, 122), (59, 122)),
        8: ((96, 122), (92, 122), (89, 122), (85, 122)),
    }
    by_name = {trigger.name: trigger for trigger in triggers}
    canonical_task_locations = {
        family: [
            (effect.location_x, effect.location_y)
            for effect in by_name[f"{family} (p3)"].effects
            if effect.effect_type == EffectId.TASK_OBJECT
        ]
        for family in ("move", "move short", "move long")
    }
    route_values = {
        "move": 0,
        "move short": 1,
        "move long": 2,
    }
    for scenario_player, expected in spawn_points.items():
        original_tasks = [
            effect
            for effect in by_name[f"move (p{scenario_player})"].effects
            if effect.effect_type == EffectId.TASK_OBJECT
        ]
        assert [
            (effect.area_x1, effect.area_y1, effect.area_x2, effect.area_y2)
            for effect in original_tasks
        ] == [(x - 1, y - 1, x + 1, y + 1) for x, y in expected]
        assert {effect.action_type for effect in original_tasks} == {
            ActionType.MOVE
        }
        for world_player in range(1, scenario_player):
            for public_family in ("", " Short", " Long"):
                sparse_tasks = [
                    effect
                    for effect in by_name[
                        f"Sparse Move{public_family} S{scenario_player} "
                        f"W{world_player}"
                    ].effects
                    if effect.effect_type == EffectId.TASK_OBJECT
                ]
                assert [
                    (
                        effect.area_x1,
                        effect.area_y1,
                        effect.area_x2,
                        effect.area_y2,
                    )
                    for effect in sparse_tasks
                ] == [(x - 1, y - 1, x + 1, y + 1) for x, y in expected]
                assert {effect.action_type for effect in sparse_tasks} == {
                    ActionType.MOVE
                }
        for family, source_locations in canonical_task_locations.items():
            target = by_name[f"{family} (p{scenario_player})"]
            target_tasks = [
                effect
                for effect in target.effects
                if effect.effect_type == EffectId.TASK_OBJECT
            ]
            assert [
                (effect.area_x1, effect.area_y1, effect.area_x2, effect.area_y2)
                for effect in target_tasks
            ] == [(x - 1, y - 1, x + 1, y + 1) for x, y in expected]
            assert [
                (effect.location_x, effect.location_y)
                for effect in target_tasks
            ] == [
                v2_cell_for_player(scenario_player, x, y)
                for x, y in source_locations
            ]
            assert {effect.action_type for effect in target_tasks} == {
                ActionType.MOVE
            }

            expected_variable_conditions = {
                (80 + scenario_player, 1),
                (31 + scenario_player, 1),
                (39 + scenario_player, scenario_player),
                (88 + scenario_player, route_values[family]),
            }
            assert target.enabled
            assert {
                (condition.variable, condition.quantity)
                for condition in target.conditions
                if condition.condition_type == ConditionId.VARIABLE_VALUE
            } == expected_variable_conditions
            pending_resets = [
                effect
                for effect in target.effects
                if effect.effect_type == EffectId.CHANGE_VARIABLE
                and effect.variable == 80 + scenario_player
            ]
            assert len(pending_resets) == 1
            assert (
                pending_resets[0].operation,
                pending_resets[0].quantity,
            ) == (Operation.SET, 0)

        public_families = {
            "": "move",
            " Short": "move short",
            " Long": "move long",
        }
        for world_player in range(1, scenario_player):
            for public_family, family in public_families.items():
                movement = by_name[
                    f"Sparse Move{public_family} S{scenario_player} W{world_player}"
                ]
                assert movement.enabled
                assert {
                    (condition.variable, condition.quantity)
                    for condition in movement.conditions
                    if condition.condition_type == ConditionId.VARIABLE_VALUE
                } == {
                    (80 + scenario_player, 1),
                    (31 + scenario_player, 1),
                    (39 + scenario_player, world_player),
                    (88 + scenario_player, route_values[family]),
                }
                pending_resets = [
                    effect
                    for effect in movement.effects
                    if effect.effect_type == EffectId.CHANGE_VARIABLE
                    and effect.variable == 80 + scenario_player
                ]
                assert len(pending_resets) == 1
                assert (
                    pending_resets[0].operation,
                    pending_resets[0].quantity,
                ) == (Operation.SET, 0)

        selectors = {
            "short": 1,
            "med": 0,
            "long": 2,
        }
        route_trigger_ids = {
            by_name[f"{family} (p{scenario_player})"].trigger_id
            for family in route_values
        } | {
            by_name[
                f"Sparse Move{public_family} S{scenario_player} W{world_player}"
            ].trigger_id
            for world_player in range(1, scenario_player)
            for public_family in public_families
        }
        for selector_name, route_value in selectors.items():
            selector = by_name[f"{selector_name} (p{scenario_player})"]
            assert not any(
                effect.effect_type
                in {EffectId.ACTIVATE_TRIGGER, EffectId.DEACTIVATE_TRIGGER}
                and effect.trigger_id in route_trigger_ids
                for effect in selector.effects
            )
            route_changes = [
                effect
                for effect in selector.effects
                if effect.effect_type == EffectId.CHANGE_VARIABLE
                and effect.variable == 88 + scenario_player
            ]
            assert len(route_changes) == 1
            assert (
                route_changes[0].operation,
                route_changes[0].quantity,
            ) == (Operation.SET, route_value)


def test_evolution_alpha_hero_milestones_work_for_every_color_and_runtime_owner(
    evolution_alpha,
):
    triggers = evolution_alpha.trigger_manager.triggers
    milestone_pattern = re.compile(
        r"Hero Milestone S([1-8]) W([1-8]) K(200|400|600|800|1000|2000)"
    )
    order_pattern = re.compile(
        r"Hero Orders (Short|Medium|Long) S([1-8]) W([1-8])"
    )
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
    previous_threshold = {}
    for color in range(1, 9):
        spawn = v2_cell_for_player(color, 16, 38)
        tile = evolution_alpha.map_manager.get_tile(x=spawn[0], y=spawn[1])
        assert tile.terrain_id == TerrainId.GRASS_2
        assert spawn not in occupied_tiles
        for world_player in range(1, color + 1):
            for threshold, unit_id in milestone_units.items():
                trigger = milestone_triggers[color, world_player, threshold]
                assert trigger.enabled and trigger.looping

                kill_conditions = [
                    condition
                    for condition in trigger.conditions
                    if condition.condition_type == ConditionId.ACCUMULATE_ATTRIBUTE
                    and condition.attribute == Attribute.UNITS_KILLED
                ]
                assert len(kill_conditions) == 1
                assert (
                    kill_conditions[0].source_player,
                    kill_conditions[0].quantity,
                ) == (world_player, threshold)
                assert any(
                    condition.condition_type == ConditionId.OWN_FEWER_OBJECTS
                    and condition.source_player == world_player
                    and condition.quantity == 250
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

                deactivations = [
                    effect
                    for effect in trigger.effects
                    if effect.effect_type == EffectId.DEACTIVATE_TRIGGER
                ]
                previous = previous_threshold.get((color, world_player))
                if previous is None:
                    assert not deactivations
                else:
                    assert len(deactivations) == 1
                    assert deactivations[0].trigger_id == milestone_triggers[
                        color,
                        world_player,
                        previous,
                    ].trigger_id
                previous_threshold[color, world_player] = threshold

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
        "Short": (1, (25, 54)),
        "Medium": (0, (31, 52)),
        "Long": (2, (43, 53)),
    }
    order_triggers = {
        (match.group(1), int(match.group(2)), int(match.group(3))): trigger
        for trigger in triggers
        if (match := order_pattern.fullmatch(trigger.name))
    }
    assert len(order_triggers) == len(canonical_orders) * len(
        VALID_COLOR_WORLD_PAIRS
    )
    assert not any(
        trigger.name.startswith("Hero Orders Open ")
        for trigger in triggers
    )
    for family, (route_value, source_destination) in canonical_orders.items():
        for color in range(1, 9):
            spawn_x, spawn_y = v2_cell_for_player(color, 16, 38)
            destination = v2_cell_for_player(color, *source_destination)
            for world_player in range(1, color + 1):
                trigger = order_triggers[family, color, world_player]
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
                    (88 + color, route_value, Comparison.EQUAL),
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


def test_evolution_alpha_remaps_location_sensitive_triggers_to_v2(evolution_alpha):
    by_name = {
        trigger.name: trigger
        for trigger in evolution_alpha.trigger_manager.triggers
    }

    def transformed_area(player, component):
        if min(
            component.area_x1,
            component.area_y1,
            component.area_x2,
            component.area_y2,
        ) < 0:
            return None
        corners = (
            v2_cell_for_player(player, component.area_x1, component.area_y1),
            v2_cell_for_player(player, component.area_x1, component.area_y2),
            v2_cell_for_player(player, component.area_x2, component.area_y1),
            v2_cell_for_player(player, component.area_x2, component.area_y2),
        )
        return (
            min(x for x, _y in corners),
            min(y for _x, y in corners),
            max(x for x, _y in corners),
            max(y for _x, y in corners),
        )

    families = {
        family: {
            player: f"{family} (p{player})"
            for player in range(1, 9)
        }
        for family in ("short", "med", "long")
    }
    families.update(
        {
            family: {
                player: family if player == 1 else f"{family} (p{player})"
                for player in range(1, 9)
            }
            for family in ("herospawnclose", "herospawnopen")
        }
    )
    for family, names in families.items():
        source = by_name[names[3]]
        for player, name in names.items():
            target = by_name[name]
            source_components = list(source.conditions)
            target_components = list(target.conditions)
            if family.startswith("hero"):
                source_components.extend(source.effects)
                target_components.extend(target.effects)
            assert [
                getattr(component, "condition_type", None)
                for component in target_components
            ] == [
                getattr(component, "condition_type", None)
                for component in source_components
            ]
            assert [
                getattr(component, "effect_type", None)
                for component in target_components
            ] == [
                getattr(component, "effect_type", None)
                for component in source_components
            ]
            for source_component, target_component in zip(
                source_components,
                target_components,
                strict=True,
            ):
                expected_area = transformed_area(player, source_component)
                if expected_area is not None:
                    assert (
                        target_component.area_x1,
                        target_component.area_y1,
                        target_component.area_x2,
                        target_component.area_y2,
                    ) == expected_area
                if (
                    hasattr(source_component, "location_x")
                    and source_component.location_x >= 0
                    and source_component.location_y >= 0
                ):
                    assert (
                        target_component.location_x,
                        target_component.location_y,
                    ) == v2_cell_for_player(
                        player,
                        source_component.location_x,
                        source_component.location_y,
                    )

    expected_hay = {
        1: ((48, 21), (52, 21), (55, 21), (59, 21)),
        2: ((95, 21), (84, 21), (88, 21), (91, 21)),
        3: ((21, 59), (21, 55), (21, 52), (21, 48)),
        4: ((122, 48), (122, 52), (122, 55), (122, 59)),
        5: ((21, 95), (21, 84), (21, 88), (21, 91)),
        6: ((122, 95), (122, 84), (122, 88), (122, 91)),
        7: ((48, 122), (52, 122), (55, 122), (59, 122)),
        8: ((95, 122), (84, 122), (88, 122), (91, 122)),
    }
    for player, positions in expected_hay.items():
        for index, position in enumerate(positions, start=1):
            creates = [
                effect
                for effect in by_name[f"hay{index} (p{player})"].effects
                if effect.effect_type == EffectId.CREATE_OBJECT
            ]
            assert len(creates) == 1
            assert (creates[0].location_x, creates[0].location_y) == position



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
        for legacy in ("Mova-me", "Médio", "Longo")
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
        activators = [
            trigger.name
            for trigger in evolution_alpha.trigger_manager.triggers
            for effect in trigger.effects
            if effect.effect_type == EffectId.ACTIVATE_TRIGGER and effect.trigger_id == free_costs.trigger_id
        ]
        assert activators == [
            f"Occupied Slot S{color} W{player}"
            for color in range(player, 9)
        ]
