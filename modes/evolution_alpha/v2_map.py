"""Apply the Excel V2 complete-sector symmetry blueprint.

Blueprint: ``CBA_Hero_Reforged_Evolution_Alpha_Map_Catalogue_V2_``
``Structure_Aware_Exact_Symmetry.xlsx`` (SHA-256
``8f530fa2d8e6cc54c679363dee0d593aee6d4e95e810a8273e527cbad747dd5c``).

The workbook uses P3's complete 111-object sector as the canonical template,
then rotates or reflects it into every player position. Terrain follows the
same eight transforms. Existing reference IDs are retained; only missing Stone
Wall slots are added.
"""

from __future__ import annotations

import math
from collections import defaultdict
from dataclasses import dataclass
from itertools import permutations

from AoE2ScenarioParser.datasets.buildings import BuildingInfo
from AoE2ScenarioParser.datasets.other import OtherInfo
from AoE2ScenarioParser.datasets.players import PlayerId
from AoE2ScenarioParser.datasets.terrains import TerrainId

from aoe2modes.context import BuildContext

MAP_SIZE = 144
SOURCE_SECTOR = 2
GATE_IDS = {64, 88}
KING_ROLE_IDS = {434, 838}
EXPECTED_SOURCE_UNITS = 1_217
EXPECTED_SOURCE_CORE = 111
EXPECTED_TERRAIN_CHANGES = 4_677
EXPECTED_EXISTING_MOVES = 623
EXPECTED_NEW_WALLS = 20

# The complete P3 workbook sector has a solid side wall where the four corner
# bases need their protected teammate gate.  Those openings are deliberately
# excluded from the copied wall template; otherwise V2 places four Stone Walls
# through each gate and turns the route into a dead end.
TEAM_GATE_WALL_CUTS = {
    PlayerId.ONE: frozenset((64.5, y) for y in (20.5, 21.5, 22.5, 23.5)),
    PlayerId.TWO: frozenset((79.5, y) for y in (20.5, 21.5, 22.5, 23.5)),
    PlayerId.SEVEN: frozenset((64.5, y) for y in (120.5, 121.5, 122.5, 123.5)),
    PlayerId.EIGHT: frozenset((79.5, y) for y in (120.5, 121.5, 122.5, 123.5)),
}

# Existing reference IDs are retained so Antidelete and any legacy object
# selections keep working.  P2/P8 move to the mirrored V2 side wall; the lower
# pair moves one tile north so it is the exact reflection of the upper pair.
TEAM_SIDE_GATES = {
    PlayerId.ONE: (109_743, 64.5, 22.0),
    PlayerId.TWO: (109_744, 79.5, 22.0),
    PlayerId.SEVEN: (109_745, 64.5, 122.0),
    PlayerId.EIGHT: (109_746, 79.5, 122.0),
}

# A four-tile allied causeway connects each same-team pair.  Copying
# P3's terrain into every sector filled these two routes with water; restoring
# only the top/bottom corridors avoids opening an enemy route on either side.
TEAM_ROUTE_RECTANGLES = (
    (65, 20, 78, 23),
    (65, 120, 78, 123),
)

# The four outer team corners inherited broad eight-tile land aprons. Keep the
# inner five-tile L routes that meet the side gates and flood only the empty
# outer apron. The source mask is symmetric across its diagonal, so its eight
# map transforms produce the four identical team corners without one-off edits.
SOURCE_CORNER_ROUTE_WATER_TILES = frozenset(
    {
        *((x, y) for x in range(15, 38) for y in range(15, 19)),
        *((x, y) for x in range(15, 19) for y in range(19, 38)),
    }
)

# The milestone-hero shore inherited a narrow Beach ribbon from the winter
# baseline. Beach looks like dry sand but rejects normal building placement in
# DE. Replace only the exact twenty-cell ribbon in each transformed color
# sector; the surrounding grass, water, flags, and hero landing tile stay put.
SOURCE_MILESTONE_SHORE_BEACH_TILES = frozenset(
    {
        *((15, y) for y in range(38, 43)),
        (16, 39),
        (17, 38),
        (17, 39),
        *((x, 39) for x in range(18, 24)),
        *((24, y) for y in range(38, 44)),
    }
)

