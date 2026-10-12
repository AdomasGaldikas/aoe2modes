# RA logic and design audit

Started 2026-10-11 from GitHub main `c1aaba3` (RA v1.1).

Goal: audit the maintained RA source and serialized scenario, fix confirmed logic
and map-design defects, validate the changes, and push a reproducible candidate.
Automated checks cannot certify DE pathfinding or multiplayer scheduling.

## 2026-10-12 code-only full audit

The user requested preserving the four-human lobby and auditing code only.
No game input or live acceptance test is part of this audit. The source review
covers owner identity, start/closed-slot resolution, Castle spawning and defeat,
hero bands and buffs, builder entitlement, population admission, backup lifetime,
route guards, vote-kicks, selection initialization, and Speed activation/expiry.

Confirmed correction: serialized builder rewards consumed a pending pair and
announced creation unconditionally, even when one or both XS creates returned -1.
Normal v1.7 and Speed v0.1.2 track delivered halves per color, retain entitlement
until both births succeed, and retry only the missing half. Population admission
uses the cost of the undelivered half on a retry. The existing owner-resolved
builder acknowledgement emits the completion notice. No new trigger variables
or map objects are needed; the state arrays are initialized by embedded XS main.

The suspected extra-Hero pad mismatch was ruled out: unbuffed milestone templates
have no pad buff and allow shared births, while boosted Genghis tiers already
guard their own type. Their triggers are preserved. Owner-wide backup cleanup,
native owner selectors outside ASC-053's declared sweep, and lobby-cap enforcement
still have the engine limits described below; this audit does not certify them.

Plan:

1. Review shared normal/Speed code and replay serialized failure paths.
2. Correct confirmed builder entitlement loss and partial-delivery duplication.
3. Run all repository tests, embedded XS validation, strict artifact audits,
   callable binding checks, and full terrain/object/player preservation comparison.
4. Push source and install the tested candidates without interacting with the game.
5. Keep public listing updates gated on the outstanding fresh-engine acceptance.

Artifact validation passed: embedded XS validation on both builds; strict
readback audits with zero errors/warnings; every embedded callable resolved;
129 changed triggers per mode (64 builder rewards, 64 builder acknowledgements
and XS SCRIPT). Terrain, units, players, options, variables, display order and
unrelated effect execution orders exactly match v1.6/v0.1.1. Normal has 22,827
conditions and 15,563 effects; Speed has 22,829 conditions and 15,563 effects.

Candidate files:

- `dist/CBA Hero 4v4 RA v1.7.aoe2scenario` —
  `1161eb5bff67136386d13d022361b0bbfa2454980329242e4f31d8969ee8caa1`.
- `dist/CBA Hero 4v4 RA Speed v0.1.2.aoe2scenario` —
  `9d4bd7cfb5590c5393651060f98a785b00255400680a3d1c771c8f942ef33950`.

All 177 repository tests passed in 440.86 seconds, including the three new
serialized builder failure cases. Repository Ruff and `git diff --check` passed.
Both files were atomically installed into the verified active DE profile's
scenario directory and their SHA-256 values above rechecked after installation.
Older scenario files were preserved. No game input was sent and the human lobby
was kept open. The currently selected lobby scenario is not switched by copying
new files; select the new version for the next fresh lobby/match.

The correction and audit evidence are delivered as source on GitHub main.
The earlier downloadable candidate directory and public mod listing remain
unchanged pending the fresh-engine acceptance items below.

## Current to-do list

- [x] Apply exact-type double-click selection (Run Pattern 140 = 255) in the
  shared normal/Speed initialization, covering each runtime player's complete
  engine object table, including new and upgraded types.
- [ ] Check double-click selection in a fresh DE match with different Hero/army
  types mixed together and with renamed controllers nearby. Drag-box and explicit
  mixed control groups retain their standard engine behavior.

- [x] Use lowercase `p# | k | d | r | b` HUD headings at the same text size as
  player rows, instead of the large bold objective-header style. Numeric and active
  rows now explicitly disable header styling and use matching lowercase `p#` tags.
- [ ] Check heading and player-row column alignment in a fresh DE match, including
  multi-digit kills/deaths/razings and backup states `1`, `A`, and `0`. The native
  objectives font has proportional widths; lowercase text alone does not guarantee
  fixed-width columns.
- [x] Remove the north-island population chooser, King, four signs, labels,
  ownership transfer and 60-second lock/default from both modes. Remove the
  script-selected limit and repeated free-housing rewrites. Use the stock 200
  fallback, retain native free-housing admission and clear civilization bonuses.
- [ ] In fresh normal and Speed matches, choose different population limits in
  the lobby (including 25 and 500). Verify every player has the same effective
  maximum and automatic births stop there, resume after losses and retain full
  builder/backup batch admission. Resource 4 is free housing, not the lobby cap;
  XS creation bypass behavior and lobby override still need engine evidence.
- [ ] Resolve the reported load/startup and missing-spawn failures in a fresh
  match; verify occupied-player HUD rows appear as well as the headings.
