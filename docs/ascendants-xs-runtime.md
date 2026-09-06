# Ascendants XS runtime

Everything Ascendants does that a trigger cannot do — per-civilization army spawning,
builder-pair accounting, the live combat HUD values, free costs at runtime, and the
authoritative color-active bit — lives in one XS script. This document describes that
script, how it reaches the trigger graph, and the one identity rule that everything else
depends on.

Source: `modes/evolution_alpha/build.py::_render_color_spawn_xs`.
Trigger-side counterpart: [`ascendants-architecture.md`](ascendants-architecture.md).

## Ascendants generates its XS; it does not bundle it

Every other mode in the repo lists `.xs` files under `[xs] include` / `[xs] scripts` in
`mode.toml` and lets `lib/xs.bundle_xs` concatenate them. Ascendants declares **both lists
empty on purpose**:

```toml
[xs]
include = []
scripts = []
```

`_render_color_spawn_xs(ctx)` returns the entire runtime as a Python f-string and `build.py`
hands it to the builder via `ctx.add_xs`. `aoe2modes info evolution_alpha` therefore
reports no XS for this mode, which is accurate about the *files* and misleading about the
*scenario* — the built artifact contains a full script.

The reason is that the script is mostly **data**, and that data is Python:

- `CIV_SPAWN_RULES` — 59 rows of (unique unit, military population cap, spawn interval).
- `CIV_BUILDER_RULES` — 59 rows of (public civilization name, razing threshold).
- `SPAWN_WORLD_POSITIONS` — 8 colors × 4 wave pads, each derived from one canonical row
  through the eight-way map transform.
- Every trigger-variable base id.

Keeping the tables in Python means the same values drive the trigger graph, the tests and
the XS, and a change to one table cannot leave the other side stale. A hand-written `.xs`
file would need those 300-odd numbers duplicated by hand.

The generated script is still linted like any other: the build runs `xs-check` on it and a
failure raises `BuildError`.

### Generation-time guards

`_render_color_spawn_xs` refuses to emit an inconsistent script:

- **Table symmetry.** `CIV_SPAWN_RULES` and `CIV_BUILDER_RULES` must cover exactly the
  same civilization ids; the symmetric difference is reported and the build fails.
- **Array sizing.** Every civilization-indexed XS array is sized from
  `max(civ ids) + 1`, not from a literal. Adding a civilization to the tables used to be
  able to write past the end of a hardcoded size-60 array at runtime — something
  `xs-check` cannot see and no test would catch.

## The identity rule

This is the single most important thing in the file, and the cause of the worst bug the
mode has had (ASC-020: Red/Green and Green/Yellow armies spawning in each other's
territory).

**A custom-scenario player number and a runtime lobby slot are different numbers.**

| Domain | What it is | Where it is valid |
| --- | --- | --- |
| Scenario color | The fixed P1–P8 territory identity | Map geometry, per-color variables |
| Trigger-side owner | Which trigger player selector owns that Castle row, latched into variables 40–47 | Trigger condition and effect `source_player` / `target_player` fields |
| World player | The lobby slot DE actually seated there | **Every XS player API** |

Do not assume a color number, compacted player index, and trigger selector coincide.
v1.0.18 failed in a six-player match with two explicitly closed slots: P7/P8 had no
custom HUD and did not purge on defeat. The shared runtime resolver used
`xsGetWorldPlayerId(color)` without independently checking the actual objects. Its
precise engine failure is not yet captured; source assertions that the converter was
called were not behavioral proof.

v1.0.19's Castle-reference lookup also failed live acceptance. v1.0.20 removes both
lookup dependencies. Native owner detection latches occupancy after lobby settling;
HUD values copy kills/deaths/razings from that same trigger owner. Elimination,
cleanup and victory do not require a successful XS identity binding.

XS stamps `1000 + API player index` into reserved unused resource **10** for each
runtime player in `main()`. Each `Color XS Identity S# W#` trigger waits for its
Castle-owner latch and a token in 1001–1008, then copies that owner's resource into
variables 137–144. The resolver subtracts 1000 and rejects out-of-range values.
This translates through shared player data, never by assuming the two index domains
agree. A delayed token retries; a successful binding remains after elimination.
Resource 10 must not be reused by score, economy or civilization changes.

XS never reads trigger-selector variables 40–47. Spawning and builder rewards require
native occupancy, no elimination, and a valid decoded token. The objective HUD and
participation no longer depend on XS conversion or aliveness reads. The old debug
chat is removed. Tests exercise all 255 nonempty color subsets in two seat orders
with independently permuted trigger owners, plus delayed/invalid tokens and zero-
binding HUD/cleanup. These checks do not emulate native DE execution.

## The variable bridge

XS and triggers share state through trigger variables, read with `xsTriggerVariable` and
written with `xsSetTriggerVariable`. Both sides address them **through a named base
constant interpolated from Python**, never a bare literal:

```python
xsSetTriggerVariable(
    {ARMY_MOVE_PENDING_VARIABLE_BASE} + scenarioPlayer - 1,
    1
)
```

Before this, `8 + ((n - 1) * 3)` and `int(player) - 1` appeared as literals in Python, in
the trigger code, and again inside the XS source string, with nothing tying them together.
The full id map is in [`ascendants-data-tables.md`](ascendants-data-tables.md), and
`_assert_variable_ids_are_contiguous` fails the build on a hole, duplicate or collision.

Blocks XS touches:

| Block | Direction | Purpose |
| --- | --- | --- |
| `PENDING_BUILDER_VARIABLE_BASE` (0–7) | XS writes, triggers consume | Queue of unclaimed builder pairs |
| `COMBAT_ROW_VARIABLE_BASE` (8–31, stride 3) | XS writes, triggers display | Kills / Deaths / Razings per color |
| `COLOR_ACTIVE_VARIABLE_BASE` (32–39) | **XS writes exclusively** | Color is occupied and not eliminated |
| `COLOR_ELIMINATED_VARIABLE_BASE` (48–55) | Triggers write, XS reads and latches | Color has been eliminated |
| `ARMY_MOVE_PENDING_VARIABLE_BASE` (81–88) | XS arms, triggers consume | One-shot new-wave pulse |

## Global state

All XS globals are arrays created in `main()`:

| Array | Indexed by | Holds |
| --- | --- | --- |
| `gCbaNextSpawnByColor` | scenario color (size 9) | Game time of that color's next wave |
| `gCbaUnitByCiv` | civilization id | Unique unit id to spawn |
| `gCbaCapByCiv` | civilization id | Military population cap |
| `gCbaIntervalByCiv` | civilization id | Seconds between waves |
| `gCbaNameByCiv` | civilization id | Public civilization name for chat |
| `gCbaBuilderThresholdByCiv` | civilization id | Razings needed for the first builder pair |
| `gCbaEarnedBuilderPairsByColor` | scenario color (size 9) | Pairs earned so far, for edge detection |

Colour-indexed arrays are size 9 so that scenario color `n` indexes slot `n` directly with
no off-by-one arithmetic at every use site.

## What `main()` does once

Beyond filling the tables, `main()` stamps resource 10 with its XS API identity token, then walks every player in the lobby and:

- sets food/wood/stone/gold cost to zero for **every technology** the player has;
- sets food/wood/stone/gold cost to zero for **every object** the player has;
- calls `cbaRefreshCombatValues` to establish the combat-only score baseline.

This is why the mode's "everything is free" rule holds for content the trigger graph never
enumerates, including civilization-specific technologies.

## The rules

Five XS rules drive the runtime. All are throttled with `minInterval`.

### `cbaColorArmySpawns` — every 1s

Calls `cbaSpawnColor(color)` for all eight colors. For a live color with a mapped
civilization it:

1. reads unit id, population cap and interval from the civilization tables;
2. on first sight, schedules the first wave at `now + interval` and returns — so nobody
   gets a wave at t=0;
3. once due, checks `cAttributeMilitaryPopulation - 1` against the cap;
4. calls `cbaCreateWave`, which creates one unit at each of that color's four pads and
   **arms the army move pulse**;
5. schedules the next wave.

Two details matter. The `- 1` excludes the permanent War Penguin, which is a
military-class one-population object every live color owns — subtracting it here avoids
depending on a post-load unit-data mutation that is unreliable after object naming. And
units are created at **cell centres** (`x + 0.5, y + 0.5`), which is what lets each route
trigger capture its exact creation cell instead of an ambiguous integer boundary.

An unmapped civilization returns early and silently. That silence is covered by
`cbaBuilderRewardInfo` below.

### `cbaCombatHudValues` — every 2s

Calls `cbaUpdateCombatRow(color)`, which refreshes combat-only score weighting for a
resolved XS player. Native `Color Combat Values S# W#` triggers separately copy
resource 20 (kills), 154 (deaths), and 43 (razings) into HUD variables 8–31 every 2s.
HUD activation reads persistent occupancy and the trigger owner, not XS identity.

### `cbaColorRuntimeState` — every 1s

Calls `cbaUpdateColorRuntime(color)`. **This is the sole writer of `p#coloractive`.**

```
active = 1 iff native occupied latch == 1 AND eliminated latch == 0
```

Native Castle-owner detectors latch `coloroccupied` (121–128) once and reset
`colorcleaned` (129–136) to zero. Closed colors start clean in `main()`.
Native resignation/defeat conditions and Castle-loss conditions set elimination;
only owner-empty confirmation marks an occupied eliminated color clean again.
No XS identity lookup can stop this state transition. XS remains the sole writer
of active bits; triggers write occupancy and elimination. Spawning and builder
queuing also test elimination directly before the next active refresh.

### `cbaBuilderRewardQueue` — every 1s

Calls `cbaQueueColorBuilders(color)`:

```
earnedPairs = razings - threshold + 1      (floored at 0)
```

When `earnedPairs` exceeds the previously recorded value, the difference is **added** to
the pending-builder variable rather than assigned. Pairs therefore accumulate if the
trigger side cannot deliver them immediately, and no razing is ever lost.

### `cbaBuilderRewardInfo` — once, at 4s

Sends the local player a chat line naming their civilization and its builder threshold,
then calls `xsDisableSelf()`.

This rule is also the **unsupported-civilization warning**. An id past the end of the
tables means a civilization released after this build was made; without the warning the
player simply gets no army and no builder pairs, which reads in-game as "the mode is
broken" rather than "this civ is unsupported". The message names the supported id range
and tells the reader to update `CIV_SPAWN_RULES` and rebuild.

## Changing the XS

- **Adding a civilization** is a data change in two Python tables, not an XS edit. See the
  runbook in [`ascendants-data-tables.md`](ascendants-data-tables.md).
- **Adding a variable block** means adding a `*_VARIABLE_BASE` constant, allocating ids
  contiguously, and referencing the constant from both sides. Never write a bare id into
  the XS string.
- **Adding a player-facing call** means converting the identity first. If you find
  yourself passing a variable value into an XS player API, stop: that value is
  trigger-side.
- **Verify with** `pytest -q tests/test_evolution_alpha.py -k "xs or identity or writer"`
  and a full build, which runs `xs-check` over the rendered script.
