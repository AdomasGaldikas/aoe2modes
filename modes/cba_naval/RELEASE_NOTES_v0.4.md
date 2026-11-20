# CBA Naval: Admirals v0.4

Select **CBA Naval Admirals v0.4** and start a fresh match. Existing saves contain
old scripts, and earlier versions remain separate scenario files.

- Ordinary and siege reinforcements launch at the **actual producing dock**, at
  nearby water positions within four tiles. The fixed lagoon pads are removed.
  Original and completed additional ports use the same collision-checked logic.
  A blocked dock skips that cycle; queued siege rewards retry.
- Each port now produces **one ship every 10 game seconds**, alternating
  ranged/fire/ranged/demo. Four ports produce 24 ships per minute, down from 60.
  The first wave is at second 13. RA's civilization-dependent castle waves
  generally produce one unit per castle every 8–13 seconds.
- Each player starts with **one Longboat hero flagship at a separate berth**.
  It stays under manual control. After sinking it returns after **30 seconds**,
  at its own berth, using the current tier: Longboat, Turtle Ship or Admiral Yi.
  A living hero retains its type. Placement/population failures leave the return
  pending, and creation refuses a second living hero.
- Starting and newly constructed ports have **3,000 HP**, up from 2,200.
  Slow repair remains **1 HP/s within 14 tiles**, without stacking.
- A starting **Harbor Quarters (Barracks)** satisfies the native Archery Range
  prerequisite. Naval previously disabled Barracks without providing one,
  leaving the Range inaccessible for ordinary civilizations. Infantry and new
  Barracks remain disabled.
- Builder rewards remain at **30/60/90/120 real kills**, each giving a Villager,
  **400 wood and 150 stone**. Once a worker arrives, the Range needs **200 wood**
  and no extra kill unlock; each Archer costs **50 wood**. Limits remain two
  additional ports, four additional Watch Towers, one Range and twelve Archers
  alive. No transports; land units remain on their island.

The prerequisite is the ordinary game rule documented in the
[official Feudal Age guide](https://www.ageofempires.com/learn-to-play/advancing-to-the-next-age-xbox/).

Validation covers serialized XS execution with mocked APIs, all eight reflected
launch directions, moved and completed built docks, blocked shoreline behavior,
first/repeat production timing, one-hero replacement and retry, prerequisite
placement, port HP, healing, rewards, construction limits, allied vision and
owner-resolved native defeat/victory. These checks do not simulate the DE build
menu, scheduling, collision/pathfinding or combat balance; live acceptance still
needs a fresh game.
