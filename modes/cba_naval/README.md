# CBA Naval: Admirals v0.5.1

The v0.5.1 release makes new ships move clear of their launching dock before
heading to battle. It retains the slow production and bounded siege rewards
from v0.5. See [the release notes](RELEASE_NOTES_v0.5.1.md). Start a fresh match.

A separate sea CBA with RA's eight symmetric perimeter bases, four fleet ports
as lives, narrow island harbors and automatic naval battles. The land modes remain
independent. See [the v0.3 construction plan](PLAN_v0.3.md) and [the 0.1 investigation](PLAN_v0.2.md).

## The opening

Each player starts with four ports, Harbor Quarters, two Guard Towers, two shore
Archers and one Longboat hero flagship at a separate berth inside the lagoon.
There are **no preplaced ordinary warships** and no separate ordinary spawn pads. At three seconds the runtime resolves the actual
owners and shares allied vision. The hero receives no fleet order. The
first reinforcement wave arrives at **18 game seconds**, then every **15 seconds**.
Each surviving port launches **one ship**, for four ships per full wave. Each
port cycles ranged/fire/ranged/demo, with staggered phases to form a mixed fleet.
Four ports produce **16 ships per game minute**, including siege rewards, down
from the v0.4 regular rate of 24 plus extra siege releases. Six ports produce 24.
Timing uses game seconds, so faster game speed also speeds up the wall-clock rate. The cap is **120 military population**, including siege, flagships and shore archers.

Every new ordinary or siege ship first receives a **move order about three tiles
away from its producing shore**, into the lagoon. A pure move keeps it from
stopping to fight at the launch cell. Its queued attack-move then heads toward
the central water tile **(72.5, 72.5)**. Both commands select only that new ship;
each living ship has its own stable selector. The engine finds the route through
the narrow entrance. There are no color-route arrays, default corner destinations
or later movement pulses. Your subsequent orders remain yours. Creation checks
collision and tries water positions within four tiles of the actual producing
dock. It never falls back to a remote spawn pad. A blocked dock misses that wave;
clear its shoreline for the next cycle. Failed reward creation keeps its
entitlement rather than silently consuming it. The Waves counter counts only
waves which successfully launched at least one ship.

The navy is automatic; ships and workers cannot be trained. Transport ships,
markets, economy buildings and research are disabled. Only Archers can be
manually trained, from an earned Archery Range. Civilizations are selectable
and can still affect engine unit stats.

## Defend and break the harbors

Starting and newly built ports have **3,000 HP**, harbor batteries **1,100 HP**. The batteries are
attackable and permanently lost when destroyed. Each lost port permanently
removes its reinforcement contribution; the fourth lost port eliminates the
player immediately unless they have a completed additional port. Losing the last
completed port purges all their ships, civilians, archers, towers and buildings.
Surviving ships do not count as extra lives. Default conquest requirements are
explicitly disabled; results come from the port-based custom victory graph.

Near a surviving own port, ships regain **1 HP per game second**, including
during combat, up to their actual maximum HP. Healing starts on the next heartbeat
with no damage cooldown. Several ports do not stack the rate. Range is **14 tiles**;
ships outside the harbor, enemy ships and destroyed ports receive no repair.
Retreat a valuable flagship instead of losing it, and break harbor batteries
before committing your siege ships. Builders can add or replace defenses.

Each lagoon is surrounded by a continuous ring of land, with one **four-tile sea
entrance**. The eight land islands are separated by deep/medium water, including
a three-tile outer moat. Civilians and archers can walk around their own harbor
but cannot reach another harbor or the reef islands. Ships do the attacking;
shore archers and towers can shoot into the entrance and lagoon.

Four symmetric reef islands give fleets cover and flank routes around the
central sea. The azure central square is unobstructed and remains the control
objective. The small terrain preview highlights its exact 16×16 boundary.

## Earn civilians and build the harbor

At **30, 60, 90 and 120 real kills**, earn one Villager, **400 wood and 150 stone**.
Prestige advances naval tiers but does not earn builders. Rewards retry when
placement fails; supplies are credited only when the builder actually appears.
Builders receive no automatic movement orders. Select them and use the normal
construction menu. Housing is supplied automatically; no Houses are needed.
There are no resource deposits or gathering buildings.

The starting **Harbor Quarters** is a Barracks that satisfies the normal Archery
Range prerequisite. Infantry and additional Barracks stay disabled. Once your
first builder arrives, you can build the Range immediately if you have **200
wood**; no separate kill threshold or research is required. Training an Archer
costs **50 wood**, with no food/gold charge. The first reward can pay for a Range
and four more Archers, or a port and two Archers (if a Range already exists).

| Choice | Cost | Limit per harbor |
| --- | ---: | --- |
| Additional Fleet Port (Dock) | 300 wood | 2 in addition to the original ports |
| Watch Tower | 100 wood + 100 stone | 4 in addition to the starting batteries |
| Archery Range | 200 wood | 1 |
| Archer from the Range | 50 wood | 12 alive, including the two starting archers |

Place docks along the **inside lagoon shore**, clear of the entrance. Good spots
are the middle of the inner north/south banks. Docks outside the inner build area
or beyond the limit are removed and their configured cost refunded. Extra towers,
ranges and archers placed/queued beyond their limits are similarly refunded.
Destroyed structures/archers free their limit but replacements still cost supplies.

