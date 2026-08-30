"""Render a built scenario's map as a self-contained HTML report.

``aoe2modes inspect`` answers *what is in this file*; this module answers *what shape
is the map*.  It reads terrain and object placement out of a parsed scenario, derives
the walkable regions, measures how far every player is from the middle and from each
other, and writes a single HTML file with the renders inlined as data URIs.

Three things are worth knowing before trusting a number out of here:

* **Footprints come from a table, not the game.** ``AoE2ScenarioParser`` does not carry
  building dimensions, so :data:`FOOTPRINTS` lists the ones that matter for connectivity
  and everything else falls back to a deliberately *small* guess (2x2 for a building on
  an integer tile centre, 1x1 on a half tile).  Under-stating a footprint merges regions;
  over-stating one would invent walls that are not there, which is the worse failure for a
  report that claims a base is sealed.
* **Gates are modelled both ways.** Regions are computed once with gates open (how a match
  actually plays) and once with them shut (which proves whether a base has any other way
  in).  Both counts are reported.
* **Distances are tile steps, not seconds.** Eight-neighbour breadth-first search between
  player anchors, so an even-sized map yields a one-step parity spread between mirrored
  positions.  That is the grid, not an asymmetry.

The renderer writes PNG bytes directly through ``zlib`` — Pillow is not a dependency of
this repo and one image encoder is cheaper than one more install step.
"""

from __future__ import annotations

import base64
import html
import struct
import zlib
from collections import Counter, defaultdict, deque
from collections.abc import Callable, Iterable, Sequence
from dataclasses import dataclass, field
from typing import Any

# --- terrain -----------------------------------------------------------------------

def _terrain_names() -> dict[int, str]:
    from AoE2ScenarioParser.datasets.terrains import TerrainId

    names: dict[int, str] = {}
    for member in TerrainId:
        names.setdefault(int(member), member.name)
    return names


TERRAIN_NAMES = _terrain_names()

#: Terrain that stops a land unit.  DE's naming is the reliable signal: anything called
#: ``WATER_*`` is water (including ``WATER_YELLOW_SHALLOW``), while ``SHALLOWS*`` is a
#: ford that land units walk straight through, and ``WATER_2D_BRIDGE`` is a bridge.
WATER_TERRAINS = frozenset(
    terrain_id
    for terrain_id, name in TERRAIN_NAMES.items()
    if "WATER" in name and "BRIDGE" not in name
)

# Explicit colours for the terrain a CBA map actually uses; everything else is classified
# by name so an unfamiliar map still renders in sensible families rather than magenta.
_TERRAIN_COLORS: dict[int, str] = {
    0: "#6C8A48",    # grass 1
    2: "#CEBE8C",    # beach
    9: "#688446",    # grass 3
    12: "#5E7B45",   # grass 2
    14: "#C6B07E",   # desert sand
    20: "#3A502C",   # forest oak bush
    22: "#223C60",   # water deep
    23: "#3A6089",   # water medium
    24: "#8C826E",   # road
    42: "#8C7050",   # dirt 4
    75: "#78785E",   # road fungus
    78: "#96927E",   # road gravel
}

_TERRAIN_FAMILIES: tuple[tuple[str, str], ...] = (
    ("WATER_DEEP", "#223C60"),
    ("WATER", "#3A6089"),
    ("SHALLOW", "#4A7A9C"),
    ("BEACH", "#CEBE8C"),
    ("FOREST", "#3A502C"),
    ("GRASS", "#5E7B45"),
    ("FARM", "#9A8A50"),
    ("DESERT", "#C6B07E"),
    ("SAND", "#C6B07E"),
    ("DIRT", "#8C7050"),
    ("GRAVEL", "#8E8A78"),
    ("ROAD", "#96927E"),
    ("SNOW", "#D6DCDE"),
    ("ICE", "#B9C8D0"),
    ("BLACK", "#101418"),
)
_TERRAIN_FALLBACK = "#5E7B45"


def terrain_color(terrain_id: int) -> str:
    """A stable colour for one terrain id: explicit first, then by name family."""
    explicit = _TERRAIN_COLORS.get(terrain_id)
    if explicit:
        return explicit
    name = TERRAIN_NAMES.get(terrain_id, "")
    for token, color in _TERRAIN_FAMILIES:
        if token in name:
            return color
    return _TERRAIN_FALLBACK

# --- objects -----------------------------------------------------------------------

#: Tile footprint per object id, for the objects that decide whether a region is sealed.
#: Anything absent falls back to :func:`_fallback_size`.
FOOTPRINTS: dict[int, int] = {
    12: 3,     # barracks
    45: 3,     # dock
    49: 3,     # siege workshop
    68: 2,     # mill
    70: 2,     # house
    72: 1,     # palisade wall
    79: 1,     # watch tower
    82: 4,     # castle
    87: 3,     # archery range
    101: 3,    # stable
    103: 3,    # blacksmith
    104: 3,    # monastery
    109: 4,    # town centre
    117: 1,    # stone wall
    155: 1,    # fortified wall
    209: 4,    # university
    234: 1,    # guard tower
    235: 1,    # keep
    236: 1,    # bombard tower
    562: 2,    # lumber camp
    584: 2,    # mining camp
    598: 1,    # outpost
    684: 1,    # the accursed tower
    685: 1,    # the tower of flies
}

#: Gates are four tiles long along whichever axis carries the integer coordinate.
GATE_IDS = frozenset({64, 88, 659, 660, 661, 662, 663, 664, 667, 669, 671, 673})

#: Objects that never block movement even though they sit on a tile.
_NON_BLOCKING = frozenset(
    {285, 434, 499, 548, 594, 600, 601, 602, 603, 706, 711, 720, 731, 838, 2254}
)

PLAYER_COLORS: dict[int, str] = {
    1: "#3E6FC9", 2: "#BE3B3B", 3: "#3D9A4C", 4: "#A88F16",
    5: "#2E9BA6", 6: "#9A4CB0", 7: "#6E767C", 8: "#D2761F",
}

# Roles a walkable region can play, in the order they are reported.
ARENA = "arena"
BASE = "base"
LINKED = "linked"
ISLAND = "island"

