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

`_render_color_spawn_xs()` returns the entire runtime as a Python f-string and `build.py`
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

DE compacts sparse lobbies: with only Blue and Teal occupied, Teal is runtime player 2,
not 5. A trigger effect aimed at a fixed `P5` therefore hits the wrong person, and an XS
call given a trigger-side selector hits a different wrong person.

The conversion is an engine function, and XS uses it at every boundary:

```c
int cbaWorldPlayerForColor(int scenarioPlayer = 0) {
    return(xsGetWorldPlayerId(scenarioPlayer));
}
```

Rules that follow from this:

1. **XS never reads variables 40–47.** They carry the historical serialized name
   `p#worldplayer`, which is actively misleading: they are trigger-side selectors. Passing
   one into an XS player API is the ASC-020 bug.
2. **Triggers never call `xsGetWorldPlayerId`.** They use the Castle-row resolver.
3. Every XS function that touches a player starts by converting the scenario color and
   bailing out if the result is not a live slot:

   ```c
   int worldPlayer = cbaWorldPlayerForColor(scenarioPlayer);
   if (worldPlayer < 1 || xsGetPlayerInGame(worldPlayer) == false) {
       return;
   }
   ```

A test pins the boundary itself rather than enumerating Python permutations —
`test_evolution_alpha_keeps_xs_spawn_and_trigger_routes_in_separate_identity_domains`.
Enumerating permutations in Python does not simulate the DE engine and proves nothing
about this.

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
| `gCbaSeenInGameByColor` | scenario color (size 9) | Whether this color was ever seen live |

Colour-indexed arrays are size 9 so that scenario color `n` indexes slot `n` directly with
no off-by-one arithmetic at every use site.

## What `main()` does once

Beyond filling the tables, `main()` walks every player in the lobby and:

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

Calls `cbaUpdateCombatRow(color)`, which publishes kills, deaths and razings into that
color's three HUD variables and then calls `cbaRefreshCombatValues`, which zeroes the
thirteen non-combat score attributes and republishes kill/death/razing value from live
engine attributes.

### `cbaColorRuntimeState` — every 1s

Calls `cbaUpdateColorRuntime(color)`. **This is the sole writer of `p#coloractive`.**

```
active = 1  iff  world player >= 1  AND  slot in game  AND  not eliminated
```

It also **latches elimination**: a color that was seen in the game and has now left it
gets its eliminated bit set. Without that latch, the active bit would flap back on if the
engine ever reported the slot in game again, and the opposing side's victory would never
resolve — a color that has left cannot be resolved by the owner-resolved defeat triggers,
because those need a live player selector.

Triggers write only `p#coloreliminated`. A second trigger-side writer of `p#coloractive`
used to be silently reverted here within one second unless every defeat path also
remembered to write the elimination bit — which made every future defeat path depend on
remembering an unrelated second write.
`test_evolution_alpha_color_active_has_exactly_one_writer` pins this.

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
