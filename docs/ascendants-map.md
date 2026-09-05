# Ascendants arena geometry

How the 144×144 map is built, why every coordinate in the source is written once, and
which parts of the arena are load-bearing.

This is the *mechanism*. The exact per-color cell manifests — controller lanes, Castle
rows, spawn pads, destinations, the wall-role table — live in
[`ascendants-control-map.md`](ascendants-control-map.md) and are not repeated here.
Where the map pass sits in the build is described in
[`ascendants-architecture.md`](ascendants-architecture.md).

## One sector, eight ways

The arena is eight identical territories arranged around a central battlefield. Rather
than describing eight of them, Ascendants describes **one** — P3 Green's left-edge frame —
and derives the rest through a single eight-way transform.

```python
from .v2_map import v2_cell_for_player, v2_position_for_player

pad   = v2_cell_for_player(player, 22, 48)        # inclusive tile cell
wall  = v2_position_for_player(player, 39.5, 45.5) # object position
```

### Cells reflect across 143; positions reflect across 144

This is the single easiest thing to get wrong.

| Kind | Reflection axis | Used for |
| --- | --- | --- |
| Inclusive tile cell | `143` (`MAP_SIZE - 1`) | Trigger areas, terrain, spawn pads, destinations |
| Object position | `144` (`MAP_SIZE`) | Unit and building placement, effect locations |

A tile cell is an index into a 0–143 grid; an object position is a point on the 0–144
lattice between them. Even-footprint buildings sit on whole coordinates and reflect across
144, while the tiles under them reflect across 143. Applying the tile transform to a
Castle anchor shifts four mirrored rows by one — which is exactly why
`_mirrored_position_bounds` exists alongside `_mirrored_area_bounds`.

The eight orbit members, in `PlayerId` order:

| Color | Cell transform of `(x, y)` |
| --- | --- |
| P1 Blue | `(y, x)` |
| P2 Red | `(143-y, x)` |
| P3 Green | `(x, y)` |
| P4 Yellow | `(143-x, y)` |
| P5 Teal | `(x, 143-y)` |
| P6 Purple | `(143-x, 143-y)` |
| P7 Gray | `(y, 143-x)` |
| P8 Orange | `(143-y, 143-x)` |

Object positions use the same eight operations with `144` substituted for `143`.

Because the transform is a group action, `_canonical_representative` can reduce any map
cell to its canonical P3 form and `_sector_for` can say which color's territory a cell
belongs to. That is what makes "is this map symmetric?" a decidable question rather than
an eyeball judgement.

### Why this is worth the indirection

The anti-Trebuchet zones are the cautionary tale. They used to be eight hand-written
rectangles, and they had drifted: only one of the eight matched any mirror of another, and
P4/P6/P7/P8's zones stopped at x=123 while their Castle rows sit at 125 — so a Trebuchet
parked beside those four players' Castles was never removed, while the same position in
P1/P2/P3/P5's base was. Deriving all eight from `ANTI_TREB_SOURCE_AREA = (18, 38, 25, 64)`
makes that class of asymmetry **unstateable**, and keeps each zone clear of its own rear
route by construction.

The rule that follows: **never write per-color coordinates.** Write the P3 source constant
and transform it.

## The V2 pass

`v2_map.py::apply_v2_map(ctx)` applies the symmetry blueprint. Its source is an Excel
workbook (`CBA_Hero_Reforged_Evolution_Alpha_Map_Catalogue_V2_Structure_Aware_Exact_Symmetry.xlsx`,
SHA-256 `8f530f…d747dd5c`) that used P3's complete **111-object** sector as the canonical
template and rotated or reflected it into every player position. The workbook is a
historical input; the constants distilled from it now live in `v2_map.py`.

Pass order inside `apply_v2_map`:

1. `_apply_exact_terrain` — write the symmetric terrain (≈4,677 cells changed).
2. `_restore_team_routes` — copying P3's terrain everywhere fills the two allied causeways
   with water; restore **only** the top and bottom corridors, never the side ones, or the
   enemy gets a shortcut.
3. `_trim_corner_team_routes` — flood the empty outer aprons of the four team corners while
   keeping the inner five-tile L routes that meet the side gates.