_STEPS_8 = ((1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1))
_STEPS_4 = ((1, 0), (-1, 0), (0, 1), (0, -1))


def _fallback_size(x: float, y: float) -> int:
    """Guess a footprint for an object missing from :data:`FOOTPRINTS`.

    A tile centre at ``x.0`` means an even footprint, ``x.5`` an odd one.  Guessing small
    keeps the report honest: a missed blocker merges two regions, an invented one would
    claim a base is sealed when it is not.
    """
    return 2 if float(x).is_integer() and float(y).is_integer() else 1


def _footprint(const: int, x: float, y: float) -> list[tuple[int, int]]:
    """Tiles covered by one object, or an empty list when it does not block."""
    if const in _NON_BLOCKING:
        return []
    if const in GATE_IDS:
        if float(x).is_integer():
            return [(int(x) - 2 + step, int(y)) for step in range(4)]
        return [(int(x), int(y) - 2 + step) for step in range(4)]
    size = FOOTPRINTS.get(const)
    if size is None:
        size = _fallback_size(x, y)
    left, top = int(x - size / 2), int(y - size / 2)
    return [(left + dx, top + dy) for dx in range(size) for dy in range(size)]


# --- map transforms ----------------------------------------------------------------

def _transforms(size: int) -> dict[str, Callable[[int, int], tuple[int, int]]]:
    """The eight symmetries of the square, on tile indices."""
    last = size - 1
    return {
        "mirror x": lambda x, y: (last - x, y),
        "mirror y": lambda x, y: (x, last - y),
        "rotate 180": lambda x, y: (last - x, last - y),
        "rotate 90": lambda x, y: (y, last - x),
        "rotate 270": lambda x, y: (last - y, x),
        "diagonal": lambda x, y: (y, x),
        "anti-diagonal": lambda x, y: (last - y, last - x),
    }


# --- report ------------------------------------------------------------------------

@dataclass(frozen=True)
class Placement:
    const: int
    x: float
    y: float
    player: int


@dataclass
class Region:
    """One connected run of walkable tiles."""

    tiles: int
    bbox: tuple[int, int, int, int]
    role: str
    players: tuple[int, ...] = ()
    gate_owners: tuple[int, ...] = ()

    @property
    def label(self) -> str:
        if self.role == ARENA:
            return "shared arena"
        if self.role == BASE:
            owners = ", ".join(f"P{player}" for player in self.players)
            return f"base — {owners}"
        if self.role == LINKED:
            owners = ", ".join(f"P{player}" for player in self.gate_owners)
            return f"gated area — {owners}" if owners else "gated area"
        return "island (no land route)"


@dataclass
class PlayerReport:
    player: int
    anchor: tuple[int, int]
    objects: int
    kinds: int
    base_tiles: int
    gates: int
    territory: int
    to_centre: int | None
    distances: dict[int, int] = field(default_factory=dict)


@dataclass
class MapReport:
    """Everything the HTML page and the CLI summary are rendered from."""

    size: int
    terrain: Counter
    elevations: Counter
    land_tiles: int
    walkable_open: int
    objects: int
    regions: list[Region]
    sealed_regions: list[Region]
    players: list[PlayerReport]
    contested: int
    terrain_symmetry: dict[str, int]
    object_symmetry: dict[str, int]
    centre: tuple[int, int]

    # -- derived views used by both outputs ---------------------------------------

    @property
    def water_tiles(self) -> int:
        return self.size * self.size - self.land_tiles

    def region_classes(self) -> list[tuple[str, int, int, tuple[int, int, int, int]]]:
        """Regions grouped as ``(label, tile count, how many, example bbox)``."""
        grouped: dict[tuple[str, int], list[Region]] = defaultdict(list)
        for region in self.sealed_regions:
            key = (region.role if region.role != BASE else BASE, region.tiles)
            grouped[key].append(region)
        rows = []
        for (role, tiles), members in grouped.items():
            label = members[0].label if role != BASE else "base pocket"
            rows.append((label, tiles, len(members), members[0].bbox))
        rows.sort(key=lambda row: (-row[1], row[0]))
        return rows

    def summary(self, *, label: str | None = None) -> str:
        lines = []
        if label:
            lines.append(f"file        {label}")
        lines.append(
            f"map         {self.size}x{self.size}  "
            f"({self.land_tiles} land, {self.water_tiles} water)"
        )
        lines.append(f"objects     {self.objects}")
        flat = len(self.elevations) == 1
        elevation = "flat" if flat else f"{len(self.elevations)} levels"
        lines.append(f"elevation   {elevation}")
        best = min(self.terrain_symmetry.items(), key=lambda item: item[1], default=None)
        if best:
            lines.append(f"symmetry    best under {best[0]}: {best[1]} mismatched tiles")
        lines.append(
            f"regions     {len(self.sealed_regions)} with gates shut, "
            f"{len(self.regions)} with gates open"
        )
        for player in self.players:
            centre = "-" if player.to_centre is None else str(player.to_centre)
            lines.append(
                f"  P{player.player:<2}      {player.objects:>4} objects  "
                f"base {player.base_tiles:>5} tiles  territory {player.territory:>5}  centre {centre:>4}"
            )
        return "\n".join(lines)


# --- analysis ----------------------------------------------------------------------

def _placements(scenario: Any) -> list[Placement]:
    out = []
    for owner in scenario.unit_manager.units:
        for unit in owner:
            out.append(Placement(int(unit.unit_const), float(unit.x), float(unit.y), int(unit.player)))
    return out


def _blocked(size: int, placements: Iterable[Placement], *, gates_block: bool) -> list[list[bool]]:
    grid = [[False] * size for _ in range(size)]
    for item in placements:
        if item.const in GATE_IDS and not gates_block:
            continue
        for x, y in _footprint(item.const, item.x, item.y):
            if 0 <= x < size and 0 <= y < size:
                grid[y][x] = True
    return grid


def _walkable(size: int, terrain: Sequence[int], blocked: list[list[bool]]) -> list[list[bool]]:
    return [
        [terrain[y * size + x] not in WATER_TERRAINS and not blocked[y][x] for x in range(size)]
        for y in range(size)
    ]


