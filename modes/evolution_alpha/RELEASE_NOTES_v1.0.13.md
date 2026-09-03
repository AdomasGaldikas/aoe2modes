# CBA Hero: Ascendants v1.0.13 candidate

v1.0.13 replaces the collision-prone five-position shared Sheep control with two
simple, independent proportional sliders for every color.

## Spawn controls

- One **Sheep** controls new Castle armies. Its six positions are levels 0–5: level 0
  parks each newly created wave one tile Castle-ward, while every step forward sends
  the wave farther into battle.
- One **War Penguin** controls Heroes. Level 0 disables all automatic Hero production;
  levels 1–5 enable it and route each new Hero progressively farther into battle.
- Both controllers start at level 3 and have clear rear and forward endpoint signs
  plus descriptive in-game names. Reference-specific bands cover the full 9×7 island,
  so crossing the visual lane separator or reaching either beach cap cannot strand a
  controller between levels.
- All eight colors use the same canonical geometry transformed around the map. The 96
  selector triggers and 704 color/runtime-owner movement triggers are generated from
  shared tables rather than hand-maintained per-color copies.
- The controller objects cannot be deleted or attacked. The Penguin has No Attack
  stance and zero scenario attack so AI behavior cannot turn it into a combat unit.
- The Penguin's real one-population cost is excluded from custom army/Hero ceilings;
  the hard cap is 251 so every player retains 250 normal gameplay slots.
- The old 40 Relics, 40 Rugs, 32 selector Torches, five-position trigger geometry, and
  Hero shoreline blocker toggle are removed.
- XS creates Castle waves at the centres of transformed map cells, and one-shot routes
  capture only that exact cell. All 32 decorative Hay Stack creates are removed after
  footprint validation found that they overlapped 16 launch pads and eight L0 targets.

## Hero tier safety

Hero production now uses mutually exclusive kill bands: 200–399, 400–599, 600–799,
800–999, 1,000–1,999, 2,000–3,499, 3,500–4,999, and 5,000+. Every band requires the
Penguin to be at level 1–5. Turning Heroes off therefore pauses spawning without
leaving lower tiers waiting to burst when Heroes are enabled again.

Castle army, Hero, and builder routes retain their one-shot creation pulses. Moving a
controller affects only future spawns, and returning units are not reclaimed when they
cross their creation pads.

## Verification

- Ascendants-focused tests: 54 PASS; full repository tests: 114 PASS.
- Ruff: PASS.
- Full XS build: PASS, 616 embedded XS lines.
- Strict structural audit: PASS, 0 errors / 0 warnings.
- Final graph: 3,535 triggers, 14,065 conditions, 11,855 effects, 924 units, and 121
  contiguous variables (ids 0–120).
- Artifact size: 131,255 bytes.
- SHA-256:
  `41d907e24018d5453f2dbd51abff6b04a85a5cc5a4f75a2f7dd80fbaa719d4c0`.

The artifact still requires an in-game pass for controller movement, pathfinding, Hero
OFF/ON behavior, all eight orientations, full/sparse/shuffled ownership, and multiplayer
scheduling. Static verification cannot execute the Definitive Edition engine.
