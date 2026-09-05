# CBA Hero: Ascendants v1.0.17 candidate

A live 1 v 4 ended with one player having destroyed every enemy Castle and every
reachable building, and no victory. This release fixes that and the eight other
defects the source review found around it. The map, every placed object, the
controllers, Hero tiers, walls, rewards, and the XS army runtime are unchanged.

Two findings are deliberately **not** fixed: they change civilization balance rather
than correct a defect, and that is the maintainer's call. Both are recorded below.

## The reported deadlock

Victory is gated on `p#coloractive`, which XS clears only from `p#coloreliminated`.
Elimination had a single reachable path: `castle (p#)`, a one-shot trigger holding four
`Destroy Object` conditions on four exact preplaced Castle references. Three separate
properties of that design could each leave a colour permanently alive with nothing left
on the map to kill, and there was no fallback, no timeout, and — in a 1 v 4 — no
vote-kick escape, because a kick needs three live colours on a side.

| Failure | Before | v1.0.17 |
| --- | --- | --- |
| ASC-039: Castles that leave the map without being *destroyed* | A `Remove Object`, a defeat purge, or engine cleanup of a closed slot satisfies nothing. `castle (p#)` never fires, the eight `Color Defeat Resolve S# W#` triggers it activates stay disabled, and the colour is never eliminated. | Each resolver ships **enabled** and fires from the Castle-row condition it already carried: *no Castle of this owner in this colour's row*. Any way those Castles leave the map resolves the colour. `castle (p#)` remains wired as a redundant fast path, and nothing depends on it. |
| ASC-040: the two player-identity domains disagreeing | `p#worldplayer` is latched in the trigger-player domain; `p#coloractive` is written by `xsGetWorldPlayerId` in the lobby-slot domain. When they differ — most likely in a sparse lobby — all eight of a colour's resolvers require a `p#worldplayer` value that never arrives, while the colour still reads alive. | Eight new `Color Castle Row Empty S#` triggers, one per colour: a settle timer plus one inverted Castle check per candidate owner. They ask only whether *anybody* still holds a Castle in that row, so they need neither latch. XS additionally latches elimination once a colour that was seen in game leaves it. |
| ASC-041: two writers for the aliveness bit | Triggers wrote `p#coloractive` and XS recomputed it every second. It worked only by convention: a trigger that cleared the active bit without also setting the elimination bit was silently reverted within a second. | XS is the **only** writer. Every trigger path writes `p#coloreliminated` alone, and a regression rejects any trigger effect targeting the active block. |

## Roster corrections

| Issue | Before | v1.0.17 |
| --- | --- | --- |
| ASC-042: seven civilizations could train their own auto-spawned unit | The shared training ban was the union of the imported per-colour lists, which predate recent DLC. Achaemenids, Macedonians, Thracians, Puru, Muisca, Mapuche and Tupi could queue their unique unit for free, from four Castles, on top of the automatic army — a ceiling the other 52 do not have. | The ban is derived from `CIV_SPAWN_RULES` and covers each unit's Elite and non-Elite forms and its ranged/melee siblings. Adding a civilization to that table now also bans its unit. 143 → **159** disabled units. |
| ASC-043: Krepost and Donjon escaped the Castle ban | `CASTLE` was banned so nobody could add a fifth one, but the two civilization-specific castle-class fortifications were not. With free stone, Bulgarians and Sicilians could raise unlimited extra fortresses, and the Donjon trains Serjeants. | Castle, Krepost and Donjon are banned together. 14 → **16** disabled buildings. |

Inherited `disabled_buildings` id 621 resolves to no building in the pinned dataset and
is kept on purpose: removing an entry from a ban list is a live gameplay change, and a
ban on an id the game does not have is inert either way.

## Maintenance corrections

