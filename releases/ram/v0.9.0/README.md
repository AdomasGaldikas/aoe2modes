# RAM v0.9.0

Use the matching Data Mod and scenario in a fresh match. The scenario requires the
Data Mod because its starting leaders use a reserved civilization-specific unit.

[Unlisted RAM Data Mod](https://www.ageofempires.com/mods/details/551448/)

- Civilization-specific starting leaders for all 62 installed civilizations, using
  native game heroes or documented commander substitutes. Britons use King Arthur,
  Lithuanians use Vytautas, and Mongols retain Genghis Khan.
- Native melee/ranged fighting styles with normalized starting combat profiles.
  Existing leader HP/attack growth and separate double-click selection remain.
  All leaders retain the original one-population cost.
- Lithuanian Elite Leitis gain 8 HP; their army cap rises from 60 to 64.
- Roman waves slow from eight to nine seconds; Varangian waves slow to nine seconds
  with their army cap reduced from 80 to 72.
- Center geometry, team rewards and all 509 packaged audio files remain unchanged.

Validation: 74 automated test cases, Ruff, embedded XS validation, and strict
audit with zero errors/warnings. DAT stages prove that restoring permitted
changes reproduces every original byte, and the modified DAT reloads stably.
Native leader loading, fighting, animation, save/load and selection still need
a fresh DE match. Balance values are initial playtest settings, not equal-win-rate
claims.

Build from repository root:

```sh
python -m pip install -e '.[dev,ram-data]'
python -m aoe2modes build ram
python modes/ram/package.py --game-dir /path/to/AoE2DE
```

The installed game DAT supplies native unit/graphic definitions; model weights and
local generation environments are not required. Audio licenses and provenance are
in the RAM assets folder and are not replaced by the repository code license.
The mixed-content ZIP is produced by the packaging command and published through
the unlisted mod page above. `SHA256SUMS` records both release payload hashes.
