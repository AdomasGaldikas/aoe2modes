# RA logic and design audit

Started 2026-10-11 from GitHub main `c1aaba3` (RA v1.1).

Goal: audit the maintained RA source and serialized scenario, fix confirmed logic
and map-design defects, validate the changes, and push a reproducible candidate.
Automated checks cannot certify DE pathfinding or multiplayer scheduling.

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
5. **Validation done; delivery pending.** Build/XS lint, 150 repository tests,
   strict audit and map report passed. Clean v1.1 readback comparison passed.
   Push and checkout synchronization are the final delivery steps.

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
