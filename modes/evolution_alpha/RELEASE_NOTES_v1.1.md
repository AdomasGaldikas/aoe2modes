# CBA Hero 4v4: RA v1.1

## Wider allied routes

The four corner reinforcement routes widen from five to eight tiles along their
main sections. The north and south causeways widen from four to eight tiles in
the middle, while retaining their original four-tile gate approaches. The water
gaps between opposing teams and all existing gates and walls remain in place.

## Enemy exclusion

Enemy objects entering any of the six allied links are removed on a one-second
check. This includes hostile foundations and grants no combat kill credit.
Protection continues when a route's friendly endpoint is defeated or starts
closed; attacking still happens through the central arena.

Adrenaline Rush's post-defeat route kill zones inspired the rule. RA uses its own
geometry and resolved native player selectors rather than copying that mode's
fixed-player triggers. All 64 color/selector combinations are covered, without
new variables, native player conditions, or changes to the XS spawning runtime.

## Clarity

All twelve allied access gates are named `Allied route - enemy units removed`.
Objectives explain the wider routes, narrow gate entrances, and enemy-removal
rule. The instructions, history and victory message now use the RA name.

## Validation

Automated checks cover route widths and symmetry, six clear allied centerlines,
base-barrier reachability, protected controller tracks, and all 64 serialized
route-guard mappings, including inactive/closed protected endpoints. Build-time
XS lint and strict scenario audit are required before shipping.

These checks do not execute DE pathfinding or multiplayer scheduling. A new
in-game match must still confirm allied formations through the wider corners,
enemy removal before and after a teammate's elimination, and a sparse shuffled
lobby. v1.1 has not received live DE acceptance.

Artifact: `dist/CBA Hero 4v4 RA v1.1.aoe2scenario`.
