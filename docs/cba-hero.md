# CBA Hero: what the mode actually is

**CBA** is *Castle Blood Automatic*, a long-running fan-made AoE2 scenario. Economy
plays no role: players start with enormous resources, cannot build castles, and fight
with units that arrive automatically. Losing your last castle eliminates you instantly
— your remaining units die and your buildings fall with it. The standard setup is
eight players in two teams of four.

**CBA Hero** is the variant where each player controls a *hero* unit rather than an
army composition, and that hero grows over the match. It is credited to "T3nchy".

## The mechanics a CBA Hero build has to provide

| Mechanic | Where it lives here |
| --- | --- |
| Symmetric arena, one base per player | `lib/spawns.lane_bases` + `lib/terrain` |
| Castle-as-lives loss condition | `lib/triggers.defeat_when_object_destroyed` |
| Huge starting resources, no economy | `[players.resources]` in `mode.toml` |
| Automatic reinforcement waves | `lib/triggers.spawn_units` + `attack_move_all` |
| One hero per player, upgraded over time | `lib/heroes.HeroLine` + `upgrade_hero` |
| Hero stat scaling | `lib/heroes.buff` / `buff_attack` / `buff_armour` |
| Match clock and wave pacing | `modes/cba_hero/xs/main.xs` |

## How the hero part is modelled

A **hero line** is an archetype plus an ordered ladder of hero units:

```python
HeroLine(
    key="paladin",
    label="Paladin",
    tiers=(HeroInfo.SIEUR_BERTRAND, HeroInfo.ROLAND, HeroInfo.FRANKISH_PALADIN),
)
```

Upgrading is a `Replace Object` effect from one tier to the next, so a player's hero
changes identity in place without losing its position. Stat growth is a
`Modify Attribute` effect, which applies to the unit *type* for that player — meaning
it also covers heroes created later.

`heroes.CLASSIC_LINES` ships eight archetypes (paladin, huskarl, archer, cavalry
archer, monk, siege, elephant, duelist) — one per player in a standard lobby. **The
balance is a starting point, not a reproduction of any published CBA Hero scenario.**
Retune the tiers and thresholds for your own mode; that is what the structure is for.

## Two knobs that decide how a CBA Hero feels

**Wave interval and size.** Waves are the pacing. Too fast and heroes drown in chaff;
too slow and the arena is empty. `cba_hero` uses 20s with a linear ramp to a cap;
`cba_hero_duel` uses 12s and cuts waves off entirely at the sudden-death wave.

**Where the upgrade thresholds sit.** `TIER_UNLOCK_WAVES` in `modes/cba_hero/build.py`
gates each tier on the wave counter that XS publishes. Move them and the whole arc of
a match moves.

## Things worth knowing before you build one

* **Assign heroes deterministically at build time, or randomly at runtime — not both.**
  `HeroPool.for_player` is deterministic so that builds are reproducible. If you want
  players to pick or roll a hero, drive that from XS and keep the build deterministic.
* **XS runs on every machine independently.** Anything that branches on
  `xsGetLocalPlayerId()` before touching shared state will desync. Keep per-player
  presentation and shared simulation apart.
* **Unit counts are the performance ceiling.** Eight players spawning uncapped waves
  will bring a lobby to its knees. Both modes here cap wave size on purpose.
* **Test with 8 players, not 1.** Trigger behaviour that looks right in single-player
  can behave differently in a full lobby, particularly anything touching diplomacy or
  player-scoped effects.

## Sources

* [Castle Blood Automatic — Age of Empires Wiki](https://ageofempires.fandom.com/wiki/Castle_Blood_Automatic)
* [CBA Hero community site](https://cbahero.weebly.com/)
* [AoE2DE UGC Guide — Triggers](https://ugc.aoe2.rocks/scenarios/triggers/)
