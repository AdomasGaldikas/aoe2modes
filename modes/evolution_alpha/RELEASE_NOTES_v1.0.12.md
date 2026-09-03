# CBA Hero: Ascendants v1.0.12 candidate

This candidate removes the last Palisade-specific gameplay mechanic. It contains the
v1.0.11 shuffled-lobby ownership, Sheep, army, and hero route fixes unchanged.

## Removed mechanic

- The legacy rule did not create Palisades and was not a razing reward. It waited for
  a Goth player to research Elite Huskarl and place exactly 12 Palisade Walls in a
  designated row near the Castle lane, then added 2,750 HP to those walls.
- All eight imported `hp (p#)` triggers are reset and removed, along with their incoming
  activations. The build no longer creates the 64 color/player replacement triggers.
- The serialized scenario contains no static Palisade object and no condition or effect
  targeting the Palisade Wall unit. The 56 corner Palisades and eight corner Saboteurs
  removed in v1.0.11 remain absent.
- Goth army spawning, civilization balance, milestone heroes, and the separate
  Anarchy/Barracks restriction are unchanged.

## Verification

Produces 3,319 uniquely named non-empty triggers, 1,012 objects, 11,384 conditions,
10,807 effects, 113 variables, and 613 generated XS lines. The strict parser audit
passes with 0 errors and 0 warnings.

Focused tests: 69 passed

Repository tests: 114 passed

Ruff: clean

All six modes: build successfully

File size: 123,686 bytes

SHA-256:
`b9096bf0140c4b1db87d9bbe37d2dafc20c1dd3ac0ab7bdc2f7899f12eb2622f`

## Required in-game acceptance

As Goths, research Elite Huskarl and place Palisades near the Castle lane. They must
retain ordinary game HP and receive no scenario-specific increase. Confirm that Goth
Anarchy/Barracks progression and normal army/hero spawning still work. The complete
ownership and Sheep-route matrix remains in `docs/ascendants-issue-register.md`.
