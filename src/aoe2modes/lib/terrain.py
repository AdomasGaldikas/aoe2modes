"""Map and terrain helpers."""

from __future__ import annotations

from collections.abc import Iterable

from AoE2ScenarioParser.datasets.terrains import TerrainId
from AoE2ScenarioParser.objects.managers.map_manager import MapManager

from aoe2modes.config import MapSpec


def apply_map_spec(mm: MapManager, spec: MapSpec) -> None:
    """Resize the map, then flood-fill terrain and elevation."""
    mm.map_size = spec.size
    fill(mm, spec.terrain, elevation=spec.elevation)


def fill(mm: MapManager, terrain: TerrainId, *, elevation: int | None = None) -> None:
    for tile in mm.terrain:
        tile.terrain_id = terrain
        if elevation is not None:
            tile.elevation = elevation


def rect(
    mm: MapManager,
    x1: int, y1: int, x2: int, y2: int,
    terrain: TerrainId | None = None,
    *,
    elevation: int | None = None,
) -> None:
    """Paint an inclusive rectangle, clamped to the map."""
    limit = mm.map_size - 1
    for y in range(max(0, min(y1, y2)), min(limit, max(y1, y2)) + 1):
        for x in range(max(0, min(x1, x2)), min(limit, max(x1, x2)) + 1):
            tile = mm.get_tile(x, y)
            if terrain is not None:
                tile.terrain_id = terrain
            if elevation is not None:
                tile.elevation = elevation


def disc(
    mm: MapManager,
    cx: int, cy: int, radius: int,
    terrain: TerrainId | None = None,
    *,
    elevation: int | None = None,
) -> None:
    """Paint a filled circle — the usual shape for a CBA arena or a spawn pad."""
    limit = mm.map_size - 1
    r2 = radius * radius
    for y in range(max(0, cy - radius), min(limit, cy + radius) + 1):
        for x in range(max(0, cx - radius), min(limit, cx + radius) + 1):
            if (x - cx) ** 2 + (y - cy) ** 2 > r2:
                continue
            tile = mm.get_tile(x, y)
            if terrain is not None:
                tile.terrain_id = terrain
            if elevation is not None:
                tile.elevation = elevation


def border(mm: MapManager, thickness: int, terrain: TerrainId) -> None:
    """Ring the map edge — keeps players out of the unrendered outer tiles."""
    limit = mm.map_size - 1
    rect(mm, 0, 0, limit, thickness - 1, terrain)
    rect(mm, 0, limit - thickness + 1, limit, limit, terrain)
    rect(mm, 0, 0, thickness - 1, limit, terrain)
    rect(mm, limit - thickness + 1, 0, limit, limit, terrain)


def tiles_of(mm: MapManager, coords: Iterable[tuple[int, int]]):
    for x, y in coords:
        yield mm.get_tile(x, y)
