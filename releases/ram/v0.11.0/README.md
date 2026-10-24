# RAM v0.11.0 whole-roster balance test

Use the matching RAM v0.11.0 scenario and Data Mod in a fresh match.
This package is prepared for manual testing, without installation or publication.

- 57 civilizations receive revised role-specific targets; all 62 are covered.
- 26 armies gain additional health; the Lithuanian durability bonus is retained.
- Caps and replacements are reviewed around frontline, ranged support, cavalry,
  counters, swarms and siege roles.
- The overall theoretical four-Castle birth rate stays within 5% of v0.10.0.
- Native weapons, armour classes, abilities, speed, range and vulnerabilities stay
  distinct. Main leaders remain ranged and keep eight-second HP/attack growth.
- Center mechanics, native kill accounting and hero thresholds remain unchanged.
- The accepted audio, unit bindings and reserved leader definitions are retained.

Validation: 96 tests pass, repository Ruff passes, embedded XS validates, and
strict written-file audit reports zero errors/warnings. All 910 package files
pass ZIP/hash checks; all 893 audio files and the Data Mod DAT match v0.10.0.

[Full roster targets and comparison limits](../../../docs/ram-balance-v0.11.0.md)

The corrected comparison handles melee/pierce armour bypass, equal-exposure
paired teams and separate health/kill-feed metrics. Half-population cap behavior,
contact width and fresh/full fields are sensitivity cases. Native DE mechanics,
late upgrades and human play still require fresh-match testing; no equal-win-rate
or guaranteed-fun claim is made from the automated comparison.

Rebuild with the project environment:

```sh
python -m aoe2modes build ram
python modes/ram/package.py --game-dir /path/to/AoE2DE
```

Validation and payload hashes are recorded beside this file. Audio licenses and
provenance remain under the mode assets and inside the mixed-content package.