def _components(size: int, walkable: list[list[bool]]) -> list[list[tuple[int, int]]]:
    seen = [[False] * size for _ in range(size)]
    out = []
    for y in range(size):
        for x in range(size):
            if seen[y][x] or not walkable[y][x]:
                continue
            stack = [(x, y)]
            seen[y][x] = True
            tiles = []
            while stack:
                cx, cy = stack.pop()
                tiles.append((cx, cy))
                for dx, dy in _STEPS_4:
                    nx, ny = cx + dx, cy + dy
                    if 0 <= nx < size and 0 <= ny < size and not seen[ny][nx] and walkable[ny][nx]:
                        seen[ny][nx] = True
                        stack.append((nx, ny))
            out.append(tiles)
    out.sort(key=len, reverse=True)
    return out


def _bbox(tiles: Sequence[tuple[int, int]]) -> tuple[int, int, int, int]:
    xs = [tile[0] for tile in tiles]
    ys = [tile[1] for tile in tiles]
    return min(xs), min(ys), max(xs), max(ys)


def _bfs(size: int, walkable: list[list[bool]], start: tuple[int, int]) -> dict[tuple[int, int], int]:
    if not walkable[start[1]][start[0]]:
        start = _nearest_walkable(size, walkable, start)
        if start is None:
            return {}
    dist = {start: 0}
    queue = deque([start])
    while queue:
        current = queue.popleft()
        for dx, dy in _STEPS_8:
            nx, ny = current[0] + dx, current[1] + dy
            if 0 <= nx < size and 0 <= ny < size and (nx, ny) not in dist and walkable[ny][nx]:
                dist[(nx, ny)] = dist[current] + 1
                queue.append((nx, ny))
    return dist


def _nearest_walkable(
    size: int, walkable: list[list[bool]], start: tuple[int, int]
) -> tuple[int, int] | None:
    """A player's anchor often lands inside its own Castle; step out to the nearest tile."""
    for radius in range(1, size):
        for dx in range(-radius, radius + 1):
            for dy in (-radius, radius):
                for x, y in ((start[0] + dx, start[1] + dy), (start[0] + dy, start[1] + dx)):
                    if 0 <= x < size and 0 <= y < size and walkable[y][x]:
                        return (x, y)
    return None


def _home_regions(
    placements: Sequence[Placement], region_of: dict[tuple[int, int], int]
) -> dict[int, int]:
    """Match each player to the sealed region their own buildings enclose.

    Picking a tile near a player's Castles instead would quietly break symmetry: the
    centroid of a Castle row lands *inside* a Castle, and "step outwards until walkable"
    resolves in a different direction for a base that faces north than for its mirror
    facing south.  Counting how many of a player's footprint tiles touch each region has
    no such preferred direction.
    """
    touching: dict[int, Counter] = defaultdict(Counter)
    for item in placements:
        if not item.player:
            continue
        for x, y in _footprint(item.const, item.x, item.y):
            for dx, dy in _STEPS_4:
                region = region_of.get((x + dx, y + dy))
                if region is not None:
                    touching[item.player][region] += 1

    homes = {}
    for player, counts in sorted(touching.items()):
        # Ties break on the lower region index, which is the larger region.
        homes[player] = min(counts.items(), key=lambda item: (-item[1], item[0]))[0]
    return homes


def _region_anchor(tiles: Sequence[tuple[int, int]]) -> tuple[int, int]:
    """The tile of a region closest to its own centroid — mirror-stable by construction."""
    cx = sum(tile[0] for tile in tiles) / len(tiles)
    cy = sum(tile[1] for tile in tiles) / len(tiles)
    return min(tiles, key=lambda tile: ((tile[0] - cx) ** 2 + (tile[1] - cy) ** 2, tile[1], tile[0]))


def _symmetry(size: int, terrain: Sequence[int]) -> dict[str, int]:
    out = {}
    for name, fn in _transforms(size).items():
        mismatched = 0
        for y in range(size):
            row = y * size
            for x in range(size):
                tx, ty = fn(x, y)
                if terrain[row + x] != terrain[ty * size + tx]:
                    mismatched += 1
        out[name] = mismatched
    return out


def _placement_transforms(size: int) -> dict[str, Callable[[float, float], tuple[float, float]]]:
    """The same eight symmetries, on continuous object coordinates.

    Objects are not tiles: a 1x1 sits at ``x.5`` and a 4x4 at ``x.0``, so mirroring has to
    reflect the coordinate itself (``size - x``).  Reflecting the tile index and re-adding
    the fraction lands an even-footprint building one tile off its true mirror.
    """
    return {
        "mirror x": lambda x, y: (size - x, y),
        "mirror y": lambda x, y: (x, size - y),
        "rotate 180": lambda x, y: (size - x, size - y),
        "rotate 90": lambda x, y: (y, size - x),
        "rotate 270": lambda x, y: (size - y, x),
        "diagonal": lambda x, y: (y, x),
        "anti-diagonal": lambda x, y: (size - y, size - x),
    }


def _object_symmetry(size: int, placements: Sequence[Placement]) -> dict[str, int]:
    """How many objects have no counterpart under each transform, ignoring ownership."""
    present = Counter((item.const, item.x, item.y) for item in placements)
    out = {}
    for name, fn in _placement_transforms(size).items():
        missing = 0
        for (const, x, y), count in present.items():
            mirrored_x, mirrored_y = fn(x, y)
            if present.get((const, mirrored_x, mirrored_y), 0) != count:
                missing += count
        out[name] = missing
    return out


