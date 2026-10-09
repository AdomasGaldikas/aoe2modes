# CBA Hero King Zalabatta Adrenaline Rush

Decompiled from `base.aoe2scenario` (v1.58, 8 players, 4v4, 11619 triggers, 1209 units,
3 variables) — a legacy, hand-authored CBA Hero variant. Unlike `evolution_alpha`
(Ascendants), this mod has no XS runtime: every mechanic below is implemented as
flat native triggers, carried over unchanged from the decompile.

Rebuild and verify it still matches the source:

```
aoe2modes build adrenaline_rush
aoe2modes verify adrenaline_rush
```

Structural changes go into `generated/` (overwritten by `aoe2modes decompile`);
small local tweaks go into `build.py` after `generated.apply(ctx)`.

## Mechanics

- **Civilization-driven army.** Every civilization in the game (including Chieftains,
  Three Kingdoms and Greece DLC civs) has its own per-player trigger block, named e.g.
  `azt (p1)`, `camelarch (p3)`. Picking a civ activates that civ's "feeder" trigger,
  which auto-spawns waves of that civ's (usually Elite) unique unit whenever the
  player's military unit count drops below a threshold. Civ choice is a real build
  decision here — it directly determines your unique-unit supply.
- **Kill-count age-ups.** `accumulate_attribute(UNITS_KILLED)` thresholds force
  `force_research_technology`: 200/250/300 kills (civ-dependent) for Castle Age,
  450/500/600 kills (civ-dependent) for Imperial Age, each with a chat announcement.
- **"SGK" Genghis Khan ladder.** At 2,501 kills a loop removes/recreates one Genghis
  Khan every 2s at a fixed pad (+25 attack, HP set to 300). At 3,001 kills that loop
  is deactivated and replaced by one that creates an *additional* Genghis Khan every
  5s without removing earlier ones (+250 attack, HP 300, +10 range) — an accumulating
  horde rather than a single escalating hero, announced with a HUD banner and sound.
- **Raze-count reward.** A one-shot countdown chain (`5 razes` → `4 razes` → ... →
  `1 raze`) tributes Gaia, spawns a decoration object and a Hawk, and decrements an
  HP counter on a marker unit per raze — a building-destruction incentive with no
  direct equivalent in `evolution_alpha` (which instead grants builder-pair Villagers
  for razing).
- **Vote-kick.** Each teammate has an Outpost object named
  `Delete Vote Kick <COLOR>`; deleting a teammate's marker casts a vote. A
  combinatorial native trigger per (target, voter, voter) triple (e.g.
  `VoteKickP1-P2-P4`) fires the kick once two different teammates' markers are
  both gone — the same two-of-three-teammates rule `evolution_alpha` uses,
  just resolved with one native trigger per combination instead of through an
  XS identity layer.
- **HUD.** `display_instructions` banners announce milestones and hero spawns; kill
  counts are broadcast via color-coded `send_chat` messages. Hundreds of
  auto-retask-idle-villager triggers rebuild lost population automatically.
- **Elimination.** Native `player_defeated` conditions per player, cleaned up with a
  `remove (p#)` trigger that strips the defeated player's Castle.

## Known risk

The elimination and civ/age-up conditions above are all **native** trigger
conditions. `evolution_alpha` originally used the same native conditions and found
(via live 8-player testing, not automated tests) that they silently fail for high
player colors in sparse lobbies — see "Custom-scenario player identity is two
separate domains" in `CLAUDE.md` and `docs/ascendants-closed-slot-investigation.md`.
This mod has not been patched for that failure mode. Treat correctness in sparse/
closed-slot lobbies as unverified until tested live.

## Comparison to evolution_alpha

See [`docs/adrenaline-rush-vs-ascendants.md`](../../docs/adrenaline-rush-vs-ascendants.md)
for a full mechanics comparison against the Ascendants line.
