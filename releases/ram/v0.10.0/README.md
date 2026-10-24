# RAM v0.10.0 test candidate

Use the matching **RAM v0.10.0 Data Mod and scenario** in a fresh match after
restarting DE. Existing matches and saves keep their original scripts/data.
This candidate is prepared for the user's manual test; the unlisted mod listing
still carries the previously published v0.9.0 until native acceptance.

- All 62 starting commanders use native bows, crossbows or firearms. Their
  starting profiles share 300 HP, 25 pierce attack, 5 range, two-second reload,
  100% accuracy, 1.4 speed, 2/2 armour and the original Khan's counter classes.
  Native national appearances and firing animations remain distinct.
- The original eight-second +5 HP / +3 attack growth remains attached to each
  starting leader's exact object reference. Separate double-click selection and
  one population slot are retained.
- Actual Castle-wave unit IDs for every civilization are audited. Accepted
  custom voices cover 48 civilizations; 14 keep explicit native speech fallbacks.
  Selection and both legacy command-response slots now use accepted role clips.
  Short extensionless aliases are added; original audio bytes, paths, Wwise
  fallbacks and weapon/death sounds are preserved.
- All 62 army pacing decisions are explicit. Thirteen change from v0.9.0:
  Lithuania gains stronger Leitis and faster/larger waves; Spanish and Saracen
  masses/replacements are reduced; small additional support/frontline changes
  preserve native units, vulnerabilities and counters.
- Center control, map geometry and progression tiers remain unchanged.

Automated validation: 89 distinct current test cases covered, repository Ruff,
embedded XS validation, and strict written-file audit with zero errors/warnings.
`validation.json` records the run boundaries and native test gaps.

The full table and reproducible screening limits are in
[the balance review](../../../docs/ram-balance-v0.10.0.md).
The screen is a playtest aid; it does not reproduce native combat or prove fair
win rates. The filename adjustment is not a proven cause of the reported silence.
Fresh-match voice playback, leader firing/growth/selection and representative
mixed-team matchups remain the user's acceptance checks. Do not publish this
candidate as resolving the reported audio failure before that test succeeds.

Build from repository root:

```sh
python -m pip install -e '.[dev,ram-data]'
python -m aoe2modes build ram
python modes/ram/package.py --game-dir /path/to/AoE2DE
```

The installed game DAT supplies native unit/graphic definitions. Model weights
and local voice-generation environments are unnecessary. Source audio licenses
and provenance are retained under the RAM assets folder. The package manifest
contains full-file hashes and both DAT mutation/roundtrip proofs.
