# CBA Naval: Admirals v0.5

Start a fresh match using **CBA Naval Admirals v0.5**. The startup announcement
and first Objectives rule identify version 0.5 and the 15-second port cycle.
Earlier versions and existing saved matches retain their old behavior.

The game's generated `default0.xs` showed v0.4 was loaded when the latest issues
were reported. This release therefore fixes the active design rather than
assuming an older scenario was selected.

## Production and actual dock launches

- Removed all eight preplaced ordinary ships per player. The opening now has
  only one hero flagship; there is no fleet burst or ordinary spawn point.
- Every completed owned port launches **at most one ship every 15 game seconds**.
  First regular wave: second 18. Four ports produce at most **16 ships per game
  minute**, six ports at most 24. Faster game speed changes wall-clock timing.
- Siege had bypassed the wave clock: v0.4 released one queued Cannon Galleon
  every heartbeat, potentially creating a ship every second. Siege now replaces
  one ordinary ship on a scheduled wave, at most one reward per wave. It cannot
  increase the wave size, and blocked/population-limited rewards remain queued.
- Ordinary and siege creation uses the actual producing dock reference and
  collision-checked water cells within four tiles. Original, relocated and
  completed built ports use that same path. Dead/captured docks cannot produce,
  and a blocked shore has no remote fallback.
- Duplicate or backward heartbeat callbacks do not produce ships, heal twice or
  advance center rewards twice. Late callbacks cannot catch up missed waves in
  a burst.

## Blue/Green movement

Replaced the two queued staging/battle orders with one unqueued attack-move
command to the concrete central water tile **(72.5, 72.5)**. Removed both color
route arrays and their mixed arithmetic/modulo lookup, which could supply an
invalid default destination. The new command contains no color-dependent
lookup or corner coordinate. It selects only the newly born ship; heroes,
builders and existing player-controlled units receive no automatic retasking.
The engine must still pathfind through the four-tile harbor mouth.

The movement API/action signature is verified against the installed
`Constants.xs` and the [official update 185872 API notes](https://www.ageofempires.com/news/age-of-empires-ii-definitive-edition-update-185872/).

## Retained mechanics

One hero at its own berth, 30-second death-to-return timer, current-tier
replacement, 3,000 HP ports, 1 HP/s repair within 14 tiles, allied vision,
30/60/90/120-kill builders with 400 wood/150 stone, Harbor Quarters satisfying
the Archery Range prerequisite, shore archers/towers, construction limits,
completed additional ports as lives, and owner-resolved defeat/cleanup/victory.

## Verification scope

The serialized XS runtime harness now checks the actual movement destination,
actual serialized terrain at ship creation, all eight color transformations,
all 32 initial dock exits, moved/built/blocked docks, exact wave deadlines,
large siege queues without extra births, missed-wave behavior, duplicate
callbacks, hero replacement/retry, fractional healing, kill/score totals,
construction limits, shared vision and sparse P7 native cleanup/victory.
Parser/XS validation and strict audit are separate from live DE acceptance.
No DE match was controlled during this change; pathfinding, AI overrides and
multiplayer behavior still require a fresh in-game test.
