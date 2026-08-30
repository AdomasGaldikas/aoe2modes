# CBA Hero: Ascendants v1.0.6 candidate

This candidate keeps v1.0.3 as its sole comparison baseline and carries forward the
v1.0.5 army-order and buildable-shore fixes with route-selection and cleanup changes.

- Replaces Short/Medium/Long trigger activation switching with eight persistent
  color-route variables read by all 108 full/sparse movement triggers.
- Expands every visible Sheep route marker into a disjoint three-cell approach strip,
  so Relic/Rug collision cannot prevent the route from latching.
- Keeps movement one-shot: the selected route consumes only the next-wave pulse, while
  existing armies remain under manual control.

- Removes all eight decorative Transport Ship milestone markers because the hero
  spawn works without them.
- Removes the complete marker implementation: unit creation plus 56 stop, freeze,
  speed, selection, deletion, targeting, and attack-protection effects.
- Adds a full-map object purge to all 36 valid color/runtime resignation resolvers.
  The purge targets the resolved runtime player, so compact-lobby colors remove the
  correct resigned player's units and buildings.
- Keeps the existing full-map cleanup for Castle defeat and vote-kick resolution.
- Retains all milestone hero creation, ownership, location, and order regression tests.
- Produces 2,327 uniquely named non-empty triggers, 1,076 objects, 7,048 conditions,
  6,655 effects, 97 variables, and 606 generated XS lines.
- Passes the serialized strict audit with 0 errors and 0 warnings.

File size: 91,541 bytes

SHA-256:
`b48699bf988bce31b002283b94230a96f611e6932365991849cb43447b7b0ca7`

AoE2:DE resignation scheduling, multiplayer, pathing, construction, and XS acceptance
remain required; see `docs/ascendants-issue-register.md` for the exact in-game cases.
