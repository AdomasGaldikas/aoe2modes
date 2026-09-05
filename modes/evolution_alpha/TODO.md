# Ascendants TODO

Open work from the v1.0.7–v1.0.17 source review. Current candidate: **v1.0.17**;
what remains is either a decision for the maintainer or something only the game engine
can settle.

Status key: `[x]` done · `[~]` decision needed · `[ ]` open

---

## v1.0.17 — the reported 1 v 4 deadlock

A live 1 v 4 ended with one player having destroyed every enemy Castle and every
reachable building, and no victory. The review found the victory gate had three
independent ways to become permanently unreachable. All are closed; see ASC-039…046 in
[`../../docs/ascendants-issue-register.md`](../../docs/ascendants-issue-register.md).

- [x] ASC-039–041: elimination is map state, not a one-shot `Destroy Object` event;
  `Color Castle Row Empty S#` clears the gate without either identity latch; XS is the
  sole writer of `p#coloractive` and latches elimination when a seen colour leaves.
- [x] ASC-042–043: the training ban is derived from `CIV_SPAWN_RULES`; Krepost and
  Donjon join the Castle ban.
- [x] ASC-044–046: XS addresses every trigger-variable block through a named base; the
  victory fan-out is armed by its owner detector; hero-order templates are named in
  English; the README tracks `mode.toml`.
- [ ] **Engine acceptance.** Replay the reported 1 v 4 and confirm the match ends
  within about five seconds of the last enemy Castle falling. Repeat with a
  resignation, with a closed slot on the losing side, and in a shuffled lobby.
- [~] Not changed, deliberately: the four civilizations that spawn the **non-Elite**
  unit (Persians, Turks, Spanish, Portuguese) and the fact that the army cap is a
  **military population** cap, so a 0.5-population Karambit Warrior buys the Malay
  roughly twice the units. Both are balance calls for the maintainer, not defects.
  Inherited `disabled_buildings` id 621 resolves to nothing in the pinned dataset and
  is kept: removing a ban is a live gameplay change, and a ban on an absent id is inert.

## v1.0.16 audit follow-up

- [x] ASC-031–036: shared training bans, preserve parked reward units, clear pending
  Hero orders on OFF, guard Goth Imperial transition, protect vote markers from combat.
- [x] ASC-038: first ON Hero distance shares the Army HOLD line directly in front of
  Castles. All 64 mappings and all eight footprint/path orientations are checked.
- [ ] ASC-037: an old unit on a capture pad during a new birth can still be retasked.
  One-shot pulses protect orders between births, not unit identity during births.
  This qualifies the stronger historical claims below. Per-unit routing needs engine
  validation before replacing the current movement system.
- [x] Preserve the intentional 50-second Scorpion lifetime.
- [ ] Run the v1.0.16 engine acceptance cases in the release notes and issue register.

## Closed in v1.0.15

### [x] I1 — remove side walls while keeping front and University barriers

Implementation removes the short shoulders plus all 30 long side-wall pieces per
color through 64 exact-reference `Wall Breach` mappings. The resulting counts are
44 walls for P1/P2/P7/P8 and 48 for P3/P4/P5/P6. The front gates/wall row, rear
University wall/gate, joins, and teammate access gates stay. Two front-row end posts
per color prevent an around-the-gate route after the side walls disappear. The
University gate is still distinct from the deletable switch. Exact targets and
closed-gate reachability are tested across all eight transforms, including simultaneous
side-wall removal.

### [x] I2 — restore the 200-wall warning and 220-wall wipe safely

Implementation restores the original one-shot WALL-class thresholds, including owned
preplaced walls in the count, through 64 owner-resolved warning/wipe pairs. The wipe
removes that owner's walls across the map outside protected permanent barrier
footprints. Front and University defenses retain manual-delete protection; the switch
remains deletable. Some side walls retain legacy Delete protection, but scripted
removal ignores it. No ownership swapping or barrier recreation is used. Tests cover
every owner mapping and the exact 49-rectangle wipe complement of
368 protected cells. Engine acceptance remains separate.

## Closed in v1.0.14

### [x] H1 — controllers could leave their own slider lanes

Each color now has separate 9×2 Sheep and Penguin tracks. Three rows of Deep Water
divide them without beach bridges. Track-specific selectors cover every dry cell,
and containment needs no repeated task, stop, freeze, or teleport effect. Connectivity
checks cover all six reachable levels and separation for all eight orientations.