- [x] Validate the v1.6 / Speed v0.1.1 source candidates with all 110 focused
  tests, Ruff, embedded XS validation and strict audits of both written files.
- [ ] Complete fresh-game acceptance for lobby population and the reported
  load/spawn/UI problems before publishing new scenario files. An active match
  with human players must not be interrupted for testing.

The completed v1.2 audit below is historical evidence, not acceptance of the
current candidate. Current engine checks remain open until actually observed.

2026-10-11 candidate checks: all 168 repository tests passed in 492.89 seconds,
including 98 normal RA checks and 10 Speed checks. Repository Ruff and
`git diff --check` passed. Both builds validated their embedded XS, and both
written files passed strict audit with zero errors/warnings. The Speed tests
execute the emitted state machine and compare the serialized normal/Speed map,
units, players and ordinary gameplay triggers. These results do not establish
live DE acceptance. The active human match was preserved.

Candidate files and SHA-256:

- `dist/CBA Hero 4v4 RA v1.5.aoe2scenario` —
  `c2f44b1d2b327f5f230afc02489d50eb910e74353d553a5999c15c9234f1024a`.
- `dist/CBA Hero 4v4 RA Speed v0.1.0.aoe2scenario` —
  `670e127b426616964db34d8c72e98f9d3bcb4ca40ed2e1c4658af91f48e6808e`.

On 2026-10-11 the user explicitly requested installing both candidates and
pushing both to GitHub. Both exact files were installed in the active DE profile's
scenario folder and their hashes verified. Downloadable copies and `SHA256SUMS`
are tracked under `releases/ra-candidates`; the source and files are delivered on
GitHub main. The open human match was preserved. No Steam/AoE mod listing was
updated. The lobby-population replacement and fresh-game acceptance items above
remain open; installation and GitHub delivery do not establish live acceptance.

## 2026-10-12 selector removal and unit selection source checks

Normal RA v1.6 and Speed v0.1.1 remove the in-game population island, King,
four signs, labels, ownership transfer, script-selected cap and timed lock.
Both also initialize exact-type double-click selection without changing unit
classes or military/civilian interface roles.

All 110 focused tests passed (98 normal and 12 Speed). Repository Ruff and
`git diff --check` passed. Both written scenarios validated embedded XS and
passed strict audits with zero errors/warnings. Normal has 4,442 triggers,
994 objects and 153 variables; Speed has 4,444 triggers, 994 objects and
155 variables. Comparison with the delivered v1.5 file confirms exactly
48 changed terrain tiles and five removed objects; all other terrain and
object values remain unchanged.

Local build files and SHA-256:

- `dist/CBA Hero 4v4 RA v1.6.aoe2scenario` —
  `9451991fc1fee7e5ee97af5d4e0a4c277fc4003adf5878aa42b7a774ffca2f70`.
- `dist/CBA Hero 4v4 RA Speed v0.1.1.aoe2scenario` —
  `e023dcc73552a601433fb1c1d49638413e759f77640ac5ed60c000d5214de4ee`.

At source delivery these files had not been installed or added to the downloadable
candidate directory or mod listing. On the later explicit quick-install request,
both exact v1.6/v0.1.1 files above were installed and their hashes verified.
The downloadable directory and public mod listing remained unchanged. The existing
human match was left open. Fresh DE acceptance of lobby cap override, XS birth
hard-cap enforcement, loading/spawning, double-click selection and the HUD
remains required. In particular, resource 4 is free housing; mocked headroom
tests do not prove consumption of the lobby maximum. The only unused diagnostic
scenario created for this check was removed from the game folder.

## Separate Speed candidate

- [x] Add `ra_speed` (CBA Hero 4v4: RA Speed v0.1.0) using the maintained normal
  RA builder, map and hero roster; keep the normal artifact independent.
- [x] Implement a 900-second warm-up and 300-second teammate-loss rush: 2x
  movement and 3x fire rate, with independent teams, refresh without stacking,
  no closed-slot/early-loss payout, and visible remaining seconds.
- [x] Finish automated parity/runtime tests, XS build and strict audit.
- [ ] Complete fresh DE acceptance before public publishing; the user's current
  human match remains open as requested. See `modes/ra_speed/README.md` for coverage.

## Plan and completion

1. **Done — identity and match resolution.** Reviewed the 145-variable allocation,
   Castle-owner detection, resource-10 XS ownership bridge, closed-slot admission,
   persistent occupancy, elimination, owner-only cleanup and victory gating.
2. **Done — production and progression.** Reviewed all 59 civilization tables,
   bound Castle references, wave timers and caps, Hero kill bands/OFF/caps/buffs,
   queued builder pairs, movement, center rewards, costs and training restrictions.
3. **Done — map and destructive safety.** Reviewed six allied links, enemy guard
   rectangles, permanent/deletable gate roles, wall-breach masks, wall caps,
   anti-Trebuchet zones, spawn footprints, isolated controllers and vote eligibility.
