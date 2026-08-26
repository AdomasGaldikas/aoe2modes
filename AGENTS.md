# AGENTS.md

Guidance for AI coding agents working in this repository. Kept in sync with
[CLAUDE.md](./CLAUDE.md) — the two files have the same content so tools that
look for either filename (Claude Code, Aider, Codex, and others) find the same
project knowledge. If you edit one, edit the other.

## What this repo is

A Python build pipeline that generates Age of Empires II: Definitive Edition `.aoe2scenario` files from a mix of declarative config (`mode.toml`), Python trigger/unit code (`build.py`), and XS scripts. Focused on CBA Hero-style scenarios. Built on top of `AoE2ScenarioParser`.

The name "aoe2modes" is about *scenario modes* (custom scenarios shipped as a single file). See `docs/tooling.md` for why the parser was chosen and how DE actually distributes XS.

## Common commands

Setup lives in the `Makefile`; the CLI is `aoe2modes` (module: `python -m aoe2modes`).

- `make setup` — create `.venv` and install with dev extras (editable).
- `make build` / `aoe2modes build --all` — build every mode into `dist/`.
- `aoe2modes build <mode_id>` — build one mode.
- `aoe2modes build <mode_id> --deploy` — build and copy into the game's scenario folder (override with `AOE2_SCENARIO_DIR` env var or `--scenario-dir`).
- `aoe2modes list` / `aoe2modes info <mode_id>` — inspect modes without building.
- `aoe2modes new <mode_id>` — scaffold a new mode from `modes/_template`.
- `aoe2modes inspect <file.aoe2scenario> [--triggers]` — summarise a built scenario. First step when reverse-engineering an existing CBA Hero variant.
- `aoe2modes diff <a.aoe2scenario> <b.aoe2scenario>` — structural trigger diff (added / removed / reshaped) between two scenarios. See `src/aoe2modes/lib/diff.py`. Auto-loads newest-first to sidestep the parser version leak below.
- `aoe2modes decompile [--mode <id> | <file> --out <dir>] [--chunk-size N]` — turn an existing scenario into regenerable Python under `generated/`. Splits triggers into `part_N.py` files sized by `--chunk-size` (default 250). See `src/aoe2modes/lib/decompile.py`.
- `aoe2modes verify <mode_id> [--against <file>]` — rebuild a decompiled mode into a tempdir and diff its content against the original it came from. Uses `scenario.reference` in `mode.toml` by default. See `src/aoe2modes/lib/verify.py`.
- `make test` / `pytest` — run tests. `pytest tests/test_build.py::test_cba_hero_has_one_castle_and_hero_per_player` runs a single test. `pytest -k <name>` filters by name.
- `make lint` (ruff check) / `make fmt` (ruff --fix). Ruff config is in `pyproject.toml`; `select = ["E", "F", "I", "UP", "B"]`, line length 110.
- `pytest` runs with `filterwarnings = ["error", ...]` — warnings fail tests. There is one intentional exception for a `player_manager` DeprecationWarning inside `AoE2ScenarioParser`; do not broaden it without cause.

Python 3.11+ is required (uses `tomllib`).

## Architecture: how a build actually happens

The pipeline is defined in `src/aoe2modes/builder.py::build_mode`. Reading that function top-to-bottom is the fastest way to understand the whole system:

1. **Discover** — `registry.discover()` walks `modes/`, skipping `_`/`.`-prefixed dirs, and loads each `mode.toml` via `config.load_mode_spec`. Invalid config raises rather than being silently skipped.
2. **Toolchain configure** — `toolchain.configure()` normalises `AoE2ScenarioParser` settings and chmod's the bundled `xs-check` binary (installs sometimes lack the executable bit, which is why builds silently permission-fail otherwise).
3. **Create scenario** — blank, or from `scenario.base` in the TOML.
4. **Declarative phase** — `terrain.apply_map_spec` and `players.apply_players_spec` apply everything expressible in TOML (map size/terrain, teams, ages, resources, pop cap). This runs *before* the mode's own code so `build.py` can freely override.
5. **Mode's `build(ctx)`** — `_load_build_module` imports `<mode>/build.py` via a synthetic module name (`aoe2modes._modes.<id>`) and calls `build(ctx)`. `ctx` is a `BuildContext` (see `context.py`) — it exposes managers under short aliases (`ctx.tm`, `ctx.um`, `ctx.mm`, `ctx.pm`, `ctx.xm`) because trigger-heavy code is unreadable otherwise.
6. **XS bundle** — `lib/xs.bundle_xs(ctx)` concatenates `xs.include` (repo-wide from `xs/`) then `xs.scripts` (mode-local), substituting `${NAME}` placeholders from `ctx.set_xs_vars(...)`. A missing placeholder is an error, never a silent pass-through.
7. **XS lint + write** — `xs-check` runs; failures raise `BuildError`. Output goes to `dist/<filename>.aoe2scenario`.