### [x] H2 — HOLD/OFF endpoints and long controller names were unclear

The whole level-0 pad is Snow, ending exactly where level 1 starts on the road. Each
track has its own HOLD/OFF and FAR Signs, with one row left clear for movement. Names
are `Army range - snow = HOLD` and `Hero range - snow = OFF`. HOLD still produces
Castle armies and keeps new waves near home; OFF pauses new Heroes. Existing armies
and Heroes keep their orders.

### [x] H3 — superseded wall interpretation

v1.0.14 narrowed deletion to the short shoulders and retired the 220-wall wipe. This
misread the required rules: the user wants the long side walls removed and the wipe
active, while preserving the front and University barriers. I1/I2 above correct that
interpretation in v1.0.15. The v1.0.14 validation record remains historical evidence
only, not the current wall-behavior contract.

## Closed in v1.0.13

### [x] G1 — independent Castle-army and Hero controls

The shared five-position Sheep system is removed. Every color now has one Sheep with
six proportional Castle-army levels and one War Penguin with Hero OFF at level 0 plus
five progressively farther active levels. Both begin at level 3 on separate dry lanes.
At that release point, their reference-specific detectors covered the complete island,
including both beach caps; v1.0.14 confines them to separate tracks. The old selector
Relics, Rugs, Torches, and Hero shoreline blocker toggle are absent.

### [x] G2 — Hero OFF could not leave stale tiers armed

The six milestone loops and late 3500/5000 loops now have mutually exclusive kill
bands and require Hero level 1 or greater. Re-enabling Heroes starts only the current
tier. All active Hero routes retain a one-shot creation pulse, so later manual orders
cannot be reclaimed at a spawn line.

### [x] G3 — controller clarity and safety

At that release point, shared endpoint Signs identified `CASTLE HOLD / HERO OFF` and
`FAR BATTLE ROUTE`; v1.0.14 replaces those labels and shared signs. Sheep and Penguins
are undeletable and untargetable. Penguins additionally use No Attack stance and zero
scenario attack.
Their one real population slot is excluded from custom caps, and a 251 hard cap keeps
250 normal gameplay slots. Tests pin all 96 selector areas, 704 movement mappings,
controller references, terrain, destinations, and eight player transforms. All 32
blocking Castle Hay creates are removed after footprint checks found pad overlap.

## Closed in v1.0.12

### [x] F1 — hidden Goth Palisade HP exception was not wanted

The legacy mechanic did not award or create walls: Elite Huskarl plus exactly 12
player-built Palisade Walls in a designated row caused a 2,750 HP increase. The eight
imported triggers and all 64 shuffled-lobby replacements are now absent. A regression
rejects every Palisade-targeting condition/effect in the serialized scenario while
retaining the independent Goth Anarchy/Barracks restriction.

## Closed in v1.0.11

### [x] E1 — trigger and XS player identities were conflated

The v1.0.8–v1.0.10 implementation passed the Castle detector's trigger-side player
selector into XS. Engine reports proved that this could create Red-owned units from a
Green Castle, Green-owned units from a Red Castle, or Green/Yellow cross-spawns under
other lobby orders. XS now calls `xsGetWorldPlayerId(scenarioPlayer)` at one explicit
boundary. Trigger conditions and effects continue to use the independently resolved
Castle owner. The distinction is documented in both repository guidance files.

### [x] E2 — the ownership test did not model the failing boundary

The former 8! Python loop only selected eight existing dictionary keys for each
permutation; it never executed or modeled the DE engine. It is removed. A replacement
regression asserts the engine conversion in generated XS and follows every color's
Sheep-selected route through normal-wave and hero creation/movement under identity,
an explicit Red/Green swap, and a full rotation. Exact control geometry is recorded in
`docs/ascendants-control-map.md`.

### [x] E3 — obsolete corner staging objects

Exactly 56 submerged static Palisade Walls and eight static Saboteurs are removed from
the outer corners. A regression pins their reference ids and proves no trigger refers
to them. The separate Goth Palisade HP trigger remained at this release point and is
removed by v1.0.12 F1 above.

### [x] E4 — current artifact and issue documentation lagged the engine reports

The issue register now distinguishes source/parser proof from required engine
acceptance, records the Red/Green and Green/Yellow failures, adds the corner cleanup,
and links the exact eight-color control map.

