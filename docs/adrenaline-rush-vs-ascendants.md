# Adrenaline Rush vs Evolution Alpha (Ascendants) — mechanics comparison

`modes/adrenaline_rush` was decompiled into this repo on 2026-10-09 as reference
material. This doc compares its mechanics against `modes/evolution_alpha`
("Ascendants", shipped as "CBA Hero 4v4: RA") — the repo's mature, code-defined
descendant of the same CBA Hero lineage. See `docs/cba-hero.md` for genre
background and `CLAUDE.md` for the architectural split between the two
("decompiled build" vs "code-defined build").

Both are 8-player, 144x144, 4v4 CBA Hero arenas (Blue/Red/Green/Yellow vs
Teal/Purple/Gray/Orange), won by eliminating the enemy team.

## Where they diverge

**Progression trigger**
- Adrenaline Rush: raw kill count ages a player up (~200–750 kills) and eventually
  spawns one escalating "Super Genghis Khan" hero every 2s at 2500+ kills.
- Evolution Alpha: six discrete hero tiers gated by kill *bands*
  (200/400/600/800/1000/2000/3500/5000+), controlled by a "War Penguin" slider.

**Army spawns**
- Adrenaline Rush: dozens of independent per-civ, per-player looping spawners at
  fixed map coordinates.
- Evolution Alpha: a unified Castle-army spawner (one unit per surviving Castle),
  controlled by a "Sheep" slider (levels 0–5).

**Civilization role**
- Adrenaline Rush: civ choice matters directly — your civ's unique unit auto-feeds
  in waves as you fight.
- Evolution Alpha: every unique unit/building is banned outright — civ identity is
  neutralized by design.

**Building destruction reward**
- Adrenaline Rush: a "raze count" mechanic (1–5 razes) buffs a unit's attack —
  unique to this mod.
- Evolution Alpha: no equivalent found.

**Anti-grief**
- Adrenaline Rush: chat-command vote-kick (`Delete Vote Kick <COLOR>`).
- Evolution Alpha: vote-kick integrated with the XS runtime, plus a 220-object
  wall-limit wipe and automated elimination cleanup (neither found in Adrenaline
  Rush).

**HUD**
- Adrenaline Rush: `display_instructions` milestone banners plus color-coded chat
  spam, and hundreds of auto-retask-idle-villager triggers.
- Evolution Alpha: a structured Objectives row plus a live K/D/R panel.

**Resources / population**
- Adrenaline Rush: 99,999 of all resources, population cap 1000, Feudal start.
- Evolution Alpha: code-driven resources, population cap 251 (250 gameplay slots
  + 1 protected "Penguin"), Feudal start.

**Architecture**
- Adrenaline Rush: 11,619 flat native triggers, 3 variables, zero XS — hand-authored
  over years by multiple contributors (credited "By: Milhao" in several trigger
  names), with no identity-correctness handling.
- Evolution Alpha: 3,903 triggers backed by a 145-variable XS runtime handling
  player identity, slider state, HUD math and elimination logic; 138 passing tests
  plus a structural audit.

**Robustness**
- Adrenaline Rush: native `player_defeated`/`research_technology` conditions — the
  same failure class Evolution Alpha specifically patched (ASC-053: native
  conditions failed for high player-colors in sparse lobbies) — left unaddressed
  here.
- Evolution Alpha: fixed via XS-guarded Castle-owner detection (see CLAUDE.md,
  "Custom-scenario player identity is two separate domains").

## Key takeaways

- Different reward philosophies: Adrenaline Rush rewards kills with civ-flavored
  unit spam and one big super-hero; Ascendants rewards kills with a curated hero
  ladder, decoupled from civ.
- Civ identity is the single biggest mechanical split — central to one mod,
  deliberately erased in the other.
- Architecturally they're opposites: Adrenaline Rush is legacy-style — more
  triggers doing less logic each; Ascendants pushes logic into XS so trigger count
  drops even as mechanics get richer.
- Adrenaline Rush likely carries the same sparse-lobby correctness risk that
  Ascendants had to fix — worth keeping in mind if this mod is ever played with
  closed/empty slots.
