# RAM v0.10.0 civilization balance review

All 62 installed civilizations have an explicit reviewed decision. This release changes 13 and retains the deployed pacing of 49. Native unit IDs, weapons, speed, attack bonuses and vulnerabilities remain intact; only Lithuanian army HP and the listed military caps/spawn intervals change.

This is a conservative playtest release. Neither the matchup screen nor the tests establish equal native win rates. A fresh DE match is still required.

## Changes driven by live gameplay

- Lithuanians: 64 → 72 military cap, 10 → 9 seconds between four-Castle waves; HP bonus +8 → +18. Native Elite Leitis HP therefore goes from 138 to 148 before later technologies. Their armour-ignoring melee attacks and anti-cavalry vulnerabilities remain intact.
- Spanish: 60 → 48 cap and 10 → 12 seconds. Their ranged gunpowder attack and mobility remain native.
- Saracens: 68 → 56 cap and 12 → 14 seconds. Their ranged-melee camel attack and cavalry bonus remain native. The automatic native +25% camel HP bonus is included in the screen: the base Mameluke becomes 100 HP, not 80.

Other adjustments are small support or field-mass changes. Newer civilizations and poorly approximated special mechanics retain their deployed pacing. Retaining a row is an explicit decision, not an omitted civilization.

## Reproducible screen and limits

Inputs are compact measured stats from the installed VER 8.9 DAT, plus reachable native Feudal-age civilization bonuses and the explicit Chinese Chemistry/Thumb Ring and Turkish Chemistry startup grants. Costs are not used as a universal power score.

The pure-Python screen includes matching attack/armour classes, melee armour bypass, reduced secondary projectile damage, bounded splash and ordinary damage charges, accuracy, finite melee frontage, range lead-in, movement speed, simultaneous attrition and four-Castle replacements. It checks distinct-lineup 1v1, 2v2 and 4v4 teams, including mixed ranged/melee groups. Native armour classes and unit counters are retained.

It omits native terrain/pathfinding, human micro and kiting, Castle fire, hero tiers, manually researched upgrades, full team-bonus interactions, armour stripping, Konnik dismounts, reflection and most newer special abilities. Unsupported relevant automatic effects are inventoried in screen-inputs.json. New/special units are not mass-nerfed on this model alone.

The simplified screen disagrees with the live report for Spanish cavalry and does not prove an overall fairness improvement. The observed Spanish/Saracen dominance and Lithuanian weakness therefore take priority over its estimates. The screen is a regression aid and a playtest checklist, not an optimizer or acceptance gate.

```sh
python modes/ram/army_balance.py \
  --inputs modes/ram/assets/balance/screen-inputs.json \
  --review modes/ram/assets/balance/review.json \
  --output /tmp/ram-balance-screen.json
```

## Complete reviewed table

Intervals are game seconds; one wave can produce one unit from each surviving Castle. Military caps include other military units, so hero armies can suppress ordinary waves later in the match.

