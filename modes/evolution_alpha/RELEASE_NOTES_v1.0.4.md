# CBA Hero: Ascendants v1.0.4 candidate

This candidate keeps v1.0.3 as its sole baseline and completes the parser-backed
trigger cleanup needed for safer local development.

- Removes 810 triggers proven to contain no conditions or effects, including the
  retired static army, cleanup, edge-delete, resource, and wall-removal shells.
- Removes the only 16 external references to those shells after proving they are
  no-op deactivations of the retired `no wall` family.
- Merges 189 byte-identical legacy civilization age-up triggers and rewires all 346
  incoming activations to 99 canonical triggers.
- Preserves three non-identical P7 parser variants as separate, explicitly named
  triggers instead of guessing that `0` and `-1` fields behave identically in-engine.
- Reduces the scenario from 3,326 to 2,327 triggers and from 99,694 to 92,111 bytes.
- Passes the serialized parser audit with 0 errors and 0 warnings.
- Exhaustively models all 6,560 occupied/alive sparse-lobby states for victory and
  defeat eligibility.
- Flood-fills every rear technology route to both buildings while treating water,
  walls, towers, Castles, and cliffs as blockers.

SHA-256:
`37207f4ea76bc7db60da631c9bfc24c0771ce3e39d936fd085e2df6fd3aa2e0c`

AoE2:DE multiplayer, XS, pathfinding, and UI acceptance remain required before this
candidate is called publish-ready; see `docs/ascendants-issue-register.md`.
