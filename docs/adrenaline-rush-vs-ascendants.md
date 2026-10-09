# Adrenaline Rush vs Evolution Alpha (Ascendants) — mechanics comparison

`modes/adrenaline_rush` was decompiled into this repo on 2026-10-09 as reference
material. This doc compares its mechanics against `modes/evolution_alpha`
("Ascendants", shipped as "CBA Hero 4v4: RA") — the repo's mature, code-defined
descendant of the same CBA Hero lineage. See `docs/cba-hero.md` for genre
background and `CLAUDE.md` for the architectural split between the two
("decompiled build" vs "code-defined build").

Everything below the lobby-setup table was confirmed by reading the actual
generated trigger code for Adrenaline Rush (`modes/adrenaline_rush/generated/triggers/`)
against the documented Ascendants mechanics (`docs/ascendants-gameplay.md`,
`docs/ascendants-control-map.md`). Where Adrenaline Rush's runtime behavior
couldn't be fully pinned down from static trigger inspection alone, that
uncertainty is called out explicitly rather than guessed at.

## Lobby setup

| | Adrenaline Rush | Evolution Alpha (Ascendants) |
| --- | --- | --- |
| Map | 144x144 | 144x144, eight equal mirrored territories |
| Players | 8 (Blue/Red/Green/Yellow vs Teal/Purple/Gray/Orange) | same |
| Starting age | Feudal | Feudal |
| Population cap | 1000 | 251 (250 usable slots + 1 reserved for the protected War Penguin controller) |
| Starting resources | 99,999 food/wood/gold/stone | zero — everything costs nothing instead |
| Civilizations | Free choice; your civ **is** your army (see below) | Free choice; every unique unit/building banned regardless of civ |
| Trigger / variable count | 11,619 triggers, 3 variables, 0 XS lines | 3,903 triggers, 145 XS variables, a full inline XS runtime |

## Civilization-driven army (Adrenaline Rush only)

Every civilization in the game — including Chieftains, Three Kingdoms and Greece
DLC civs — gets its own per-player trigger, e.g. `mong (p6)`, `tue (p6)`. The
condition is `research_technology(source_player=P6, technology=TechInfo.MONGOLS)`
— i.e. "this player's civilization grants the Mongols civ bonus", which is how a
native trigger detects which civilization a player picked. Firing it:

- activates 3-4 downstream triggers per civ (a spawner/feeder loop, an
  attack-move "mover" loop, and sometimes more), which auto-create that
  civilization's unique unit (Elite or base, civ-dependent) in waves whenever the
  player's military unit count drops below a threshold;
- for some civs, also grants a free bonus tech outright — e.g. the Teutons
  trigger force-researches Squires and announces `<PURPLE> Teutons - Squires
  Researched +10% Speed` in chat.
- a companion `move (p<n>)` looping trigger attack-moves that player's military
  units from the spawn pad toward the arena, similar in spirit to Ascendants'
  one-shot move order on newly created waves, but implemented as a repeating
  `task_object` loop rather than a per-spawn pulse.

Evolution Alpha deliberately removes this axis: it bans every civilization's
unique unit and building outright (in both Elite and base form) so nobody can
hand-train the unit their Castles already produce for free. Civ choice still
matters for the free Feudal upgrade package and the Castle-army unique unit
feed (6-15s interval, 31-92 population cap, scaled by population cost), but not
for an exclusive tech/army unlock the way it does in Adrenaline Rush.

## Kill-count progression

**Adrenaline Rush** ties age advancement directly to kills, with the exact
threshold varying by civilization (confirmed via distinct `accumulate_attribute`
quantities across per-player trigger copies):

| Milestone | Observed thresholds | Effect |
| --- | --- | --- |
| Castle Age | 200 / 250 / 300 kills (civ-dependent) | `force_research_technology(CASTLE_AGE)` + chat ("200 Kills - Castle Age") |
| Imperial Age | 450 / 500 / 600 kills (civ-dependent) | `force_research_technology(IMPERIAL_AGE)` + color-coded chat ("<RED>600 Kills - Imperial Age") |
| "SGK" (Super Genghis Khan), tier 1 | 2,501 kills | Loop every 2s: remove the previous Genghis Khan at a fixed pad, create a fresh one, +25 attack, HP set to 300 |
| "SGK250", tier 2 | 3,001 kills | Deactivates tier 1; loop every 5s creating **additional** Genghis Khans (no removal of earlier ones) with +250 attack, HP 300, +10 range — an accumulating horde rather than one persistent hero. HUD banner + sound: `<BLUE> p1 SUPER GK 250 UNLEASHED !!!` |

