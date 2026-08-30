# CBA Hero: Ascendants v1.0.7 candidate

This candidate replaces the v1.0.6 Sheep-selector implementation after direct engine
testing showed that none of the five positions reliably controlled milestone heroes.

- Rebuilds all 40 Short, Medium, Long, Hero Spawn Closed, and Hero Spawn Open
  conditions as symmetric approach regions that include the Sheep's reachable
  collision-limited stopping cells.
- Keeps all five controls mutually exclusive for all eight transformed island
  orientations, so crossing the center cannot change the latched route.
- Routes all 108 full/sparse milestone-hero order triggers through the same eight
  persistent route variables used by normal army waves.
- Removes all 36 competing `Hero Orders Open` triggers that continuously issued a
  fixed Medium order after Short or Long.
- Preserves the selected route when the Sheep moves to Closed/Open; those positions
  only create or remove the milestone-shore blocker.
- Retains the one-shot normal-wave launch guard, Transport Ship removal, and
  resignation object cleanup from v1.0.6.
- Produces 2,291 uniquely named non-empty triggers, 1,076 objects, 6,904 conditions,
  6,475 effects, 97 variables, and 606 generated XS lines.
- Passes the serialized strict audit with 0 errors and 0 warnings.

File size: 89,119 bytes

SHA-256:
`28dfec1fdf2d17e6b9bf00500d1167ad4dc780f2a350f8037b1c006722c20378`

AoE2:DE selector collision, hero routing, Close/Open blocking, multiplayer, pathing,
and XS acceptance remain required; see `docs/ascendants-issue-register.md` for the
exact in-game cases.
