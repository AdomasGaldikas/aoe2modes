# Ascendants: how the mode plays

Player- and host-facing rules for **CBA Hero: Ascendants**, the scenario built by
`modes/evolution_alpha`. This document describes the mode as it behaves in a lobby. It
carries no coordinates and no code — for those see
[`ascendants-control-map.md`](ascendants-control-map.md) (exact geometry),
[`ascendants-map.md`](ascendants-map.md) (arena layout) and
[`ascendants-architecture.md`](ascendants-architecture.md) (how it is built).

The current version number lives in `modes/evolution_alpha/mode.toml`; a test keeps the
mode README in step with it. This file deliberately does not repeat it.

## The short version

Eight fortified territories ring a central arena. Your four Castles produce a free army
forever. You kill things, and at kill milestones your base starts producing Heroes. Two
movable animals decide how far each newly produced group walks before it stops.
Everything you can build or research is free. You win when your side has destroyed every
Castle the other side owns.

## Lobby setup

| | |
| --- | --- |
| Map | 144×144, eight equal mirrored territories |
| Players | 8 fixed scenario colors |
| Sides | Blue, Red, Green, Yellow **vs** Teal, Purple, Gray, Orange |
| Starting age | Feudal |
| Population | 250 usable slots (the scenario cap is 251; one slot is reserved) |
| Civilizations | Free choice, ids 1–59 |

Close any slots you do not need, **but keep at least one occupied color on each side**.
Slots may be closed in any pattern — non-adjacent, one-versus-four, colors out of order.
The scenario resolves who actually owns each territory from the Castles standing in it,
so a shuffled or compacted lobby does not misassign armies, Heroes, rewards, HUD rows or
victory.

If you pick a civilization the build does not know about (an id past the table it was
compiled with) you get a chat warning at four seconds and **no army at all**. That is a
build that predates your DLC, not a bug in your lobby.

## Economy: everything is free

- Starting stockpiles are zero and stay zero.
- Every technology costs zero food, wood, stone and gold.
- Every buildable object costs zero.
- Unit and building repair costs zero.
- A timed Feudal upgrade package is applied at your Blacksmith.
- Bombard Towers are unlocked for every color.

Resources are therefore not a currency in this mode; build time and population are. The
score panel is repurposed — see *Combat HUD* below.

## Castle armies

Each color owns four Castles. While your slot is in the game, the scenario creates a
**four-unit wave** — one unit at each of your four Castle-front pads — on a fixed
interval, for free, forever.

Which unit, how often, and how many you may hold at once are all decided by your
**civilization**:

- the unit is that civilization's unique unit (Elite or non-Elite, depending on the
  civilization);
- the interval ranges from 6 to 15 seconds;
- the cap is a **military population** cap, from 31 to 92.

Because the cap counts military population rather than unit count, a civilization whose
unique unit costs half a population slot fields roughly twice as many of them. That is a
deliberate, unresolved balance property of the mode, not an accident.

Nobody can hand-train the unit their Castles already produce for free — every
automatically spawned unique unit is banned from training in both its Elite and
non-Elite forms.

## The two spawn controls

Every color owns two protected animals sitting on two separate water-isolated tracks
behind its base. Each track is a six-position slider, and where you park the animal
decides how far each **newly created** group walks.

### Sheep — Castle army range

| Position | Effect |
| --- | --- |
| On the snow (level 0) | **HOLD** — each new wave steps one tile back toward your Castles |
| Road, first step (level 1) | New waves stop just in front of your Castles |
| Road, levels 2–4 | Progressively farther into the arena |
| Road, far end (level 5) | Deepest position, toward the central battle |

**HOLD does not stop production.** Your Castles keep making waves; the waves just stay
home.

### War Penguin — Hero range

| Position | Effect |
| --- | --- |
| On the snow (level 0) | **OFF** — no new Heroes are produced at all |
| Road, first step (level 1) | Heroes stop right in front of your Castles, on the Army HOLD line |
| Road, levels 2–4 | Progressively farther into the arena |
| Road, far end (level 5) | Deepest position |

Both animals start at level 3.

### What the sliders do and do not do

- The snowy pad **is** the HOLD/OFF zone. The road begins exactly where the snow ends —
  the visual boundary is the real one.
- Each track is surrounded by water with a three-tile deep-water gap between the two, so
  neither animal can wander onto the other's slider.
- Both animals are undeletable and cannot be attacked. The Penguin also holds No Attack
  stance and deals no damage.
- A slider affects **only units created after you move it**. Nothing already fighting is
  recalled, retasked or stopped.
- Each newly created group receives exactly **one** automatic move order. After that the
  unit is yours: manual orders you give later are not overridden, including orders that
  walk back across a spawn pad.
- Known limitation: an *older* unit standing on a spawn pad at the exact moment a new
  group is born there can still be caught by that group's move order. The system protects
  orders between births, not unit identity during one.

## Heroes

Heroes are produced automatically from your **kill count**, provided the Penguin is not
on OFF.