| Civilization | Previous cap / interval | New cap / interval | Added HP | Rationale |
|---|---:|---:|---:|---|
| 1 British | 72 / 9 | 76 / 9 | +0 | Small longbow field-cap increase gives a fragile ranged army more sustained team support. |
| 2 French | 76 / 8 | 76 / 8 | +0 | Retain current pacing after review; no strong live evidence supports changing this native matchup role. |
| 3 Goths | 92 / 10 | 92 / 10 | +0 | Retain current pacing after review; no strong live evidence supports changing this native matchup role. |
| 4 Teutons | 76 / 8 | 76 / 8 | +0 | Retain current pacing after review; no strong live evidence supports changing this native matchup role. |
| 5 Japanese | 80 / 9 | 80 / 9 | +0 | Retain current pacing after review; no strong live evidence supports changing this native matchup role. |
| 6 Chinese | 76 / 8 | 76 / 8 | +0 | Retain current pacing; Multiple native projectiles and immediate Chemistry/Thumb Ring grants. |
| 7 Byzantine | 56 / 10 | 56 / 10 | +0 | Retain current pacing after review; no strong live evidence supports changing this native matchup role. |
| 8 Persians | 40 / 13 | 36 / 14 | +0 | Reduce stacked elephant frontline mass modestly; retain each elephant's native HP, splash and spear/camel vulnerabilities. |
| 9 Saracens | 68 / 12 | 56 / 14 | +0 | Live test found ranged-melee camel masses oppressive; lower field mass and replacement, preserving their cavalry counter. |
| 10 Turks | 50 / 9 | 50 / 9 | +0 | Retain current pacing; Gunpowder accuracy, automatic HP bonus and free startup Chemistry. |
| 11 Vikings | 86 / 9 | 86 / 9 | +0 | Retain current pacing; Native regeneration and age-dependent infantry HP bonus. |
| 12 Mongols | 56 / 9 | 56 / 9 | +0 | Retain current pacing after review; no strong live evidence supports changing this native matchup role. |
| 13 Celts | 80 / 9 | 80 / 9 | +0 | Retain current pacing after review; no strong live evidence supports changing this native matchup role. |
| 14 Spanish | 60 / 10 | 48 / 12 | +0 | Live test found Spanish ranged cavalry oppressive; lower field mass and replacement while preserving native gunpowder damage and mobility. |
| 15 Aztecs | 92 / 8 | 92 / 8 | +0 | Retain current pacing after review; no strong live evidence supports changing this native matchup role. |
| 16 Mayan | 70 / 8 | 70 / 8 | +0 | Retain current pacing after review; no strong live evidence supports changing this native matchup role. |
| 17 Huns | 80 / 13 | 80 / 13 | +0 | Retain current pacing after review; no strong live evidence supports changing this native matchup role. |
| 18 Koreans | 60 / 12 | 60 / 12 | +0 | Retain current pacing after review; no strong live evidence supports changing this native matchup role. |
| 19 Italians | 72 / 9 | 76 / 9 | +0 | Small Genoese crossbow field-cap increase strengthens an existing anti-cavalry team response. |
| 20 Hindustanis | 60 / 12 | 64 / 12 | +0 | Small Ghulam field-cap increase strengthens native anti-archer frontline support; retain pass-through attack. |
| 21 Incas | 77 / 8 | 77 / 8 | +0 | Retain current pacing after review; no strong live evidence supports changing this native matchup role. |
| 22 Magyars | 80 / 13 | 80 / 12 | +0 | Modestly improve Magyar Huszar replacements while retaining their light-cavalry and anti-siege role. |
| 23 Slavs | 56 / 10 | 56 / 10 | +0 | Retain current pacing after review; no strong live evidence supports changing this native matchup role. |
| 24 Portuguese | 34 / 12 | 34 / 12 | +0 | Retain current pacing; Organ Gun spread and multiple-projectile contact require native playtests. |
| 25 Ethiopians | 80 / 8 | 84 / 8 | +0 | Small Shotel field-cap increase supports fragile melee armies crossing ranged fire. |
| 26 Malians | 81 / 10 | 81 / 10 | +0 | Retain current pacing after review; no strong live evidence supports changing this native matchup role. |
| 27 Berbers | 61 / 10 | 64 / 10 | +0 | Small Camel Archer field-cap increase improves an existing response to enemy mounted archers. |
| 28 Khmer | 31 / 14 | 31 / 14 | +0 | Retain current pacing; Ballista Elephant pass-through shots, high body size and multiple-target interactions. |
| 29 Malay | 80 / 6 | 88 / 6 | +0 | Small Karambit field-cap increase supports the native low-HP swarm role; replacement interval remains six seconds. |
| 30 Burmese | 61 / 10 | 61 / 10 | +0 | Retain current pacing after review; no strong live evidence supports changing this native matchup role. |
| 31 Vietnamese | 81 / 10 | 84 / 10 | +0 | Small Rattan Archer field-cap increase supports native resistance to ranged fire. |
| 32 Bulgarians | 41 / 12 | 41 / 12 | +0 | Retain current pacing; Konnik dismount provides a second body beyond this screen. |
| 33 Tatars | 61 / 12 | 61 / 12 | +0 | Retain current pacing after review; no strong live evidence supports changing this native matchup role. |
| 34 Cumans | 61 / 12 | 61 / 12 | +0 | Retain current pacing after review; no strong live evidence supports changing this native matchup role. |
| 35 Lithuanians | 64 / 10 | 72 / 9 | +18 | Live test found Lithuanian cavalry too weak; increase mounted frontline staying power and replacement without changing speed, armour-ignore attack or counters. |
| 36 Burgundians | 60 / 8 | 60 / 8 | +0 | Retain current pacing; Coustillier opening charge can dominate short fights. |
| 37 Sicilians | 92 / 8 | 92 / 8 | +0 | Retain current pacing after review; no strong live evidence supports changing this native matchup role. |
| 38 Poles | 60 / 8 | 60 / 8 | +0 | Retain current pacing; Obuch armour stripping benefits allied attacks and is not fully simulated. |
| 39 Bohemians | 35 / 15 | 32 / 16 | +0 | Modestly reduce overlapping Hussite Wagon screens and ranged replacement; preserve native resistance and projectile mechanics. |
| 40 Dravidians | 60 / 8 | 60 / 8 | +0 | Retain current pacing; Urumi charge, splash and recovery are native special mechanics. |
| 41 Bengalis | 40 / 8 | 40 / 8 | +0 | Retain current pacing after review; no strong live evidence supports changing this native matchup role. |
| 42 Gurjaras | 41 / 11 | 41 / 11 | +0 | Retain current pacing after review; no strong live evidence supports changing this native matchup role. |
| 43 Romans | 60 / 9 | 60 / 9 | +0 | Retain the previous conservative v0.9 pacing correction; no further automatic change. |
| 44 Armenians | 80 / 8 | 80 / 8 | +0 | Retain current pacing: newer civilization/special unit lacks native matchup evidence; no automatic equal-power assumption. |
| 45 Georgians | 80 / 8 | 80 / 8 | +0 | Retain current pacing: newer civilization/special unit lacks native matchup evidence; no automatic equal-power assumption. |
| 46 Achaemenids | 70 / 10 | 70 / 10 | +0 | Retain current pacing: newer civilization/special unit lacks native matchup evidence; no automatic equal-power assumption. |
| 47 Athenians | 80 / 10 | 80 / 10 | +0 | Retain current pacing: newer civilization/special unit lacks native matchup evidence; no automatic equal-power assumption. |
| 48 Spartans | 80 / 8 | 80 / 8 | +0 | Retain current pacing: newer civilization/special unit lacks native matchup evidence; no automatic equal-power assumption. |
| 49 Shu | 60 / 10 | 60 / 10 | +0 | Retain current pacing: newer civilization/special unit lacks native matchup evidence; no automatic equal-power assumption. |
| 50 Wu | 60 / 10 | 60 / 10 | +0 | Retain current pacing: newer civilization/special unit lacks native matchup evidence; no automatic equal-power assumption. |
| 51 Wei | 60 / 10 | 60 / 10 | +0 | Retain current pacing: newer civilization/special unit lacks native matchup evidence; no automatic equal-power assumption. |
| 52 Jurchens | 80 / 10 | 80 / 10 | +0 | Retain current pacing: newer civilization/special unit lacks native matchup evidence; no automatic equal-power assumption. |
| 53 Khitans | 80 / 10 | 80 / 10 | +0 | Retain current pacing: newer civilization/special unit lacks native matchup evidence; no automatic equal-power assumption. |
| 54 Macedonians | 70 / 10 | 70 / 10 | +0 | Retain current pacing: newer civilization/special unit lacks native matchup evidence; no automatic equal-power assumption. |
| 55 Thracians | 92 / 8 | 92 / 8 | +0 | Retain current pacing: newer civilization/special unit lacks native matchup evidence; no automatic equal-power assumption. |
| 56 Puru | 72 / 9 | 72 / 9 | +0 | Retain current pacing: newer civilization/special unit lacks native matchup evidence; no automatic equal-power assumption. |
| 57 Muisca | 80 / 8 | 80 / 8 | +0 | Retain current pacing: newer civilization/special unit lacks native matchup evidence; no automatic equal-power assumption. |
| 58 Mapuche | 80 / 10 | 80 / 10 | +0 | Retain current pacing: newer civilization/special unit lacks native matchup evidence; no automatic equal-power assumption. |
| 59 Tupi | 80 / 8 | 80 / 8 | +0 | Retain current pacing: newer civilization/special unit lacks native matchup evidence; no automatic equal-power assumption. |
| 60 Saxons | 80 / 8 | 80 / 8 | +0 | Retain current pacing: newer civilization/special unit lacks native matchup evidence; no automatic equal-power assumption. |
| 61 Varangians | 72 / 9 | 72 / 9 | +0 | Retain current pacing: newer civilization/special unit lacks native matchup evidence; no automatic equal-power assumption. |
| 62 Danes | 80 / 8 | 80 / 8 | +0 | Retain current pacing: newer civilization/special unit lacks native matchup evidence; no automatic equal-power assumption. |
