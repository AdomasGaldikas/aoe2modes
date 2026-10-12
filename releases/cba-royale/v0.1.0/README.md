# CBA Royale: Last Caravan v0.1.0 prototype

[Download the playable scenario](CBA%20Royale%20Last%20Caravan%20v0.1.0.aoe2scenario?raw=true)
and place it in your AoE2 DE profile's `resources/_common/scenario` folder.
In a new lobby select Custom Scenario and **CBA Royale Last Caravan v0.1.0**.
Use fixed teams P1-P4 versus P5-P8, Faster (2x), and Lock Speed. Civilization
selection is free, including Random. Requires DE update 185872 or newer.

Protect your command wagon, enter the announced safe zone and destroy enemy
wagons. Four-player teams escort their caravans across a shrinking battlefield;
rescue teammates, contest supplies and build limited defenses. The enforced
ending is 70:00 on the game clock, nominally 35 active minutes at Faster speed.

The source build passed embedded XS validation, all three Royale regression
tests (including emitted-script runtime execution), strict scenario audit with
zero errors or warnings, and Ruff. `SHA256SUMS` identifies this exact scenario.
Fresh DE acceptance and twenty human balance matches remain pending. This is a
published prototype, and publication does not establish live engine acceptance.

[Mode source and complete rules](../../../modes/cba_royale/)
| [Live acceptance and balance checklist](../../../docs/cba-royale-playtesting.md)

This delivery adds a standalone scenario file; it does not update an AoE mod
listing or replace any existing RA or Naval scenario.
