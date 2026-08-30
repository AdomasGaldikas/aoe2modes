# CBA Hero: Ascendants v1.0.5 candidate

This candidate keeps v1.0.3 as its sole comparison baseline and carries forward the
warning-free v1.0.4 graph migration while resolving three engine-reported issues.

- Changes automatic army movement from a permanent one-second capture band to a
  color-specific one-shot launch pulse set only when XS creates a new wave.
- Guards all 24 original and 84 compact-owner Short, Medium, and Long move triggers,
  preserving collision-tolerant three-by-three launch areas without overriding a
  player's later return order.
- Converts the exact 20-cell non-buildable Beach ribbon beside each color's milestone
  hero shore into Grass 2: 160 symmetric repaired cells, with no water moved.
- Moves all eight Transport Ship markers two tiles nearer their matching shores.
- Makes marker ships Gaia-owned and applies stop, freeze, speed zero, selection,
  deletion, targeting, and attack protection so neither humans nor player AI control
  them.
- Retains 2,327 uniquely named non-empty triggers and 1,084 objects. The candidate has
  6,940 conditions, 6,975 effects, 89 variables, and 606 generated XS lines.
- Passes the serialized strict audit with 0 errors and 0 warnings.

File size: 93,590 bytes

SHA-256:
`b5182d2b123a389ca50a584ab341a5ea957246867b0528d44865b2079a3e3903`

AoE2:DE pathing, construction, AI, multiplayer, and XS acceptance remain required;
see `docs/ascendants-issue-register.md` for the exact in-game cases.