### The TOML/Python split is deliberate

`config.py` header states it explicitly: **anything that is "just settings" belongs in `mode.toml`; anything that is logic belongs in `build.py`**. Don't move tunables into Python unless they can't be represented declaratively, and don't push logic into config.

### Three mode flavours: blank / base+patch / decompiled

- **Blank build** (`cba_hero`, `cba_hero_duel`, `_template`): no `scenario.base`. Scenario starts from `from_default()`, and the declarative phase (map + player apply) runs before `build(ctx)`. Trigger and unit content is fully authored in Python.
- **Base+patch** (no mode uses this today; it is the intermediate step on the way to decompiled): `scenario.base = "base.aoe2scenario"`. The base file is opened via `AoE2DEScenario.from_file` and the declarative phase is **skipped** (`builder.py::build_mode` gates it on `spec.base is None`), because otherwise the TOML defaults would resize the map and wipe the base's terrain/players. All modification happens in `build.py` on top of the loaded scenario. Fast to set up, but the base stays a binary blob in git.
- **Decompiled build** (`big_ytri`, `evolution_alpha`): the scenario has been dumped to Python under `modes/<id>/generated/` by `aoe2modes decompile`. `build.py` calls `generated.apply(ctx)` on a blank scenario, then adds any post-generation tweaks. `scenario.reference = "..."` in `mode.toml` points at the original scenario file so `aoe2modes verify <mode>` can prove the code-generated output still matches. This is the diffable, git-friendly end state; base+patch is the intermediate step.
  A decompiled mode always rebuilds at the *current* scenario version, not the original's: the parser only ships blank templates for v1.57 and v1.58, so `big_ytri` moved from v1.51 to v1.58. Content is unchanged — `verify` buckets the v1.55+ fields the old format lacked (`execute_on_load`, `caption_string`, `max_units_affected`, `disable_sound`) as `version_only` rather than differences.

**The reverse-engineering loop** (see `docs/tooling.md` for the surrounding context):

```
aoe2modes inspect X.aoe2scenario           # understand its shape
aoe2modes diff old.aoe2scenario new.aoe2scenario  # spot what changed between versions
aoe2modes decompile --mode <id>            # write generated/ from the base
# edit build.py / generated/, or add post-tweaks after generated.apply(ctx)
aoe2modes verify <id>                      # rebuild + prove content still matches
aoe2modes build <id> --deploy              # ship
```

The decompiler works because `AoE2ScenarioParser`'s effect and condition factories (`NewEffectSupport`, `NewConditionSupport`) have introspectable signatures — the fields a factory *accepts* are exactly the fields we need to read back. `decompile.py` uses `inspect.signature` to derive the schema, then emits only fields that differ from a freshly constructed default. `verify.py` reduces both scenarios to plain-data snapshots (dicts) and diffs field-by-field, with a `version_only` bucket for fields that legitimately exist on the newer rebuild but not on the older original.

### The triggers/XS split is also deliberate

Documented at length in `docs/tooling.md`. Short version:

- **Triggers** know about the map (tile coordinates, unit instances, areas). Use for placement, defeat conditions, one-shot effects.
- **XS** is where counters, timers, scaling formulas, and match state live. It has no direct access to coordinates.
- **The bridge is a trigger variable**: `variables.py` declares ids on the Python side; `xs/lib/util.xs` mirrors them as `const int VAR_*`. Keep both sides in sync when adding one.
- **XS must be embedded, not referenced.** DE does *not* ship loose `.xs` files to other players in a lobby; the parser embeds the whole script into a disabled trigger's script-call effect. This is why the repo keeps XS in normal files and concatenates at build time. `xs_manager.add_script(xs_string=...)` is the only reliable distribution path.

### Shared libraries

`src/aoe2modes/lib/` is where cross-mode helpers live:

| Module | Purpose |
| --- | --- |
| `terrain` | `fill`, `rect`, `disc`, `border` — declarative terraforming |
| `spawns` | `lane_bases`, `ring_bases`, `block`, `line` — symmetric arena geometry, returns `Base` records with `castle`/`center`/`spawn`/`target` tiles |
| `players` | camera placement, team diplomacy, resources |
| `triggers` | `on_start`, `every`, `objective`, `announce`, `spawn_units`, `attack_move_all`, `defeat_when_object_destroyed`, `set_stance` |
| `heroes` | `HeroLine` (an ordered ladder of hero unit ids), `HeroPool.for_player` (deterministic assignment), `upgrade_hero`, `make_heroic`, `buff`, `CLASSIC_LINES` |
| `variables` | trigger-variable ids shared with XS |
| `xs` | placeholder substitution and bundling |
| `diff` | structural trigger diff between two scenarios, used by `aoe2modes diff` |
| `decompile` | read a scenario back as regenerable Python; factory-signature introspection derives the schema |
| `verify` | plain-data snapshot + field diff so a decompiled rebuild can be checked against its original |

`xs/lib/` mirrors this for XS-side shared code (`util.xs`, `random.xs`).

`modes/cba_hero_duel` is intentionally built from the same library as `modes/cba_hero` — only pacing and win conditions differ. When editing a shared helper, check that both consumers still make sense.

### Path resolution

`paths.py::repo_root` walks up from the module's file until it finds `pyproject.toml`, so the CLI works from any subdirectory. `find_game_scenario_dir` handles Windows, macOS, and Linux/Proton install layouts for `--deploy`.

## Project-scoped reference material

`.claude/skills/aoe2-scenario-parser/` is a curated reference for `AoE2ScenarioParser`, generated against the version actually pinned in this repo (0.8.4) rather than the upstream docs (which are ahead in places). Even if your tool cannot invoke a "skill", read these files as markdown when writing or debugging a mode's `build.py`:

- `SKILL.md` — entry point. **The `Version drift` section flags concrete divergences between the upstream docs at ksneijders.github.io/AoE2ScenarioParser and what 0.8.4 actually exposes** (e.g. `PlayerId` instead of `Player`, no `UnitInfo.VILLAGER`). Consult it before trusting an upstream snippet.
- `references/managers.md`, `references/conditions.md`, `references/effects.md`, `references/xs.md`, `references/area.md`, `references/data-triggers.md`, `references/datasets.md` — API and dataset reference.
- `references/values/{buildings,heroes,other,projectiles,techs,terrains,trigger-lists,units}.md` — dataset enum reference; look here for the correct `UnitInfo.*` / `BuildingInfo.*` / `TechInfo.*` name before guessing.
- `scripts/dump_signatures.py` — extracts signatures from the installed parser; run against `.venv/` when a doc example fails and you need ground truth.

Prefer these over `WebFetch`-ing upstream docs when writing code for this repo.

## AoE2ScenarioParser gotchas (documented in `toolchain.py`)

Three quirks in the pinned parser (v0.8.4) that this repo works around:

1. **Version-scoped global state leak.** Once a v1.51 scenario is loaded in a Python process, any subsequent v1.58 load (`from_default()` or `from_file()`) crashes with `UnsupportedAttributeError: 'execute_on_load' is supported since 1.55`. The workaround is `builder.build_order()`, which sorts specs newest-first by `scenario.version` in the TOML — used by both the CLI and the test fixture. Modes with a base **must** declare `scenario.version` so the sort key is accurate. The `diff` command peeks the 4-byte ASCII version stamp at the start of each file to load newest-first automatically.
2. **XS temp-file encoding bug on Windows.** `XsManager.validate` writes the XS temp file with the platform default encoding (cp1252 on Windows), but `xs-check` refuses non-UTF-8 input. The parser reports "XS validation failed" with no visible errors. `toolchain._patch_xs_validate_encoding` monkey-patches the method to write UTF-8. Idempotent; applied every `toolchain.configure()`.
3. **`xs-check` executable bit missing** on some installs. `toolchain.ensure_xs_check_executable()` repairs it in place.

If the parser is upgraded past 0.8.x, re-check whether these workarounds are still needed. The pin lives in `pyproject.toml`.

Related: parser status output uses emoji (`\U0001f504`) that Windows `cp1252` cannot encode. Run with `PYTHONIOENCODING=utf-8` (or `-X utf8`) if you enable verbose mode on Windows, otherwise `s_print` failures silently break status reporting.

## Conventions worth preserving

- **Trigger names carry their owner**: `Wave — P3`, `Defeat — P3 loses last castle`. A 400-trigger scenario is only navigable in-game if the names sort usefully. Keep this pattern when adding new triggers.
- **Determinism**: hero assignment via `HeroPool.for_player` is deterministic so builds reproduce. If a mode wants runtime randomness (player rolls a hero), drive it from XS and keep the Python build deterministic.
- **Mode folder name must match `mode.id`** in `mode.toml`. `config.load_mode_spec` enforces this.
- **Do not silently skip malformed modes.** `registry.discover` raises on bad TOML; keep that behaviour.
