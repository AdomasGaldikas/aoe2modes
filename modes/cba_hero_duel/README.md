# CBA Hero Duel

The 1v1 cut of [CBA Hero](../cba_hero/README.md), on a smaller map with a tighter
clock. Built from the same library — only pacing and the win condition differ.

## Rules

* One hero each, **top tier from the start**. No upgrade ladder to climb.
* One castle each. Raze your opponent's and you win.
* **Waves every 12 seconds**, smaller than the 4v4's.
* At **wave 20 reinforcements stop entirely** — sudden death, heroes settle it.
* Your hero gains hit points and attack every second wave, so the fight escalates
  even after the chaff dries up.

## Hero pool

Narrowed to two archetypes so the matchup stays legible: **Paladin** and **Huskarl**,
both at their top tier.

## Tuning

| Constant | Default |
| --- | --- |
| `WAVE_INTERVAL` | 12 |
| `WAVE_SIZE_BASE` / `_CAP` | 3 / 10 |
| `SUDDEN_DEATH_WAVE` | 20 |

## Build

```
aoe2modes build cba_hero_duel --deploy
```