# The canonical transform intentionally treats King and relic-selector objects
# as one semantic class, because both use unit 434 in most sectors.  Pinning
# their established references after assignment prevents P8's two unit-434
# objects from exchanging jobs and silently breaking selected-object triggers.
ROLE_REFERENCE_TARGETS = {
    PlayerId.ONE: {95_792: (39.5, 0.5), 48_301: (45.5, 5.5)},
    PlayerId.TWO: {95_959: (104.5, 0.5), 42_394: (98.5, 5.5)},
    PlayerId.THREE: {95_961: (0.5, 39.5), 42_395: (5.5, 45.5)},
    PlayerId.FOUR: {95_962: (143.5, 39.5), 42_396: (138.5, 45.5)},
    PlayerId.FIVE: {95_963: (0.5, 104.5), 42_397: (5.5, 98.5)},
    PlayerId.SIX: {95_964: (143.5, 104.5), 42_398: (138.5, 98.5)},
    PlayerId.SEVEN: {95_965: (39.5, 143.5), 42_399: (45.5, 138.5)},
    PlayerId.EIGHT: {95_966: (104.5, 143.5), 42_400: (98.5, 138.5)},
}

# Gaia's spawn-selector props are outside the player sectors, so the workbook's
# player-object pass never moved them with the symmetric terrain. Rebuild all
# eight edge islands from the complete P3 island instead of leaving Relics and
# Rugs in the surrounding water.
SOURCE_EDGE_SELECTOR_SLOTS = {
    OtherInfo.RELIC.ID: (
        (1.5, 61.5),
        (1.5, 63.5),
        (1.5, 65.5),
        (7.5, 61.5),
        (7.5, 65.5),
    ),
    OtherInfo.RUGS.ID: (
        (2.5, 61.5),
        (2.5, 63.5),
        (2.5, 65.5),
        (6.5, 61.5),
        (6.5, 65.5),
    ),
}
SOURCE_KING_ISLAND_ORNAMENT = (2.5, 39.5)

DEFAULT_CLIFF_IDS = frozenset(
    getattr(OtherInfo, f"CLIFF_DEFAULT_{index}").ID
    for index in range(1, 10)
)

# P3 is the canonical left-hand sector. Its compact rear boundary is a vertical
# wall at x=14.5 with a four-tile gate centred at y=54. The previous x=12.5
# boundary still left four walkable rows behind every castle. Build this same
# complete wall in every transformed sector instead of mixing sparse cliff
# artwork with walls. Continuous one-tile wall slots stop diagonal gaps and
# make the water boundary visually unambiguous.
SOURCE_LEGACY_REAR_X = 10.5
SOURCE_REAR_X = 14.5
SOURCE_REAR_WALL_SLOTS = tuple(
    (SOURCE_REAR_X, position + 0.5)
    for position in (*range(43, 52), *range(56, 65))
)
SOURCE_REAR_GATE_POSITION = (SOURCE_REAR_X, 54.0)

# Reuse the existing wall references when the boundary moves. Two sparse rear
# anchors move straight inward; the six obsolete side overhangs become rear-wall
# pieces so every side terminates exactly on the new boundary.
SOURCE_REAR_WALL_RELOCATIONS = (
    ((SOURCE_LEGACY_REAR_X, 51.5), (SOURCE_REAR_X, 51.5)),
    ((SOURCE_LEGACY_REAR_X, 56.5), (SOURCE_REAR_X, 56.5)),
    ((11.5, 43.5), (SOURCE_REAR_X, 44.5)),
    ((12.5, 43.5), (SOURCE_REAR_X, 45.5)),
    ((13.5, 43.5), (SOURCE_REAR_X, 46.5)),
    ((11.5, 64.5), (SOURCE_REAR_X, 63.5)),
    ((12.5, 64.5), (SOURCE_REAR_X, 62.5)),
    ((13.5, 64.5), (SOURCE_REAR_X, 61.5)),
)
SOURCE_REAR_GATE_TOWER_RELOCATIONS = (
    ((12.5, 52.5), (15.5, 52.5)),
    ((12.5, 55.5), (15.5, 55.5)),
)

# Keep land on the protected side of the rear wall, water on its outer side,
# and a three-tile path through the gate to the technology island. Applying the
# same source cells through all eight transforms prevents one-off shoreline
# edits from making any territory larger or smaller.
SOURCE_REAR_LAND_TILES = frozenset(
    (x, y)
    for x in range(14, 17)
    for y in range(43, 65)
)
SOURCE_REAR_OUTSIDE_WATER_TILES = frozenset(
    (x, y)
    for x in range(8, 14)
    for y in range(43, 65)
    if y not in {53, 54}
)
SOURCE_REAR_GATE_PATH_TILES = frozenset(
    (x, y)
    for x in range(7, 17)
    for y in (53, 54, 55)
)
SOURCE_FRONT_ENTRANCE_TILES = frozenset(
    (x, y)
    for x in range(36, 39)
    for y in range(53, 56)
)
FRONT_ENTRANCE_TERRAINS = {
    PlayerId.ONE: TerrainId.ROAD_GRAVEL,
    PlayerId.TWO: TerrainId.DIRT_4,
    PlayerId.THREE: TerrainId.GRASS_1,
    PlayerId.FOUR: TerrainId.DESERT_SAND,
    PlayerId.FIVE: TerrainId.GRASS_3,
    PlayerId.SIX: TerrainId.ROAD_FUNGUS,
    PlayerId.SEVEN: TerrainId.ROAD,
    PlayerId.EIGHT: TerrainId.DIRT_1,
}
WINTER_TERRAIN_REPLACEMENTS = {
    TerrainId.SNOW: TerrainId.GRASS_2,
    TerrainId.BEACH_ICE: TerrainId.BEACH,
    TerrainId.ICE: TerrainId.BEACH,
}


