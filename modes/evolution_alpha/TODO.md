# Ascendants TODO

Open work from the v1.0.7/v1.0.8 source review. Most of it was closed in **v1.0.9**;
what remains is either a decision for the maintainer or something only the game engine
can settle.

Status key: `[x]` done in v1.0.9 · `[~]` decision needed · `[ ]` open

---

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

### [x] P5 — docs, Makefile, CI

Variable range corrected to 0–96 in `CLAUDE.md` / `AGENTS.md` / `docs/authoring.md`; a
fourth "code-defined" mode flavour documented; `README.md` verify claim fixed;
`mode.toml`'s `[xs]` block explains why it is empty; `make check-ascendants` and CI
derive the filename from `mode.toml` via the new `aoe2modes info --output-name`; CI now
runs `aoe2modes audit`; stale `dist/` artifacts removed; the audit verdict line is
ASCII.

---

## Still open

### [~] Attribution

`authors = []`, and all `By:` attribution is stripped from trigger names (0 remain in
the build) on a mode derived from a community CBA Hero scenario. This was left alone
deliberately — it is a call for the maintainer, not a defect. Either populate `authors`
and credit the original author in `README.md`, or record that the derivation is distant
enough not to warrant it.

### [ ] `make` is unavailable on the current machine

`make check-ascendants` is documented as the verification route but `make` is not on
PATH here. `docs/ascendants-development.md` now lists the three equivalent commands;
consider whether the Makefile is worth keeping as the primary interface.

### [ ] `chieftains_ffa` fails `aoe2modes audit`

24 `dangling-unit-reference` errors in trigger 889 `==Rename======`, all
`change_object_name` effects selecting objects 106643–106671 that do not exist. The
same 24 errors are present in `modes/chieftains_ffa/base.aoe2scenario`, so this is
inherited from the community scenario and is not an Ascendants problem — but it is why
CI audits the other modes informationally rather than gating on them. Fix or baseline
it if the audit should ever become a repo-wide gate.

### [ ] Sweep the remaining tests for the T1 pattern

`tests/test_evolution_alpha.py` is ~3,900 lines and 49 tests. One was tautological and
hid a real defect; the others have not been individually checked for the same shape
(restating `build.py`'s literals rather than asserting a property).

---

## Engine acceptance — nothing static can close these

`docs/ascendants-issue-register.md` marks ASC-001…ASC-020 "Guarded", which that doc
correctly defines as *"the serialized scenario and tests contain the intended
correction; it does not mean the engine has been observed running it"*. **None has been
engine-verified.**

- [ ] **v1.0.9 regression** — an enemy Trebuchet beside P4/P6/P7/P8's Castles is now
      removed, matching P1/P2/P3/P5. This is the only behavior change in v1.0.9.
- [ ] **ASC-003** — territory equality. C1 was a static counterexample; recheck.
- [ ] **ASC-005** — sparse-lobby spawn, including the unsupported-civilization message.
      Test P1 vs P5 and P2+P4 vs P5+P8.
- [ ] **ASC-019** — five-position Sheep routing, reworked twice. All eight colors, full
      and sparse, normal waves and 200/400/600/800/1000/2000 heroes.
- [ ] **ASC-020** — arbitrary lobby color order; a full lobby with Yellow before Green.
- [ ] **ASC-006** — vote kick with three and four teammates, and proof that two cannot.
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
- v1.0.9 build: `aoe2modes audit` PASS, 0 errors / 0 warnings; 3,383 triggers, 1,076
  units, 97 variables; 97 tests pass; `ruff` clean; all 6 modes build.
