# aoe2modes

Build Age of Empires II: Definitive Edition custom scenarios from source, with a focus
on **CBA Hero** modes.

Scenarios here are *code*, not binaries you edit by hand. Each mode is a folder with a
`mode.toml` (settings) and a `build.py` (logic); one command turns them into
`.aoe2scenario` files you can drop into the game.

```
aoe2modes build --all
```

## Why

A CBA Hero scenario is thousands of near-identical triggers — the same wave spawner
once per player, the same upgrade ladder once per hero tier. That is loop work, and
the in-game editor cannot loop, cannot diff and cannot be reviewed. Generating them
with [AoE2ScenarioParser][asp] means the mode gets version control, a test suite, and
shared building blocks across variants.

See [docs/tooling.md](docs/tooling.md) for the other ways to edit AoE2:DE scenarios
and why this repo picks this one.

[asp]: https://github.com/KSneijders/AoE2ScenarioParser

## Layout

```
modes/                  one folder per mode — the things you build
  cba_hero/               8-player 4v4 hero arena
  cba_hero_duel/          1v1 sudden-death cut of the same mode
  _template/              scaffolding for `aoe2modes new`
src/aoe2modes/          the build tool
  lib/                    shared building blocks (heroes, spawns, triggers, terrain)
xs/lib/                 shared XS libraries, bundled into modes that ask for them
docs/                   tooling comparison, authoring guide, CBA Hero notes
tests/                  config validation + every mode builds and reloads
dist/                   build output (gitignored)
```

## Setup

Python 3.11+.

```bash
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
```

Or `make setup`.

## Usage

```bash
aoe2modes list                          # every mode in modes/
aoe2modes info cba_hero                 # resolved config for a mode
aoe2modes build cba_hero                # -> dist/CBA Hero v0.1.0.aoe2scenario
aoe2modes build --all                   # build everything
aoe2modes build cba_hero --deploy       # build, then copy into the game folder
aoe2modes new cba_hero_blitz            # scaffold a new mode
aoe2modes inspect "some.aoe2scenario"   # summarise an existing scenario
```

`--deploy` finds the game's scenario folder automatically for Steam installs,
including Proton on Linux. Override it with `AOE2_SCENARIO_DIR` or `--scenario-dir`.

## The modes

| Mode | Players | Map | Summary |
| --- | --- | --- | --- |
| `cba_hero` | 8 (4v4) | 144² | One hero and one castle each. Waves every 20s, hero tiers unlock at waves 6 and 14. |
| `cba_hero_duel` | 2 (1v1) | 96² | Top-tier hero from the start, faster waves, reinforcements stop at wave 20. |

## Adding a mode

```bash
aoe2modes new my_mode --name "My Mode"
```

Then edit `modes/my_mode/mode.toml` and `modes/my_mode/build.py`. The full walkthrough
is in [docs/authoring.md](docs/authoring.md); the CBA Hero mechanics are covered in
[docs/cba-hero.md](docs/cba-hero.md).

## Triggers and XS

Triggers know where things are on the map; XS knows how to count. Modes use both, and
they talk through trigger variables declared once in `src/aoe2modes/lib/variables.py`
and mirrored in `xs/lib/util.xs`.

XS files are linted with the bundled `xs-check` on every build — a script the linter
rejects fails the build rather than silently doing nothing in-game.

## Development

```bash
make test     # pytest
make lint     # ruff
make build    # every mode into dist/
```