@dataclass(frozen=True)
class V2MapReport:
    """Guardrail totals and new wall references from the V2 transformation."""

    terrain_changes: int
    moved_units: int
    new_wall_ids: dict[PlayerId, tuple[int, ...]]


def _transform_cell(index: int, x: int, y: int) -> tuple[int, int]:
    return (
        (x, y),
        (MAP_SIZE - 1 - x, y),
        (y, x),
        (MAP_SIZE - 1 - y, x),
        (y, MAP_SIZE - 1 - x),
        (MAP_SIZE - 1 - y, MAP_SIZE - 1 - x),
        (x, MAP_SIZE - 1 - y),
        (MAP_SIZE - 1 - x, MAP_SIZE - 1 - y),
    )[index]


def _transform_position(index: int, x: float, y: float) -> tuple[float, float]:
    return (
        (x, y),
        (MAP_SIZE - x, y),
        (y, x),
        (MAP_SIZE - y, x),
        (y, MAP_SIZE - x),
        (MAP_SIZE - y, MAP_SIZE - x),
        (x, MAP_SIZE - y),
        (MAP_SIZE - x, MAP_SIZE - y),
    )[index]


def _canonical_representative(x: int, y: int) -> tuple[int, int]:
    orbit = {_transform_cell(index, x, y) for index in range(8)}
    candidates = [
        (candidate_x, candidate_y)
        for candidate_x, candidate_y in orbit
        if 2 * candidate_x - (MAP_SIZE - 1) <= 0
        and 2 * candidate_y - (MAP_SIZE - 1)
        <= 2 * candidate_x - (MAP_SIZE - 1)
    ]
    return sorted(candidates)[0]


def _sector_for(x: int, y: int) -> int:
    canonical = _canonical_representative(x, y)
    for index in range(8):
        if _transform_cell(index, *canonical) == (x, y):
            return index
    raise RuntimeError(f"unable to resolve V2 sector for ({x}, {y})")


def _from_source_position(
    target_sector: int, x: float, y: float
) -> tuple[float, float]:
    # Sector 2 is a transpose, and a transpose is its own inverse.
    return _transform_position(target_sector, y, x)


def v2_cell_for_player(
    player: PlayerId | int,
    source_x: int,
    source_y: int,
) -> tuple[int, int]:
    """Transform an inclusive P3 trigger cell into a target color sector."""
    return _transform_cell(int(player) - 1, source_y, source_x)


def v2_position_for_player(
    player: PlayerId | int,
    source_x: float,
    source_y: float,
) -> tuple[float, float]:
    """Transform a P3 object/effect point into a target color sector."""
    return _from_source_position(int(player) - 1, source_x, source_y)


def _semantic_unit_key(unit_const: int) -> int | str:
    if unit_const in GATE_IDS:
        return "gate"
    if unit_const in KING_ROLE_IDS:
        return "king-role"
    return unit_const


def _transformed_gate(
    source_const: int,
    target_sector: int,
    source_x: float,
    source_y: float,
) -> int:
    # In scenario coordinates, gate 64 closes a horizontal wall run and gate
    # 88 closes a vertical one.  The earlier diagonal-vector model described
    # their isometric artwork instead of the map axis, so every reflected base
    # received sideways gates.
    vector_x, vector_y = (1, 0) if source_const == 64 else (0, 1)
    first = _from_source_position(target_sector, source_x, source_y)
    second = _from_source_position(
        target_sector,
        source_x + vector_x,
        source_y + vector_y,
    )
    delta_x = abs(second[0] - first[0])
    delta_y = abs(second[1] - first[1])
    return 64 if delta_x > delta_y else 88