def analyse(scenario: Any) -> MapReport:
    """Measure a parsed scenario.  Pure computation — nothing is written."""
    size = int(scenario.map_manager.map_size)
    tiles = scenario.map_manager.terrain
    terrain = [int(tile.terrain_id) for tile in tiles]
    elevations = Counter(int(tile.elevation) for tile in tiles)
    placements = _placements(scenario)

    open_walk = _walkable(size, terrain, _blocked(size, placements, gates_block=False))
    shut_walk = _walkable(size, terrain, _blocked(size, placements, gates_block=True))
    land_tiles = sum(1 for value in terrain if value not in WATER_TERRAINS)

    centre = (size // 2, size // 2)

    open_regions = _components(size, open_walk)
    shut_regions = _components(size, shut_walk)

    # Which sealed region each player sits in, and which regions their gates touch.
    region_of: dict[tuple[int, int], int] = {}
    for index, tiles_in_region in enumerate(shut_regions):
        for tile in tiles_in_region:
            region_of[tile] = index

    homes = _home_regions(placements, region_of)
    holders: dict[int, set[int]] = defaultdict(set)
    for player, home in homes.items():
        holders[home].add(player)
    anchors = {player: _region_anchor(shut_regions[home]) for player, home in homes.items()}

    gate_owners: dict[int, set[int]] = defaultdict(set)
    gate_counts: Counter = Counter()
    for item in placements:
        if item.const not in GATE_IDS:
            continue
        gate_counts[item.player] += 1
        for x, y in _footprint(item.const, item.x, item.y):
            for dx, dy in _STEPS_4:
                neighbour = region_of.get((x + dx, y + dy))
                if neighbour is not None:
                    gate_owners[neighbour].add(item.player)

    def _describe(index: int, tiles_in_region: Sequence[tuple[int, int]], largest: int) -> Region:
        if index in holders:
            role = BASE
        elif index == largest:
            role = ARENA
        elif index in gate_owners:
            role = LINKED
        else:
            role = ISLAND
        return Region(
            tiles=len(tiles_in_region),
            bbox=_bbox(tiles_in_region),
            role=role,
            players=tuple(sorted(holders.get(index, ()))),
            gate_owners=tuple(sorted(gate_owners.get(index, ()))),
        )

    biggest_shut = max(range(len(shut_regions)), key=lambda i: len(shut_regions[i])) if shut_regions else -1
    sealed = [_describe(i, tiles_in, biggest_shut) for i, tiles_in in enumerate(shut_regions)]
    open_listing = [
        Region(tiles=len(tiles_in), bbox=_bbox(tiles_in), role=ARENA if i == 0 else ISLAND)
        for i, tiles_in in enumerate(open_regions)
    ]

    # Distances and territory, with gates open — that is how a match actually moves.
    reach = {player: _bfs(size, open_walk, anchor) for player, anchor in anchors.items()}
    territory: Counter = Counter()
    contested = 0
    for y in range(size):
        for x in range(size):
            if not open_walk[y][x]:
                continue
            best = None
            winners: list[int] = []
            for player, dist in reach.items():
                value = dist.get((x, y))
                if value is None:
                    continue
                if best is None or value < best:
                    best, winners = value, [player]
                elif value == best:
                    winners.append(player)
            if len(winners) == 1:
                territory[winners[0]] += 1
            elif winners:
                contested += 1

    base_tiles = {player: len(shut_regions[home]) for player, home in homes.items()}
    objects_by_player = Counter(item.player for item in placements)
    kinds_by_player: dict[int, set[int]] = defaultdict(set)
    for item in placements:
        kinds_by_player[item.player].add(item.const)

    players = [
        PlayerReport(
            player=player,
            anchor=anchor,
            objects=objects_by_player[player],
            kinds=len(kinds_by_player[player]),
            base_tiles=base_tiles[player],
            gates=gate_counts[player],
            territory=territory[player],
            to_centre=reach[player].get(centre),
            distances={
                other: reach[player][anchors[other]]
                for other in anchors
                if other != player and anchors[other] in reach[player]
            },
        )
        for player, anchor in sorted(anchors.items())
    ]

    return MapReport(
        size=size,
        terrain=Counter(terrain),
        elevations=elevations,
        land_tiles=land_tiles,
        walkable_open=sum(len(region) for region in open_regions),
        objects=len(placements),
        regions=open_listing,
        sealed_regions=sealed,
        players=players,
        contested=contested,
        terrain_symmetry=_symmetry(size, terrain),
        object_symmetry=_object_symmetry(size, placements),
        centre=centre,
    )


# --- PNG rendering -----------------------------------------------------------------

def _png(width: int, height: int, pixels: bytearray) -> bytes:
    raw = b"".join(
        b"\x00" + bytes(pixels[row * width * 3:(row + 1) * width * 3]) for row in range(height)
    )

    def chunk(kind: bytes, data: bytes) -> bytes:
        return (
            struct.pack(">I", len(data))
            + kind
            + data
            + struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF)
        )

    header = struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)
    return (
        b"\x89PNG\r\n\x1a\n"
        + chunk(b"IHDR", header)
        + chunk(b"IDAT", zlib.compress(raw, 9))
        + chunk(b"IEND", b"")
    )


def _rgb(value: str) -> tuple[int, int, int]:
    value = value.lstrip("#")
    return int(value[0:2], 16), int(value[2:4], 16), int(value[4:6], 16)


def _blit(pixels: bytearray, width: int, x0: int, y0: int, span: int, color: tuple[int, int, int]) -> None:
    height = len(pixels) // (width * 3)
    for dy in range(span):
        y = y0 + dy
        if not 0 <= y < height:
            continue
        for dx in range(span):
            x = x0 + dx
            if 0 <= x < width:
                index = (y * width + x) * 3
                pixels[index], pixels[index + 1], pixels[index + 2] = color


def render_terrain(scenario: Any, *, scale: int = 5) -> bytes:
    """Top-down terrain render with every object painted in its owner's colour."""
    size = int(scenario.map_manager.map_size)
    width = size * scale
    pixels = bytearray(width * width * 3)
    tiles = scenario.map_manager.terrain

    for y in range(size):
        for x in range(size):
            color = _rgb(terrain_color(int(tiles[y * size + x].terrain_id)))
            _blit(pixels, width, x * scale, y * scale, scale, color)

    gaia = _rgb("#A8A8A8")
    for item in _placements(scenario):
        color = _rgb(PLAYER_COLORS[item.player]) if item.player in PLAYER_COLORS else gaia
        footprint = _footprint(item.const, item.x, item.y) or [(int(item.x), int(item.y))]
        for x, y in footprint:
            _blit(pixels, width, x * scale, y * scale, scale, color)
    return _png(width, width, pixels)


