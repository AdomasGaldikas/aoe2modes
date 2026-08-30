# aoe2modes

A Python build pipeline for **Age of Empires II: Definitive Edition** custom scenarios. Focused on **CBA Hero**-style modes: hero-arena scenarios with automatic wave spawning, castle-as-lives loss conditions, and everything expressed as diffable code rather than binary editor saves.

Built on top of [AoE2ScenarioParser](https://github.com/KSneijders/AoE2ScenarioParser). One `aoe2modes build` command turns a mode's `mode.toml` + `build.py` (+ optional `xs/*.xs`) into a `.aoe2scenario` file the game can load.

## Quick start

```bash
make setup                              # create .venv and install (editable) with dev extras
aoe2modes list                          # every mode in modes/
aoe2modes build --all                   # build all four modes into dist/
aoe2modes build cba_hero --deploy       # build one mode and copy it to the game folder
```

Then in-game: **Single Player → Scenarios**, or host a lobby and pick it under Custom Scenario.

`--deploy` auto-detects the AoE2:DE scenario folder for Steam installs (including Proton on Linux). Override with `AOE2_SCENARIO_DIR` or `--scenario-dir` for non-standard installs.

Requires **Python 3.11+** (uses `tomllib`).

## What's here

Six modes ship with the repo, illustrating both authoring styles:

| Mode | Kind | Notes |
| --- | --- | --- |
| [`cba_hero`](modes/cba_hero/) | blank build | 8-player 4v4 hero arena. 45 triggers, 16 units, XS wave clock — everything is Python. The canonical example. |
| [`cba_hero_duel`](modes/cba_hero_duel/) | blank build | 1v1 sudden-death cut of the above, on a smaller map. Same library, different pacing. |
| [`big_ytri`](modes/big_ytri/) | decompiled | Big_Ytri's Royal 4v4, decompiled to Python: 2993 triggers, 3314 conditions, 7814 effects, 1123 units, 20736 terrain tiles. `verify` compares 100,857 fields against the original. |
| [`evolution_alpha`](modes/evolution_alpha/) | decompiled + patches | **CBA Hero: Ascendants v1.0.3** — the reproducible baseline for ongoing fixes: color-aware compact lobbies, automatic armies, six hero tiers, protected team routes, center rewards, vote-kicks, and live K/D/R. 3326 triggers, 1084 units. |
| [`chieftains_4v4`](modes/chieftains_4v4/) | decompiled | Big_Ytri's published Chieftains 2026 4v4 (workshop `469500`) — Royal 4v4 plus the Chieftains/Greece/Three Kingdoms DLC blocks and a team vote-kick. 3184 triggers, 1171 units; `verify` compares 117,824 fields. |
| [`chieftains_ffa`](modes/chieftains_ffa/) | decompiled | The free-for-all cut of the same 2026 release (workshop `469501`): all-enemy diplomacy, no vote-kick. 3151 triggers, 1059 units; `verify` compares 115,299 fields. |

Three authoring styles are supported:

- **Blank build** — the mode's `build.py` generates the whole scenario from scratch, using helpers in `src/aoe2modes/lib/`. Diffable end-to-end. (`cba_hero`, `cba_hero_duel`)
- **Decompiled** — an existing `.aoe2scenario` has been dumped to Python under `modes/<id>/generated/`, so it rebuilds from source and `aoe2modes verify` proves the output still matches. This is where a reverse-engineered mode should end up. (`big_ytri`, `evolution_alpha`, `chieftains_4v4`, `chieftains_ffa`)
- **Base+patch** — the mode loads a real `.aoe2scenario` binary and modifies it in place. The quick intermediate step, but the base stays an opaque blob in git. No mode uses it today.

A decompiled mode rebuilds at the *current* scenario version rather than the original's, because the parser only ships blank templates for v1.57 and v1.58 — `big_ytri` moved from v1.51 to v1.58. The content is unchanged; `verify` reports the v1.55+ fields the older format never had (`execute_on_load`, `caption_string`, `max_units_affected`, `disable_sound`) separately from real differences. Ascendants starts from a v1.58 decompiled reference and then applies intentional gameplay and map patches in `build.py`; `tests/test_decompile.py` verifies the reference round trip, while `tests/test_evolution_alpha.py` verifies the final patched scenario.

Scaffold a new mode from the template:

```bash
aoe2modes new my_mode
```

## Authoring a mode

Every mode is a folder under `modes/` with two files that split cleanly:

```
modes/my_mode/
├── mode.toml     # settings: map, players, teams, resources, which XS to bundle
├── build.py      # logic: triggers, unit placement, XS injection
├── xs/           # optional: mode-local XS scripts
├── generated/    # optional: `aoe2modes decompile` output, called from build.py
└── README.md     # what the mode is and how it plays
```

Rule of thumb: **anything a non-Python-user could reasonably tune goes in `mode.toml`; anything with logic goes in `build.py`.** Full guide: [`docs/authoring.md`](docs/authoring.md).

## Reverse-engineering an existing scenario

Five CLI commands cover the loop from opaque binary to code-generated mode:

```bash
aoe2modes inspect "input/CBA Hero Royal 4v4 Big_Ytri.aoe2scenario" --triggers
aoe2modes audit "dist/CBA Hero Ascendants v1.0.3.aoe2scenario"
aoe2modes diff modes/big_ytri/base.aoe2scenario modes/evolution_alpha/base.aoe2scenario
aoe2modes decompile --mode evolution_alpha        # writes modes/evolution_alpha/generated/
pytest tests/test_decompile.py                     # prove the reference round trip
pytest tests/test_evolution_alpha.py               # verify the patched Ascendants build
```

- **`inspect`** — map size, player count, unit/trigger counts, and (with `--triggers`) the full trigger summary. First look at a scenario.
- **`audit`** — fail on broken trigger/object/variable references, invalid coordinates,
  and immediate unconditional victory/defeat. Scheduling and editor risks such as
  timerless loops, unconditional cleanup, duplicate names, and empty shells are warnings.
- **`diff`** — compare two scenarios by trigger signature (name + condition/effect types) and report added / removed / reshaped groups. Fastest way to see what changed between versions of the same mode. Auto-orders newest-first (see gotcha below).
- **`decompile`** — read a scenario back as regenerable Python under `modes/<id>/generated/`, chunked into `part_N.py` files. Works by introspecting the parser's factory signatures — the fields a factory accepts are exactly the fields to read back — and only emitting fields that differ from a freshly constructed default.
- **`verify`** — build the decompiled mode into a tempdir, snapshot both it and the original as plain-data dicts, and diff field-by-field. Fields that exist only on the newer version go into a `version_only` bucket rather than reported as differences. This is what makes decompiling trustworthy.

The `input/` folder is where local mod dumps and scenario files go for analysis — not part of the build.

## Project layout

```
aoe2modes/
├── src/aoe2modes/          # the CLI, builder, and shared library
│   ├── cli.py              # build, inspect, audit, diff, decompile, verify, and deployment commands
│   ├── builder.py          # build_mode: TOML + build.py → .aoe2scenario
│   ├── config.py           # mode.toml schema and validation
│   ├── context.py          # BuildContext passed to every build(ctx)
│   ├── registry.py         # discover / load / sort modes
│   ├── paths.py            # repo layout + game scenario folder detection
│   ├── toolchain.py        # parser fixups (encoding, xs-check bit)
│   └── lib/                # shared helpers: terrain, spawns, triggers, heroes, xs,
│                           #   plus diff / decompile / verify for reverse-engineering
├── modes/                  # one folder per mode; see above
│   └── <id>/generated/     # decompiled modes only — machine-written, excluded from ruff
├── xs/lib/                 # shared XS (util.xs, random.xs)
├── docs/                   # deeper design docs
│   ├── authoring.md        # writing a mode, ctx API, XS bundling
│   ├── cba-hero.md         # what CBA Hero is and how this repo models it
│   └── tooling.md          # why AoE2ScenarioParser; triggers vs XS; alternatives surveyed
├── tests/                  # pytest — every mode must build and round-trip
├── input/                  # (untracked) local mod dumps and scenarios for analysis
├── CLAUDE.md / AGENTS.md   # onboarding for AI coding agents (kept in sync)
└── .claude/skills/         # curated AoE2ScenarioParser reference pinned to 0.8.4
```

## Developing

```bash
make test              # pytest — every mode must build into a file the parser can re-read
make lint              # ruff check .
make fmt               # ruff check --fix .
make clean             # remove dist/ and Python caches
```

CI (`.github/workflows/build.yml`) runs lint + tests + `build --all` on every push and uploads the resulting scenarios as artefacts.

## For AI coding agents

The full architecture, gotchas (AoE2ScenarioParser has a real version-state leak and a Windows encoding bug — both worked around in `toolchain.py`), and conventions live in [`CLAUDE.md`](CLAUDE.md) / [`AGENTS.md`](AGENTS.md) (identical content, two filenames so Claude Code, Aider, Codex and others each find their expected file). Version-pinned parser reference material lives under [`.claude/skills/aoe2-scenario-parser/`](.claude/skills/aoe2-scenario-parser/) and is worth reading before trusting any upstream API snippet — the pinned 0.8.4 diverges from ksneijders.github.io in a few named places.

## Further reading

- [`docs/authoring.md`](docs/authoring.md) — writing a mode from scratch.
- [`docs/cba-hero.md`](docs/cba-hero.md) — what CBA Hero is, what mechanics a build has to provide, and how this repo models each one.
- [`docs/tooling.md`](docs/tooling.md) — the landscape of AoE2 scenario tooling, why this repo uses AoE2ScenarioParser, and how DE actually distributes XS.
- [`docs/ascendants-development.md`](docs/ascendants-development.md) — the v1.0.3 baseline, verification layers, and safe issue-fixing loop.
- [`docs/ascendants-issue-register.md`](docs/ascendants-issue-register.md) — reports recovered from the publishing task, parser evidence, and the in-game acceptance matrix.
- [AoE2ScenarioParser docs](https://ksneijders.github.io/AoE2ScenarioParser/) — upstream. Ahead of the pinned 0.8.4 in places; the version-pinned reference in `.claude/skills/aoe2-scenario-parser/` calls out the divergences.
- [Castle Blood Automatic — Age of Empires Wiki](https://ageofempires.fandom.com/wiki/Castle_Blood_Automatic) — background on the scenario family this repo is aimed at.