def _transformed_wall_rotation(
    source_rotation: float,
    target_sector: int,
    source_x: float,
    source_y: float,
) -> float:
    """Rotate straight Stone Wall artwork with its map axis.

    Rotation 0 is a horizontal run, 1 is vertical, and 2 is the shared
    corner/endcap artwork.  The corner form is invariant under the V2 map
    transforms.
    """
    if source_rotation == 2:
        return source_rotation
    if source_rotation not in (0, 1):
        raise RuntimeError(
            f"unexpected Stone Wall rotation {source_rotation} at "
            f"({source_x}, {source_y})"
        )
    vector_x, vector_y = (1, 0) if source_rotation == 0 else (0, 1)
    first = _from_source_position(target_sector, source_x, source_y)
    second = _from_source_position(
        target_sector,
        source_x + vector_x,
        source_y + vector_y,
    )
    return 0 if abs(second[0] - first[0]) > abs(second[1] - first[1]) else 1


def _restore_team_routes(ctx: BuildContext) -> None:
    for x1, y1, x2, y2 in TEAM_ROUTE_RECTANGLES:
        for y in range(y1, y2 + 1):
            for x in range(x1, x2 + 1):
                tile = ctx.mm.get_tile(x=x, y=y)
                tile.terrain_id = TerrainId.GRASS_2
                tile.elevation = 1
                tile.layer = -1


def _trim_corner_team_routes(ctx: BuildContext) -> None:
    trimmed = set()
    for source_x, source_y in SOURCE_CORNER_ROUTE_WATER_TILES:
        for player in PlayerId.all(exclude_gaia=True):
            trimmed.add(v2_cell_for_player(player, source_x, source_y))
    for x, y in trimmed:
        tile = ctx.mm.get_tile(x=x, y=y)
        tile.terrain_id = TerrainId.WATER_MEDIUM
        tile.elevation = 1
        tile.layer = -1


def _align_team_side_gates(ctx: BuildContext) -> None:
    for player, (reference_id, x, y) in TEAM_SIDE_GATES.items():
        matches = [
            unit
            for unit in ctx.um.units[player]
            if unit.reference_id == reference_id
        ]
        if len(matches) != 1:
            raise RuntimeError(
                f"expected one V2 teammate gate {reference_id} for P{int(player)}, "
                f"found {len(matches)}"
            )
        gate = matches[0]
        gate.unit_const = BuildingInfo.GATE_NORTHWEST_TO_SOUTHEAST.ID
        gate.x = x
        gate.y = y


def _align_role_references(ctx: BuildContext) -> None:
    for player, targets in ROLE_REFERENCE_TARGETS.items():
        by_reference_id = {
            unit.reference_id: unit
            for unit in ctx.um.units[player]
        }
        for reference_id, (x, y) in targets.items():
            unit = by_reference_id.get(reference_id)
            if unit is None:
                raise RuntimeError(
                    f"missing V2 role reference {reference_id} for P{int(player)}"
                )
            unit.x = x
            unit.y = y


def _minimum_distance_assignment(units, positions):
    ordered_units = sorted(units, key=lambda unit: unit.reference_id)
    return min(
        permutations(positions),
        key=lambda candidate_positions: (
            sum(
                (unit.x - x) ** 2 + (unit.y - y) ** 2
                for unit, (x, y) in zip(
                    ordered_units,
                    candidate_positions,
                    strict=True,
                )
            ),
            candidate_positions,
        ),
    ), ordered_units