A completed additional port becomes a life, a repair point and another one ship
per wave. Six completed ports therefore launch six ships, still subject to the
military cap. A foundation provides none of those benefits. Losing all completed
ports eliminates immediately: starting a foundation cannot buy extra time, and
finishing a port after defeat cannot revive a player.

Archers can move, fight or garrison in defenses within their own land island.
No transports or land bridges exist. Extra docks are restricted away from the
four-tile mouth to preserve the shipping route.

## Kills, tiers and siege

Kills plus control prestige unlock improved **new** reinforcements. Existing
ships retain their types; only one flagship may be alive at a time.

| Tier | Kills + prestige | Ranged fleet | Support fleet | Replacement flagship |
| --- | ---: | --- | --- | --- |
| 0 | 0–19 | Galley | Fire Galley / Demolition Raft | Longboat |
| 1 | 20–59 | War Galley | Fire Ship / Demolition Ship | Longboat |
| 2 | 60–119 | Galleon | Fire Ship / Heavy Demolition Ship | Turtle Ship |
| 3 | 120+ | Galleon | Fast Fire Ship / Heavy Demolition Ship | Admiral Yi Sun-shin |

The hero starts available from the opening. It receives **no automatic fleet
orders**; move it yourself, defend the entrance or send it to battle. Only one
hero flagship can be alive at a time. A sunk hero returns **30 seconds after its
death is detected**, at the separate berth and at the current naval tier.
A surviving hero retains its type; the new tier applies to its replacement.
If placement or the military cap blocks its return, the reward retries.
Nearby own ports heal the hero at the same 1 HP/s rate.
Everyone earns a Cannon Galleon entitlement every **75 seconds**, starting at
second 75. Each enemy building razed earns another. Siege rewards queue and
replace **one ordinary ship on a scheduled port wave**, at most one reward per
wave. They never increase the total ships in that wave or release one per second.
The first timed entitlement normally launches at second **78**. Failed placement
or the fleet cap preserves the entitlement. A missed wave is never caught up
with a burst; the next deadline starts from the current game time.

Holding the azure center with a live ship and **no enemy ships** pays each
participating player **15 prestige per 30 seconds** and a Cannon Galleon per
**90 seconds**. Leaving resets your own timer; enemy presence resets both sides.
Allies do not contest one another. Prestige advances tiers without adding fake
kills to combat statistics. Defeated fleets cannot contest rewards.

## Shared map and combat Objectives

Allied vision and exploration are embedded in the scenario. Cartography is
forced at startup, and sharing masks are set from actual occupied XS owners,
restricted to their own side. This does not depend on the lobby's sharing box.

The compact panel shows only participating colors:

    P# | Ports | K | D | R | Tier | Waves | Builders

K/D/R are actual engine kill/death/raze totals; eliminated rows retain final
values. Builders counts delivered rewards (not surviving civilians). Regular economy/exploration score inputs are neutralized, while the
combat score channels receive kill value ×100, death value ×100 and razing
value ×500. DE may still display its own team-average number beside the score.

Blue/Red/Green/Yellow fight Teal/Purple/Gray/Orange. Competitive victory begins
only once both sides have participated, and waits for defeated-player cleanup.
One-sided practice lobbies **do produce fleets**, but never award automatic
competitive victory. Closed harbors are removed by their preplaced references.

## Build and test

Build/install with `aoe2modes build cba_naval --deploy`, then select
**CBA Naval Admirals v0.5.1** as a Custom Scenario. Keep the fixed colors/teams.
Start a fresh match; old saves embed old logic. Earlier releases remain separate files; select v0.5.1 for this release.

DE update 185872 or later is required for exact-reference `xsTaskUnits` orders.
The validator-only declaration in `xs-check-prelude.xs` is never embedded.
Settings live in `mode.toml`; harbor geometry/native results live in `build.py`;
match state and fleet behavior live in the embedded `xs/main.xs`. There is no
binary base, copied RA trigger graph or loose XS file required for distribution.

Run `pytest tests/test_cba_naval.py` and strict audit on the built file. The
regressions execute the serialized XS with real seconds clock semantics and
independently numbered selectors/XS owners. They replay the actual native
cleanup/defeat effects, including Grey/P7 losing all ports with ships alive.
Other checks cover startup guards, first/repeat waves, bounded siege queues, repeated-callback guards, central
clearance and central destinations for every color, shared-vision masks,
immediate slow healing, cap/reward retry, combat totals, one-sided practice, build completion,
additional-port lives/production, refund caps and island/entrance connectivity
with building footprints/reefs blocked. Host execution requires `g++`.

The generic map report computes **land** regions; use the naval tests for water
connectivity evidence. Neither those grids nor XS mocks simulate DE pathfinding,
trigger scheduling, UI or combat. Live behavior
still needs a fresh DE acceptance match, including allied vision with sharing
disabled, repeat waves, AI engagement, repair/tower combat, port-only elimination,
construction availability/completion, Archer training/garrisoning, score rendering
and multiplayer balance. The completion check compares current build points to
the building’s required construction time; offline mocks cannot establish its
DE engine behavior. See the [developer unit APIs](https://www.forgottenempires.net/age-of-empires-ii-definitive-edition/xs-scripting-in-age-of-empires-ii-definitive-edition).