4. `_apply_exact_objects` — move ≈623 existing objects to their symmetric positions and add
   the 20 missing Stone Wall slots. **Existing reference ids are retained**, so Antidelete
   and every legacy selected-object trigger keeps working.
5. `_align_team_side_gates` — the four corner bases need a teammate gate where the P3
   template has solid wall; `TEAM_GATE_WALL_CUTS` excludes those four slots so V2 does not
   wall the route into a dead end.
6. `_align_role_references` — pin the King and relic-selector objects. Both use unit 434 in
   most sectors, so the transform treats them as one semantic class; without pinning,
   P8's two unit-434 objects can exchange jobs and silently break selected-object triggers.
7. `_align_edge_island_objects` — Gaia's selector props sit outside the player sectors, so
   the workbook's player-object pass never moved them. Rebuild all eight edge islands from
   the complete P3 island.
8. `_compact_rear_boundaries` — move every rear wall to the compact boundary and seal its
   joins.
9. `_tidy_rear_terrain`, `_replace_winter_terrain`, `_remove_default_cliffs`.
10. `_add_complete_rear_walls` — build the continuous rear wall in every sector.

It returns a `V2MapReport` carrying the terrain-change count, the moved-object count, and
the new wall reference ids. `build.py` folds those ids into each color's `Antidelete`
protection, and the expected totals (`EXPECTED_SOURCE_UNITS`, `EXPECTED_SOURCE_CORE`,
`EXPECTED_TERRAIN_CHANGES`, `EXPECTED_EXISTING_MOVES`, `EXPECTED_NEW_WALLS`) are build
assertions: a change to any of them fails closed.

**Ordering consequence:** `apply_v2_map` moves objects and rewrites terrain, so every
build pass that depends on final coordinates must run after it. `_remap_v2_trigger_geometry`
runs immediately afterwards to repair trigger geometry the move invalidated.

## Territory anatomy

Working outward from the map edge in the canonical P3 frame:

| Feature | Canonical x | Notes |
| --- | --- | --- |
| Controller island | 1–9 | Two 9×2 dry tracks, y=60–61 and y=65–66, separated by three rows of Deep Water |
| King island | ornament at (2.5, 39.5) | Scorpion reward and the live-kill King |
| Technology area | Blacksmith detection area (1, 50)–(6, 58) | University and Blacksmith, reached through the rear gate |
| Rear wall + gate | 14.5 | Gate centred at y=54; land inside at x=14–16, water outside at x=8–13 |
| Rear gate path | x=7–16, y=53–55 | Three tiles wide, guaranteed dry |
| Castle row | 19 | Four Castles at y=48, 52, 56, 60 |
| Castle-wave pads | 22 | y=48, 52, 55, 59 — units created at cell centres |
| Milestone Hero shore | 15–24, y≈38–43 | The 20-cell ribbon repaired from Beach to Grass 2 |
| Side walls | y=47.5 and 60.5, x=24–38 | The long flanks, removable via the switch gate |
| Front wall/gate row | 39.5 | Three gates at y=50, 54, 58; posts and two added end posts |
| Arena | 40+ | Open battlefield toward the center |

The center reward zone is the square `(65, 65)–(78, 78)`, and the allied causeways are
`(65, 20)–(78, 23)` and `(65, 120)–(78, 123)`.

### The rear boundary and why it moved

The rear wall used to sit at x=10.5, leaving four walkable rows behind every Castle. It now
sits at **x=14.5**: one wall row plus exactly two protected interior rows (ASC-001). Two
sparse rear anchors moved straight inward and six obsolete side overhangs were reused as
rear-wall pieces, so every side terminates exactly on the new boundary and existing
references survive. Continuous one-tile wall slots stop diagonal gaps and make the water
boundary unambiguous.

Inside the boundary is land; outside is water; a three-tile path runs through the gate to
the technology island. All three are stated as source cell sets and transformed, so no
one-off shoreline edit can make one territory larger than another.

### Terrain that lies

Two inherited terrain traps are repaired by name:

- **Beach.** It looks like dry sand and **rejects normal building placement in DE**. The
  milestone shore inherited a 20-cell Beach ribbon; `SOURCE_MILESTONE_SHORE_BEACH_TILES`
  names those exact cells and replaces them with Grass 2, leaving the surrounding grass,
  water, flags and hero landing tile untouched (ASC-016).
- **Winter terrain.** `WINTER_TERRAIN_REPLACEMENTS` maps Snow → Grass 2 and Beach Ice /
  Ice → Beach, so the arena reads as grass and sand everywhere while water and buildability
  stay intact.

The one place snow survives is deliberate: the HOLD/OFF pads on the controller tracks,
where the visible snow/road boundary **is** the level 0/1 trigger boundary.

### Front entrance colouring

`FRONT_ENTRANCE_TERRAINS` gives each color a distinct terrain in its front entrance tiles
(Road Gravel, Dirt 4, Grass 1, Desert Sand, Grass 3, Road Fungus, Road, Dirt 1). It is
cosmetic orientation help, not a gameplay surface.

## Gates and walls rotate with the axis

A gate has separate horizontal and vertical unit ids, and straight Stone Wall artwork has
a rotation field. Four of the eight transforms are transposes, so a naive copy leaves half
the map with sideways gates and wall art — the visible half of ASC-003.

- `_transformed_gate` picks the correct gate id for the target sector's axis.
- `_transformed_wall_rotation` rotates straight wall runs: rotation 0 is horizontal, 1 is
  vertical, and 2 is the shared corner/endcap artwork, which is invariant under all eight
  transforms.

`test_evolution_alpha_orients_every_v2_wall_and_gate_by_map_axis` pins every one.

## Protected geometry

Some geometry must survive both the side-wall switch and the 220-wall wipe. The complete
role table is in [`ascendants-control-map.md`](ascendants-control-map.md); the shape of the
rule is:

- **Removable:** the deletable switch gate, the short yard shoulders, the 30 long side
  walls per color.
- **Permanent:** the front gate/wall row (including the two added end posts), the rear
  University wall and its gate, teammate access gates.

Removal is done by **exact object reference**, never by a mirrored inclusive rectangle — a
rectangle cannot distinguish a gate that happens to sit in a shoulder slot from a
removable wall.

The wipe is the inverse problem: `Remove Object` has no exclude-reference option, so
`_wall_wipe_areas` partitions the map *minus* the protected footprints into disjoint
rectangles — 49 of them, covering the 20,368 cells outside 368 protected cells. Merging
identical row spans keeps the one-shot wipe small without ownership swaps or
remove-and-recreate tricks.

The static contract, checked in all eight orientations: after deleting the switch and every
permitted side wall, with all other gates closed, neither the front arena nor the
University area may become reachable from inside the base.

## Reading the map report

```bash
aoe2modes map evolution_alpha --html dist/ascendants-map.html
```

The report renders terrain and zone views, walkable regions with gates open and shut,
symmetry against all eight transforms, per-player parity, and a distance matrix.

It is **not a pass/fail gate** — it is the half of the scenario the trigger tests cannot
see. What to look at:

| Metric | What a change means |
| --- | --- |
| Land / water cell counts | Terrain changed. Intentional? |
| Walkable regions, gates closed | Barriers changed. A drop means something opened |
| Walkable regions, gates open | Route topology changed |
| Symmetry orbits | An asymmetry was introduced — almost always a per-color coordinate |
| Per-player parity | One territory is no longer equal to the others |
| Distance matrix | Spawn-to-center or spawn-to-spawn distances shifted |

A metric that moves without a matching geometry change in the diff is a signal to
investigate before shipping.

## Working on geometry

1. Change the **canonical P3 source constant**, never a per-color value.
2. If you are placing an object, use `v2_position_for_player`; if you are describing a tile
   area, use `v2_cell_for_player`. Mixing them shifts four colors by one tile.
3. If your change depends on final coordinates, it belongs **after** `apply_v2_map` in the
   build order.
4. Update the affected expected total in `v2_map.py` only when you meant to change it — it
   is a guardrail, not a nuisance.
5. Rebuild, run the geometry tests, and re-read the map report.
6. Then walk it in-game. Flood fill is not DE's pathfinder, and that gap is the whole
   reason the issue register has a "Required game check" column.