def _align_edge_island_objects(ctx: BuildContext) -> None:
    """Put every visible selector prop onto its transformed ground island."""
    water = {int(terrain) for terrain in TerrainId.water_terrains()}
    for unit_const, source_positions in SOURCE_EDGE_SELECTOR_SLOTS.items():
        candidates = [
            unit
            for unit in ctx.um.units[PlayerId.GAIA]
            if unit.unit_const == unit_const
        ]
        if len(candidates) != len(source_positions) * len(PlayerId.all(exclude_gaia=True)):
            raise RuntimeError(
                f"expected 40 edge-selector objects of type {unit_const}, "
                f"found {len(candidates)}"
            )

        positions_by_player = {
            player: tuple(
                v2_position_for_player(player, x, y)
                for x, y in source_positions
            )
            for player in PlayerId.all(exclude_gaia=True)
        }
        centers = {
            player: (
                sum(x for x, _y in positions) / len(positions),
                sum(y for _x, y in positions) / len(positions),
            )
            for player, positions in positions_by_player.items()
        }
        grouped = defaultdict(list)
        for unit in candidates:
            player = min(
                centers,
                key=lambda candidate: (
                    (unit.x - centers[candidate][0]) ** 2
                    + (unit.y - centers[candidate][1]) ** 2,
                    int(candidate),
                ),
            )
            grouped[player].append(unit)

        for player, positions in positions_by_player.items():
            if len(grouped[player]) != len(source_positions):
                raise RuntimeError(
                    f"expected five selector objects of type {unit_const} "
                    f"near P{int(player)}, found {len(grouped[player])}"
                )
            assigned_positions, ordered_units = _minimum_distance_assignment(
                grouped[player],
                positions,
            )
            for unit, (x, y) in zip(
                ordered_units,
                assigned_positions,
                strict=True,
            ):
                unit.x = x
                unit.y = y
                if ctx.mm.get_tile(x=int(x), y=int(y)).terrain_id in water:
                    raise RuntimeError(
                        f"selector object {unit.reference_id} remains on water"
                    )

    ornaments = [
        unit
        for units in ctx.um.units
        for unit in units
        if unit.unit_const == OtherInfo.NINE_BANDS.ID
    ]
    ornament_positions = tuple(
        v2_position_for_player(player, *SOURCE_KING_ISLAND_ORNAMENT)
        for player in PlayerId.all(exclude_gaia=True)
    )
    if len(ornaments) != len(ornament_positions):
        raise RuntimeError(
            f"expected eight King-island ornaments, found {len(ornaments)}"
        )
    assigned_positions, ordered_ornaments = _minimum_distance_assignment(
        ornaments,
        ornament_positions,
    )
    for ornament, (x, y) in zip(
        ordered_ornaments,
        assigned_positions,
        strict=True,
    ):
        ornament.x = x
        ornament.y = y
        if ctx.mm.get_tile(x=int(x), y=int(y)).terrain_id in water:
            raise RuntimeError(
                f"King-island ornament {ornament.reference_id} remains on water"
            )


def _compact_rear_boundaries(ctx: BuildContext) -> None:
    """Move every rear wall to its two-row defensive boundary and seal its joins."""
    for player in PlayerId.all(exclude_gaia=True):
        target_sector = int(player) - 1
        old_gate_position = v2_position_for_player(
            player,
            SOURCE_LEGACY_REAR_X,
            54.0,
        )
        new_gate_position = v2_position_for_player(
            player,
            *SOURCE_REAR_GATE_POSITION,
        )
        gates = [
            unit
            for unit in ctx.um.units[player]
            if unit.unit_const in GATE_IDS
            and (unit.x, unit.y) == old_gate_position
        ]
        if len(gates) != 1:
            raise RuntimeError(
                f"expected one legacy rear gate for P{int(player)} at "
                f"{old_gate_position}, found {len(gates)}"
            )
        gates[0].x, gates[0].y = new_gate_position

        for source_position, target_position in SOURCE_REAR_WALL_RELOCATIONS:
            old_x, old_y = v2_position_for_player(player, *source_position)
            new_x, new_y = v2_position_for_player(player, *target_position)
            walls = [
                unit
                for unit in ctx.um.units[player]
                if unit.unit_const == BuildingInfo.STONE_WALL.ID
                and (unit.x, unit.y) == (old_x, old_y)
            ]
            if len(walls) != 1:
                raise RuntimeError(
                    f"expected one compacted rear wall for P{int(player)} at "
                    f"({old_x}, {old_y}), found {len(walls)}"
                )
            if any(
                unit.unit_const == BuildingInfo.STONE_WALL.ID
                and (unit.x, unit.y) == (new_x, new_y)
                for unit in ctx.um.units[player]
            ):
                raise RuntimeError(
                    f"occupied compacted rear-wall slot for P{int(player)} at "
                    f"({new_x}, {new_y})"
                )
            wall = walls[0]
            wall.x = new_x
            wall.y = new_y
            wall.rotation = _transformed_wall_rotation(
                1,
                target_sector,
                *target_position,
            )

        for source_position, target_position in SOURCE_REAR_GATE_TOWER_RELOCATIONS:
            old_x, old_y = v2_position_for_player(player, *source_position)
            new_x, new_y = v2_position_for_player(player, *target_position)
            towers = [
                unit
                for unit in ctx.um.units[player]
                if unit.unit_const == BuildingInfo.BOMBARD_TOWER.ID
                and (unit.x, unit.y) == (old_x, old_y)
            ]
            if len(towers) != 1:
                raise RuntimeError(
                    f"expected one rear gate tower for P{int(player)} at "
                    f"({old_x}, {old_y}), found {len(towers)}"
                )
            if any(
                (unit.x, unit.y) == (new_x, new_y)
                for unit in ctx.um.units[player]
                if unit is not towers[0]
            ):
                raise RuntimeError(
                    f"occupied compacted rear-tower slot for P{int(player)} at "
                    f"({new_x}, {new_y})"
                )
            towers[0].x = new_x
            towers[0].y = new_y


