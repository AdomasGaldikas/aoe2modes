# RA scenario candidates

Download either scenario file here and place it in your AoE2 DE profile's
`resources/_common/scenario` folder. In a new lobby choose Custom Scenario and
select the normal or Speed filename.

- **CBA Hero 4v4 RA v1.5**: normal RA with compact lowercase HUD labels.
- **CBA Hero 4v4 RA Speed v0.1.0**: the same map and rules, plus a teammate-loss
  rush after 15 minutes: 2x movement and 3x fire rate for five minutes, refreshed
  without stacking. Each team has its own countdown.

All 168 repository tests passed, as did embedded XS validation, repository Ruff
and strict serialized audits. `SHA256SUMS` identifies those exact built files.

Fresh DE acceptance remains pending, including startup, spawning, HUD alignment,
old/new Hero speed, upgrades during rush and expiry. The lobby-population chooser
replacement is also unfinished. These are candidates, not a claim those engine
checks have passed. The user explicitly requested local installation and GitHub
delivery while the current human match stays open. No Steam/AoE mod listing is
updated by this delivery.

Source: `modes/evolution_alpha` and `modes/ra_speed`. Shared rules stay in normal
RA; the independent Speed layer lives in `modes/ra_speed/rush.py`.
