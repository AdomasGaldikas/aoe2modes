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
  how you reverse-engineer a published CBA Hero variant — and it goes further than
  inspection: because the parser's effect and condition factories have introspectable
  signatures, a scenario can be dumped back out as Python that rebuilds it. See
  "Reverse-engineering an existing scenario" below.
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

Four commands take a published scenario from opaque binary to editable code.

```
aoe2modes inspect "~/path/to/CBA Hero.aoe2scenario" --triggers
aoe2modes diff old.aoe2scenario new.aoe2scenario
aoe2modes decompile --mode <id>
aoe2modes verify <id>
```

**`inspect`** prints the map size, player count, unit and trigger counts, and (with
`--triggers`) the full trigger summary. First look at anything.

**`diff`** compares two scenarios by trigger signature — name plus the sorted
condition and effect type ids — and reports added, removed and reshaped groups. The
fastest way to see what changed between two versions of the same mod.

**`decompile`** writes the whole scenario back out as Python under
`modes/<id>/generated/`: terrain as a run-length table, every unit with its reference
id preserved, every declared trigger variable as an `(id, name)` pair, and every
trigger as `add_trigger` / `new_condition` / `new_effect` calls. It works by introspecting the factory signatures — the fields a factory
*accepts* are exactly the fields to read back — and emits only the fields that differ
from a freshly constructed default, so an effect with sixty fields prints as three
lines. Values resolve to named constants (`TechInfo.AZTECS.ID`, `PlayerId.SEVEN`)
wherever they map cleanly, which is safe because every substitution preserves the
underlying integer.

**`verify`** rebuilds the decompiled mode and diffs it against the original
content-wise. A byte compare would be useless — the rebuild targets the newest
scenario version, so the file layout differs by construction — so both sides are
reduced to plain-data snapshots and compared field by field. Fields the older format
never had are reported separately from real differences.

Variables are compared as part of that snapshot, and they are worth calling out: a
condition or effect names a variable by **id**, never by name, so a lost variable
declaration changes no trigger field and would otherwise pass every other check while
silently rewiring the logic.

Two constraints shape this design, both from the parser:

* **The version-state leak** (see `CLAUDE.md`) means a v1.51 scenario cannot be read in
  the same process that builds a v1.58 one. `decompile` therefore *writes source* and
  the build happens later, in its own process. `verify` reads the newer file first for
  the same reason.
* **Only v1.57 and v1.58 ship a blank template**, so a from-scratch rebuild cannot
  target an older scenario version. Decompiling a v1.51 mod moves it to v1.58; the
  game upgrades such a file on first save anyway.

Decompiling is the end state — the binary stops being the source of truth and the mod
becomes something you can grep, diff and review. Hand-rebuilding selected parts as
Python is still fine when you only want a mechanic rather than a whole mod.

## Reading the map, not the triggers

Everything above works on the trigger graph. A CBA map has a second half that no trigger
diff can see: which ground is walkable, what the walls actually enclose, and whether the
eight starting positions are really equivalent. `aoe2modes map` measures that half.

```
aoe2modes map evolution_alpha --html dist/ascendants-map.html
aoe2modes map "dist/CBA Hero Ascendants v1.0.10.aoe2scenario" --png map.png --zones --scale 8
```

The report is one self-contained HTML file — both renders inlined as data URIs, no assets
to keep next to it. It carries a terrain view, a zone view colouring every walkable region
by role, the region inventory, symmetry against all eight transforms of the square,
per-player parity, and a distance matrix. `--png` writes just the render, with `--zones`
choosing which of the two.

Four measurements are worth knowing how to read:

**Regions are computed twice.** Once with every gate shut and once with them open. The
shut pass is the interesting one: if a base shows up as its own region, nothing reaches it
except through a gate — no gap at the end of a wall, no diagonal leak along a shoreline.
The open pass is how a match actually moves, and it is what distances and territory use.

**Players are anchored to a region, not to a building.** The obvious anchor — the centroid
of a player's Castle row — lands *inside* a Castle, and "step outwards until walkable"
resolves in a different direction for a base facing north than for its mirror facing
south. That alone reported a 40% territory spread across eight identical bases. The anchor
is instead the centre of the sealed region a player's own buildings enclose, which mirrors
when the map does.

**Symmetry is reported per transform, terrain and objects separately.** The mirror group
and the diagonal group usually differ, and the gap between them is informative: a map whose
teams sit across a horizontal line *cannot* be diagonally symmetric, because the strip that
joins two teammates on one edge has to be water on the edge where it would join enemies.
Objects are matched on continuous coordinates (`size - x`), not on tile indices — a 4x4
building sits at `x.0` and a 1x1 at `x.5`, so reflecting the tile index and re-adding the
fraction lands every even-footprint building one tile off its true mirror.

**Distances are tile steps.** Eight-neighbour breadth-first search, so on an even-sized map
two mirrored positions can differ by one step. That is grid parity, not an asymmetry.

The one approximation to keep in mind: the parser does not carry building dimensions, so
footprints come from `FOOTPRINTS` in `lib/mapview.py`, and anything absent falls back to a
deliberately small guess (2x2 on an integer tile centre, 1x1 on a half tile). Guessing
small merges two regions that are really separate; guessing large would invent a wall and
report a base as sealed when it is not. If a mode uses a building that matters for
connectivity and is not in the table, add it there.