def _tidy_rear_terrain(ctx: BuildContext) -> None:
    for player in PlayerId.all(exclude_gaia=True):
        for source_cells, terrain_id in (
            (SOURCE_REAR_LAND_TILES, TerrainId.GRASS_2),
            (SOURCE_REAR_OUTSIDE_WATER_TILES, TerrainId.WATER_MEDIUM),
            (SOURCE_REAR_GATE_PATH_TILES, TerrainId.GRASS_2),
        ):
            for source_x, source_y in source_cells:
                x, y = v2_cell_for_player(player, source_x, source_y)
                tile = ctx.mm.get_tile(x=x, y=y)
                tile.terrain_id = terrain_id
                tile.elevation = 1
                tile.layer = -1


def _replace_winter_terrain(ctx: BuildContext) -> None:
    """Use grass and sand everywhere while keeping water and buildability intact."""
    for y in range(MAP_SIZE):
        for x in range(MAP_SIZE):
            tile = ctx.mm.get_tile(x=x, y=y)
            replacement = WINTER_TERRAIN_REPLACEMENTS.get(tile.terrain_id)
            if replacement is not None:
                tile.terrain_id = replacement

    for player in PlayerId.all(exclude_gaia=True):
        for source_x, source_y in SOURCE_MILESTONE_SHORE_BEACH_TILES:
            x, y = v2_cell_for_player(player, source_x, source_y)
            tile = ctx.mm.get_tile(x=x, y=y)
            if tile.terrain_id != TerrainId.BEACH:
                raise RuntimeError(
                    f"P{int(player)} milestone shore ({x}, {y}) expected Beach, "
                    f"found {tile.terrain_id}"
                )
            tile.terrain_id = TerrainId.GRASS_2
            tile.elevation = 1
            tile.layer = -1

    water = {int(terrain) for terrain in TerrainId.water_terrains()}
    for player, terrain_id in FRONT_ENTRANCE_TERRAINS.items():
        if int(terrain_id) in water:
            raise RuntimeError(
                f"P{int(player)} front entrance terrain {terrain_id} is water"
            )
        for source_x, source_y in SOURCE_FRONT_ENTRANCE_TILES:
            x, y = v2_cell_for_player(player, source_x, source_y)
            tile = ctx.mm.get_tile(x=x, y=y)
            if tile.terrain_id in water:
                raise RuntimeError(
                    f"P{int(player)} front entrance ({x}, {y}) is water"
                )
            tile.terrain_id = terrain_id
            tile.elevation = 1
            tile.layer = -1


def _remove_default_cliffs(ctx: BuildContext) -> int:
    cliffs = [
        unit
        for unit in ctx.um.units[PlayerId.GAIA]
        if unit.unit_const in DEFAULT_CLIFF_IDS
    ]
    if len(cliffs) != 205:
        raise RuntimeError(f"expected 205 legacy cliff pieces, found {len(cliffs)}")
    for cliff in cliffs:
        ctx.um.remove_unit(unit=cliff)
    return len(cliffs)


def _add_complete_rear_walls(
    ctx: BuildContext,
) -> dict[PlayerId, tuple[int, ...]]:
    added: defaultdict[PlayerId, list[int]] = defaultdict(list)
    water = {int(terrain) for terrain in TerrainId.water_terrains()}

    for player in PlayerId.all(exclude_gaia=True):
        target_sector = int(player) - 1
        gate_x, gate_y = v2_position_for_player(
            player,
            *SOURCE_REAR_GATE_POSITION,
        )
        gates = [
            unit
            for unit in ctx.um.units[player]
            if unit.unit_const in GATE_IDS and (unit.x, unit.y) == (gate_x, gate_y)
        ]
        if len(gates) != 1:
            raise RuntimeError(
                f"expected one rear gate for P{int(player)} at "
                f"({gate_x}, {gate_y}), found {len(gates)}"
            )

        by_position = {
            (unit.x, unit.y): unit
            for unit in ctx.um.units[player]
            if unit.unit_const == BuildingInfo.STONE_WALL.ID
        }
        for source_x, source_y in SOURCE_REAR_WALL_SLOTS:
            x, y = v2_position_for_player(player, source_x, source_y)
            if (x, y) in by_position:
                continue
            wall = ctx.um.add_unit(
                player=player,
                unit_const=BuildingInfo.STONE_WALL.ID,
                x=x,
                y=y,
                rotation=_transformed_wall_rotation(
                    1,
                    target_sector,
                    source_x,
                    source_y,
                ),
            )
            added[player].append(wall.reference_id)
            by_position[x, y] = wall

        expected_positions = {
            v2_position_for_player(player, source_x, source_y)
            for source_x, source_y in SOURCE_REAR_WALL_SLOTS
        }
        if expected_positions - set(by_position):
            raise RuntimeError(f"incomplete rear wall for P{int(player)}")
        if any(
            ctx.mm.get_tile(x=int(x), y=int(y)).terrain_id in water
            for x, y in (*expected_positions, (gate_x, gate_y))
        ):
            raise RuntimeError(f"water remains under P{int(player)} rear wall")

    added_count = sum(len(reference_ids) for reference_ids in added.values())
    if added_count != 64:
        raise RuntimeError(
            "expected 64 new complete-rear-wall pieces, found "
            f"{added_count}"
        )
    return {
        player: tuple(reference_ids)
        for player, reference_ids in added.items()
    }


