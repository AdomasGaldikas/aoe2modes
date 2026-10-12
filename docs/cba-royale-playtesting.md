# Last Caravan acceptance and balance

Status: v0.1.0 prototype. Automated checks are separate from live acceptance.
On 2026-10-11 a desktop inspection found an existing Naval match; it was left
untouched. No Royale live match was started or deployed over an existing copy.

## Fresh private DE matches

- [ ] Record build SHA-256 and DE version; deploy a uniquely named copy while the game is closed.
- [ ] Full 4v4: fixed colors/teams, Faster 2×, Lock Speed, free civilizations/Random.
- [ ] Sparse P1/P3/P5/P8: closed high colors, participant-only HUD, correct shared vision and winners.
- [ ] Initialization: three starting anchors, eight actual civilization soldiers, hero and usable wagon.
- [ ] Native civilization bonuses, unmapped fallback, fractional/multi-pop units and transformations.
- [ ] Moving births, blocked pads, no queued-wave burst, birth-only orders and 120 population/object limits.
- [ ] Protected opening wagons, no wagon conversion/deletion/economic commands, regeneration delay.
- [ ] No ordinary training/research, no gathering economy, universal camp choices including meso Stable.
- [ ] Four gate orientations, foundation limits, placement/refunds, ownership changes and relocated wagons.
- [ ] Camp completion and counter intervals; stop production during wagon loss and after outcome.
- [ ] Hero respawn timing, nearest allied support wagon and stranded army control.
- [ ] Continuous rescue: enemy interruption, unsafe wreck, failed placement, repeat loss, expiry and 29:00 cutoff.
- [ ] Boundary markers visible through fog, zero obstruction and no enemy vision disclosure.
- [ ] Circle interpolation, main/flank routes, ponds and flat unbuildable final arenas.
- [ ] Storm affects troops, garrisons, buildings and foundations; delayed engine kill counters grant no rewards.
- [ ] Outpost/chest channels, contention, expiry, supply splitting/caps and duplicate XP prevention.
- [ ] Simultaneous last-wagon destruction, resignation, every deadline tiebreak and both-team draw presentation.
- [ ] Deadline exactly 70:00 game time; measure active real duration, pauses and slowdown effects.
- [ ] Save/reload mid-closure and mid-rescue: timers, arrays, ownership and random sequence persist.
- [ ] Spectator objectives/signals, native sound cues and end-of-match team summaries.
- [ ] Maximum-army final phase: no recurring freezes or loss of existing orders.

Use fresh matches; saved scenarios contain their original script. Built-in AI is
useful for engine smoke tests but cannot establish human tactical balance. Keep
private-lobby logs, screenshots and saves outside repository commits.

## Twenty human balance matches

Use ten matched pairs with starting sides swapped and a spread of recorded seeds
and civilization compositions. Do not infer fairness from one winning side or one
match. Record these columns per match, with per-player details where appropriate:

```text
match_id,scenario_sha,de_version,seed,speed,teams,civilizations,
first_contact_real_seconds,first_permanent_wagon_loss,rescues,
rank_1_time,rank_2_time,rank_3_time,storm_deaths,
outpost_control_seconds,chests_captured,winning_team,
active_real_duration,game_clock_duration,pauses,performance_notes
```

Acceptance targets: first contact within two active minutes; useful objectives
through the middle game; surviving teams reach concentrated fighting around minutes
29–35. Investigate persistent side/civilization advantages, early snowballs, rescue
stalling, uncontested supply loops, unusable routes and excessive storm-only endings.
Change the mode-owned tunables, rerun automated checks, then repeat affected live
checks. Record failures and untested cases explicitly before promoting the prototype.
