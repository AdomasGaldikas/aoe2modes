"""Serialized hill geometry and independent broad-route checks."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest
from AoE2ScenarioParser.datasets.other import OtherInfo
from AoE2ScenarioParser.datasets.players import PlayerId
from AoE2ScenarioParser.datasets.terrains import TerrainId
from AoE2ScenarioParser.scenarios.aoe2_de_scenario import AoE2DEScenario


def _module(repo):
    name = "ram_center_map_test"
    spec = importlib.util.spec_from_file_location(name, repo.modes / "ram/center_map.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def _context(tmp_path: Path, **overrides):
    settings = dict(enabled=True, plateau_half_width=10, rise=3, slope_step_width=3, approach_width=5)
    settings.update(overrides)
    lines = ["[center]", "x1=65", "y1=65", "x2=79", "y2=79", "[center_hill]"]
    lines += [f"{key}={str(value).lower()}" for key, value in settings.items()]
    (tmp_path / "mode.toml").write_text("\n".join(lines))
    scenario = AoE2DEScenario.from_default()
    scenario.map_manager.map_size = 144
    for tile in scenario.map_manager.terrain:
        tile.elevation = 1
        tile.terrain_id = TerrainId.GRASS_2 if tile.x < 72 else TerrainId.DESERT_SAND
    for x in (65.5, 78.5):
        scenario.unit_manager.add_unit(player=PlayerId.GAIA, unit_const=OtherInfo.FLAG_A.ID, x=x, y=72)
    return SimpleNamespace(
        scenario=scenario, mm=scenario.map_manager, um=scenario.unit_manager,
        map_size=144, mode_dir=tmp_path, log=lambda _: None,
    )


def test_center_hill_serializes_eight_broad_approaches_and_flat_meter(repo, tmp_path):
    ctx = _context(tmp_path)
    before = [(t.terrain_id, t.elevation, t.layer) for t in ctx.mm.terrain]
    report = _module(repo).configure_center_hill(ctx)
    assert report.patch_bounds == (53, 53, 90, 90)
    assert report.plateau_bounds == (62, 62, 81, 81)
    output = tmp_path / "hill.aoe2scenario"
    ctx.scenario.write_to_file(str(output))
    loaded = AoE2DEScenario.from_file(str(output))
    mm = loaded.map_manager
    for tile, old in zip(mm.terrain, before, strict=True):
        assert (tile.terrain_id, tile.layer) == (old[0], old[2])
        if not (53 <= tile.x <= 90 and 53 <= tile.y <= 90):
            assert tile.elevation == old[1]
    assert {t.elevation for t in mm.get_square_1d(62, 62, 81, 81)} == {4}
    assert {mm.get_tile(x, 72).elevation for x in range(65, 80)} == {4}
    assert len(loaded.unit_manager.units[0]) == 2  # Only the existing flags; no cliff/ramp props.

    # Independent five-lane paths from each octant, all the way into the flat
    # summit. Check diagonal steps too, so eight spokes cannot hide corner cliffs.
    water = {int(terrain) for terrain in TerrainId.water_terrains()}
    for dx, dy in ((0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1)):
        ox, oy = (72 if dx >= 0 else 71), (72 if dy >= 0 else 71)
        for offset in range(-2, 3):
            route = [mm.get_tile(ox + dx * distance - dy * offset,
                                 oy + dy * distance + dx * offset)
                     for distance in range(21, -1, -1)]
            assert route[0].elevation == 1 and route[-1].elevation == 4
            assert all(t.terrain_id not in water for t in route)
            assert all(0 <= b.elevation - a.elevation <= 1
                       for a, b in zip(route, route[1:], strict=False))
    for tile in mm.get_square_1d(53, 53, 90, 90):
        for x, y in ((143 - tile.x, tile.y), (tile.y, tile.x), (tile.x, 143 - tile.y)):
            assert tile.elevation == mm.get_tile(x, y).elevation


def test_center_hill_disabled_preserves_map_and_objects(repo, tmp_path):
    ctx = _context(tmp_path, enabled=False)
    before = [(t.terrain_id, t.elevation, t.layer) for t in ctx.mm.terrain]
    assert _module(repo).configure_center_hill(ctx) is None
    assert before == [(t.terrain_id, t.elevation, t.layer) for t in ctx.mm.terrain]
    assert len(ctx.um.units[0]) == 2


@pytest.mark.parametrize("overrides", [
    {"rise": 0}, {"rise": True}, {"rise": 5}, {"slope_step_width": 1},
    {"plateau_half_width": 4}, {"approach_width": 2}, {"approach_width": 6},
    {"plateau_half_width": 70},
])
def test_center_hill_rejects_unsafe_geometry_before_mutating(repo, tmp_path, overrides):
    ctx = _context(tmp_path, **overrides)
    before = [t.elevation for t in ctx.mm.terrain]
    with pytest.raises(ValueError):
        _module(repo).configure_center_hill(ctx)
    assert before == [t.elevation for t in ctx.mm.terrain]


@pytest.mark.parametrize("obstacle", ["water", "cliff"])
def test_center_hill_does_not_hide_an_obstructed_approach(repo, tmp_path, obstacle):
    ctx = _context(tmp_path)
    if obstacle == "water":
        ctx.mm.get_tile(72, 55).terrain_id = TerrainId.WATER_DEEP
    else:
        ctx.um.add_unit(player=PlayerId.GAIA, unit_const=OtherInfo.CLIFF_DEFAULT_1.ID, x=72.5, y=55.5)
    before = [t.elevation for t in ctx.mm.terrain]
    with pytest.raises(ValueError, match="water|object"):
        _module(repo).configure_center_hill(ctx)
    assert before == [t.elevation for t in ctx.mm.terrain]