| Issue | Before | v1.0.17 |
| --- | --- | --- |
| ASC-044: XS addressed a variable block through a bare literal | `cbaQueueColorBuilders` read the pending-builder variable through the interpolated base and wrote it through `scenarioPlayer - 1`. The two agreed only because that base happens to be zero. | Both sides use the named base, and a regression requires every XS trigger-variable access to address one. |
| ASC-045: the victory fan-out stayed live all match | All 64 `Color Team Victory` triggers were enabled with eight conditions each, though only one candidate per colour can ever match. | Each ships disabled and is armed by the single owner detector whose latch it can match, so 56 leave the tick loop at start-up. Initially enabled triggers are unchanged at 3,195, because the 64 defeat resolvers became enabled in the same change. |
| ASC-046: imported language and a stale README | The three hero-order template triggers were still found by their Portuguese names from the source scenario, and the mode README tracked v1.0.15 while `mode.toml` and the docs were on v1.0.16. | The templates are named in English in the hand-maintained `scenario/` source and `HERO_ORDER_FAMILIES` is a plain tuple. A regression asserts the README title matches `mode.toml`. `_possible_world_players` also lost the parameter it discarded. |

## Left open — balance calls, not defects

- **Four civilizations spawn the non-Elite unit.** Persians (War Elephant `239`), Turks
  (Janissary `46`), Spanish (Conquistador `771`) and Portuguese (Organ Gun `1001`),
  inherited from the legacy loops. XS creates the unit by explicit id, so researching
  the Elite upgrade does not change later waves. All four already sit in the bottom
  third on cap and interval alone. Promoting them moves four civilizations' power level.
- **The army cap is a *military population* cap, not a unit count.** `cbaSpawnColor`
  gates on `cAttributeMilitaryPopulation`, so per-unit population cost is an unmodelled
  multiplier. The 0.5-population Malay Karambit Warrior turns a cap of 80 into roughly
  160 units; a two-population unique unit gets the inverse. Normalising this would
  re-scale every civilization's army at once.

## New tests

Two liveness tests sit alongside the existing structural victory test. They select the
victory subsystem **from the serialized data** — every trigger that writes victory state
or declares a result, closed over incoming `Activate Trigger` edges — and run it as a
state machine rather than checking trigger shapes:

- Six lobby shapes (full 4v4, solo vs four, four vs solo, minimum 1v1, non-adjacent
  2v2, shuffled full) × closed slots both cleaned up and left in place × both sides
  eliminated. The winning side must never have to raze a colour nobody is playing, and
  nobody may win while both sides still hold Castles.
- The same subsystem with the trigger-side owners permuted against the XS seats, so no
  owner-resolved resolver can match and only the row-empty fallback can clear the gate.

`Destroy Object` conditions evaluate to **false** in the model on purpose: an object can
leave the map by being removed rather than destroyed, so nothing that resolves a match
may lean on that condition. Start-up is modelled as a separate phase, because owner
detection and the two-sided readiness latch run while every base is still standing.

Both tests fail on the pre-fix build. Five further regressions cover the single active
writer, the named XS variable bases, the derived unit ban, the castle-class building
ban, and the README version.

## Verification

- All 133 repository tests pass: 73 Ascendants and 60 other tests, in the two
  complementary runs the mode README documents.
- All six modes build. Repository Ruff checks pass.
- Full build and 637-line embedded XS validation pass.
- Strict readback audit: 0 errors, 0 warnings; 3,655 triggers, 15,081 conditions,
  14,752 effects, 956 units, and 121 variables. There are 3,195 initially enabled and
  3,646 conservatively reachable triggers.
- No terrain cell and no placed object changed. The diff touches trigger logic, the
  shared roster lists, three trigger names in `scenario/`, tests and documentation;
  nothing that writes terrain or places units was modified, and the existing pinned
  terrain hash and object-set tests still pass.
- Artifact: `CBA Hero Ascendants v1.0.17.aoe2scenario`, 145,667 bytes.
- SHA-256: `fe6e287ea09ce9abeaae221d72bf9e0aec6a8fdcca85fe6b6804b95c756d44e4`.

**No live DE match was run.** The acceptance check this release exists for is a single
replay: run the reported 1 v 4 and confirm the match ends within about five seconds of
the last enemy Castle falling. Repeat with a resignation, with a closed slot on the
losing side, and in a shuffled lobby. If it hangs again, record
`p1..p8worldplayer` and `p1..p8coloractive` at that moment — those two rows say which
of the three failure paths is still open.

Start a new match; an existing saved or running match cannot pick up scenario-file
changes.