def _apply_exact_terrain(ctx: BuildContext) -> int:
    source = [
        [
            (
                ctx.mm.get_tile(x=x, y=y).terrain_id,
                ctx.mm.get_tile(x=x, y=y).elevation,
                ctx.mm.get_tile(x=x, y=y).layer,
            )
            for x in range(MAP_SIZE)
        ]
        for y in range(MAP_SIZE)
    ]
    revised = [[(0, 0, 0)] * MAP_SIZE for _ in range(MAP_SIZE)]
    changes = 0

    for y in range(MAP_SIZE):
        for x in range(MAP_SIZE):
            canonical_x, canonical_y = _canonical_representative(x, y)
            source_x, source_y = _transform_cell(
                SOURCE_SECTOR,
                canonical_x,
                canonical_y,
            )
            tile_values = source[source_y][source_x]
            revised[y][x] = tile_values
            changes += tile_values[0] != source[y][x][0]

    if changes != EXPECTED_TERRAIN_CHANGES:
        raise RuntimeError(
            "Excel V2 pre-transform terrain source changed: "
            f"expected {EXPECTED_TERRAIN_CHANGES} changes, found {changes}"
        )

    for y in range(MAP_SIZE):
        for x in range(MAP_SIZE):
            tile = ctx.mm.get_tile(x=x, y=y)
            tile.terrain_id, tile.elevation, tile.layer = revised[y][x]
            for index in range(1, 8):
                transformed_x, transformed_y = _transform_cell(index, x, y)
                if revised[transformed_y][transformed_x] != revised[y][x]:
                    raise RuntimeError(
                        f"Excel V2 terrain symmetry failed at ({x}, {y})"
                    )

    return changes