## Closed in v1.0.10

### [x] D1 — milestone heroes continuously reclaimed player control

All 192 hero route triggers used to poll the three-by-three milestone spawn area every
second. A hero sent back toward its Castle could therefore be caught and turned around
again. Eight color-specific hero pulses now arm only when a 200–2000 milestone or
3500/5000 Genghis loop creates a unit; the matching runtime-owner route consumes the
pulse once.

### [x] D2 — builder movers had the same continuous-order defect

All 64 builder movers now require and consume a separate color-specific pulse armed by
the raze reward that creates the villager pair. The initial auto-park remains, but a
later player order cannot be overwritten merely because a builder re-enters its spawn
pad.

### [x] D3 — no whole-scenario order-overwrite invariant

A new regression scans all 448 reachable looping `Task Object` triggers. Every one must
have a one-second timer, an explicit Move action, and exactly one variable that is both
required at value 1 and reset to 0 by the same trigger. This covers normal armies,
milestone/late heroes, and builders as one gameplay rule.

### [x] D4 — stale variable-range authoring note

The general authoring guide still said Ascendants occupied ids 0–80 even though the
v1.0.9 docs claimed it had been corrected to 0–96. All live guidance now records the
v1.0.10 range, 0–112.

## Closed in v1.0.9

### [x] B1 / B2 / B3 — the reference layer was a fiction

Ascendants is now **code-defined**. `scenario.reference` is gone, `base.aoe2scenario` is
deleted, `generated/` is renamed to `scenario/`, and all 13 file headers say what the
files actually are. `aoe2modes verify` and `decompile` no longer apply to this mode.

The decompiler kept a real round-trip test, repointed at `chieftains_4v4` (a mode that
genuinely still is a decompile) plus a synthetic scenario that pins trigger-variable ids
and names across a decompile cycle. A new
`test_ascendants_is_code_defined_not_decompiled` asserts the reference cannot regrow.

### [x] C1 — anti-trebuchet zones were not mirrored

Both area tables are now derived from one canonical P3 rectangle through the V2 cell
transform. All eight zones cover 4/4 of their own Castles (P4/P6/P7/P8 previously
covered 0/4). Verified safe: each effect is filtered to `TREBUCHET_PACKED` owned by one
specific enemy player, so a wider area cannot catch anything else.

### [x] C2 — civ array size was a magic `60`

Derived from `CIV_SPAWN_RULES`, with a build-time check that the spawn and builder
tables cover the same ids. An unsupported civilization id now reports itself in chat
instead of silently producing no army.

### [x] A1 — unnamed variable bases

`PENDING_BUILDER_VARIABLE_BASE` and `COMBAT_ROW_VARIABLE_BASE` are named and
interpolated into the XS. `_assert_variable_ids_are_contiguous` runs at the end of
`build()` and fails the build on a hole or a collision.

### [x] A3 — `free_costs.py` dead code

Deleted, and removed from `docs/ascendants-development.md`.

### [x] T1 — tautological anti-treb test

Replaced with a property test (one mirror orbit; every zone covers its own four
Castles) that uses the test file's independent transform rather than restating
`build.py`'s constants.

### [x] T2 — sweep the remaining Ascendants tests for the T1 pattern

All 50 Ascendants tests were reviewed. The wall-cleanup test was the remaining weak
case: it repeated all eight production rectangles without proving its stated rear-route
property. It now derives the serialized cleanup zones, proves they form one independent
mirror orbit, confirms they never intersect the protected rear paths, and still checks
the correct destroyed gate and runtime owner. Three repeated Castle-row tables were
also replaced by bounds derived directly from the four serialized Castles per color.

### [x] P5 — docs, Makefile, local release gate

Variable range corrected to 0–96 in `CLAUDE.md` / `AGENTS.md`; a
fourth "code-defined" mode flavour documented; `README.md` verify claim fixed;
`mode.toml`'s `[xs]` block explains why it is empty; `make check-ascendants` derives
the filename from `mode.toml` via the new `aoe2modes info --output-name` and runs
`aoe2modes audit`; stale `dist/` artifacts were removed; the audit verdict line is
ASCII. No hosted GitHub Actions workflow is committed, so pushes cannot consume
runner minutes.

### [x] Local `make` availability

