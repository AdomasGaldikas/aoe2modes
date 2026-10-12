# CBA Hero 4v4: RA Speed v0.1.1

Double-click/type selection is set to match the exact object type in both modes;
shared names and selection groups cannot broaden it. Military/civilian roles remain
intact: drag-box selection uses the engine's army priority with civilians selected
separately. Fresh DE verification remains pending.

The shared v0.1.1 source also removes the in-game population chooser island,
King, signs and script-selected limit. Population is chosen in the lobby for
all players. Native lobby-cap enforcement and spawning at different limits still
need a fresh DE test; the source does not overwrite free housing.

An independent Speed candidate built from the maintained normal RA
map and rules. It does not import Zalabatta's scenario or trigger graph. Normal RA
remains `evolution_alpha`; this mode is `ra_speed` with a separate filename/version.

After 15 minutes, losing a teammate who actually started the match gives the
survivors on that team 2x movement and 3x attack rate for five minutes. Another
teammate loss refreshes the deadline, without stacking the bonuses. Early departures
are consumed during warm-up; they do not produce a delayed boost. Closed slots never
count as losses. Both teams have independent deadlines and compact HUD countdowns.

Castle armies, all shared RA Hero tiers, Scorpions and builder types are included.
The controller Sheep, Penguin and Kings, buildings, spawn timers, population rules,
Hero thresholds, birth orders, protected routes, backup, cleanup and victory are
preserved. Reload time and attack delay are shortened together. Attribute changes
happen only on transitions, with reciprocal restoration on expiry. Player mutations
use RA's XS identity tokens, rather than native color selectors.

`build.py` calls the shared RA builder. Hero config comes from normal RA, so its
future roster fixes automatically reach both modes. Map/player config drift makes
the Speed build fail. The only extra trigger variables are the two countdowns;
the ordinary gameplay triggers and units are identical apart from mode-name text.

Tune the warm-up, duration and multipliers in `[speed_rush]` in `mode.toml`.

```bash
.venv/bin/python -m aoe2modes build evolution_alpha ra_speed
.venv/bin/python -m aoe2modes audit "dist/CBA Hero 4v4 RA Speed v0.1.1.aoe2scenario" --strict
.venv/bin/python -m pytest tests/test_ra_speed.py tests/test_evolution_alpha.py
```

The tests compile and execute the emitted XS state machine with independent
engine API stubs, including shuffled owners, closed slots, early and simultaneous
losses, independent teams, refreshes, expiry and repeated apply/remove cycles.
Serialized comparisons verify that normal RA geometry and gameplay are preserved.

Historical v0.1.0 validation on 2026-10-11: all 168 repository tests passed, including 10 Speed
checks; repository Ruff, embedded XS validation and strict serialized audits of
both candidates passed. Speed contains 4,445 triggers, 999 objects and 155 trigger
variables. Artifact SHA-256:
`670e127b426616964db34d8c72e98f9d3bcb4ca40ed2e1c4658af91f48e6808e`.

Live DE acceptance is pending: verify old and new armies/Heroes, individual Hero
modifications, upgrades during a rush, conversions, save/reload, full expiry and the
HUD countdowns in a fresh private match. Reciprocal factors preserve multiplicative
technology upgrades; additive changes during the window require an engine check.
The user requested keeping the current human match open, so it was not interrupted.
The user subsequently requested installing both candidates and delivering them
on GitHub. Those historical v0.1.0/v1.5 files are installed locally and available under
[`releases/ra-candidates`](../../releases/ra-candidates/). No Steam/AoE mod listing
was updated, and the fresh-game checks above remain pending.
