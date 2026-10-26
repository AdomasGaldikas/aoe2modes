# RA logic and design audit

Started 2026-10-11 from GitHub main `c1aaba3` (RA v1.1).

Goal: audit the maintained RA source and serialized scenario, fix confirmed logic
and map-design defects, validate the changes, and push a reproducible candidate.
Automated checks cannot certify DE pathfinding or multiplayer scheduling.

## 2026-10-26 RAM v0.11.1 starting-leader attack growth

The user reports that v0.11.0 leaders still do not gain attack over time. The
previous simulated XS callbacks did not establish native behavior. This patch
restores native exact-reference Change Object Attack effects and explicitly
selects base pierce class 3 for all eight normalized ranged starting leaders.
The eight-second timer and eight +5 HP effects are preserved exactly.

- [x] Remove custom attack mutation callbacks and their simulated engine model.
- [x] Require eight native ADD +3 effects, explicit pierce class and the original
  starting references; retain separate selection and national names.
- [x] Finish tests, Ruff, embedded XS, strict artifact audit and package hashes:
  96 passed, strict audit 0/0, all 910 files verified; DAT and 893 audio files
  match v0.11.0.
- [ ] Fresh native match: displayed total attack increases at 8/16/24 game seconds
  while later spawned heroes remain unaffected. Observe multiple ranged actors.
- [x] Install the new v0.11.1 scenario while the game remains open at the user
  explicit request. Keep the loaded v0.11.0 Data Mod: its DAT is byte-identical.
- [ ] Update the existing unlisted listing after user native acceptance.

The user explicitly chose manual testing without closing the game. The new
scenario is installed atomically under its versioned name; no game input or
Data Mod reload is performed. The native-failure acceptance check remains open
until the user tests a fresh v0.11.1 match.

## 2026-10-24 RAM v0.11.0 whole-roster balance candidate

The user rejected limiting the balance pass to the reported problem civilizations.
The new candidate reviews team roles across all 62 and changes 57, including
modest new health increases for 26 ordinary armies and the retained Lithuanian
bonus. Native attack/armour classes,
weapons, movement, abilities, kill progression, center mechanics and growing
ranged starting leaders remain intact. Theoretical global four-Castle birth
frequency remains 95.25% of v0.10.0; health delivery proxy remains 97.68%.

- [x] Correct the comparison's missing Armenian pierce-armour bypass and retain
  explicit inventories of native auras, slows, damage/attack-speed growth and
  melee-blocking armour. Avoid interpreting encoded charge fields as raw DPS.
- [x] Give every civilization equal paired-lineup exposure, report separate
  1v1/2v2/4v4 results and health/kill-feed metrics, and exercise eight cap/contact/
  starting-field sensitivities. Keep mixed/unfavorable proxy results visible.
- [x] Preserve native population admission; resource40 military-cap weighting
  remains unverified, with body/population interpretations compared separately.
- [x] Complete tests, Ruff, embedded XS validation, strict written audit and
  full-package hash checks for the new version: 96 passed, strict audit 0/0,
  all 910 payload files verified; all 893 audio files and DAT match v0.10.0.
- [x] Inventory written-file native/class-wide stat scopes and all embedded XS
  stat writes: no native wave stat overwrite, exactly 27 guarded additive HP
  mutations, no wave HP SET/multiply overrides.
- [ ] User fresh-match balance/voice/leader acceptance, including early armies,
  later researched armies, hero transitions, center fights and mixed teams.

The user initially requested leaving the test package ready, then explicitly
requested a full update and closed DE. Version 0.11.0 is now installed as the
subscribed RAM entry (online ID 551448 preserved) with its matching scenario, and
published to the same unlisted listing at service revision 1.8. The existing
preview is retained; old installed files are backed up outside the mod scan.
Native gameplay acceptance remains open. The full target table and screening
limits are in `docs/ram-balance-v0.11.0.md`.

## 2026-10-24 RAM v0.10.0 candidate after live v0.9.0 feedback

The user reported missing Lithuanian speech, weak Lithuanian armies, and dominant
Spanish/Saracen armies. RAM v0.10.0 is a local test candidate; the user opted to
perform fresh-match testing. The existing public human lobby is left untouched.

- [x] Trace actual Lithuanian Castle births to Elite Leitis 1236 and inspect its
  installed selection Sound group; the unit ID was correctly bound in v0.9.0.
- [x] Cover selection and both legacy command-response slots, preserving Wwise
  fallbacks, weapon/death audio, original voice bytes and old resource aliases.
- [x] Require voice coverage of all 62 actual civilization Castle-wave IDs;
  retain explicit native-language fallbacks where no accepted custom voice exists.