`/usr/bin/make` is available on the current development machine, and
`make check-ascendants` completed successfully for v1.0.9. The explicit equivalent
commands remain in `docs/ascendants-development.md` for environments without `make`.

---

## Still open

### [~] Attribution

`authors = []`, and all `By:` attribution is stripped from trigger names (0 remain in
the build) on a mode derived from a community CBA Hero scenario. This was left alone
deliberately — it is a call for the maintainer, not a defect. Either populate `authors`
and credit the original author in `README.md`, or record that the derivation is distant
enough not to warrant it.

### [ ] `chieftains_ffa` fails `aoe2modes audit`

24 `dangling-unit-reference` errors in trigger 889 `==Rename======`, all
`change_object_name` effects selecting objects 106643–106671 that do not exist. The
same 24 errors are present in `modes/chieftains_ffa/base.aoe2scenario`, so this is
inherited from the community scenario and is not an Ascendants problem. Fix or
baseline it before making the audit a repo-wide release gate.

---

## Engine acceptance — nothing static can close these

`docs/ascendants-issue-register.md` tracks ASC-001…ASC-030. It marks verified fixes "Guarded"
or statically resolved, which that doc correctly defines as *"the serialized scenario
and tests contain the intended
correction; it does not mean the engine has been observed running it"*. Engine reports
confirmed the old ASC-019/ASC-020 behavior was still broken in v1.0.10. v1.0.13 replaces
the ASC-019 control mechanism; the new controls and ownership boundary still require
engine verification.

- [ ] **ASC-021 / v1.0.9 regression** — an enemy Trebuchet beside P4/P6/P7/P8's Castles is now
      removed, matching P1/P2/P3/P5. This is the only behavior change in v1.0.9.
- [ ] **ASC-003** — territory equality. C1 was a static counterexample; recheck.
- [ ] **ASC-005** — sparse-lobby spawn, including the unsupported-civilization message.
      Test P1 vs P5 and P2+P4 vs P5+P8.
- [ ] **ASC-019 / ASC-026** — independent sliders in all eight colors, full and sparse:
      Sheep L0–L5 for Castle waves; Penguin L0 OFF and L1–L5 for the current Hero tier.
      Confirm no lower-tier catch-up burst after re-enabling Heroes.
- [ ] **ASC-028** — order each Sheep/Penguin across the water gap and beyond every
      track edge. It must stay on its own track and reach every level. Confirm the
      entire snowy pad means HOLD/OFF, the first road tile means level 1, and all four
      per-color Signs plus both short controller names are readable.
- [ ] **ASC-029** — delete each side/rear Castle-yard switch gate and verify its
      short shoulders and long side walls disappear. The complete front gate/wall
      row, rear University walls/gate, and teammate access gates remain. Check both
      front ends and the University boundary for closed-gate bypasses in every color,
      including sparse and shuffled lobbies.
- [ ] **ASC-030** — reach 200 owned WALL-class objects to warn and 220 to wipe, using
      the count including preplaced walls. Verify the owner's walls disappear outside
      protected permanent barrier footprints, while front and University defenses,
      teammate access gates, and other players' walls survive. Confirm one-shot
      behavior and repeat after side-wall deletion in sparse and shuffled lobbies.
      Permanent barriers reject manual deletion; the switch remains deletable.
      Legacy side-wall Delete protection must not block scripted removal.
- [ ] **ASC-020** — shuffled lobby ownership: Red/Green reversed, Yellow before Green,
      then another nonnumeric order. Check ownership and civilization at every Castle.
- [ ] **ASC-022** — return milestone and 3500/5000 heroes through their spawn pads after
      they have received their automatic route.
- [ ] **ASC-023** — return both raze-reward villagers through their creation pads after
      the initial auto-park.
- [ ] **ASC-006** — vote kick with three and four teammates, and proof that two cannot.
- [ ] **ASC-024** — no static Palisade Wall or Saboteur in any outer corner.
- [ ] **ASC-025** — after Elite Huskarl, verify Goth Palisades retain ordinary game HP
      while the independent Anarchy/Barracks restriction still resolves normally.
- [ ] ASC-001, 002, 004, 007–018 — per the register's own "Required game check" column.

---

## Verified sound — do not re-review

- `wall_cleanup_bounds` was already 8/8 mirror-consistent (now derived anyway).
- `BASE_CASTLE_AREAS` is correct under the 144-position convention; Castles confirmed
  at 19 / 125 in the built file.
