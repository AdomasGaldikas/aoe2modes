# RAM v0.11.0: whole-roster team balance candidate

This pass changes **57 of 62 civilizations**, including individual durability
increases for **26 armies**, while retaining the Lithuanian increase. All 62 have
explicit role targets. It follows the
user's request for a fun mixed-team game across the roster, extending the smaller
v0.10.0 correction. These are test settings; native playtesting still decides
whether the result feels fair and enjoyable.

## Team roles and pace

- Fragile frontline and counter troops gain modest health instead of simply more
  disposable bodies. Longbows, Berserks, Woad Raiders, Shotel Warriors, Ghulams,
  Karambits, Rattan Archers and several newer units receive distinct adjustments.
- Heavy cavalry, durable ranged wagons and siege batteries retain their native
  weapons and vulnerabilities, with caps and replacement rates suited to their
  stacked team-fight strength.
- Anti-archer, anti-cavalry, anti-siege, raiding and armour-stripping roles remain
  available. Nobody receives a generic replacement unit or universal attack buff.
- Armour-ignoring arrows, mass cavalry bonuses, auras, slows, opening attacks,
  melee-blocking armour, lasting damage and attack-speed ramping are considered
  explicitly. A low listed attack value is not treated as proof a unit is weak.
- Main leaders retain v0.10.0's ranged appearances, common combat profiles,
  separate selection, one population slot and eight-second +5 HP / +3 attack
  growth. Center capture, rewards, hero thresholds, native kill accounting and
  map geometry are unchanged.

The summed theoretical four-Castle birth frequency is **95.25%** of
v0.10.0. This preserves overall battle pace while redistributing strength; it
does not mean every individual civilization produces at the same rate. Each
flat health addition is at most 20% of that unit's measured starting health.

## What the comparison corrects

The native DAT's combat-ability bit1 is set for both Leitis and Composite Bowmen;
the comparison now respects armour bypass for melee and pierce base attacks.
Karambit native population storage is 0.5; normal military bodies are generally
1. The scenario cap reads resource40 (military population), whose weighting is
not established by resource4/11 storage values. Body-cap and population-weighted
interpretations are separate sensitivity runs, with no new population override.

Iron Pagoda durable armour blocks melee attacks; it is not an extra life.
Monaspa proximity bonuses, Strategos ally auras, Obuch stripping, Liao Dao lasting
damage, Shu/Mapuche slows, Wei kill-based growth and Temple Guard attack-speed
ramping add team utility that a simple direct-damage duel cannot reproduce. Hearth Troops' opening javelins and
Jomsvikings' anti-building/ship torches are not generic sustained damage charges.
The raw ability byte and verified notes are retained in the compact inputs.

The offline comparison uses exactly equal civilization and lineup-position
exposure in paired side-swapped rounds. It reports 1v1, 2v2 and 4v4 separately,
with both health/field-fraction and kill-feed trade metrics. It exercises fresh
build-up versus full fields, and frontal versus wider contacts. Existing native
kill progression remains unchanged: durability is used to reduce fragile-body
feeding; no synthetic combat-XP or recursive bonus-kill ledger is introduced.

This comparison still omits actual DE pathfinding, human micro and kiting,
Castle fire, full aura/ability behavior, researched late-game technologies,
hero progression and native batch-spawn timing. Results are stress-test evidence,
not win rates or proof of enjoyable play. Numeric targets are reviewed role
choices, not the output of blindly optimizing that proxy.

```sh
python modes/ram/army_balance.py \
  --inputs modes/ram/assets/balance/screen-inputs.json \
  --review modes/ram/assets/balance/review.json \
  --output /tmp/ram-v0.11.0-screen.json \
  --cap-basis bodies --contacts frontal --start fresh
```

Change `--cap-basis` to `population`, `--contacts` to `wide`, and `--start` to `full`
for the other sensitivity cases. `screen-report.json` records a compact default-run summary;
`screen-sensitivity.json` records compact results for the comparison cases.

## Comparison results and limits

Eight cases cover both cap interpretations, frontal/wide contacts and fresh/full
fields, with equal exposure of every civilization. The aggregate ordinary-unit
health delivery proxy stays at 97.68% of v0.10.0, alongside 95.25% birth frequency.
For full-field 4v4, the spread in paired lineup health fraction falls from 0.4194
to 0.4134 with frontal contacts and from 0.4299 to 0.4209 with wider contacts.
Kill-feed spread also falls slightly in those full-field cases. Fresh build-up
mixed-team spreads worsen slightly (0.1956 to 0.1978 in health fraction and
0.3013 to 0.3066 in kill feed). These mixed results are retained openly: the
comparison does not establish a universal improvement, and targets are not tuned
to hide the unfavorable case. Two denser four-round checks (16/32/64 appearances
per civilization in 1v1/2v2/4v4) improve the fresh/frontal 4v4 health spread from
0.1296 to 0.1198 and kill-feed spread from 0.1891 to 0.1771; wide/full spreads
also improve slightly. Thin and denser samples disagree about early build-up,
which demonstrates sampling uncertainty. Add `--draws 384` to reproduce those
denser checks. Native Spanish performance previously contradicted the simplified
model, so reported gameplay retains priority over those scores.