4. **Done — confirmed corrections and regressions.** Replaced area capture with
   exact-reference birth orders, suppressed empty/failed-wave pulses, corrected
   switch labels, and made the release audit strict. See the evidence below.
5. **Done — validation and delivery.** Build/XS lint, 150 repository tests,
   strict audit and map report passed. Clean v1.1 readback comparison passed.
   Source commit `c44e026` was pushed to GitHub main. The local game candidate
   was installed with its hash verified, and both checkouts were synchronized.

## Confirmed findings and fixes

| Finding | Before | Correction and evidence |
| --- | --- | --- |
| ASC-037: returning-pad order collision | 1,984 native area-based task effects could include an older army/Hero/builder when a new birth armed the pulse. A one-shot timer did not identify a newborn. | `birth_orders.py` uses the reference returned by `xsCreateUnit` with `xsTaskUnits`. All 704 Hero/builder create effects call embedded zero-argument wrappers; Castle waves use the same helper. Serialized runtime tests execute 5,632 wrapper/XS-owner combinations, with an old pad occupant present, and check only the newly returned reference is ordered. Old movement triggers retain bookkeeping resets but no task effects. |
| ASC-054: side-wall switches mislabeled | v1.1 named all twelve access gates as generic allied routes, including the eight Delete switches controlling wall breaches. | Four permanent gates retain the route label; eight switches say `Side-wall switch - DELETE opens walls`. The regression independently derives those eight references from the serialized breach conditions. |
| ASC-055: false wave movement pulse | `cbaCreateWave` armed movement even with no eligible Castle or when all creates failed. | A pulse requires at least one nonnegative creation reference. All eight colors, all sixteen survival masks and three invalid-Castle states are executed, including all-create-failure cases and exact ordered references. |
| ASC-056: release audit accepted warnings | `make check-ascendants` audited without `--strict`, despite the documented warning-free requirement. | The target now rejects warnings. The candidate independently passes a strict audit with zero errors/warnings. |

Hero/builder creators additionally wait for token 1001–1008 before calling the new
XS path. This prevents a delayed ownership bridge from consuming a reward while
its creation helper cannot resolve an owner. The old native kill/cap/age/pad/vote
conditions and native buff effects remain. Emitted dynamic coordinates use float-first
arithmetic (`0.5 + x`), and wrapper definitions follow their helpers in XS.

## Validation and preservation

- 150 repository tests passed; 90 RA tests cover the serialized scenario.
- XS lint and repository Ruff passed. The validator's new-API stub is not embedded.
- Strict audit: 3,968 triggers, 3,508 enabled, 3,959 conservatively reachable;
  18,978 conditions, 13,922 effects, 956 objects, 145 variables; zero errors/warnings.
- A clean build of GitHub v1.1 was compared field by field with v1.2. Terrain,
  map size, players, restrictions, options, objects, display order and variables
  match. All 1,410 changed triggers belong to the declared birth/movement/label/XS
  scope; unrelated effect execution orders match.
- Map report and PNG inspected: 10,776 land / 9,960 water tiles, flat elevation,
  103 regions with gates shut / 81 open. The 72 mirror-x terrain differences are
  unchanged entrance accents. Existing eight-orientation geometry regressions pass.
- Artifact: `dist/CBA Hero 4v4 RA v1.2.aoe2scenario`.
  SHA-256: `77699334ee3b2eb517ace105726531d92891a3ba0c4f8f8722250be79279ca0c`.

## Remaining engine acceptance and design choices

The new exact-reference API comes from
[DE update 185872](https://www.ageofempires.com/news/age-of-empires-ii-definitive-edition-update-185872/).
A new DE match must confirm immediate creation references, `xsTaskUnits` array
consumption, all newborn routes, native Hero buffs, both builder sexes, and manual
orders on returned pad occupants. No live gameplay test was run in this audit.

ASC-053 remains open: 3,499 player-scoped conditions still use native selectors.
The previous live match showed working tiers/upgrades and no spurious votes, so
widening that XS sweep without a diagnostic probe would be an unsupported change.
This audit preserves its declared inventory and the existing cleanup/victory model.

A resignation before the three-second owner latch needs a startup probe: current
liveness tests assume starting owners are observed before departure. Distinguishing
an already-departed participant from a closed slot whose Castles remain requires
engine evidence; treating every owned closed-slot Castle as a participant would
break the existing closed-slot contract. This is an acceptance gap, not a claim
that the timing has been reproduced in DE.

Population tables remain wave-admission thresholds, checked before a wave, rather
than per-unit hard ceilings. A final four-Castle batch can exceed that threshold.
Changing batch size or civilization balance is outside these confirmed corrections.
The terrain and reward timings are preserved.

The source delivery is [commit c44e026](https://github.com/AdomasGaldikas/aoe2modes/commit/c44e026).
The audit goal is complete within the source/automated-validation scope above;
the explicitly listed engine checks remain unverified.
