# CBA Royale: Last Caravan v0.1.1

A separate code-defined 4v4 prototype. P1–P4 fight P5–P8 while escorting one
Command Wagon each. Civilization armies follow the wagon; fire progressively
forces both caravans toward one of nine randomly chosen final arenas.

Build with `aoe2modes build cba_royale`. The output is
`dist/CBA Royale Last Caravan v0.1.1.aoe2scenario`. All gameplay XS is embedded;
there are no loose scripts to distribute. Existing modes, including Naval, are
independent. `civilizations.py` owns its snapshot of the Ascendants table.

## Hosting

Requires **DE update 185872 or newer** for the exact-reference order, property and
name APIs listed in the [official release notes](https://www.ageofempires.com/news/age-of-empires-ii-definitive-edition-update-185872/).
The older unit/clock functions follow the [official XS reference](https://www.forgottenempires.net/age-of-empires-ii-definitive-edition/xs-scripting-in-age-of-empires-ii-definitive-edition).

Use a private custom-scenario lobby, **Faster speed (2×), Lock Speed enabled**,
fixed teams P1–P4/P5–P8, and free civilization selection. The pinned scenario
format has no exposed speed-lock field: the host must set both options. Full
Tech Tree is off to preserve passive civilization bonuses. All counter-camp
types are enabled explicitly, including for civilizations without native Stables.
That last behavior requires live verification.

The deadline is **70:00 game time**, nominally 35 active real minutes. Pauses stop
the shared game clock. Slower hosting speed or performance stalls change the
actual elapsed duration. A three-game-second initialization delay resolves
ownership; it does not move the final deadline.

## Rules

- Protect your wagon, move into the announced safe zone, and destroy enemy wagons.
- Initial assets: a 1,500-HP wagon, a starting Castle, a King Arthur hero and eight
  civilization soldiers. Runtime births use the civilization actually selected.
  Castles disappear at 3 nominal real minutes; wagons resist enemy targeting for
  the first 90 seconds. Each destroyed enemy opening Castle awards team supplies.
- Four soldiers arrive per wave. The mode-owned civilization table determines
  intervals and main-army caps. Actual population costs and a 120-combat-object
  cap gate each birth. Counters have a separate 24-population allowance. Failed
  births retry without accumulating missed waves. Only newly born soldiers receive
  one movement order. The plan supplies no siege-award mechanism; this prototype
  therefore introduces no automatic siege reward.
- Renown comes from combat kill-counter deltas and capped objective rewards.
  Main-army ranks unlock at 40/120/260 Renown, with time floors at 12/20/28 minutes.
  Each adds 5% baseline HP and +1 primary attack; heroes gain 100 HP and +2 attack.
  Promotions preserve current HP percentage. K/D remains separate from Renown.
- Dead heroes return after 45 seconds beside their wagon. Players whose wagons
  are permanently lost retain their armies; a dead support hero returns after
  60 seconds beside the nearest surviving allied wagon.
- A first wagon loss before minute 29 leaves a 60-second wreck. A different
  teammate's hero must remain within five tiles for 15 uninterrupted seconds.
  Enemy combat units within six tiles, or an unsafe wreck, reset the channel.
  Rescue restores 50% wagon HP once; it grants no free army. A team's last living
  wagon falling ends the match immediately, regardless of pending rescues.
- Six outposts require five uncontested combat population for ten seconds. Holding
  one pays the team 60 wood/20 stone every 30 seconds while occupied and safe.
  War chests appear at minutes 4/8/12/16/20/24/28, take 12 seconds to capture and
  expire after 90 seconds. They award 200 wood/100 stone. Team payments split by
  connected participant count; integer remainders go in color order.
- Builders unlock at 40/100/200/350 combat kills. At most two live at once;
  undelivered entitlements persist. Each delivered builder awards 250 wood/100
  stone. Supplies cap at 1,000 wood/500 stone.
- Allowed construction: two Watch Towers (100 wood/75 stone), 12 Palisades
  (10 wood), one Palisade Gate (30 wood, all orientations), and one counter camp
  (200 wood). Barracks/Range/Stable camps produce two Pikemen/Elite Skirmishers/
  Light Cavalry every 20 seconds, subject to population limits and a living wagon.
  New foundations must be safe, within ten tiles of their wagon, and clear of all
  nine final arenas. Their footprints count toward the exclusion. Invalid
  construction is removed and its configured cost refunded. Existing legal
  structures remain when the wagon moves. Ordinary training/research and other
  construction are disabled; the terrain contains no gathering economy.

## Storm

The map is 240×240 with mirrored starts, 12-tile approaches, four ponds and nine
flat final arenas. The final landmark and first circle center are uniformly
selected with synchronized runtime randomness. Later centers use reservoir
sampling over eligible four-tile-grid positions. A whole path is retried if the
lattice leaves no next center; its final landmark and first center are preserved.
After 32 unsuccessful attempts, a deterministic greedy path bounds initialization
work. Selection never reads player positions or strength.

| Nominal real minute | Radius | Outside max-HP damage per nominal real second |
|---|---:|---:|
| Start | 112 | 0% |
| 6 | 96 | 1% |
| 11 | 80 | 2% |
| 16 | 64 | 3% |
| 21 | 48 | 4% |
| 25 | 36 | 6% |
| 29 | 24 | 8% |
| 32 | 14 | 10% |
| 34 | 6 | 15% |
| 35 | Closed | Resolve before final damage |

Destinations are announced two minutes ahead where possible; each closure lasts
one minute. Center and radius interpolate continuously. Fire and warning rings
use at most 256 zero-sight, nonblocking, protected markers. Stationary rings retain
their references; moving rings update every four nominal seconds.

Hazards use maximum HP, ignore armor and follow garrison-carrier references.
Kill/death counters are sampled before and after scripted damage/removal so those
deaths do not grant Renown, builders or supplies. Exact engine counter timing and
garrison enumeration remain live acceptance gates.

## Ownership and outcome

Scenario color, native trigger selector and XS owner are separate domains.
Occupancy is resolved from the actual ownership of the three starting references.
HUD activation and native victory effects check the resolved owner. Closed colors
have their starting objects removed and no HUD row. All 78 trigger variables belong
to one mode-local ledger; runtime arrays are allocated before guards execute.

Players are active, recoverable, stranded or resigned. The fixed update order is:
combat credit; clock/storm; losses and rescues; construction/progression/production;
objectives; hazard damage and counter absorption; simultaneous outcome snapshot;
boundary markers and HUD. The deadline latches its result before further production,
rescues or final damage. Ties compare surviving wagons, combined remaining HP
percentage, combat population and combat kills. An exact draw sends native victory
to both teams; DE's presentation of that case is unverified.

`xs-check-prelude.xs` supplies validator-only declarations for newer engine APIs;
it is neither embedded nor shipped as a runtime replacement. `DiscardedFn` is the
only ignored XS warning, for intentionally unused mutator return values. Arithmetic
and numeric-promotion warnings remain enabled.

## Validation and release

Run `pytest tests/test_cba_royale.py tests/test_build.py`, `ruff check .`,
`aoe2modes build cba_royale`, and strict audit of the resulting file.
The C++ harness executes the XS read back from that file, with bounded engine mocks:
2,000 seeded paths, route-clearance samples, all fallback combinations, shuffled
full/sparse ownership, births/population, rescues, hazards, progression, builders,
construction/refunds, objectives, simultaneous outcomes and deadline latching.
Restoring mock arrays and RNG verifies deterministic script continuation, **not
native DE save/load**. The load simulation likewise does not prove engine performance.

This is an automated-validated prototype. Fresh full and sparse DE matches, save/
load, spectator behavior, marker visibility, measured timing, native construction,
and at least 20 human balance matches remain release gates. See
[the acceptance checklist](../../docs/cba-royale-playtesting.md).

## v0.1.1 startup correction

DE rejected v0.1.0 at the compound population-cap condition in `royaleBirth`
(Error 0308, generated `default0.xs` line 296). The offline checker and C++
harness accepted that expression. v0.1.1 calculates candidate populations
before comparisons and separates arithmetic from compound logical conditions
throughout the runtime. An emitted-script regression guard covers this parser
mismatch. Population limits and gameplay rules are unchanged. A fresh native
DE load of v0.1.1 remains required; an existing match retains its original XS.