| Kills | Hero | Active band |
| ---: | --- | --- |
| 200 | Robin Hood | 200–399 |
| 400 | Theodoric the Goth | 400–599 |
| 600 | Charles Martel | 600–799 |
| 800 | Subotai | 800–999 |
| 1,000 | Genghis Khan | 1,000–1,999 |
| 2,000 | Super Genghis | 2,000–3,499 |
| 3,500 | boosted Genghis loop | 3,500–4,999 |
| 5,000 | two boosted Genghis loops | 5,000+ |

The bands are **mutually exclusive**: only the tier matching your current kill count is
ever live. This matters when you use the OFF switch — parking the Penguin on snow pauses
production, and moving it forward again resumes only at the tier you have actually
earned. Lower tiers cannot burst-spawn to "catch up". Switching to OFF also discards any
Hero move order still pending.

## Builder pairs

Razing enemy buildings earns **builder pairs** — one male and one female Villager
delivered beside your Castles.

- The number of razings needed for your *first* pair depends on your civilization: 1, 2,
  3 or 4.
- After the first pair, **every further razing earns another pair**.
- Earned pairs are persistent: if you cannot receive them immediately they queue rather
  than being lost.
- At four seconds into the match you get a private chat line naming your civilization and
  its threshold.

## Center control rewards

Holding the middle of the map with at least one military unit pays out on two timers:

| Reward | Cadence | Detail |
| --- | --- | --- |
| **+10 kills** | every 3 minutes | Added to your kill counter, so it also advances Hero tiers |
| **Trebuchet** | every 30 minutes | A packed Trebuchet with +200 HP, delivered to your reward pad |

The Trebuchet reward waits for a clear pad rather than destroying whatever is parked
there, so a Trebuchet you left standing is never quietly replaced.

Trebuchets **cannot be trained** by anyone, and packed Trebuchets are removed from the
protected zone around every color's Castle row — including your own. The center reward is
the only route to one.

## King islands and the kill display

Each color has a King on a small island. Two things run off it:

- Bringing a unit to the island awards a burst of **Scorpions** to that color. They have
  a deliberate 50-second lifetime — they are a raid, not a standing army.
- The white King displays your **live kill total** as its attack statistic. Trigger
  variables are not expanded inside object names, so the number is published through the
  stat rather than the label.

## Combat HUD

The right-hand panel is a compact ordered list showing, for P1 through P8:

    P# | Kills | Deaths | Razings

It refreshes roughly every two seconds and reads live engine attributes. The ordinary
score attributes (map explored, building value, tribute, wonders, resource scores) are
neutralized to zero so nothing competes with the combat numbers.

One quirk is not a scenario defect: DE renders a **second number** beside a player — its
own team-average display. There is no supported way to hide it.

## Walls

Ascendants inherits CBA Hero's wall rules, with two switches worth knowing:

**The side-wall switch.** Deleting the small side/rear gate in your Castle yard removes
your side walls — both the short shoulders and the long flanks. It is a one-way choice
that opens your flanks for movement. The **front gate row and the rear University
enclosure stay** either way, and two small end posts prevent a route around the ends of
the front row. The University access gate is a different gate and is not the switch.

**The wall limit.** At **200** owned wall-class objects you get a warning. At **220** a
one-shot wipe clears your walls across the map. The count includes preplaced walls you
own, not only walls you built. The wipe spares protected permanent barriers: the front
row, the University boundary and teammate access gates. Permanent walls and gates also
refuse manual deletion; the side switch stays deletable on purpose.

## Team routes

Guarded rear causeways connect same-team pairs, and each player has a protected gate onto
them, so allies can reinforce one another. The corresponding corridors on the enemy side
are water. Rear gates open onto a dry three-tile path to your University and Blacksmith.

## Vote kick

Behind each base sits one Outpost marker per teammate, named `Delete Vote Kick <COLOR>`.
**Deleting the marker casts a vote against that teammate.**

- **Two different occupied teammates** must vote against the same target.
- The target and both voters must be live colors.
- A side therefore needs at least **three live colors** before any kick can resolve — a
  side reduced to two cannot kick at all.
- Closed slots never count as votes, so a sparse lobby cannot produce a kick at start-up.
- Markers cannot be destroyed by combat, only deleted by their owner. An enemy cannot
  cast your vote for you.

## Winning and losing

A color is **eliminated when it no longer holds a Castle in its own Castle row**. That is
a state, not an event: it does not matter whether the Castles were destroyed in combat,
removed by cleanup, or lost when a slot closed.

- Destroy every Castle belonging to the opposing side and your side wins.
- When a player resigns or is defeated, **all** of their remaining units and buildings are
  removed from the map.
- Victory resolves within a few seconds of the last enemy Castle leaving the map.
- A match needs at least one occupied color on each side to be meaningful; that is the one
  lobby rule the scenario cannot enforce for you.

## What the build cannot promise

The scenario is checked structurally before release, but AoE2ScenarioParser cannot
execute DE pathfinding, lobby compaction or multiplayer scheduling. Anything that depends
on those is verified by playing it. The open acceptance cases are listed in
[`ascendants-issue-register.md`](ascendants-issue-register.md), and what *is* proven
statically is described in [`ascendants-testing.md`](ascendants-testing.md).
