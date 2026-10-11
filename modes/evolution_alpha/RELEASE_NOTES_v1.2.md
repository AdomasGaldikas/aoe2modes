# CBA Hero 4v4: RA v1.2

Source-validated candidate following the [RA audit](../../docs/ra-audit-plan.md).

## Corrections

- New Castle armies, Heroes and builders receive an immediate Move order addressed
  only to their returned creation reference. An old unit parked on the birth pad is
  no longer selected by an area-based movement trigger (ASC-037 source correction).
- No wave movement pulse is armed when no Castle is eligible or every create fails.
- Eight deletable wall switches now say `Side-wall switch - DELETE opens walls`.
  Four permanent access gates keep `Allied route - enemy units removed`.
- Hero/builder production waits for its independent XS ownership token. Elimination,
  unused-color and Hero OFF guards remain, as do native kill/cap/buff conditions.
- The release Make target now treats structural audit warnings as failures.

The four Castle bindings, all range destinations, unit rosters, kill bands, costs,
terrain, route guards, walls, rewards, player settings and 145 variable IDs remain.
The old pulse/reset variables remain as bookkeeping; they no longer issue orders.

## Validation

150 repository tests passed, including 90 RA tests. The emitted XS wrappers are
executed for every XS owner, including parked old units, failed creation, delayed
identity, elimination and Hero OFF. Castle-wave tests execute all survival masks
and verify every ordered reference came from that wave's successful creates.

XS lint and Ruff passed. Strict readback audit reports zero errors/warnings:
3,968 triggers, 18,978 conditions, 13,922 effects, 956 objects and 145 variables.
A clean v1.1 comparison confirms all unrelated serialized systems, the full terrain,
placed objects, restrictions and effect execution orders are preserved. Map metrics
are unchanged: 10,776 land / 9,960 water tiles, 103 closed-gate / 81 open-gate regions.

## Live acceptance

Requires DE update 185872 or newer, which provides `xsTaskUnits` and corrected
creation IDs. See the [official update notes](https://www.ageofempires.com/news/age-of-empires-ii-definitive-edition-update-185872/).
The new API's immediate-reference and array behavior, native Hero buffs after the
new birth path, all route destinations and returned-unit orders need a fresh DE
match. Automated mocks do not prove engine scheduling or pathfinding.
ASC-053's native-condition probe and pre-owner-latch resignation also remain open
acceptance questions. v1.2 has not received live DE acceptance.

Artifact: `dist/CBA Hero 4v4 RA v1.2.aoe2scenario`.
SHA-256: `77699334ee3b2eb517ace105726531d92891a3ba0c4f8f8722250be79279ca0c`.
