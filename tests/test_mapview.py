from __future__ import annotations

import struct
from types import SimpleNamespace

from aoe2modes.lib import mapview

GRASS = 12
WATER = 23
CASTLE = 82
STONE_WALL = 117
GATE = 88


def _scenario(size: int, terrain: list[int], units: list[list[SimpleNamespace]]):
    tiles = [SimpleNamespace(terrain_id=value, elevation=1) for value in terrain]
    return SimpleNamespace(
        map_manager=SimpleNamespace(map_size=size, terrain=tiles),
        unit_manager=SimpleNamespace(units=units),
    )


def _unit(const: int, x: float, y: float, player: int):
    return SimpleNamespace(unit_const=const, x=x, y=y, player=player)


def _split_map():
    """A 12x12 field cut in half by two columns of water, one Castle on each side."""
    size = 12
    terrain = [GRASS] * (size * size)
    for y in range(size):
        terrain[y * size + 5] = WATER
        terrain[y * size + 6] = WATER
    units = [
        [],
        [_unit(CASTLE, 2.0, 2.0, 1)],
        # 10.0 is the true mirror of 2.0 on a 12-wide map: the 4x4 covers tiles 8-11.
        [_unit(CASTLE, 10.0, 2.0, 2)],
    ]
    return _scenario(size, terrain, units)


def _walled_map():
    """A 12x12 field with one wall column at x=3 and a four-tile gate through it."""
    size = 12
    terrain = [GRASS] * (size * size)
    walls = [_unit(STONE_WALL, 3.5, y + 0.5, 1) for y in range(size) if y not in (3, 4, 5, 6)]
    walls.append(_unit(GATE, 3.5, 5.0, 1))
    return _scenario(size, terrain, [[], walls])


# --- footprints ---------------------------------------------------------------------

def test_gate_covers_four_tiles_along_its_integer_axis():
    vertical = mapview._footprint(GATE, 3.5, 5.0)
    horizontal = mapview._footprint(GATE, 5.0, 3.5)

    assert vertical == [(3, 3), (3, 4), (3, 5), (3, 6)]
    assert horizontal == [(3, 3), (4, 3), (5, 3), (6, 3)]


def test_unknown_objects_fall_back_to_a_small_footprint():
    # Understating a footprint merges regions; overstating one would invent a wall.
    assert len(mapview._footprint(999_999, 4.5, 4.5)) == 1
    assert len(mapview._footprint(999_999, 4.0, 4.0)) == 4


def test_decorative_objects_do_not_block():
    assert mapview._footprint(285, 4.5, 4.5) == []  # relic


# --- terrain ------------------------------------------------------------------------

def test_water_is_classified_by_name_not_by_a_hardcoded_list():
    assert WATER in mapview.WATER_TERRAINS          # water medium
    assert 22 in mapview.WATER_TERRAINS             # water deep
    assert 4 not in mapview.WATER_TERRAINS          # shallows are a ford
    assert 2 not in mapview.WATER_TERRAINS          # beach is dry land
    assert GRASS not in mapview.WATER_TERRAINS


def test_terrain_colours_fall_back_to_a_family_for_unlisted_ids():
    assert mapview.terrain_color(WATER) == "#3A6089"
    assert mapview.terrain_color(57) == "#223C60"   # water deep ocean, not in the table


# --- analysis -----------------------------------------------------------------------

def test_water_splits_the_map_and_each_side_holds_one_player():
    report = mapview.analyse(_split_map())

    assert report.size == 12
    assert report.land_tiles == 12 * 10
    assert len(report.sealed_regions) == 2
    assert [player.player for player in report.players] == [1, 2]
    # 60 tiles a side, less the 4x4 Castle standing in each.
    assert {player.base_tiles for player in report.players} == {44}


def test_players_are_anchored_symmetrically_not_by_stepping_off_a_castle():
    report = mapview.analyse(_split_map())
    first, second = report.players

    # The map mirrors in x, so the two anchors must mirror too.
    assert first.anchor[1] == second.anchor[1]
    assert first.anchor[0] + second.anchor[0] == report.size - 1
    assert first.territory == second.territory


def test_a_gate_is_the_difference_between_sealed_and_open():
    report = mapview.analyse(_walled_map())

    assert len(report.sealed_regions) == 2   # gate shut: the wall cuts the field
    assert len(report.regions) == 1          # gate open: one field again
    assert sum(player.gates for player in report.players) == 1


def test_terrain_symmetry_is_zero_for_a_mirrored_map():
    report = mapview.analyse(_split_map())

    assert report.terrain_symmetry["mirror x"] == 0
    assert report.object_symmetry["mirror x"] == 0
    assert report.terrain_symmetry["rotate 90"] > 0


def test_summary_names_every_player():
    summary = mapview.analyse(_split_map()).summary(label="fixture.aoe2scenario")

    assert "fixture.aoe2scenario" in summary
    assert "P1" in summary and "P2" in summary
    assert "flat" in summary


# --- rendering ----------------------------------------------------------------------

def _png_size(data: bytes) -> tuple[int, int]:
    assert data[:8] == b"\x89PNG\r\n\x1a\n"
    width, height = struct.unpack(">II", data[16:24])
    return width, height


def test_render_terrain_emits_a_png_scaled_per_tile():
    scenario = _split_map()

    assert _png_size(mapview.render_terrain(scenario, scale=4)) == (48, 48)


def test_render_zones_matches_the_terrain_render_size():
    scenario = _split_map()
    report = mapview.analyse(scenario)

    assert _png_size(mapview.render_zones(scenario, report, scale=3)) == (36, 36)


def test_write_report_inlines_both_renders(tmp_path):
    scenario = _split_map()
    destination = tmp_path / "nested" / "report.html"

    report = mapview.write_report(scenario, destination, title="Fixture Map", scale=2)
    page = destination.read_text(encoding="utf-8")

    assert report.size == 12
    assert "<title>Fixture Map</title>" in page
    assert page.count("data:image/png;base64,") == 2
    assert "prefers-color-scheme" in page          # both themes are defined
    assert "{" not in page.split("<style>")[0]     # no unresolved format placeholders
