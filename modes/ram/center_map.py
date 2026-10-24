"""A broad, cliff-free center hill with approaches through all eight octants."""

from __future__ import annotations

import tomllib
from dataclasses import dataclass

from AoE2ScenarioParser.datasets.other import OtherInfo
from AoE2ScenarioParser.datasets.terrains import TerrainId


@dataclass(frozen=True)
class CenterHillReport:
    """Inclusive tile bounds, elevation and minimum checked approach width."""

    patch_bounds: tuple[int, int, int, int]
    plateau_bounds: tuple[int, int, int, int]
    base_elevation: int
    summit_elevation: int
    approach_width: int


def configure_center_hill(ctx) -> CenterHillReport | None:
    """Raise nested plateaux using the parser's native elevation helper.

    DE stores integer tile elevations, not a separate authored slope mesh. The
    engine renders the intervening slopes. Spaced, one-level transitions in
    every direction preserve the terrain routes; no cliff objects are added.
    These are structural guarantees, not a substitute for live DE pathfinding.
    """
    config = tomllib.loads((ctx.mode_dir / "mode.toml").read_text())
    settings = config.get("center_hill", {})
    if not settings.get("enabled", False):
        return None
    names = ("plateau_half_width", "rise", "slope_step_width", "approach_width")
    for name in names:
        if type(settings.get(name)) is not int or settings[name] <= 0:
            raise ValueError(f"center_hill.{name} must be a positive integer")
    half = settings["plateau_half_width"]
    rise = settings["rise"]
    step = settings["slope_step_width"]
    width = settings["approach_width"]
    if ctx.map_size % 2:
        raise ValueError("center hill requires an even map size for exact eight-way symmetry")
    if rise > 4 or step < 2:
        raise ValueError("center hill needs rise <= 4 and slope_step_width >= 2")
    if width < 5 or width % 2 == 0 or width > 2 * half:
        raise ValueError("center hill approach_width must be odd, >= 5 and fit the plateau")
    center = ctx.map_size // 2
    outer = half + rise * step
    low, high = center - outer, center + outer - 1
    if low < 2 or high >= ctx.map_size - 2:
        raise ValueError("center hill patch leaves insufficient surrounding map")
    plateau_low, plateau_high = center - half, center + half - 1
    capture = config["center"]
    if any(
        capture[f"{axis}1"] < plateau_low or capture[f"{axis}2"] > plateau_high + 1
        for axis in ("x", "y")
    ):
        raise ValueError("center hill plateau must contain the entire capture area and meter")

    # Existing grass/sand and their decorative layers remain untouched. Refuse
    # to silently pave a route through water, structures, resources or cliffs.
    water = {int(terrain) for terrain in TerrainId.water_terrains()}
    patch = ctx.mm.get_square_1d(low, low, high, high)
    levels = {int(tile.elevation) for tile in patch}
    if len(levels) != 1:
        raise ValueError("center hill requires the existing center patch to be flat")
    base = levels.pop()
    if base + rise > 8:
        raise ValueError("center hill summit exceeds the supported modest hill height")
    for tile in patch:
        if tile.terrain_id in water:
            raise ValueError(f"center hill approach contains water at {tile.xy}")
    flags = {OtherInfo.FLAG_A.ID, OtherInfo.FLAG_B.ID, OtherInfo.FLAG_C.ID, OtherInfo.FLAG_D.ID}
    for units in ctx.um.units:
        for unit in units:
            if low - 4 <= unit.x <= high + 5 and low - 4 <= unit.y <= high + 5:
                if unit.unit_const not in flags:
                    raise ValueError(f"center hill approach contains object {unit.reference_id}")

    before = [(tile.terrain_id, tile.elevation, tile.layer) for tile in ctx.mm.terrain]
    for level in range(1, rise + 1):
        radius = half + (rise - level) * step
        ctx.mm.set_elevation(
            base + level,
            center - radius, center - radius,
            center + radius - 1, center + radius - 1,
        )
    for tile, original in zip(ctx.mm.terrain, before, strict=True):
        inside = low <= tile.x <= high and low <= tile.y <= high
        if (tile.terrain_id, tile.layer) != (original[0], original[2]):
            raise RuntimeError("center hill changed terrain or decorative layers")
        if not inside and tile.elevation != original[1]:
            raise RuntimeError(f"center hill escaped its bounded patch at {tile.xy}")
        if inside:
            for dx, dy in ((1, 0), (0, 1), (1, 1), (-1, 1)):
                neighbor = ctx.mm.get_tile(tile.x + dx, tile.y + dy)
                if abs(tile.elevation - neighbor.elevation) > 1:
                    raise RuntimeError(f"center hill has an abrupt elevation edge at {tile.xy}")
            reflected = ctx.mm.get_tile(ctx.map_size - 1 - tile.x, tile.y)
            transposed = ctx.mm.get_tile(tile.y, tile.x)
            if tile.elevation != reflected.elevation or tile.elevation != transposed.elevation:
                raise RuntimeError("center hill lost eight-way elevation symmetry")
    report = CenterHillReport(
        (low, low, high, high),
        (plateau_low, plateau_low, plateau_high, plateau_high),
        base, base + rise, width,
    )
    ctx.log(f"center hill: plateau {report.plateau_bounds}, elevation {base} -> {base + rise}")
    return report
