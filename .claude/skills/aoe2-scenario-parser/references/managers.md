# Manager reference

Signatures verified against AoE2ScenarioParser 0.8.4.

---

## trigger_manager

```py
add_trigger(name, description=None, description_stid=None, display_as_objective=None,
            short_description=None, short_description_stid=None, display_on_screen=None,
            description_order=None, enabled=None, looping=None, execute_on_load=None,
            header=None, mute_objectives=None, conditions=None, effects=None) -> Trigger
add_variable(name, variable_id=-1) -> Variable
get_trigger(trigger_select) -> Trigger
get_variable(variable_id=None, variable_name=None) -> Variable | None
copy_trigger(trigger_select) -> Trigger
copy_trigger_per_player(from_player, trigger_select, change_from_player_only=False,
                        include_player_source=True, include_player_target=False,
                        trigger_ce_lock=None, include_gaia=False,
                        create_copy_for_players=None) -> Dict[PlayerId, Trigger]
copy_trigger_tree(trigger_select) -> List[Trigger]
copy_trigger_tree_per_player(..., group_triggers_by=None) -> Dict[IntEnum, List[Trigger]]
import_triggers(triggers, index=-1, deepcopy=True) -> List[Trigger]
move_triggers(trigger_ids, insert_index) -> None
remove_trigger(trigger_select) / remove_triggers(trigger_selects)
reorder_triggers(new_id_order=None)
replace_player(trigger_select, to_player, only_change_from=None, include_player_source=True,
               include_player_target=False, trigger_ce_lock=None) -> Trigger
get_summary_as_string() / get_content_as_string() / get_trigger_as_string(trigger_select)
triggers            # List[Trigger]
variables           # List[Variable]
trigger_display_order
```

### Selecting triggers

`get_trigger`, `remove_trigger` and the copy functions all take a `TriggerSelect` (alias `TS`):

```py
from AoE2ScenarioParser.objects.support.trigger_select import TS, TriggerSelect

trigger_manager.get_trigger(7)              # plain int == TS.index(7) — the creation order
trigger_manager.get_trigger(TS.index(7))
trigger_manager.get_trigger(TS.display(3))  # the order shown in the in-game editor
trigger_manager.get_trigger(TS.trigger(t))
```

The per-player copy helpers take `from_player`, an optional `create_copy_for_players` list, and an
optional `trigger_ce_lock` (`TriggerCELock`, same module as `TS`) to exempt specific
conditions/effects from the player rewrite. `copy_trigger_tree_per_player` additionally takes
`group_triggers_by=GroupBy.PLAYER | GroupBy.TRIGGER | GroupBy.NONE`, imported from
`AoE2ScenarioParser.objects.support.enums.group_by`. The tree variants follow
`(de)activate trigger` effects to find everything linked to the source trigger.

`print(trigger_manager.get_summary_as_string())` shows both indices per trigger; use it instead of
opening the editor. `get_content_as_string()` dumps every condition and effect with its attributes —
this is the fastest way to reverse-engineer an existing scenario.

### On the Trigger object

```py
trigger.name / description / short_description / enabled / looping / execute_on_load
trigger.header / display_as_objective / display_on_screen / mute_objectives / description_order
trigger.trigger_id
trigger.new_condition.<name>(...)   # see references/conditions.md
trigger.new_effect.<name>(...)      # see references/effects.md
trigger.conditions / trigger.effects            # editable lists
trigger.condition_order / trigger.effect_order  # display order
trigger.get_condition(...) / trigger.get_effect(...)
trigger.remove_condition(condition_index=…, display_index=…, condition=…)
trigger.remove_effect(effect_index=…, display_index=…, effect=…)
trigger.get_content_as_string()
```

Conditions and effects returned by the factories are plain objects — edit any field after creation
(`effect.message = "..."`, `condition.quantity = 5`).

---

## unit_manager

```py
add_unit(player, unit_const, x=0, y=0, z=0, rotation=0, garrisoned_in_id=-1, animation_frame=0,
         status=2, reference_id=None, caption_string_id=-1, caption_string='',
         tile=None) -> Unit
clone_unit(unit, player=None, unit_const=None, x=None, y=None, ...) -> Unit
get_all_units() -> List[Unit]
get_player_units(player) -> List[Unit]
get_units_in_area(x1=None, y1=None, x2=None, y2=None, tile1=None, tile2=None,
                  unit_list=None, players=None, ignore_players=None) -> List[Unit]
filter_units_by_const(unit_consts, blacklist=False, player_list=None, unit_list=None) -> List[Unit]
filter_units_by(...) / filter_units_by_reference_id(...)
change_ownership(unit, to_player) -> None      # unit may be a single Unit or a list
remove_unit(reference_id=None, unit=None) -> None
remove_eye_candy() -> None
units                                          # Dict-like: units[PlayerId.THREE] = []
```