def render_zones(scenario: Any, report: MapReport, *, scale: int = 5) -> bytes:
    """The same map coloured by what each walkable region *is*, not what it looks like."""
    size = report.size
    width = size * scale
    pixels = bytearray(width * width * 3)
    for index in range(0, len(pixels), 3):
        pixels[index], pixels[index + 1], pixels[index + 2] = _rgb("#16232E")

    terrain = scenario.map_manager.terrain
    placements = _placements(scenario)
    shut = _walkable(
        size,
        [int(tile.terrain_id) for tile in terrain],
        _blocked(size, placements, gates_block=True),
    )
    regions = _components(size, shut)

    role_colors = {ARENA: "#C6A86E", LINKED: "#78BEEB", ISLAND: "#6E7A85"}
    for tiles_in_region, region in zip(regions, report.sealed_regions, strict=True):
        if region.role == BASE and region.players:
            color = _rgb(PLAYER_COLORS.get(region.players[0], "#78CD82"))
        else:
            color = _rgb(role_colors.get(region.role, "#6E7A85"))
        for x, y in tiles_in_region:
            _blit(pixels, width, x * scale, y * scale, scale, color)

    blocker = _rgb("#46505C")
    blocked = _blocked(size, placements, gates_block=True)
    for y in range(size):
        for x in range(size):
            if blocked[y][x] and int(terrain[y * size + x].terrain_id) not in WATER_TERRAINS:
                _blit(pixels, width, x * scale, y * scale, scale, blocker)
    return _png(width, width, pixels)


# --- HTML --------------------------------------------------------------------------

_DEFAULT_SUBTITLE = (
    "Terrain, walkable regions, gate access and player parity, "
    "measured from the built scenario."
)

_FONTS = (
    "https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500"
    "&family=IBM+Plex+Sans+Condensed:wght@600;700"
    "&family=IBM+Plex+Serif:ital,wght@0,400;0,600;1,400&display=swap"
)

