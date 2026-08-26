# CBA Hero

8 players, two teams of four, facing each other across an open arena.

## Rules

* Every player starts with **one castle** and **one hero**. Lose the castle and you
  are eliminated — your army dies with it.
* There is no economy. Resources are capped out and there is nothing to build.
* **Reinforcements arrive every 20 seconds** at your spawn pad and attack-move into
  the middle. Wave size grows with the wave counter and plateaus at 16.
* Your hero **upgrades to the next tier at waves 6 and 14**, and gains hit points
  every third wave.

## Hero lines

Each player is assigned one archetype from `heroes.CLASSIC_LINES`, deterministically
by player number. Every line has three tiers:

| Line | Tier 1 → 2 → 3 |
| --- | --- |
| Paladin | Sieur Bertrand → Roland → Frankish Paladin |
| Huskarl | Jarl → Siegfried → William Wallace |
| Archer | Archer of the Eyes → La Hire → Robin Hood |
| Cavalry Archer | Kushluk → Subotai → Genghis Khan |
| Monk | Friar Tuck → Imam → Pope Leo I |
| Siege | Bad Neighbor → God's Own Sling → Warwolf Trebuchet |
| War Elephant | Prithviraj → Gajah Mada → Abraha Elephant |
| Duelist | Minamoto → Nobunaga → Kitabatake |

The balance is a **starting point to tune**, not a copy of any published CBA Hero
scenario.

## Tuning

Pacing lives at the top of `build.py`:

| Constant | Default | Effect |
| --- | --- | --- |
| `WAVE_INTERVAL` | 20 | Seconds between waves. Also drives the XS clock. |
| `WAVE_SIZE_BASE` / `_STEP` / `_CAP` | 4 / 1 / 16 | Wave size ramp and ceiling. |
| `TIER_UNLOCK_WAVES` | 0, 6, 14 | When each hero tier unlocks. |
| `WAVE_COMPOSITION` | militia, spearman, archer, skirmisher | Support units per wave. |

Map size, player count, teams, ages and resources are in `mode.toml`.

## Build

```
aoe2modes build cba_hero --deploy
```
