# Ways to build and modify AoE2:DE scenarios

The repo is built on **AoE2ScenarioParser**, but that is one option among several.
This page records what exists, what each thing is good at, and why this repo picks
what it picks.

## The short version

| Approach | Language | Good for | Trade-off |
| --- | --- | --- | --- |
| **[AoE2ScenarioParser][asp]** | Python | Generating triggers/units/terrain in bulk, version control, CI | Not a GUI; you must know the data model |
| **In-game Scenario Editor** | — | Ground truth, playtesting, hand-placing decoration | No diffs, no reuse, painful past ~200 triggers |
| **[AoE2TriggerCraft][tc]** | C++ (Win32 GUI) | Fast bulk trigger editing with a UI; much faster file I/O than Python | Windows-only GUI, not scriptable from CI |
| **XS scripting** | XS | Real logic — loops, arrays, timers, state | Cannot place terrain or units directly; must be embedded to reach other players |
| **[aoe2-probe][probe]** | Rust | Byte-exact access to any field; correctness checks | Low-level; no trigger conveniences |
| **[genie-rs][geniers] / [genieutils][genieutils]** | Rust / C++ | Genie-engine formats broadly (`.scn`, `.scx`, `.dat`, DRS) | Aimed at the engine's data files, not DE scenario authoring |
| **Data mods** (`.json` + DRS) | — | Changing unit stats globally, new art, new UI | A separate mod users must subscribe to; not shipped inside a scenario |
| **[AoE2ScenarioRms][rms]** | Python | RMS-style random resource spawning on top of the parser | Narrow scope (resource placement) |

[asp]: https://github.com/KSneijders/AoE2ScenarioParser
[tc]: https://github.com/MegaDusknoir/AoE2TriggerCraft
[probe]: https://github.com/ptazithos/aoe2-probe
[geniers]: https://github.com/SiegeEngineers/genie-rs
[genieutils]: https://github.com/sandsmark/genieutils
[rms]: https://pypi.org/project/AoE2ScenarioRms/

## Why AoE2ScenarioParser for this repo

A CBA Hero scenario is thousands of near-identical triggers: the same wave spawner
once per player, the same upgrade ladder once per hero tier. That is exactly the work
a `for` loop does well and a GUI does badly. Add version control, a test suite and a
one-command build, and the parser wins on every axis except raw speed.

The parser also gives us the two things that make a repo like this viable:

* **Round-tripping.** Read any `.aoe2scenario`, inspect it, write it back out. That is
  how you reverse-engineer a published CBA Hero variant — see `aoe2modes inspect`.
* **XS embedding.** See below.

## Triggers vs XS — the division that matters

Both are "scripting", and CBA Hero needs both.

**Triggers** are the game's own condition/effect system. They know about the map:
tile coordinates, specific unit instances, areas. They are what you use to create a
unit at `(42, 88)` or to declare a player defeated. They are also verbose — no loops,
no arrays, no arithmetic beyond variables.

**XS** is a real scripting language (arrays, functions, `rule` blocks that fire on an
interval). It cannot place terrain and has only limited unit access, but it is where
counters, scaling formulas and match state belong.

The bridge between them is a **trigger variable**:

```
XS:       xsSetTriggerVariable(VAR_WAVE, gWave);
Trigger:  Condition "Variable Value": variable = wave, comparison >=, quantity = 6
```

This repo formalises that: `src/aoe2modes/lib/variables.py` declares the ids on the
Python side and `xs/lib/util.xs` mirrors them as `const int VAR_*`.

### The XS distribution catch

AoE2:DE does **not** send loose `.xs` files to the other players in a lobby. A script
sitting in your `Scripts/` folder works for you and silently does nothing for everyone
else — including spectators.

The workaround, which `xs_manager.add_script(xs_string=...)` implements, is to embed
the entire script text inside a disabled trigger's *script call* effect. The game
writes it out to `default0.xs` on every machine at match start. That is why this repo
keeps XS in normal files and concatenates them at build time rather than referencing a
script by name.

## Data mods are a different thing

"Mod" in AoE2:DE usually means a **data mod**: a Steam Workshop item with modified
`.json` unit definitions, art, or UI. Those change the game globally and require every
player to subscribe.

A CBA Hero scenario is not a data mod. It ships as a single `.aoe2scenario` file that
anyone can host, and it achieves data-mod-like effects at runtime through the
`Modify Attribute` effect — changing a unit type's hit points, attack or hero status
for one player, mid-match. `src/aoe2modes/lib/heroes.py` wraps exactly that.

If a mode genuinely needs new art or a global stat change that triggers cannot reach,
that is when a companion data mod becomes necessary — and it lives outside this repo.

## Reverse-engineering an existing scenario

```
aoe2modes inspect "~/path/to/CBA Hero.aoe2scenario" --triggers
```

Prints the map size, player count, unit and trigger counts, and (with `--triggers`)
the full trigger summary. Read that, then rebuild the parts you want as Python in a
new mode folder rather than editing the binary by hand.
