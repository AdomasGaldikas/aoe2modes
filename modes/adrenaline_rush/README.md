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
- **Kill-count age-ups.** `accumulate_attribute(UNITS_KILLED)` thresholds (roughly
  200–750 kills, varies per player) force the player into Castle Age and then
  Imperial Age via `force_research_technology`, each with a chat announcement.
- **Super Genghis Khan.** Past ~2500 kills, a single escalating hero ("Super Genghis
  Khan", +25 attack, 300 HP, faster fire rate) respawns every 2 seconds at a fixed
  per-player location — one big late-game payoff rather than a tiered hero ladder.
- **Raze-count reward.** Destroying 1–5 enemy buildings renames/buffs a unit's attack
  per raze — a building-destruction incentive with no equivalent in `evolution_alpha`.
- **Vote-kick.** Chat-command based: typing `Delete Vote Kick <COLOR>` triggers a kick
  vote for that player.
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
