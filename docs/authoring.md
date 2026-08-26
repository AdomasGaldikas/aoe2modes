# Authoring a mode

## Layout of a mode

```
modes/<mode_id>/
├── mode.toml     # settings: map, players, teams, resources, which XS to bundle
├── build.py      # logic: triggers, units, anything that needs coordinates
├── xs/           # this mode's XS files
└── README.md     # what the mode is and how it plays
```

The split is the whole design. If a value could reasonably be tweaked by someone who
does not write Python, it belongs in `mode.toml`.

## The build pipeline

`aoe2modes build <id>` runs, in order:

1. **Load** `mode.toml` and validate it. Bad config fails here, before anything else.
2. **Create** a scenario — blank, or read from `scenario.base` if set.
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