def _apply_exact_objects(
    ctx: BuildContext,
) -> tuple[int, dict[PlayerId, tuple[int, ...]]]:
    indexed_units = [
        (PlayerId(player), unit)
        for player, player_units in enumerate(ctx.um.units)
        for unit in player_units
    ]
    if len(indexed_units) != EXPECTED_SOURCE_UNITS:
        raise RuntimeError(
            "Excel V2 pre-transform object source changed: "
            f"expected {EXPECTED_SOURCE_UNITS} units, found {len(indexed_units)}"
        )

    original_reference_ids = {unit.reference_id for _player, unit in indexed_units}
    source_core = [
        unit
        for player, unit in indexed_units
        if player == PlayerId.THREE
        and _sector_for(math.floor(unit.x), math.floor(unit.y)) == SOURCE_SECTOR
    ]
    if len(source_core) != EXPECTED_SOURCE_CORE:
        raise RuntimeError(
            f"expected {EXPECTED_SOURCE_CORE} P3 template objects, "
            f"found {len(source_core)}"
        )

    used_existing: set[int] = set()
    moved_units = 0
    new_wall_ids: defaultdict[PlayerId, list[int]] = defaultdict(list)

    for target_sector in range(8):
        target_player = PlayerId(target_sector + 1)
        desired = []
        for source in source_core:
            target_x, target_y = _from_source_position(
                target_sector,
                source.x,
                source.y,
            )
            target_position = (round(target_x, 2), round(target_y, 2))
            if (
                source.unit_const == BuildingInfo.STONE_WALL.ID
                and target_position in TEAM_GATE_WALL_CUTS.get(
                    target_player,
                    frozenset(),
                )
            ):
                continue
            desired.append((source, *target_position))

        candidate_pairs = []
        for desired_index, (source, target_x, target_y) in enumerate(desired):
            for candidate_index, (candidate_player, candidate) in enumerate(
                indexed_units
            ):
                if (
                    candidate_index in used_existing
                    or candidate_player != target_player
                    or _semantic_unit_key(candidate.unit_const)
                    != _semantic_unit_key(source.unit_const)
                ):
                    continue
                candidate_pairs.append(
                    (
                        math.hypot(
                            candidate.x - target_x,
                            candidate.y - target_y,
                        ),
                        desired_index,
                        candidate_index,
                    )
                )

        candidate_pairs.sort()
        assigned_desired: set[int] = set()
        for _distance, desired_index, candidate_index in candidate_pairs:
            if (
                desired_index in assigned_desired
                or candidate_index in used_existing
            ):
                continue
            assigned_desired.add(desired_index)
            used_existing.add(candidate_index)
            source, target_x, target_y = desired[desired_index]
            _candidate_player, candidate = indexed_units[candidate_index]
            target_const = candidate.unit_const
            target_rotation = candidate.rotation
            if source.unit_const in GATE_IDS:
                target_const = _transformed_gate(
                    source.unit_const,
                    target_sector,
                    source.x,
                    source.y,
                )
            elif source.unit_const == BuildingInfo.STONE_WALL.ID:
                target_rotation = _transformed_wall_rotation(
                    source.rotation,
                    target_sector,
                    source.x,
                    source.y,
                )
            if (
                candidate.unit_const,
                candidate.x,
                candidate.y,
                candidate.rotation,
            ) != (target_const, target_x, target_y, target_rotation):
                moved_units += 1
            candidate.unit_const = target_const
            candidate.x = target_x
            candidate.y = target_y
            candidate.rotation = target_rotation

        for desired_index, (source, target_x, target_y) in enumerate(desired):
            if desired_index in assigned_desired:
                continue
            if source.unit_const != BuildingInfo.STONE_WALL.ID:
                raise RuntimeError(
                    f"missing non-wall V2 object for P{int(target_player)}: "
                    f"unit {source.unit_const} at ({target_x}, {target_y})"
                )
            if any(
                unit.unit_const == BuildingInfo.STONE_WALL.ID
                and (unit.x, unit.y) == (target_x, target_y)
                for unit in ctx.um.units[target_player]
            ):
                raise RuntimeError(
                    f"duplicate V2 wall slot for P{int(target_player)} at "
                    f"({target_x}, {target_y})"
                )
            wall = ctx.um.add_unit(
                player=target_player,
                unit_const=BuildingInfo.STONE_WALL.ID,
                x=target_x,
                y=target_y,
                rotation=_transformed_wall_rotation(
                    source.rotation,
                    target_sector,
                    source.x,
                    source.y,
                ),
                status=source.status,
            )
            new_wall_ids[target_player].append(wall.reference_id)

    new_wall_count = sum(len(reference_ids) for reference_ids in new_wall_ids.values())
    if moved_units != EXPECTED_EXISTING_MOVES:
        raise RuntimeError(
            f"expected {EXPECTED_EXISTING_MOVES} V2 object moves, found {moved_units}"
        )
    if new_wall_count != EXPECTED_NEW_WALLS:
        raise RuntimeError(
            f"expected {EXPECTED_NEW_WALLS} new V2 walls, found {new_wall_count}"
        )
    if {
        unit.reference_id
        for player_units in ctx.um.units
        for unit in player_units
        if unit.reference_id in original_reference_ids
    } != original_reference_ids:
        raise RuntimeError("Excel V2 transformation lost an original reference ID")

    return moved_units, {
        player: tuple(reference_ids)
        for player, reference_ids in new_wall_ids.items()
    }


def apply_v2_map(ctx: BuildContext) -> V2MapReport:
    """Apply V2 symmetry while preserving protected team-route details."""
    terrain_changes = _apply_exact_terrain(ctx)
    _restore_team_routes(ctx)
    _trim_corner_team_routes(ctx)
    moved_units, new_wall_ids = _apply_exact_objects(ctx)
    _align_team_side_gates(ctx)
    _align_role_references(ctx)
    _align_edge_island_objects(ctx)
    _compact_rear_boundaries(ctx)
    _tidy_rear_terrain(ctx)
    _replace_winter_terrain(ctx)
    _remove_default_cliffs(ctx)
    rear_wall_ids = _add_complete_rear_walls(ctx)
    combined_wall_ids = {
        player: tuple(new_wall_ids.get(player, ()))
        + tuple(rear_wall_ids.get(player, ()))
        for player in PlayerId.all(exclude_gaia=True)
        if new_wall_ids.get(player) or rear_wall_ids.get(player)
    }
    return V2MapReport(
        terrain_changes=terrain_changes,
        moved_units=moved_units,
        new_wall_ids=combined_wall_ids,
    )