- [x] Review all 62 civilization pacing decisions, with bounded changes and
  explicit user-reported Lithuanian/Spanish/Saracen corrections.
- [x] Use native bow/crossbow/firearm starting commanders for every civilization,
  with common starting combat profiles and separate double-click selection.
- [x] Preserve the original exact-reference eight-second +5 HP / +3 attack growth.
- [x] Run candidate tests, Ruff, embedded XS validation and written-file strict audit.
  89 distinct current cases covered (87 full-suite cases plus the final 20-case
  audio subset, including two newly added crew cases); strict audit 0/0.
- [ ] Fresh-match Lithuanian selection and command-response playback.
- [ ] Fresh-match all-leader ranged attacks, growth, selection, save/load and
  native animation, plus representative mixed-team balance tests.
- [ ] Second-client audio delivery and playback after the candidate is accepted.

Short extensionless filenames are a compatibility adjustment, not a proven cause
of the reported silence. Static Sound assignments and DAT readback do not prove
native playback or fair win rates. Publish only after the reported native failure
has been resolved by the user's fresh-match test.

## 2026-10-12 simplified hero ladder

RA v1.9 and Speed v0.1.4 remove the 100-kill Archer of the Eyes and 700-kill
Harald tiers. Charles Martel now covers 600–799 kills. Harald Hardrada replaces
Subotai at 800–999 kills, retaining the existing five-second interval. The first
Hero remains Robin Hood at 200 kills; all later Genghis tiers retain their
thresholds, buffs and spawn intervals. Both variants use the same eleven tiers.

The saved-file comparison removes exactly 128 owner/color tier triggers and
changes the 64 Charles upper bounds, 64 Harald births and embedded XS bundle.
Map/terrain, objects, players, options and variable IDs are preserved. Both XS
bundles validate, both strict audits have zero errors/warnings, and all embedded
calls resolve. Native identity exposure remains in ASC-053: this roster change
removes 256 native kill conditions without widening the identity sweep.

- RA v1.9 SHA-256: `d8c2e9df493985f2ce27cf68ce808d919da758e745bf077fe02ed2a53b404d26`.
- Speed v0.1.4 SHA-256: `9fb2bde591e966e860db961b02ea3ea7e7b519130697d08bdc2cec442926542e`.

Validation: 116 passed in 153.47s (0:02:33). Repository Ruff and `git diff --check`
passed. Both candidates were atomically copied into the game scenario folder and
the installed SHA-256 hashes match the audited files. Source is merged to main
and delivered to GitHub; no game UI actions are performed.

Fresh-match acceptance remains open: no Hero before 200 kills, Charles continues
through 799, Harald appears at 800, and neither retired Hero is created. The
human lobby stays open; public mod-listing updates still wait for outstanding
engine checks, including population and native owner selectors.

## 2026-10-12 reported zero population capacity

The user clarified the RA v1.6 HUD reads `33/0`. This reports nonzero used
population and zero displayed capacity. Inspection of the v1.6 written file
confirms all eight stored fallback caps are 200; its eight inherited startup
housing effects grant +195 free housing. The remaining XS writer is
`xsSetPlayerAttribute(worldPlayer, cAttributeUnitLimit, 0)` in combat refresh,
called from main and every two seconds. v1.7 preserved this code.

Resource 32 is documented as bonus population, so code evidence does not prove
this write causes the zero denominator. It is nevertheless an unwanted remaining
population override after the user's lobby-only requirement. RA v1.8 and Speed
v0.1.3 remove it and introduce no replacement fixed limit. The emitted scoring
body is executed three times for each runtime owner, preserving resources
4/11/32/62 while still producing correct combat scores. Remaining game acceptance
includes the displayed capacity, actual lobby cap, all-player/civilization parity
and automatic births. The current lobby is preserved and no UI test is run.

Validation: all 114 normal/Speed tests passed in 179.52 seconds; repository
Ruff and `git diff --check` passed. Both builds validated embedded XS and both
readback audits report zero errors/warnings. Compared with v1.7/v0.1.2, only
XS SCRIPT differs; all native triggers, map/terrain, objects, players, options,
variables and unrelated effect execution orders are preserved. Every script
call resolves. Both files were atomically installed and their hashes checked;
source is delivered on GitHub main. The public mod listing remains unchanged.

- RA v1.8 SHA-256: `020c80806b62becbffbb97ad56d64cc2799602f14077f4ea87c5543906d7009a`.
- Speed v0.1.3 SHA-256: `49804c7ae17da9f42cd72ab0812cbe2747a7f78410d790710999731d4e589bad`.

No claim is made that this proves the reported zero display is fixed in DE.
Existing matches/saves keep their embedded scripts; a new file must be selected
for a fresh match to exercise this correction.

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
