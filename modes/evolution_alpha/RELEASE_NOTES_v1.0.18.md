# CBA Hero: Ascendants v1.0.18 candidate

Fixes the report that a player loses all Castles but keeps some buildings/items.
Built on Adomas Galdikas's September 5 GitHub update, commit `eb9a077`, pulled by
fast-forward from v1.0.16 before making this patch. That update's victory, roster,
documentation, and naming changes are retained.

## ASC-047 — elimination did not guarantee cleanup

In v1.0.17 the row-empty fallback and XS could mark a color eliminated before its
normal defeat resolver ran. XS then cleared `p#coloractive`, but that resolver
required active=1. The fallback did not remove objects, and victory only checked
aliveness. The one-shot resignation cleanup was not an independent retry either.
Earlier tests modeled victory declarations but ignored Remove Object effects, so
they could pass with defeated owners' buildings still present.

The correction separates three states:

- `coloroccupied` (121–128): XS latches that the color actually participated. It
  does not clear on defeat. Cleanup must require this, so a residual closed-slot
  Castle row cannot authorize removal of another live player's objects.
- `coloreliminated` (48–55): existing permanent elimination signal. XS alone still
  owns the transient `coloractive` block.
- `colorcleaned` (129–136): empty lobby colors initialize clean; the first in-game
  observation resets the color to not-clean. An owner-resolved trigger confirms
  clean only after fewer than one object remains owned by that player.

All 64 Castle-loss resolvers use persistent occupancy instead of active=1. Castle
loss, resignation, and vote-kick share the same purge: enable deletion for the
resolved owner, then Remove Object with **no area, type, class, state, reference,
or quantity restriction**. No wildcard player, territory sweep, ownership swap,
or exception for protected walls/gates is used. Living owners' protections remain.

64 one-second cleanup loops continue after elimination, using the cached trigger
owner and persistent occupancy rather than the current active bit. A separate 64
empty-owner confirmation loops gate victory: every opposing color must be inactive
and clean. This catches residual objects after a one-shot purge and does not depend
on the player still being active. The main purge still precedes declaring defeat.

## ASC-048 — production could outlive the elimination signal

Trigger-based object producers with a color-active guard now additionally require
eliminated=0, closing the interval before XS refreshes active. XS Castle spawning
and builder queuing also return immediately when the color is eliminated. This
prevents a later Hero/builder/reward pass from recreating objects after cleanup.

## Regression coverage

The new object-cleanup state-machine test fails against the pulled v1.0.17 artifact.
It evaluates serialized removal effects and inspects every victory snapshot, rather
than merely checking that somebody eventually wins. Cases cover six lobby layouts,
both losing sides, XS/fallback pre-emption, and already-spent one-shot resolvers.
Inputs include the placed non-Castle objects plus foundations, unfinished objects,
garrisoned-unit representatives, dying objects, and a Gaia sentinel. Other owners'
objects must remain. Independent structural checks pin all 64 cleanup mappings,
unrestricted owner filters, retry timers, confirmation conditions, and birth guards.

This model does not execute DE's actual garrison, pathfinding, or trigger scheduler.
Live acceptance is still required: lose all four Castles with a University, walls,
gates, towers, foundations, military units and garrisoned units remaining. Repeat
for each color, sparse/shuffled lobbies, resignation and vote-kick, including the
last opponent. All defeated-owned objects should disappear; survivors and Gaia
must remain. Victory must not leave defeated-owned buildings on the map.

## Preserved behavior

No terrain, placed object, roster, Castle/Hero distance, wall-wipe rule, or reward
balance is changed from v1.0.17. The first Penguin ON setting remains on the Army
HOLD line directly in front of Castles. Scorpions still expire after 50 seconds.
ASC-037 (returning units sharing a new-birth capture pad) remains open and separate.

## Verification

- 138 repository tests pass: 78 Ascendants and 60 other tests. Targeted cleanup
  checks additionally cover resignation with Castles still intact.
- Full build and 646-line embedded XS validation pass; repository Ruff and
  whitespace checks pass.
- Strict artifact audit: 0 errors, 0 warnings; 3,783 triggers, 16,873 conditions,
  15,136 effects, 956 objects, 137 variables. There are 3,323 initially enabled and
  3,774 conservatively reachable triggers.
- Readback comparison confirms all 956 placed objects, 20,736 terrain cells, and
  all eight unit/building/technology restriction lists unchanged from v1.0.17.
- Artifact: `CBA Hero Ascendants v1.0.18.aoe2scenario`, 161,074 bytes.
- SHA-256: `5262f6250889eb1dd6d0caeb9bdc080d8bf9c59c97725588d3f827274858a19d`.
- Installed alongside previous versions in the user's DE scenario directory; the
  installed checksum matches the verified artifact.

No live DE match was run. Start a new match with v1.0.18; a running or saved match
does not inherit changes to its scenario file. The earlier scenario versions are
retained for comparison and recovery.