`get_units_in_area` with `tile1`/`tile2` covers one tile more than the coordinate form, because a
`Tile` is a 1×1 square (`Tile(0, 0)` spans x 0→1).

Removing by `unit=` is much faster than by `reference_id=`, since the unit object already knows its
owner. Wholesale clears are cheapest of all:

```py
unit_manager.units[PlayerId.THREE] = []   # drop every P3 unit
unit_manager.units = []                   # drop everything
```

### On the Unit object

```py
unit.player / unit.unit_const / unit.reference_id / unit.name
unit.x / unit.y / unit.z / unit.rotation / unit.animation_frame / unit.garrisoned_in_id
unit.tile = Tile(0, 0)     # equivalent to unit.x = 0.5; unit.y = 0.5 (tile centre)
```

---

## map_manager

```py
map_size            # read/write; square only, max 480
map_width / map_height
map_color_mood
terrain             # flat 1-D list of TerrainTile, stacked diagonally from the West corner
get_tile(x=None, y=None, i=None) -> TerrainTile
get_tile_safe(x=None, y=None, i=None) -> TerrainTile | None
get_square_1d(x1, y1, x2, y2) -> List[TerrainTile]
get_square_2d(x1, y1, x2, y2) -> List[List[TerrainTile]]
set_elevation(elevation, x1, y1, x2=None, y2=None) -> None
```

`TerrainTile`: writable `terrain_id`, `elevation`, `layer`; read-only `i`, `x`, `y`, `xy`.

`set_elevation` names the *plateau*; the slopes extend outward on their own. `elevation=1` with
`x1=3, y1=6, x2=9, y2=12` gives a flat top over (3,6)–(9,12) and slopes reaching (1,4)–(11,14).
Elevation is 0-based: `elevation=0` is the editor's elevation 1.

---

## player_manager

```py
players             # index by PlayerId, players[PlayerId.TWO]; index 0 is GAIA
active_players = 4  # enables P1–P4; no gaps allowed, which is why player.active is read-only
set_diplomacy_teams(*teams, diplomacy=DiplomacyState.ALLY) -> None
set_default_starting_resources(players=None) -> None
```

### On a Player object

| Attribute | Notes |
| --- | --- |
| `player_id`, `active` | read-only |
| `starting_age` | `StartingAge` |
| `civilization`, `architecture_set` | `Civilization` |
| `food`, `wood`, `gold`, `stone` | int |
| `color` | `ColorId` |
| `human`, `lock_civ`, `lock_personality`, `allied_victory` | bool |
| `population_cap`, `base_priority`, `string_table_name_id` | int |
| `tribe_name` | str |
| `diplomacy` | `List[int]`, non-GAIA |
| `disabled_techs`, `disabled_buildings`, `disabled_units` | `List[int]`, non-GAIA |
| `initial_player_view_x`, `initial_player_view_y` | starting camera, non-GAIA |
| `initial_camera_x`, `initial_camera_y` | deprecated, no effect |
| `set_player_diplomacy(target, state)` | **one-way only** |

```py
player_manager.set_diplomacy_teams([1, 2], [3, 4], diplomacy=DiplomacyState.ALLY)  # both ways

p1 = player_manager.players[PlayerId.ONE]
p1.set_player_diplomacy([2, 3, 4], DiplomacyState.ALLY)   # P1 → others only, not back
p1.disabled_buildings.extend([BuildingInfo.STABLE.ID, BuildingInfo.SIEGE_WORKSHOP.ID])
p1.disabled_techs.append(TechInfo.LOOM.ID)
```

---

## message_manager

Plain strings matching the in-editor Messages tab, plus a `*_string_table_id` per field:

```py
message_manager.instructions = "Do this. Do that... please."
message_manager.hints / .history / .loss / .scouts / .victory
```

---

## option_manager

```py
option_manager.victory_condition            # VictoryCondition
option_manager.victory_score / victory_years / victory_custom_conditions_required
option_manager.secondary_game_modes         # SecondaryGameMode
option_manager.lock_teams / lock_coop_alliances / allow_players_choose_teams
option_manager.random_start_points
option_manager.collide_and_correct / villager_force_drop / legacy_execution_order
```

---

## Scenario-level

```py
AoE2DEScenario.from_file(path, game_version="DE", name=None)
AoE2DEScenario.from_default(scenario_version=None)   # blank scenario, defaults to LATEST_VERSION
scenario.write_to_file(path)
scenario.variant = ScenarioVariant.ROR   # or .AOE2; needs scenario version ≥ 1.49
scenario.scenario_version / scenario_version_tuple / game_version / uuid / name
scenario.new.area()                      # object factory — see references/area.md
scenario.actions.load_data_triggers()    # see references/data-triggers.md
scenario.on_write(callback)
scenario.write_error_file(...)
```

`AoE2DEScenario.LATEST_VERSION` is `1.58` in 0.8.4; scenario versions 1.36 (Nov 2019) onward parse.