- Civ tables are complete for ids 1–59; spawn and builder tables agree exactly.
- All six XS↔Python variable bases agree at every access site.
- The `scenario/` layer is internally consistent — audits standalone with 0 errors — and
  contains **zero** variable references, so removing the old `VARIABLES` table did not
  rewire any trigger logic.
- `_compact_legacy_trigger_graph` fails closed on exact counts and asserts no empty or
  duplicate-named triggers survive.
- v1.0.9 build: `aoe2modes audit --strict` PASS, 0 errors / 0 warnings; 3,383 triggers,
  1,076 units, 97 variables; 65 focused and 110 repository tests pass; `ruff` clean;
  all 6 modes build.
- v1.0.10 build: `aoe2modes audit --strict` PASS, 0 errors / 0 warnings; 3,383
  triggers, 1,076 units, 113 variables; 67 focused and 112 repository tests pass;
  `ruff` clean; all 6 modes build. Final artifact hash is recorded in
  `RELEASE_NOTES_v1.0.10.md`.
- v1.0.11 build: `aoe2modes audit --strict` PASS, 0 errors / 0 warnings; 3,383
  triggers, 1,012 units, 113 variables; 69 focused and 114 repository tests pass;
  `ruff` clean; all 6 modes build. The final artifact hash is recorded in
  `RELEASE_NOTES_v1.0.11.md`.
- v1.0.12 build: `aoe2modes audit --strict` PASS, 0 errors / 0 warnings; 3,319
  triggers, 1,012 units, 113 variables; 69 focused and 114 repository tests pass;
  `ruff` clean; all 6 modes build. The final artifact hash is recorded in
  `RELEASE_NOTES_v1.0.12.md`.
- v1.0.13 build: `aoe2modes audit --strict` PASS, 0 errors / 0 warnings; 3,535
  triggers, 924 units, 121 variables; 54 focused and 114 repository tests pass;
  `ruff` clean; the full XS build succeeds. The final artifact hash is recorded in
  `RELEASE_NOTES_v1.0.13.md`.
- v1.0.14 build: `aoe2modes audit --strict` PASS, 0 errors / 0 warnings; 3,519
  triggers, 940 units, 121 variables; 57 focused and 117 repository tests pass;
  repository `ruff` clean; the full 616-line embedded XS build succeeds. Independent
  artifact readback verifies 484 protected permanent wall/gate references, all 64
  exact-reference wall breaches, and 16 contained controllers. The game-installed
  artifact matches the SHA-256 in `RELEASE_NOTES_v1.0.14.md`.
- v1.0.15 build: `aoe2modes audit --strict` PASS, 0 errors / 0 warnings; 3,647
  triggers, 14,561 conditions, 15,183 effects, 956 units, 121 variables. Complementary
  `.venv/bin/pytest -q tests/test_evolution_alpha.py` and
  `.venv/bin/pytest -q --ignore=tests/test_evolution_alpha.py` runs pass 59 and 60 tests
  respectively: 119/119. Repository `ruff` and the 616-line embedded XS build pass.
  Each wipe covers 20,368 cells in 49 rectangles, excluding 368 protected barrier
  cells. All 940 old objects and terrain are unchanged; 16 front posts are added.
  The game-installed artifact matches the SHA-256 in `RELEASE_NOTES_v1.0.15.md`.
- v1.0.17 build: `aoe2modes audit --strict` PASS, 0 errors / 0 warnings; 3,655
  triggers, 15,081 conditions, 14,752 effects, 956 units, 121 variables; 3,195
  initially enabled and 3,646 conservatively reachable. Complementary
  `pytest -q tests/test_evolution_alpha.py` and
  `pytest -q --ignore=tests/test_evolution_alpha.py` runs pass 73 and 60 tests
  respectively: 133/133. Repository `ruff`, all 6 mode builds, and the 637-line
  embedded XS build pass. Two liveness tests walk the serialized victory subsystem as
  a state machine and fail on the pre-fix build. Every terrain cell and all 956 placed
  objects are unchanged from v1.0.16; the diff touches trigger logic, the shared roster
  lists, three `scenario/` trigger names, tests, and documentation only. The artifact
  matches the SHA-256 in `RELEASE_NOTES_v1.0.17.md`. No live DE match was run.
