# CBA Hero: Ascendants v1.0.10 candidate

This candidate completes the one-shot movement model after a full gameplay-oriented
audit of the v1.0.3-derived trigger graph. It fixes two real order-overwrite defects
without changing civilization units, spawn pacing, builder thresholds, age thresholds,
hero tiers, map geometry, team rules, or reward balance.

## Gameplay fixes

- **Milestone and late heroes no longer turn back at their spawn line.** The 192
  Short/Medium/Long hero order triggers previously polled their three-by-three spawn
  area every second. Any owned hero that returned through the pad could be retasked
  toward the arena. Each color now has one hero-creation pulse; a 200/400/600/800/1000/
  2000 milestone or 3500/5000 Genghis loop arms it, and exactly one matching
  runtime-owner route consumes it.
- **Raze-reward builders no longer lose later player orders.** The 64 builder movers
  had the same continuous polling behavior. Each reward now arms a separate
  color-specific builder pulse after creating its male/female pair; the resolved owner
  auto-parks the new pair once and resets the pulse.
- Normal Castle-wave movement keeps its existing one-shot pulse behavior. Short,
  Medium, and Long remain persistent Sheep-selected routes shared by normal armies and
  heroes. Closed/Open still control only the milestone blocker.

## Expert audit findings

- All 448 reachable looping `Task Object` triggers now require and consume exactly one
  creation pulse, have a one-second timer, and issue an explicit Move action. A new
  scenario-wide regression enforces that invariant instead of testing only named
  families.
- All 64 color/runtime mappings remain present for army spawns, routes, builders,
  milestones, late heroes, upgrades, center rewards, defeat, resignation, victory,
  vote resolution, and HUD ownership—including Green→runtime P4 and Yellow→runtime P3.
- The full civilization tables still cover ids 1–59. Unit/cap/interval mappings,
  builder thresholds, and the v1.0.3 Castle/Imperial kill thresholds were inspected and
  deliberately left unchanged.
- Every destructive family remains narrowly filtered: anti-Trebuchet effects target
  packed Trebuchets, center cleanup targets packed units on the reward cell, wall and
  gate effects target their intended unit/class or selected reference, and the only
  full-player removals are guarded defeat/resignation/vote-kick purges.
- The map remains the same tested 144×144 geometry: 1,076 objects, all eight Castle
  territories and spawn transforms, 160 buildable milestone-shore cells, protected
  team routes, and zero Transport Ships.
- A stale authoring note that still claimed variable ids 0–80 was corrected. The
  complete v1.0.10 allocation is 113 contiguous, collision-free ids (0–112).

## Verification

Produces 3,383 uniquely named non-empty triggers, 1,076 objects, 11,640 conditions,
10,871 effects, 113 variables, and 615 generated XS lines. The strict parser audit
passes with 0 errors and 0 warnings.

Focused tests: 67 passed

Repository tests: 112 passed

Ruff: clean

All six modes: build successfully

File size: 125,566 bytes

SHA-256:
`03d1e97ce5a01bdf36ca22c72e959d55c3c1e015424d707ca71b14fafa0a161e`

## Required in-game acceptance

Parser checks cannot execute Definitive Edition pathfinding or multiplayer scheduling.
For every color in a full and a shuffled/sparse lobby, let a normal army, milestone
hero, late Genghis, and builder pair leave automatically; then order each one back
through every relevant spawn pad. No existing unit may turn around unless a genuinely
new unit is created on that same tick. The complete manual matrix remains in
`docs/ascendants-issue-register.md`.
