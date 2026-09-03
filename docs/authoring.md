# Authoring a mode

## Layout of a mode

```
modes/<mode_id>/
├── mode.toml     # settings: map, players, teams, resources, which XS to bundle
├── build.py      # logic: triggers, units, anything that needs coordinates
├── xs/           # this mode's XS files
├── generated/    # decompiled modes only — see "Decompiled modes" below
└── README.md     # what the mode is and how it plays
```

The split is the whole design. If a value could reasonably be tweaked by someone who
does not write Python, it belongs in `mode.toml`.

## The build pipeline

`aoe2modes build <id>` runs, in order:

1. **Load** `mode.toml` and validate it. Bad config fails here, before anything else.
2. **Create** a scenario — blank, or read from `scenario.base` if set. A decompiled
   mode starts blank and rebuilds itself in step 4.
3. **Apply the declarative block**: resize and terraform the map, set player count,
   ages, population caps, resources and diplomacy.
4. **Run `build(ctx)`** from the mode's `build.py`. Everything from step 3 is already
   in place and can be overridden freely.
5. **Bundle XS**: concatenate `xs.include` (repo-wide, from `xs/`) then `xs.scripts`
   (mode-local), substituting `${NAME}` placeholders from `ctx.set_xs_vars(...)`.
6. **Lint the XS** with the bundled `xs-check`. Errors fail the build.
7. **Write** `dist/<filename>.aoe2scenario`.

## Writing `build(ctx)`

```python
def build(ctx: BuildContext) -> None:
    ...
```

`ctx` exposes the managers under short names (`ctx.tm`, `ctx.um`, `ctx.mm`, `ctx.pm`,
`ctx.xm`), the resolved config (`ctx.spec`, `ctx.players`, `ctx.map_size`), and two
XS hooks (`ctx.set_xs_vars(...)`, `ctx.add_xs(...)`).

Reach for `aoe2modes.lib` before writing raw parser calls:

| Module | What it gives you |
| --- | --- |
| `lib.terrain` | `fill`, `rect`, `disc`, `border` |
| `lib.spawns` | `lane_bases`, `ring_bases`, `block`, `line` — symmetric arena geometry |
| `lib.players` | camera placement, team diplomacy, resources |
| `lib.triggers` | `on_start`, `every`, `objective`, `announce`, `spawn_units`, `attack_move_all`, `defeat_when_object_destroyed` |
| `lib.heroes` | hero lines and tiers, `spawn_hero`, `upgrade_hero`, `buff`, `make_heroic` |
| `lib.variables` | the trigger variables XS and triggers share |
| `lib.xs` | placeholder substitution and bundling |

## Decompiled modes

A mode that started life as someone else's `.aoe2scenario` does not have to stay a
binary. `aoe2modes decompile --mode <id>` reads the file and writes Python that
rebuilds it:

```
modes/<mode_id>/generated/
├── __init__.py       # apply(ctx) — runs the stages in order
├── setup.py          # map size, players, lobby options, Messages tab
├── terrain.py        # run-length terrain table (20736 tiles -> ~2000 runs)
├── units.py          # every unit, reference ids preserved
└── triggers/
    ├── __init__.py   # trigger variables + part order + in-editor display order
    └── part_000.py … # ~250 triggers each
```

`build.py` then reads:

```python
from .generated import apply as apply_generated

def build(ctx: BuildContext) -> None:
    apply_generated(ctx)
    # mode changes go here — this runs last and wins
```

Two rules make this workable:

* **Small changes go in `build.py`, after `apply_generated(ctx)`.** It runs last, so it
  can override anything without touching generated files.
* **`generated/` is overwritten by `decompile`.** Once you start editing it by hand,
  stop regenerating — or move the change up into `build.py`.

`mode.toml` keeps a `scenario.reference` pointing at the original file, so
`aoe2modes verify <id>` can rebuild and diff the two content-wise. That check is what
makes decompiling trustworthy; run it after any change to the emitter.

Generated code is excluded from ruff (`extend-exclude` in `pyproject.toml`) — it is
machine-written, with long literal lines and a deliberate star import.

Stage order in `apply(ctx)` is load-bearing: the map is sized before terrain is
painted (resizing rebuilds the terrain array), units are placed before triggers refer
to them, triggers are created in their original order because `activate_trigger`
addresses them positionally, and the `VARIABLES` table in `triggers/__init__.py` is
declared before the first trigger.

Those variable ids come from the original author, not from `lib/variables`. A mode can
also declare more variables in `build.py` after the generated package runs; Ascendants'
final build currently occupies ids 0–112. Inspect both the generated table and the final
scenario before allocating a new id. `add_variable` raises on a duplicate, but only after
the XS side may already have been written with the wrong assumption.

## Sharing between modes

Anything two modes need goes in `src/aoe2modes/lib/` (Python) or `xs/lib/` (XS).
`modes/cba_hero_duel` is deliberately built from the same library as `modes/cba_hero`
to keep that path exercised — only pacing and win conditions differ between them.

## Placeholders in XS

XS has no build system, so constants that Python already knows are injected:

```python
# build.py
ctx.set_xs_vars(WAVE_INTERVAL=20)
```

```c
// xs/main.xs
const int WAVE_INTERVAL_SECONDS = ${WAVE_INTERVAL};
```

A placeholder with no value is a build error, never a silent pass-through.

## Testing a mode in-game

```
aoe2modes build cba_hero --deploy
```

Deploy copies the built file into the game's scenario folder. The folder is detected
automatically for Steam installs (including Proton on Linux); override it with
`AOE2_SCENARIO_DIR` or `--scenario-dir` for anything unusual.

Then: **Single Player → Scenarios**, or host a lobby and pick it under Custom Scenario.

## Conventions

* Trigger names carry their owner: `Wave — P3`, `Defeat — P3 loses last castle`.
  A 400-trigger scenario is only navigable in-game if the names sort usefully.
* Tuning constants live at the top of `build.py` as named module-level values, or in
  `mode.toml` when they are not code.
* Keep `build(ctx)` a readable outline and push the detail into private `_helpers`.
