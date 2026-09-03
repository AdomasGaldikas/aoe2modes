# Ascendants TODO

Open work from the v1.0.7–v1.0.13 source review. Most of it is closed in **v1.0.13**;
what remains is either a decision for the maintainer or something only the game engine
can settle.

Status key: `[x]` done · `[~]` decision needed · `[ ]` open

---

## Closed in v1.0.13

### [x] G1 — independent Castle-army and Hero controls

The shared five-position Sheep system is removed. Every color now has one Sheep with
six proportional Castle-army levels and one War Penguin with Hero OFF at level 0 plus
five progressively farther active levels. Both begin at level 3 on separate dry lanes.
Their reference-specific detectors cover the complete island, including both beach
caps, so neither can be stranded between levels. The old selector Relics, Rugs,
Torches, and Hero shoreline blocker toggle are absent.

### [x] G2 — Hero OFF could not leave stale tiers armed

The six milestone loops and late 3500/5000 loops now have mutually exclusive kill
bands and require Hero level 1 or greater. Re-enabling Heroes starts only the current
tier. All active Hero routes retain a one-shot creation pulse, so later manual orders
cannot be reclaimed at a spawn line.

### [x] G3 — controller clarity and safety

Endpoint Signs identify `CASTLE HOLD / HERO OFF` and `FAR BATTLE ROUTE`; both
controller names explain their role. Sheep and Penguins are undeletable and
untargetable. Penguins additionally use No Attack stance and zero scenario attack.
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

`docs/ascendants-issue-register.md` marks ASC-001…ASC-026 "Guarded" or statically
resolved, which that doc
correctly defines as *"the serialized scenario and tests contain the intended
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