## Complete target table

Cap is the scenario's military-population threshold, not a claim about a fixed
number of bodies. Wave intervals are game seconds and produce at most one unit
per surviving Castle. Native population admission still applies. Health additions
apply once per runtime owner's actual civilization before army births; later
native technologies retain their normal effects.

| Civilization | Role | v0.10 cap / seconds / HP bonus | v0.11 cap / seconds / HP bonus | Reason |
|---|---|---:|---:|---|
| 1 British | foot archer | 76 / 9 / +0 | 76 / 9 / +4 | Fragile longbows get slightly sturdier individual bodies; retain their reach advantage and melee vulnerability without increasing wave frequency. |
| 2 French | throwing support | 76 / 8 / +0 | 72 / 9 / +0 | Long-range melee damage bypasses archer-style pierce protection; reduce overlapping support mass without changing axe attacks. |
| 3 Goths | anti archer infantry | 92 / 10 / +0 | 84 / 9 / +4 | Keep the high-pierce-armour archer counter, with steadier smaller waves and a small survival increase rather than more feed bodies. |
| 4 Teutons | armoured infantry | 76 / 8 / +0 | 68 / 9 / +8 | Retain slow elite armour and melee strength; slightly sturdier individuals with less stacked mass and replacement. |
| 5 Japanese | anti hero infantry | 80 / 9 / +0 | 72 / 9 / +4 | Preserve fast attack and anti-hero specialization; trade some maximum mass for modest durability. |
| 6 Chinese | volley archer | 76 / 8 / +0 | 68 / 9 / +0 | Five projectiles plus startup technologies give strong screened damage; trim saturation while retaining the volley identity. |
| 7 Byzantine | anti infantry cavalry | 56 / 10 / +0 | 52 / 11 / +0 | Preserve anti-infantry and counter resistance; reduce continuous heavy-cavalry stacking. |
| 8 Persians | elephant frontline | 36 / 14 / +0 | 36 / 14 / +0 | Large-health splash frontliners remain valuable screens; limit simultaneous mass while retaining spear/camel counters. |
| 9 Saracens | mobile melee ranged | 56 / 14 / +0 | 56 / 14 / +0 | Retain the mounted anti-cavalry skirmisher role; reduce the oppressive ranged-melee mass reported in the match. |
| 10 Turks | foot gunpowder | 50 / 9 / +0 | 56 / 10 / +4 | Fragile long-range gun crews get modest staying power and field presence, offset by a slightly slower wave. |
| 11 Vikings | regenerating infantry | 86 / 9 / +0 | 80 / 8 / +8 | Support frontline sustain and earlier replacements with fewer simultaneous bodies; preserve native regeneration. |
| 12 Mongols | mobile archer | 56 / 9 / +0 | 60 / 9 / +0 | Provide mobile ranged support and anti-siege coverage through a small cap increase; retain native fragility and range. |
| 13 Celts | fast infantry | 80 / 9 / +0 | 76 / 8 / +6 | Fast melee raiders get better survival and replacement cadence rather than a larger disposable army. |
| 14 Spanish | mobile gunpowder | 48 / 12 / +0 | 48 / 12 / +0 | Preserve gunpowder burst and mobility while reducing the oppressive mounted gun mass observed in the match. |
| 15 Aztecs | anti infantry infantry | 92 / 8 / +0 | 80 / 9 / +0 | High attack and anti-infantry bonuses keep their counter role; reduce redundant mass and continuous replacement. |
| 16 Mayan | mobile foot archer | 70 / 8 / +0 | 72 / 9 / +0 | Durable fast foot archers retain mobility; limit replacement pressure while slightly increasing field flexibility. |
| 17 Huns | raiding cavalry | 80 / 13 / +0 | 72 / 12 / +0 | Fewer fielded Tarkans with more regular replacements keep raids and building pressure active without a large tank mass. |
| 18 Koreans | armoured mobile archer | 60 / 12 / +0 | 52 / 13 / +0 | Very high-health ranged wagons should be fewer support bodies; preserve their armour, range and anti-siege vulnerability. |
| 19 Italians | anti cavalry archer | 76 / 9 / +0 | 76 / 9 / +4 | Strengthen an existing ranged counter to mounted teams through modest survival and field presence. |
| 20 Hindustanis | anti archer infantry | 64 / 12 / +0 | 68 / 11 / +4 | Make the pass-through anti-archer frontline moderately more available, with small durability and replacement improvements. |
| 21 Incas | reach anti cavalry infantry | 77 / 8 / +0 | 80 / 9 / +6 | Keep spear reach and cavalry punishment; sturdier counter bodies with a slightly slower stream. |
| 22 Magyars | anti siege cavalry | 80 / 12 / +0 | 76 / 11 / +4 | More reliable light-cavalry replacements and modest survival help teams reach enemy siege and backlines. |
| 23 Slavs | armoured cavalry | 56 / 10 / +0 | 52 / 11 / +0 | High melee armour remains their strength; reduce stacked heavy-frontline mass without removing ranged counters. |
| 24 Portuguese | volley siege | 34 / 12 / +0 | 36 / 13 / +0 | Organ Gun projectiles and spread are retained; slightly higher field capacity is offset by slower replacements. |
| 25 Ethiopians | shock infantry | 84 / 8 / +0 | 80 / 8 / +8 | Fragile high-damage infantry receive sturdier bodies instead of a larger feed-prone cap. |
| 26 Malians | mobile throwing support | 81 / 10 / +0 | 72 / 11 / +4 | Long-range melee-damage support remains mobile; slightly tougher bodies with lower saturation and replacement. |
| 27 Berbers | anti mobile archer | 64 / 10 / +0 | 64 / 10 / +4 | Maintain a useful mounted-archer counter in mixed teams with a modest durability improvement. |
| 28 Khmer | pass through elephant siege | 31 / 14 / +0 | 28 / 15 / +0 | Pass-through shots can damage several screened units; limit stacked elephant batteries while preserving their native mechanics. |
| 29 Malay | half population swarm | 88 / 6 / +0 | 76 / 6 / +8 | Retain rapid low-population swarms, but trade maximum mass for sturdier individuals to reduce death feeding. |
| 30 Burmese | scatter mobile ranged | 61 / 10 / +0 | 56 / 11 / +4 | Scattered darts retain packed-army threat; tougher individuals replace part of the old mass and firing saturation. |
| 31 Vietnamese | anti archer foot archer | 84 / 10 / +0 | 80 / 10 / +6 | Improve individual staying power against ranged pressure while trimming maximum body count. |
| 32 Bulgarians | dismounting cavalry | 41 / 12 / +0 | 44 / 12 / +0 | A small cap increase supports the combined mounted/dismounted role; preserve the extra body without additional HP. |
| 33 Tatars | durable raiding cavalry | 61 / 12 / +0 | 64 / 11 / +0 | Native gold generation has little value in this free-resource mode; improve field presence and replacement modestly. |
| 34 Cumans | volley mobile archer | 61 / 12 / +0 | 64 / 12 / +4 | Fragile multi-arrow cavalry gain modest durability and field capacity; preserve existing wave frequency and native volleys. |
| 35 Lithuanians | armour ignoring cavalry | 72 / 9 / +18 | 72 / 9 / +18 | Retain the mounted durability correction from the live report; preserve armour bypass and cavalry counters. |
| 36 Burgundians | charge cavalry | 60 / 8 / +0 | 56 / 9 / +0 | Opening charge remains dangerous; reduce overlapping charge bodies and replacement pressure. |
| 37 Sicilians | counter resistant infantry | 92 / 8 / +0 | 84 / 9 / +4 | Preserve native bonus-damage resistance; use modest individual durability with less accumulated mass. |
| 38 Poles | armour stripping infantry | 60 / 8 / +0 | 60 / 9 / +0 | Armour stripping amplifies allied damage; retain the utility and cap but slow continuous stacking. |
| 39 Bohemians | screening siege | 32 / 16 / +0 | 32 / 16 / +0 | High-health multi-projectile screens remain useful; keep the reduced battery size and replacement pace. |
| 40 Dravidians | lifesteal charge infantry | 60 / 8 / +0 | 56 / 9 / +4 | Retain native charge and recovery with a small survival improvement, offset by lower mass and replacement. |
| 41 Bengalis | hybrid cavalry | 40 / 8 / +0 | 44 / 9 / +0 | Weapon switching provides flexibility; slightly more field presence is offset by slower replacements. |
| 42 Gurjaras | pass through throwing support | 41 / 11 / +0 | 44 / 12 / +0 | Line attacks retain team-fight value; a small capacity increase is offset by a slower stream. |
| 43 Romans | aura heavy cavalry | 60 / 9 / +0 | 56 / 10 / +0 | Strong cavalry with allied-infantry support value should have less overlapping mass; preserve the native aura. |
| 44 Armenians | armour ignoring archer | 80 / 8 / +0 | 76 / 8 / +0 | Keep native armour-ignoring archers useful before later attack upgrades; reduce maximum mass slightly without slowing replacements or buffing raw attack. |
| 45 Georgians | formation cavalry | 80 / 8 / +0 | 72 / 9 / +0 | Nearby-unit attack stacking remains intact; reduce formation mass and replacement without a blanket damage rewrite. |
| 46 Achaemenids | hybrid foot archer | 70 / 10 / +0 | 72 / 10 / +4 | Retain ranged/melee flexibility with modest individual staying power and field presence. |
| 47 Athenians | aura infantry | 80 / 10 / +0 | 76 / 10 / +8 | Sturdier aura-support infantry can accompany allies; slightly smaller field mass offsets durability while wave frequency stays unchanged. |
| 48 Spartans | splash armoured infantry | 80 / 8 / +0 | 72 / 9 / +0 | Native splash and pierce protection provide strong screened frontline value; limit stacked mass and replacement. |
| 49 Shu | anti cavalry infantry | 60 / 10 / +0 | 64 / 9 / +4 | Support an existing cavalry response with moderate survival and more reliable replacements; preserve native defensive mechanics. |
| 50 Wu | long range fire archer | 60 / 10 / +0 | 60 / 11 / +0 | Extreme reach and native fire effects need screened limits; preserve the weapon and slow replacement slightly. |
| 51 Wei | anti archer cavalry | 60 / 10 / +0 | 56 / 11 / +0 | High pierce armour and archer bonus retain backline pressure; reduce simultaneous raiding mass and replacement. |
| 52 Jurchens | melee blocking cavalry | 80 / 10 / +0 | 72 / 11 / +0 | Native durable armour can block melee attacks; preserve the defensive mechanic while trimming stacked mass and replacement. |
| 53 Khitans | lasting damage infantry | 80 / 10 / +0 | 76 / 10 / +6 | Improve frontline survival while reducing field cap; retain lasting-damage utility and existing wave frequency without adding attack. |
| 54 Macedonians | anti hero cavalry | 70 / 10 / +0 | 64 / 11 / +0 | High-pierce-armour cavalry with hero pressure remains specialized; reduce mass and constant replacement. |
| 55 Thracians | anti cavalry shock infantry | 92 / 8 / +0 | 84 / 9 / +6 | Sturdier anti-cavalry bodies retain useful counters, with smaller and slightly slower waves to limit death feeding. |
| 56 Puru | foot archer | 72 / 9 / +0 | 72 / 10 / +4 | Preserve native weapon mechanics; modest individual survival replaces some continuous firing saturation. |
| 57 Muisca | combat ramping counter infantry | 80 / 8 / +0 | 72 / 9 / +0 | Native attack speed grows during sustained combat, alongside broad counters and a durable body; limit maximum mass and replacement. |
| 58 Mapuche | snaring mobile archer | 80 / 10 / +0 | 72 / 10 / +0 | Native slow and high mobility give strong team focus-fire value; reduce maximum snare saturation without buffing raw damage. |
| 59 Tupi | splash infantry | 80 / 8 / +0 | 72 / 9 / +0 | Large native splash keeps team-fight value; reduce accumulated bodies and replacement pressure. |
| 60 Saxons | opening javelin infantry | 80 / 8 / +0 | 76 / 9 / +0 | Retain the native opening javelin and pierce resistance; modestly limit dense frontline stacking. |
| 61 Varangians | mobile melee ranged | 72 / 9 / +0 | 64 / 10 / +0 | Fast ranged-melee attacks bypass pierce protection; reduce sustained mass while keeping their distinct counter role. |
| 62 Danes | counter raiding infantry | 80 / 8 / +0 | 76 / 9 / +0 | Retain anti-cavalry and building-raiding torch utility, with slightly lower field stacking and replacement. |

## Fresh-match acceptance

Use the matching v0.11.0 scenario and Data Mod. Compare mixed frontline/ranged
teams, all-ranged teams, cavalry raids into counter teams, swarms into splash,
and durable siege screens into mobile anti-siege. Check early build-up, researched
armies and hero unlocks; observe center occupancy and whether fragile roles feed
heroes before they contribute. Test representative newer native abilities too.
The user chose to receive a test package: this pass is not installed or published.