_CSS = """
:root{
  --ground:#E7EBE6; --surface:#F7F9F5; --surface-2:#DCE3DB; --sunken:#D2DBD1;
  --ink:#152229; --ink-2:#3E5155; --muted:#6C7F82; --rule:#C4CEC5;
  --accent:#9E6821; --accent-line:#C9922F; --accent-soft:#EFDDB6;
  --c1:#EDF1F3; --c2:#C9DCE5; --c3:#98BFD1; --c4:#5B9AB6; --c5:#2C6382;
  --t1:#152229; --t2:#152229; --t3:#12242D; --t4:#F7F9F5; --t5:#F7F9F5;
}
@media (prefers-color-scheme: dark){
  :root:not([data-theme="light"]){
    --ground:#0D1821; --surface:#16232E; --surface-2:#1D2F3D; --sunken:#101D26;
    --ink:#DFE8E9; --ink-2:#AEC0C4; --muted:#7F969C; --rule:#2A3D4A;
    --accent:#E0B266; --accent-line:#B98A3F; --accent-soft:#3A2E1B;
    --c1:#16232E; --c2:#1C3A4A; --c3:#265A73; --c4:#377E9C; --c5:#5FA3C6;
    --t1:#AEC0C4; --t2:#CFE0E6; --t3:#E4F0F4; --t4:#0D1821; --t5:#0D1821;
  }
}
:root[data-theme="dark"]{
  --ground:#0D1821; --surface:#16232E; --surface-2:#1D2F3D; --sunken:#101D26;
  --ink:#DFE8E9; --ink-2:#AEC0C4; --muted:#7F969C; --rule:#2A3D4A;
  --accent:#E0B266; --accent-line:#B98A3F; --accent-soft:#3A2E1B;
  --c1:#16232E; --c2:#1C3A4A; --c3:#265A73; --c4:#377E9C; --c5:#5FA3C6;
  --t1:#AEC0C4; --t2:#CFE0E6; --t3:#E4F0F4; --t4:#0D1821; --t5:#0D1821;
}
*{box-sizing:border-box}
html{color-scheme:light dark}
img{max-width:100%}
body{margin:0; background:var(--ground); color:var(--ink);
  font-family:"IBM Plex Serif",Georgia,serif; font-size:16.5px; line-height:1.65;
  -webkit-font-smoothing:antialiased}
h1,h2,.kicker,.stat-v,th,.btn,.chip{font-family:"IBM Plex Sans Condensed","Helvetica Neue",Arial,sans-serif}
code,.mono,.stat-v,td.n,th.n,.matrix td,.matrix th{
  font-family:"IBM Plex Mono",ui-monospace,Consolas,monospace}
main{display:grid; grid-template-columns:minmax(1.25rem,1fr) min(70ch,100%) minmax(1.25rem,1fr);
  padding-bottom:5rem}
main > *{grid-column:2}
.wide{grid-column:1/-1; width:min(1080px,100% - 2.5rem); margin-inline:auto}
header.mast{grid-column:1/-1; border-bottom:1px solid var(--rule); background:var(--surface);
  padding:3rem 1.25rem 2rem; margin-bottom:2.75rem}
.mast-inner{width:min(1080px,100%); margin-inline:auto}
.kicker{font-size:.72rem; letter-spacing:.14em; text-transform:uppercase; color:var(--muted); font-weight:600}
h1{font-size:clamp(2.2rem,6vw,3.6rem); line-height:1.03; font-weight:700; margin:.5rem 0 0;
  letter-spacing:-.015em; text-wrap:balance}
.standfirst{max-width:62ch; margin:1rem 0 0; color:var(--ink-2); font-size:1.05rem}
.mast-meta{display:flex; flex-wrap:wrap; gap:.4rem 1.4rem; margin-top:1.4rem; padding-top:1rem;
  border-top:1px solid var(--rule); font-family:"IBM Plex Mono",monospace; font-size:.78rem;
  color:var(--muted)}
.mast-meta b{color:var(--ink-2); font-weight:500}
section{margin-bottom:3.25rem}
section > .kicker{display:flex; align-items:center; gap:.75rem; margin-bottom:.35rem}
section > .kicker::after{content:""; flex:1; height:1px; background:var(--rule)}
h2{font-size:1.68rem; line-height:1.15; margin:0 0 .85rem; font-weight:700; text-wrap:balance}
p{margin:0 0 1rem}
figure{margin:0 0 1.5rem}
figcaption{font-size:.83rem; color:var(--muted); margin-top:.7rem; max-width:70ch}
.mapfig{display:grid; gap:1.25rem; grid-template-columns:minmax(0,1.35fr) minmax(0,1fr); align-items:start}
@media (max-width:820px){.mapfig{grid-template-columns:1fr}}
.viewport{position:relative; aspect-ratio:1; background:var(--sunken); border:1px solid var(--rule);
  border-radius:3px; overflow:hidden}
.viewport img{position:absolute; inset:0; width:100%; height:100%; image-rendering:pixelated;
  transition:opacity .28s ease}
.viewport img.off{opacity:0}
.tag{position:absolute; transform:translate(-50%,-50%); font-family:"IBM Plex Mono",monospace;
  font-size:.66rem; padding:.05rem .3rem; border-radius:2px; background:rgba(12,22,30,.72);
  color:#F2F6F4; border-bottom:2px solid currentColor; pointer-events:none}
.switch{display:flex; margin-bottom:.75rem; border:1px solid var(--rule); border-radius:3px;
  overflow:hidden; width:max-content}
.btn{font-size:.76rem; font-weight:600; letter-spacing:.05em; text-transform:uppercase;
  padding:.4rem .85rem; background:var(--surface); color:var(--muted); border:0; cursor:pointer;
  border-right:1px solid var(--rule)}
.btn:last-child{border-right:0}
.btn[aria-pressed="true"]{background:var(--accent-soft); color:var(--accent)}
.btn:focus-visible{outline:2px solid var(--accent-line); outline-offset:-2px}
.legend{display:grid; gap:.45rem; margin:0; padding:0; list-style:none}
.legend li{display:grid; grid-template-columns:14px 1fr; gap:.6rem; align-items:baseline;
  font-size:.84rem; color:var(--ink-2)}
.legend i{width:12px; height:12px; border-radius:2px; display:block; transform:translateY(2px);
  border:1px solid rgba(0,0,0,.18)}
.legend b{font-family:"IBM Plex Mono",monospace; font-weight:500; color:var(--ink)}
.stats{display:grid; gap:1px; background:var(--rule);
  grid-template-columns:repeat(auto-fit,minmax(140px,1fr)); border:1px solid var(--rule);
  border-radius:3px; overflow:hidden; margin:1.25rem 0 1.5rem}
.stats > div{background:var(--surface); padding:.85rem 1rem}
.stat-v{font-size:1.5rem; font-weight:500; line-height:1.1; letter-spacing:-.02em;
  font-variant-numeric:tabular-nums}
.stat-l{font-size:.73rem; text-transform:uppercase; letter-spacing:.08em; color:var(--muted);
  margin-top:.25rem; font-family:"IBM Plex Sans Condensed",sans-serif; font-weight:600}
.stat-n{font-size:.8rem; color:var(--ink-2); margin-top:.3rem}
.tw{overflow-x:auto; margin:1.25rem 0 .5rem; border:1px solid var(--rule); border-radius:3px;
  background:var(--surface)}
table{border-collapse:collapse; width:100%; font-size:.87rem}
th,td{padding:.5rem .75rem; text-align:left; border-bottom:1px solid var(--rule)}
thead th{font-size:.7rem; text-transform:uppercase; letter-spacing:.08em; color:var(--muted);
  font-weight:600; background:var(--surface-2); white-space:nowrap}
tbody tr:last-child td{border-bottom:0}
td.n,th.n{text-align:right; font-variant-numeric:tabular-nums; white-space:nowrap}
tbody tr:hover td{background:var(--surface-2)}
.matrix{text-align:center; font-size:.82rem}
.matrix th,.matrix td{padding:.4rem .1rem; text-align:center; border:1px solid var(--ground);
  font-variant-numeric:tabular-nums; min-width:2.9rem}
.matrix thead th,.matrix tbody th{background:var(--surface); color:var(--ink-2)}
.matrix tbody tr:hover td{background:inherit}
.matrix td:hover{outline:2px solid var(--accent-line); outline-offset:-2px}
.d0{background:var(--surface-2); color:var(--muted)}
.d1{background:var(--c2); color:var(--t2)}
.d2{background:var(--c3); color:var(--t3)}
.d3{background:var(--c4); color:var(--t4)}
.d4{background:var(--c5); color:var(--t5)}
.mlegend{display:flex; flex-wrap:wrap; gap:1rem; font-size:.78rem; color:var(--muted);
  margin-top:.75rem; font-family:"IBM Plex Mono",monospace}
.mlegend i{width:16px; height:10px; border-radius:2px; display:inline-block; margin-right:.4rem}
.note{background:var(--sunken); border:1px solid var(--rule); border-radius:3px;
  padding:1.2rem 1.4rem; font-size:.88rem; color:var(--ink-2)}
.note h3{margin:0 0 .5rem; color:var(--ink); font-size:1rem;
  font-family:"IBM Plex Sans Condensed",sans-serif}
.note ul{margin:0; padding-left:1.15rem}
.note li{margin-bottom:.4rem}
.swatch{display:inline-block; width:9px; height:9px; border-radius:2px; margin-right:.45rem;
  transform:translateY(0)}
@media (prefers-reduced-motion:reduce){*{transition:none !important}}
"""

_SCRIPT = """
(function(){
  var bt=document.getElementById('b-terrain'), bz=document.getElementById('b-zones');
  var vt=document.getElementById('v-terrain'), vz=document.getElementById('v-zones');
  if(!bt||!bz){return;}
  function show(zones){
    vz.classList.toggle('off',!zones);
    vt.classList.toggle('off',zones);
    bz.setAttribute('aria-pressed',String(zones));
    bt.setAttribute('aria-pressed',String(!zones));
  }
  bt.addEventListener('click',function(){show(false);});
  bz.addEventListener('click',function(){show(true);});
})();
"""


