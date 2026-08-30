# CBA Hero: Ascendants v1.0.3

This release fixes the shared runtime-owner regression observed in multiplayer and
finishes the distance-selector and vote-kick corrections.

- Detects every occupied color from the runtime owner of its own four-Castle row,
  avoiding ambiguous world-slot indexing.
- Restores correct-color automatic armies, builder rewards, HUD values, upgrades,
  heroes, and movement for all eight colors and compact lobbies.
- Keeps the Saracen first-builder threshold at two razings and awards every later
  razing normally.
- Uses a movable, zero-population Sheep as the five-position distance/hero-spawn
  selector instead of a cart.
- Removes all units and buildings belonging to a successfully vote-kicked player;
  two occupied teammates are still required, and kicking remains disabled below
  three active colors on a side.
- Verifies dry, unobstructed centerlines across all six links that connect each
  four-player team.
