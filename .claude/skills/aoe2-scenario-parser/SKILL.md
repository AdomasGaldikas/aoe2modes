---
name: aoe2-scenario-parser
description: Reference for AoE2ScenarioParser, the Python library behind every .aoe2scenario build in this repo. Use when writing or debugging a mode's build.py, adding triggers/conditions/effects, placing units, editing terrain or elevation, configuring players/diplomacy/disables, embedding XS, using the Area object or data triggers, or looking up dataset names (UnitInfo, BuildingInfo, TechInfo, TerrainId, PlayerId, trigger_lists enums).
---

# AoE2ScenarioParser

Python library for reading and writing `.aoe2scenario` files outside the in-game editor.
Upstream docs: <https://ksneijders.github.io/AoE2ScenarioParser/> — but **this skill is generated
against the version actually installed in this repo**, and upstream is ahead of it in places
(see [Version drift](#version-drift--read-this-first)).

## Version drift — read this first

The repo pins `AoE2ScenarioParser 0.8.4`. Verify before trusting a memory or a doc snippet:

```bash
.venv/Scripts/python -c "import importlib.metadata as m; print(m.version('AoE2ScenarioParser'))"
```

Concrete divergences between the published docs and 0.8.4:

| Docs site says | 0.8.4 actually has |
| --- | --- |
| `from AoE2ScenarioParser.datasets.player_data import Player` | **Does not exist.** Use `from AoE2ScenarioParser.datasets.players import PlayerId` |
| `Player.ONE` | `PlayerId.ONE` |
| `UnitInfo.VILLAGER` | Not a member — use `UnitInfo.VILLAGER_MALE` / `VILLAGER_FEMALE`, or `UnitInfo.vils()` |

When a doc example fails on an import or an enum member, check the installed package rather than
guessing — `dir()` on the module is faster than a web search:

```bash
.venv/Scripts/python -c "from AoE2ScenarioParser.datasets.units import UnitInfo; print([m.name for m in UnitInfo if 'VILLAGER' in m.name])"
```

## Mental model

A scenario is one object; **all editing goes through managers** hanging off it. Nothing is written
until `write_to_file`.

```py
from AoE2ScenarioParser.scenarios.aoe2_de_scenario import AoE2DEScenario

scenario = AoE2DEScenario.from_file("in.aoe2scenario")   # or .from_default() for a blank one
scenario.trigger_manager                                  # triggers, conditions, effects, variables
scenario.unit_manager                                     # units, buildings, heroes, eye candy
scenario.map_manager                                      # terrain, elevation, map size
scenario.player_manager                                   # civs, ages, resources, diplomacy, disables
scenario.option_manager                                   # victory conditions, team/lobby settings
scenario.xs_manager                                       # embedded XS scripts
scenario.message_manager                                  # the in-editor Messages tab
scenario.write_to_file("out.aoe2scenario")                # never the same path as the input
```

In this repo you rarely touch `scenario` directly — a mode's `build(ctx)` gets these pre-aliased as
`ctx.tm`, `ctx.um`, `ctx.mm`, `ctx.pm`, `ctx.xm`. See [Using this from aoe2modes](#using-this-from-aoe2modes).

## References

Load the file for the area you're working in; don't read them all up front.

| File | Contents |
| --- | --- |
| `references/effects.md` | All 104 `trigger.new_effect.*` factories with their exact parameter names |
| `references/conditions.md` | All 41 `trigger.new_condition.*` factories with their exact parameter names |
| `references/managers.md` | Per-manager API: triggers, units, map, players, messages, options |
| `references/datasets.md` | How the datasets work: the `.ID` rule, set helpers, which enum each effect takes |
| `references/values/*.md` | The raw member lists — see below |
| `references/area.md` | The `Area` object — method chaining, patterns, `to_coords`/`to_chunks` |
| `references/xs.md` | `xs_manager`, embedding XS for multiplayer, xs-check configuration |
| `references/data-triggers.md` | Reading areas/tiles/objects/triggers selected in the in-game editor |

Every enum member the library defines is dumped under `references/values/`, one file per dataset, so
you never have to guess a constant name. Open only the one you need:

| File | Members |
| --- | --- |
| `values/units.md` | `UnitInfo` — 498, GAIA-only ones marked |
| `values/buildings.md` | `BuildingInfo` — 235 |
| `values/heroes.md` | `HeroInfo` — 244 |
| `values/techs.md` | `TechInfo` — 589 |
| `values/other.md` | `OtherInfo` — 378 (relics, gold piles, trees, cliffs, eye candy) |
| `values/projectiles.md` | `ProjectileInfo` — 163 |
| `values/terrains.md` | `TerrainId` — 131 |
| `values/trigger-lists.md` | All 45 dropdown enums — 1219 members, e.g. the 147 `ObjectAttribute`s |

For a one-off lookup, grepping the installed package is still cheaper than opening a 500-line file:

```bash
.venv/Scripts/python -c "from AoE2ScenarioParser.datasets.buildings import BuildingInfo; print([m.name for m in BuildingInfo if 'TOWER' in m.name])"
```

## The 30-second version

```py
from AoE2ScenarioParser.datasets.players import PlayerId
from AoE2ScenarioParser.datasets.units import UnitInfo
from AoE2ScenarioParser.datasets.terrains import TerrainId

trigger = scenario.trigger_manager.add_trigger("Wave — P1", looping=True)
trigger.new_condition.timer(timer=20)
trigger.new_effect.create_object(
    object_list_unit_id=UnitInfo.PALADIN.ID,
    source_player=PlayerId.ONE,
    location_x=5, location_y=4,
)

scenario.unit_manager.add_unit(player=PlayerId.ONE, unit_const=UnitInfo.ARCHER.ID, x=10.5, y=10.5)

for tile in scenario.map_manager.get_square_1d(x1=0, y1=0, x2=20, y2=20):
    tile.terrain_id = TerrainId.ROAD
```

Both `new_effect.*` and `new_condition.*` return the object they created, and every field stays
editable afterwards (`effect.message = "..."`), so capture the return value when you need to fix
something up later.

## Gotchas that cost real time

- **`.ID` is mandatory on the info datasets.** `UnitInfo.PALADIN` is an enum entry carrying `ID`,
  `ICON_ID`, `DEAD_ID`, `HOTKEY_ID`, `IS_GAIA_ONLY`. Passing the entry where an int is expected
  writes the wrong number or raises. Always `UnitInfo.PALADIN.ID`.
  `TerrainId` and `PlayerId` are plain `IntEnum`s — no `.ID` there.
- **Never write over your input file.** The parser guards this
  (`settings.ALLOW_OVERWRITING_SOURCE`); a bug mid-build otherwise destroys the source scenario.
- **Whole coordinates put a unit on a tile corner.** `x=15, y=12` sits on the corner; `x=15.5,
  y=12.5` centres it on the tile. Buildings snap to their footprint regardless.
- **Elevation is 0-based.** `elevation=0` is what the editor calls elevation 1. The parser accepts
  arbitrarily high values but the camera clips into the hill above ~20 (~15 on UHD).
- **Maps must be square and ≤ 480.** A non-square or oversized map crashes the game, not the build.
- **`Area.select` is inclusive.** `area.select(1, 1, 3, 3)` selects a 3×3 block.
- **`get_units_in_area(tile1=..., tile2=...)` covers one more tile than the coordinate form**,
  because a `Tile` is a 1×1 square: `Tile(0, 0)` spans x 0→1.
- **Unicode crash on Windows consoles.** The parser prints progress glyphs; a cp1252 stdout raises
  `UnicodeEncodeError` mid-parse. Either silence it (`settings.PRINT_STATUS_UPDATES = False`, which
  `aoe2modes.toolchain.configure` already does) or set `PYTHONIOENCODING=utf-8`.
- **XS must be embedded, never referenced by filename.** DE does not ship loose `.xs` files to other
  players in a lobby. `xs_manager.add_script(xs_string=...)` is the only reliable path — see
  `references/xs.md`.
- **`XsManager.validate` writes its temp file with the platform encoding.** It calls
  `Path.write_text(xs)` with no `encoding=`, so on Windows a non-ASCII character in the bundle is
  written as cp1252 while `xs-check` reads UTF-8 — the result is an opaque "validation failed" with
  no visible errors. Keep bundled XS ASCII-only, or patch the write.
- **`player_manager.active_players` cannot have gaps.** Enabling P4 requires P1–P3 enabled, which is
  why `player.active` is read-only.
- **Diplomacy set per player is one-way.** `p1.set_player_diplomacy([2, 3], DiplomacyState.ALLY)`
  does not ally 2 and 3 back to P1. `player_manager.set_diplomacy_teams(...)` does both directions.

## Global settings

`from AoE2ScenarioParser import settings` — module-level flags; set them before loading a scenario:

```py
settings.PRINT_STATUS_UPDATES = False          # silence the parse/write progress wall
settings.NOTIFY_UNKNOWN_BYTES = False          # silence unknown-byte warnings
settings.ENABLE_XS_CHECK_INTEGRATION = True    # run xs-check on write
settings.ALLOW_OVERWRITING_SOURCE = False      # keep this False
settings.SHOW_SCENARIO_VERSION_WARNINGS = True
settings.SHOW_VARIANT_WARNINGS = True
settings.MAIN_CHARSET, settings.FALLBACK_CHARSET
settings.ALLOW_DIRTY_RETRIEVER_OVERWRITE = False
```

## Using this from aoe2modes

This repo wraps the library; prefer the wrapper when one exists, and reach for the raw API only for
what the wrapper doesn't cover.

- `aoe2modes.lib.triggers` — `on_start`, `every`, `objective`, `announce`, `spawn_units`,
  `attack_move_all`, `defeat_when_object_destroyed`, `set_stance`, `link`
- `aoe2modes.lib.terrain` — `fill`, `rect`, `disc`, `border` instead of hand-looping `get_square_1d`
- `aoe2modes.lib.spawns` — `lane_bases`, `ring_bases`, `block`, `line` for symmetric arena geometry
- `aoe2modes.lib.players` — `set_camera`, `apply_teams`, `set_resources`
- `aoe2modes.lib.heroes` — `HeroLine`, `HeroPool.for_player`, `upgrade_hero`, `make_heroic`, `buff`
- `aoe2modes.lib.xs` — placeholder substitution and bundling; `ctx.add_xs` / `ctx.set_xs_vars`
- `aoe2modes.lib.variables` — trigger-variable ids, mirrored as `const int VAR_*` in `xs/lib/util.xs`

Repo conventions that interact with the library:

- Trigger names carry their owner: `Wave — P3`, `Defeat — P3 loses last castle`. A 400-trigger
  scenario is only navigable in-game if the names sort usefully.
- Builds are deterministic. Runtime randomness belongs in XS, not in the Python build.
- Settings live in `mode.toml`; logic lives in `build.py`.

## Regenerating the generated references

`effects.md`, `conditions.md` and `trigger-list-values.md` are dumped straight from the installed
package rather than transcribed from the docs site. Re-run this after a parser upgrade:

```bash
.venv/Scripts/python .claude/skills/aoe2-scenario-parser/scripts/dump_signatures.py
```