def _esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def _data_uri(png: bytes) -> str:
    return "data:image/png;base64," + base64.b64encode(png).decode("ascii")


def _terrain_name(terrain_id: int) -> str:
    name = TERRAIN_NAMES.get(terrain_id)
    return name.replace("_", " ").title() if name else f"Terrain {terrain_id}"


def _distance_bucket(value: int, thresholds: Sequence[int]) -> str:
    for index, limit in enumerate(thresholds):
        if value <= limit:
            return f"d{index + 1}"
    return "d4"


def _matrix_section(report: MapReport) -> str:
    players = report.players
    if len(players) < 2:
        return ""
    values = sorted({d for player in players for d in player.distances.values()})
    if not values:
        return ""
    step = max(1, len(values) // 4)
    thresholds = [values[min(len(values) - 1, step * i)] for i in range(1, 4)]

    head = "".join(f"<th>P{player.player}</th>" for player in players)
    rows = []
    for player in players:
        cells = []
        for other in players:
            if other.player == player.player:
                cells.append('<td class="d0">—</td>')
                continue
            value = player.distances.get(other.player)
            if value is None:
                cells.append('<td class="d0">·</td>')
                continue
            css = _distance_bucket(value, thresholds)
            title = f"P{player.player} to P{other.player}: {value} steps"
            cells.append(f'<td class="{css}" title="{_esc(title)}">{value}</td>')
        centre = "—" if player.to_centre is None else str(player.to_centre)
        cells.append(f'<td class="d0">{centre}</td>')
        rows.append(f"<tr><th>P{player.player}</th>{''.join(cells)}</tr>")

    legend = "".join(
        f'<span><i style="background:var(--c{index + 2})"></i>&le; {limit} steps</span>'
        for index, limit in enumerate(thresholds)
    )
    return f"""
<section class="wide">
  <div class="kicker">Distance</div>
  <h2>How far every player is from the fight</h2>
  <p>Tile steps between player anchors with gates open, and to the middle of the map. On an
    even-sized map mirrored positions can differ by one step — that is grid parity, not geometry.</p>
  <div class="tw">
    <table class="matrix">
      <thead><tr><th></th>{head}<th>Centre</th></tr></thead>
      <tbody>{''.join(rows)}</tbody>
    </table>
  </div>
  <div class="mlegend">{legend}<span><i style="background:var(--c5)"></i>farther</span></div>
</section>
"""


def render_html(
    scenario: Any,
    report: MapReport,
    *,
    title: str,
    subtitle: str = "",
    source: str = "",
    scale: int = 5,
) -> str:
    """Build the whole page, images included, as one string."""
    terrain_png = _data_uri(render_terrain(scenario, scale=scale))
    zones_png = _data_uri(render_zones(scenario, report, scale=scale))

    tags = []
    for player in report.players:
        left = player.anchor[0] / report.size * 100
        top = player.anchor[1] / report.size * 100
        color = PLAYER_COLORS.get(player.player, "#A8A8A8")
        tags.append(
            f'<div class="tag" style="left:{left:.1f}%;top:{top:.1f}%;color:{color}">'
            f"P{player.player}</div>"
        )

    terrain_rows = "".join(
        f"<tr><td>{_esc(_terrain_name(terrain_id))}</td><td class='n'>{count}</td>"
        f"<td class='n'>{count / (report.size ** 2) * 100:.1f}%</td></tr>"
        for terrain_id, count in report.terrain.most_common(8)
    )

    region_rows = "".join(
        f"<tr><td>{_esc(label)}</td><td class='n'>{tiles}</td><td class='n'>{count}</td>"
        f"<td class='n'>x{bbox[0]}–{bbox[2]} · y{bbox[1]}–{bbox[3]}</td></tr>"
        for label, tiles, count, bbox in report.region_classes()[:12]
    )

    symmetry_rows = "".join(
        f"<tr><td>{_esc(name)}</td><td class='n'>{count}</td>"
        f"<td class='n'>{report.object_symmetry.get(name, 0)}</td></tr>"
        for name, count in sorted(report.terrain_symmetry.items(), key=lambda item: item[1])
    )

    player_rows = "".join(
        f"<tr><td><span class='swatch' style='background:"
        f"{PLAYER_COLORS.get(player.player, '#A8A8A8')}'></span>P{player.player}</td>"
        f"<td class='n'>{player.objects}</td><td class='n'>{player.kinds}</td>"
        f"<td class='n'>{player.base_tiles or '—'}</td><td class='n'>{player.gates}</td>"
        f"<td class='n'>{player.territory}</td>"
        f"<td class='n'>{player.to_centre if player.to_centre is not None else '—'}</td></tr>"
        for player in report.players
    )

    sealed_bases = [region for region in report.sealed_regions if region.role == BASE]
    base_sizes = {region.tiles for region in sealed_bases}
    sealed_note = (
        f"all {len(sealed_bases)} identical at {next(iter(base_sizes))} tiles"
        if len(base_sizes) == 1 and sealed_bases
        else f"{len(sealed_bases)} found, sizes {sorted(base_sizes)}"
        if sealed_bases
        else "none detected"
    )
    elevation_note = "flat" if len(report.elevations) == 1 else f"{len(report.elevations)} levels"
    best_symmetry = min(report.terrain_symmetry.items(), key=lambda item: item[1], default=("—", 0))

    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{_esc(title)}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{_FONTS}">
<style>{_CSS}</style>
</head>
<body>

<header class="mast">
  <div class="mast-inner">
    <div class="kicker">aoe2modes map report</div>
    <h1>{_esc(title)}</h1>
    <p class="standfirst">{_esc(subtitle or _DEFAULT_SUBTITLE)}</p>
    <div class="mast-meta">
      <span><b>Source</b> {_esc(source or "—")}</span>
      <span><b>Map</b> {report.size}&times;{report.size}</span>
      <span><b>Tiles</b> {report.size ** 2:,}</span>
      <span><b>Objects</b> {report.objects:,}</span>
      <span><b>Players</b> {len(report.players)}</span>
    </div>
  </div>
</header>

<main>

<section class="wide">
  <div class="kicker">The map</div>
  <h2>Terrain, and what each region is for</h2>
  <figure class="mapfig">
    <div>
      <div class="switch" role="group" aria-label="Map view">
        <button class="btn" id="b-terrain" aria-pressed="true" type="button">Terrain</button>
        <button class="btn" id="b-zones" aria-pressed="false" type="button">Zones</button>
      </div>
      <div class="viewport">
        <img id="v-terrain" src="{terrain_png}"
             alt="Top-down terrain render of the map, objects painted in their owner's colour.">
        <img id="v-zones" class="off" src="{zones_png}"
             alt="The same map with each walkable region coloured by role: bases, arena, gated
                  areas and unreachable islands.">
        {''.join(tags)}
      </div>
    </div>
    <div>
      <ul class="legend">
        <li><i style="background:#C6A86E"></i>
          <span><b>Shared arena</b> — the largest region everyone reaches</span></li>
        <li><i style="background:#78CD82"></i>
          <span><b>Player base</b> — a region holding a player's own buildings</span></li>
        <li><i style="background:#78BEEB"></i>
          <span><b>Gated area</b> — reachable only through someone's gate</span></li>
        <li><i style="background:#6E7A85"></i><span><b>Island</b> — no land route at all</span></li>
        <li><i style="background:#46505C"></i>
          <span><b>Blocking objects</b> — walls, gates, buildings</span></li>
      </ul>
      <p style="font-size:.84rem;color:var(--ink-2);margin-top:1.1rem">Zones are computed with every
        gate shut, so a base showing as its own region has no other way in. Elevation is
        {_esc(elevation_note)}.</p>
    </div>
  </figure>

  <div class="stats">
    <div><div class="stat-v">{report.land_tiles:,}</div><div class="stat-l">Land tiles</div>
      <div class="stat-n">{report.land_tiles / (report.size ** 2) * 100:.1f}% of the map</div></div>
    <div><div class="stat-v">{len(report.sealed_regions)}</div><div class="stat-l">Regions, gates shut</div>
      <div class="stat-n">{len(report.regions)} with gates open</div></div>
    <div><div class="stat-v">{sum(player.gates for player in report.players)}</div>
      <div class="stat-l">Gates</div>
      <div class="stat-n">across {len(report.players)} players</div></div>
    <div><div class="stat-v">{report.contested:,}</div><div class="stat-l">Contested tiles</div>
      <div class="stat-n">equidistant between bases</div></div>
    <div><div class="stat-v">{best_symmetry[1]:,}</div><div class="stat-l">Best symmetry</div>
      <div class="stat-n">under {_esc(best_symmetry[0])}</div></div>
  </div>
</section>

<section>
  <div class="kicker">Regions</div>
  <h2>What the map breaks into</h2>
  <p>Every walkable region with all gates shut. Bases: {_esc(sealed_note)}.</p>
  <div class="tw">
    <table>
      <thead><tr><th>Region</th><th class="n">Tiles</th><th class="n">Count</th>
        <th class="n">Example bounds</th></tr></thead>
      <tbody>{region_rows}</tbody>
    </table>
  </div>
</section>

<section>
  <div class="kicker">Symmetry</div>
  <h2>How closely the map mirrors itself</h2>
  <p>Every tile and every object compared against its image under the eight symmetries of the
    square, best match first. Objects are matched on kind and position, ignoring ownership.</p>
  <div class="tw">
    <table>
      <thead><tr><th>Transform</th><th class="n">Terrain mismatches</th>
        <th class="n">Objects unmatched</th></tr></thead>
      <tbody>{symmetry_rows}</tbody>
    </table>
  </div>
</section>

<section>
  <div class="kicker">Players</div>
  <h2>Parity across the slots</h2>
  <div class="tw">
    <table>
      <thead><tr><th>Player</th><th class="n">Objects</th><th class="n">Kinds</th>
        <th class="n">Base tiles</th>
        <th class="n">Gates</th><th class="n">Territory</th><th class="n">To centre</th></tr></thead>
      <tbody>{player_rows}</tbody>
    </table>
  </div>
  <p style="font-size:.83rem;color:var(--muted);margin-top:.4rem">Territory is the nearest-anchor
    partition over walkable tiles with gates open; {report.contested:,} further tiles are tied
    between two or more players and belong to nobody.</p>
</section>

{_matrix_section(report)}

<section>
  <div class="kicker">Terrain</div>
  <h2>What the ground is made of</h2>
  <div class="tw">
    <table>
      <thead><tr><th>Terrain</th><th class="n">Tiles</th><th class="n">Share</th></tr></thead>
      <tbody>{terrain_rows}</tbody>
    </table>
  </div>
</section>

<section>
  <div class="kicker">Method</div>
  <div class="note">
    <h3>How these numbers were produced</h3>
    <ul>
      <li>Terrain and object placement were read with the repo's pinned AoE2ScenarioParser; nothing
        here runs the game.</li>
      <li>A tile is walkable when its terrain is not water and no object footprint covers it.
        Footprints come from a table of the buildings that matter for connectivity; anything else
        falls back to a small guess, which merges regions rather than inventing walls.</li>
      <li>Regions are four-neighbour flood fill. They are computed twice: with gates shut, to show
        what is actually sealed, and with gates open, which is how a match moves.</li>
      <li>Distances are eight-neighbour breadth-first search between player anchors — the centroid of
        a player's Castles, or of all their buildings when they have none.</li>
    </ul>
  </div>
</section>

</main>
<script>{_SCRIPT}</script>
</body>
</html>
"""


def write_report(
    scenario: Any,
    destination: Any,
    *,
    title: str,
    subtitle: str = "",
    source: str = "",
    scale: int = 5,
) -> MapReport:
    """Analyse ``scenario``, write the HTML page to ``destination`` and return the report."""
    report = analyse(scenario)
    page = render_html(
        scenario, report, title=title, subtitle=subtitle, source=source, scale=scale
    )
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(page, encoding="utf-8")
    return report