Both milestone tiers found in the data are a flat two-stage ladder (2501 /
3001), not the eight-band structure a first read of the trigger names
("2501:", "3001:") might suggest — those numbers are kill thresholds, not an
index into a longer series.

**Evolution Alpha** uses a wider, explicitly tiered ladder gated by mutually
exclusive kill *bands*, controlled by the War Penguin slider (0 = off):

| Kills | Hero | Active band |
| ---: | --- | --- |
| 200 | Robin Hood | 200-399 |
| 400 | Theodoric the Goth | 400-599 |
| 600 | Charles Martel | 600-799 |
| 800 | Subotai | 800-999 |
| 1,000 | Genghis Khan | 1,000-1,999 |
| 2,000 | Super Genghis | 2,000-3,499 |
| 3,500 | boosted Genghis loop | 3,500-4,999 |
| 5,000 | two boosted Genghis loops | 5,000+ |

Ascendants' bands are mutually exclusive and resumable (parking the Penguin on
OFF and moving it back resumes only the currently-earned tier, no catch-up
burst); nothing in Adrenaline Rush's two-stage SGK ladder has an off switch —
once you cross 2,501 kills the spawner loop simply runs for the rest of the
match.

## Building-destruction rewards

Adrenaline Rush pays out on razing via a one-shot countdown chain of triggers
named `5 razes (p1)` -> `4 razes (p1)` -> ... -> `1 raze (p1)`. Each stage
tributes to Gaia, spawns a Gaia decoration object and a Hawk near the map
corner, and decrements the hit points of a fixed marker object by 1 (apparently
a visual raze counter, in the same spirit as Ascendants publishing a stat
through a unit's attribute rather than its name). Every stage's condition is
simply "at least 1 raze accumulated" — the ladder structure comes from each
stage activating the next, not from rising thresholds, so the precise
in-game pacing (whether the whole chain unlocks on your very first raze, or
only after default-disabled stages are enabled one at a time) isn't fully
pinned down from static inspection and would need a live test to confirm.

Evolution Alpha's equivalent is **builder pairs**: razing enemy buildings
delivers a male+female Villager pair beside your Castles. The first pair's
threshold is civ-dependent (1-4 razings); every razing after that earns another
pair, and earned pairs queue rather than being lost if they can't be delivered
immediately. Evolution Alpha also layers in **center control rewards** (+10
kills every 3 minutes, a packed Trebuchet every 30 minutes for holding the
map's middle) that Adrenaline Rush has no equivalent of.

## Vote-kick

Both mods implement the *same* underlying mechanic, just with different
plumbing:

- **Adrenaline Rush**: each teammate has an Outpost object named
  `Delete Vote Kick <COLOR>`. Deleting a teammate's marker casts a vote. The
  scenario pre-generates every ordered triple as its own native trigger (e.g.
  `VoteKickP1-P2-P4`), each checking (via two inverted `objects_in_area`
  conditions) that *both* of the other two teammates' markers are gone before
  activating the kick effect for the target. With 8 players in two 4-stacks,
  that's a combinatorial trigger per possible (target, voter, voter) triple per
  side.
- **Evolution Alpha**: identical rule — two different occupied teammates must
  delete the same target's marker, a side needs at least three live colors to
  kick at all, closed slots can't vote — but resolved through the XS runtime's
  owner-identity layer instead of one native trigger per combination, so it
  degrades correctly in a shuffled or sparse lobby (see Identity section
  below).

## HUD and presentation

- Adrenaline Rush: `display_instructions` banners announce age-ups and hero
  spawns, kill/age milestones are broadcast via color-coded `send_chat`
  messages, and hundreds of looping `WORK p<n> <x> <y>` triggers re-task idle
  Villagers back to a fixed work building every 5 seconds.
- Evolution Alpha: a compact ordered combat panel (`P# | Kills | Deaths |
  Razings`) refreshed every ~2 seconds from live engine attributes, with the
  ordinary score categories (map explored, building value, tribute, wonders,
  resource score) zeroed out so nothing competes with it. A King unit per
  color publishes the player's live kill total through its attack stat (since
  trigger variables can't be interpolated into object names) — the same
  "borrow a stat slot to publish a number" trick Adrenaline Rush uses for its
  raze counter.

## Elimination and player identity

- Adrenaline Rush uses native `player_defeated` conditions per player, cleaned
  up by a `remove (p#)` trigger that strips the defeated player's Castle. These
  are exactly the class of native condition Ascendants found to silently fail
  for high player colors (P5-P8) in sparse lobbies.
- Evolution Alpha replaced the equivalent native conditions with XS-guarded
  Castle-owner detection after live 8-player testing surfaced that failure
  (tracked as ASC-053; see "Custom-scenario player identity is two separate
  domains" in `CLAUDE.md`). A color counts as eliminated when it no longer
  holds a Castle in its own Castle row — a state check, not a one-time event —
  and defeated-player cleanup removes their remaining units/buildings,
  including protected walls, gates and controllers, retrying until it
  succeeds.

Adrenaline Rush has not been patched for this failure mode and should be
treated as unverified in sparse or closed-slot lobbies until tested live.

## Other mechanics unique to one side

- **Wall limit / wipe**: Ascendants warns at 200 owned wall-class objects and
  wipes at 220, sparing protected front-row and University barriers. No
  equivalent found in Adrenaline Rush.
- **Team routes**: Ascendants has guarded rear causeways connecting same-team
  pairs with protected gates; the Adrenaline Rush decompile wasn't inspected
  deeply enough to confirm or rule this out.
- **Spawn-range control**: Ascendants' Sheep/War Penguin sliders let each
  player choose how far their Castle army and Heroes walk before stopping (six
  positions each, independently). Adrenaline Rush's spawners always walk to a
  fixed per-civ destination via the looping `move (p<n>)` trigger — there's no
  player-adjustable range.

## Architecture

| | Adrenaline Rush | Evolution Alpha |
| --- | --- | --- |
| Source | Decompiled from a binary `.aoe2scenario` | Code-defined from the start; no base/reference file |
| Trigger count | 11,619 flat native triggers | 3,903 triggers |
| Variables | 3 | 145, contiguous and collision-free by design |
| XS | None | A full inline runtime (player identity resolution, slider state, HUD math, elimination logic) generated from Python data tables |
| Authorship | Hand-authored over years by multiple contributors (credited "By: Milhao" in several trigger names) | Single-authored, test-covered |
| Verification | None shipped; this repo's `aoe2modes verify` only proves the rebuild matches the original binary, not that the mechanics are correct | 138 passing tests plus a structural `aoe2modes audit`; documented open issues tracked in `ascendants-issue-register.md` |

## Key takeaways

- Different reward philosophies: Adrenaline Rush rewards kills with civ-flavored
  unit spam and a two-stage escalating Genghis Khan horde; Ascendants rewards
  kills with a curated eight-tier hero ladder, decoupled from civ, with a pause
  switch.
- Civ identity is the single biggest mechanical split — your civilization
  determines your entire auto-fed army in Adrenaline Rush, while Ascendants
  bans every unique unit so civ choice matters far less.
- Vote-kick is mechanically identical between the two (Outpost-marker deletion,
  two-of-three-teammates rule) — the difference is purely architectural:
  Adrenaline Rush pre-generates one native trigger per voter combination,
  Ascendants resolves it through its XS identity layer so it survives a
  shuffled or sparse lobby.
- Architecturally they're opposites: Adrenaline Rush is legacy-style — more
  triggers doing less logic each, duplicated per player and per civ; Ascendants
  pushes logic into XS so trigger count drops even as mechanics get richer.
- Adrenaline Rush's native `player_defeated` and kill-threshold conditions carry
  the same sparse-lobby correctness risk Ascendants specifically patched
  (ASC-053) — worth testing live before trusting it with closed slots.
