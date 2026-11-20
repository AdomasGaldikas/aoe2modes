# CBA Naval: Admirals v0.5.1

Start a fresh match using **CBA Naval Admirals v0.5.1**.

New ordinary and siege ships first move about **three tiles away from their
producing shore**, into the lagoon, so their launch cells can clear. This uses a
pure move order, followed by a queued attack-move to the central sea. The
clearance destination comes from the actual dock and ship positions, including
ports built on the north or south lagoon bank. Destinations stay inside lagoon
water and use the same eight-sector transformations as dock launches.

Each living fleet ship retains its own selector array. Commands are issued only
at birth; there are no later movement pulses. Heroes and builders still receive
no automatic orders. Production remains **one ship per completed port every
15 game seconds**, with the first wave at second 18. Siege rewards still replace
one ordinary ship on a scheduled wave.

Automated checks execute the serialized XS and verify move-before-attack ordering,
queued attack flags, water destinations, three-tile clearance at all 32 original
docks, north/south built-port clearance in every color, stable command selectors,
manual heroes/builders, and existing wave/reward/defeat rules. These checks do
not simulate DE movement or combat; live dock clearance and pathfinding still
need a fresh in-game match.
