# Datasets

Import paths verified against AoE2ScenarioParser 0.8.4. **`AoE2ScenarioParser.datasets.player_data`
does not exist in this version** — the docs site is ahead of the release. Use `datasets.players`.

```py
from AoE2ScenarioParser.datasets.players import PlayerId, PlayerColorId, ColorId
from AoE2ScenarioParser.datasets.units import UnitInfo
from AoE2ScenarioParser.datasets.buildings import BuildingInfo
from AoE2ScenarioParser.datasets.heroes import HeroInfo
from AoE2ScenarioParser.datasets.other import OtherInfo
from AoE2ScenarioParser.datasets.techs import TechInfo
from AoE2ScenarioParser.datasets.projectiles import ProjectileInfo
from AoE2ScenarioParser.datasets.terrains import TerrainId
from AoE2ScenarioParser.datasets.object_support import Civilization, StartingAge
from AoE2ScenarioParser.datasets.scenario_variant import ScenarioVariant
from AoE2ScenarioParser.datasets.conditions import ConditionId
from AoE2ScenarioParser.datasets.effects import EffectId
from AoE2ScenarioParser.datasets.trigger_lists import DiplomacyState, Operation, Comparison  # + ~40 more
```

## The `.ID` rule

`UnitInfo`, `BuildingInfo`, `HeroInfo`, `OtherInfo`, `TechInfo` and `ProjectileInfo` entries are
records, not plain ints. Suffix the field you want:

```py
UnitInfo.ARCHER.ID           # 4   — what every parser call wants
UnitInfo.ARCHER.ICON_ID      # 17
UnitInfo.ARCHER.DEAD_ID      # 3
UnitInfo.ARCHER.HOTKEY_ID    # 16083
UnitInfo.ARCHER.IS_GAIA_ONLY # False

UnitInfo.from_id(4)          # UnitInfo.ARCHER
UnitInfo.from_icon_id(17) / from_dead_id(3) / from_hotkey_id(16083)
UnitInfo["ARCHER"]           # normal Enum lookup by name
```

`TerrainId`, `PlayerId`, `ColorId` and everything in `trigger_lists` are plain `IntEnum`s — no `.ID`.

There is no `UnitInfo.VILLAGER`; the members are `VILLAGER_MALE`, `VILLAGER_FEMALE` and their
per-task variants (`..._BUILDER`, `..._FARMER`, `..._FISHERMAN`, …).

## Set helpers

```py
UnitInfo.vils(exclude_female=False, exclude_male=False)
UnitInfo.unique_units(exclude_elite_units=…, exclude_non_elite_units=…, exclude_castle_units=…,
                      exclude_non_castle_units=…, include_chronicles=False)
UnitInfo.gaia_only() / UnitInfo.non_gaia()

TechInfo.unique_techs(exclude_castle_techs=…, exclude_imp_techs=…)
TechInfo.unique_unit_upgrades(exclude_castle_techs=…, exclude_non_castle_techs=…)
TechInfo.blacksmith_techs(ages) / monastery_techs(ages) / university_techs(ages) / town_center_techs(ages)
TechInfo.eco_techs(ages=…, buildings=…)

OtherInfo.trees()
ProjectileInfo.get_unit_projectile(unit_id, has_chemistry=…, secondary=…)
PlayerId.all(exclude_gaia=False)
```

`ages` accepts a single `Age` or a list: `TechInfo.blacksmith_techs([Age.FEUDAL_AGE, Age.CASTLE_AGE])`.

## Players

`PlayerId.GAIA` is 0, then `ONE` … `EIGHT`. The enum exists because not every part of the scenario
file is laid out `0: Gaia, 1: P1 …`, so the parser normalises through this representation layer.

```py
for player in PlayerId.all(exclude_gaia=True):
    ...
```

`PlayerColorId.BLUE / RED / GREEN / YELLOW / AQUA / PURPLE / GRAY / ORANGE` addresses players by
colour instead.

## Dropdown enums (`trigger_lists`)

Every dropdown in an in-game condition or effect has a matching enum. All 45 in 0.8.4 — **the members
of each are listed in `values/trigger-lists.md`**; this page only says what uses what.

