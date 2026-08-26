# The `Area` object

`Area` turns "the ring of tiles six out from this castle" into one chained expression instead of a
nest of coordinate loops. Every configuration method returns the `Area` itself, so calls chain.

```py
from AoE2ScenarioParser.objects.support.area import Area, AreaAttr, AreaState

area = scenario.new.area()          # bound to the scenario, so it knows the map size
area = Area(map_size=120)           # standalone
```

It pays off for *patterned* selections. For "every tile on the map", loop `map_manager.terrain`
directly.

## The three stages

1. **Select** a rectangle, 2. **restrict** it to a sub-pattern, 3. **convert** it to tiles.

```py
for tile in area.center(castle.x, castle.y).size(4).expand(6).use_only_edge().to_coords():
    unit_manager.add_unit(player=PlayerId.ONE, unit_const=BuildingInfo.STONE_WALL.ID,
                          x=tile.x, y=tile.y)
```

### 1 — Select

```py
select(x1, y1, x2=None, y2=None)     # INCLUSIVE: select(1, 1, 3, 3) is a 3x3 block
select_centered(x, y, dx=1, dy=1)
select_entire_map()
center(x, y) / center_bounded(x, y)  # bounded keeps the selection inside the map
size(n) / width(n) / height(n)
expand(n) / expand_x1(n) / expand_x2(n) / expand_y1(n) / expand_y2(n)
shrink(n) / shrink_x1(n) / shrink_x2(n) / shrink_y1(n) / shrink_y2(n)
move(offset_x=0, offset_y=0)
move_to(corner, x, y)                # corner: 'west' | 'north' | 'east' | 'south'
invert()                             # select everything *outside* the current selection
copy()
```

### 2 — Restrict to a pattern

```py
use_full()                                          # default: every tile in the rectangle
use_only_edge(line_width=None, line_width_x=None, line_width_y=None)
use_only_corners(corner_size=None, corner_size_x=None, corner_size_y=None)
use_pattern_grid(block_size=None, gap_size=None,
                 block_size_x=None, block_size_y=None, gap_size_x=None, gap_size_y=None)
use_pattern_lines(axis=None, gap_size=None, line_width=None)   # axis: 'x' | 'y'
```

Anything with a general `foo_size` also has `foo_size_x` / `foo_size_y` for asymmetric patterns.
The same values can be set after the fact:

```py
area.use_pattern_grid(block_size=3, gap_size=0)
area.use_pattern_grid().attr('block_size', 3).attr('gap_size', 0)
area.use_pattern_grid().attr(AreaAttr.BLOCK_SIZE, 3)
area.use_pattern_grid().attrs(block_size=3, gap_size=0)
```

### 3 — Convert

```py
to_coords(as_terrain=False) -> OrderedSet[Tile | TerrainTile]
to_chunks(as_terrain=False) -> List[OrderedSet[Tile | TerrainTile]]
to_chunk_areas() -> List[Area]
to_dict(prefix='area_')     # {'area_x1': …, …} — feeds straight into effect/condition kwargs
```

`as_terrain=True` returns `TerrainTile` objects (writable `terrain_id` / `elevation` / `layer`)
instead of plain `Tile` coordinate pairs — the same objects `map_manager` hands out.

`to_coords` flattens everything into one set. `to_chunks` keeps each grid block or line separate,
which is what you want when the pattern itself matters (alternating colours, one spawn per block).

`to_dict` is the bridge back into triggers:

```py
trigger.new_effect.create_object(**area.select(10, 10, 20, 20).to_dict(), source_player=PlayerId.ONE)
```

### Inspect

```py
get_selection() / get_raw_selection() / get_center() / get_center_int()
get_dimensions() / get_width() / get_height() / get_range_x() / get_range_y()
is_within_bounds() / is_within_selection(x=-1, y=-1, tile=None)
x1 / y1 / x2 / y2 / state / map_size / corner1 / corner2
```

## Worked example — checkerboard terrain

```py
area = scenario.new.area()
area.select_entire_map().use_pattern_grid(block_size=3, gap_size=0)

for index, chunk in enumerate(area.to_chunks(as_terrain=True)):
    for terrain_tile in chunk:
        row = index // (map_manager.map_size / 3)      # 3 == the grid block size
        terrain_tile.terrain_id = TerrainId.BLACK if (index + row) % 2 == 0 else TerrainId.ICE
```

The `+ row` matters: with an even number of blocks per row, alternating on `index` alone produces
stripes rather than a checkerboard.

## In this repo

`aoe2modes.lib.terrain` (`fill`, `rect`, `disc`, `border`) and `aoe2modes.lib.spawns` (`lane_bases`,
`ring_bases`, `block`, `line`) already cover the shapes the modes need, and return the repo's own
`Tile`-based records. Reach for `Area` when you need a pattern those don't express — grids, lines,
corners, inverted selections.