```
ActionType            Age                   AttackPriority        AttackStance
Attribute             BlastLevel            BlockageClass         ButtonLocation
ChargeEvent           ChargeType            ColorMood             CombatAbility
Comparison            DamageClass           DecisionOption        DifficultyLevel
DiplomacyState        DisableUnitFlag       FogVisibility         GarrisonType
HeroStatusFlag        Hotkey                LocalTechnology       ObjectAttribute
ObjectClass           ObjectModifyAttributeState                  ObjectState
ObjectType            ObstructionType       OcclusionMode         Operation
PanelLocation         ProjectileHitMode     ProjectileSmartMode   ProjectileVanishMode
SecondaryGameMode     SelectionEffect       TechnologyState       TerrainRestrictions
TimeUnit              UnitAIAction          UnitTrait             VictoryCondition
VictoryTimerType      VisibilityState
```

Where they're used:

| Enum | Used by |
| --- | --- |
| `ActionType` | `task_object` effect |
| `Age` | `modify_resource` effect with the Current Age resource; the `TechInfo` age filters |
| `AttackStance` | `change_object_stance` effect |
| `Attribute` | `accumulate_attribute` condition, resource-modifying effects |
| `ButtonLocation` | `change_research_location` / `change_train_location` effects |
| `ColorMood` | `change_color_mood` effect |
| `Comparison` | any effect/condition comparing a value (`variable_value`, `compare_variables`, …) |
| `DamageClass` | `change_object_attack` / `change_object_armor` effects |
| `DifficultyLevel` | `difficulty_level` condition |
| `DiplomacyState` | `change_diplomacy` effect, `diplomacy_state` condition, `set_diplomacy_teams` |
| `ObjectAttribute` | `modify_attribute` effect — the big one |
| `ObjectClass` / `ObjectType` | every unit-selection effect and condition |
| `ObjectState` | `objects_in_area` condition |
| `Operation` | `change_variable`, `modify_attribute`, `modify_resource`, … |
| `PanelLocation` | `display_instructions` effect |
| `SecondaryGameMode` | `option_manager.secondary_game_modes` |
| `StartingAge` | `player.starting_age` (from `object_support`, not `trigger_lists`) |
| `TechnologyState` | `technology_state` condition |
| `TimeUnit` | `display_timer` effect |
| `UnitAIAction` | `object_has_action` condition |
| `VictoryCondition` | `option_manager.victory_condition` |
| `VictoryTimerType` | `victory_timer` condition |
| `VisibilityState` | `set_player_visibility` effect |

Several are used as values for a *specific* `ObjectAttribute` in `modify_attribute`:
`BlastLevel`, `BlockageClass`, `ChargeEvent`, `ChargeType`, `CombatAbility`, `FogVisibility`,
`GarrisonType`, `HeroStatusFlag`, `Hotkey`, `ObstructionType`, `OcclusionMode`,
`ProjectileHitMode`, `ProjectileSmartMode`, `ProjectileVanishMode`, `SelectionEffect`,
`TerrainRestrictions`, `UnitTrait`.

### Two enums with extra construction helpers

```py
ButtonLocation.row_col(1, 3)                 # == ButtonLocation.r1c3

HeroStatusFlag.CANNOT_BE_CONVERTED + HeroStatusFlag.DELETE_CONFIRMATION   # bit flags, additive
HeroStatusFlag.combine(cannot_be_converted=True, delete_confirmation=True)
```

## ConditionId / EffectId

Rarely needed now that `new_effect.*` / `new_condition.*` exist, but useful when inspecting an
existing scenario (`effect.effect_type == EffectId.PATROL`).

The `attributes` / `default_attributes` dicts exported alongside them are **empty in 0.8.4** — don't
reach for them to discover which fields an effect supports. Use `effects.md` (dumped from the
installed package) or `trigger_manager.get_content_as_string()`, which prints the fields a given
effect actually set.

## Terrain

```py
TerrainId.GRASS_1  TerrainId.BEACH  TerrainId.WATER_SHALLOW  TerrainId.FOREST_OAK  TerrainId.ROAD ...
map_manager.get_tile(x=5, y=8).terrain_id = TerrainId.ROAD
```

All 131 in `values/terrains.md`.

## Looking a name up

Full member lists live in `values/` — `units.md`, `buildings.md`, `heroes.md`, `techs.md`,
`other.md`, `projectiles.md`, `terrains.md`, `trigger-lists.md`.

For a single constant, grepping the installed package is cheaper than opening a 500-line file, and
is the authority when a name is in doubt:

```bash
.venv/Scripts/python -c "from AoE2ScenarioParser.datasets.buildings import BuildingInfo; print([m.name for m in BuildingInfo if 'TOWER' in m.name])"
```
