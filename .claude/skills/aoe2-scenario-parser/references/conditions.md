# Condition reference

Generated from AoE2ScenarioParser 0.8.4 (`AoE2ScenarioParser.objects.support.new_condition.NewConditionSupport`) by `scripts/dump_signatures.py`.

Every factory returns a `Condition` object whose attributes stay editable afterwards.
All parameters default to `None` (leave at the game's default) — always pass them by name.

```py
trigger.new_condition.accumulate_attribute(quantity, attribute, source_player, inverted)
trigger.new_condition.ai_signal(ai_signal, inverted)
trigger.new_condition.ai_signal_multiplayer(ai_signal, inverted)
trigger.new_condition.and_()
trigger.new_condition.bring_object_to_area(unit_object, area_x1, area_y1, area_x2, area_y2, inverted)
trigger.new_condition.bring_object_to_object(unit_object, next_object, inverted)
trigger.new_condition.building_is_trading(unit_object, inverted)
trigger.new_condition.capture_object(unit_object, source_player, inverted)
trigger.new_condition.chance(quantity)
trigger.new_condition.compare_variables(inverted, variable, comparison, variable2)
trigger.new_condition.decision_triggered(inverted, decision_id, decision_option)
trigger.new_condition.destroy_object(unit_object, inverted)
trigger.new_condition.difficulty_level(quantity, inverted)
trigger.new_condition.diplomacy_state(quantity, source_player, inverted, target_player)
trigger.new_condition.display_timer_triggered(timer_id, inverted)
trigger.new_condition.hero_power_cast(source_player)
trigger.new_condition.local_tech_researched(
    local_technology, source_player, unit_object, area_x1, area_y1, area_x2, area_y2, inverted, quantity
)
trigger.new_condition.none()
trigger.new_condition.object_attacked(
    object_list, quantity, source_player, object_group, object_type, unit_object, inverted
)
trigger.new_condition.object_has_action(
    unit_object, next_object, object_list, object_group, object_type, inverted, unit_ai_action
)
trigger.new_condition.object_has_target(unit_object, next_object, object_list, object_group, object_type, inverted)
trigger.new_condition.object_hp(quantity, unit_object, inverted, comparison)
trigger.new_condition.object_not_visible(unit_object)
trigger.new_condition.object_selected(unit_object, inverted)
trigger.new_condition.object_selected_multiplayer(unit_object, source_player, inverted)
trigger.new_condition.object_visible(unit_object)
trigger.new_condition.object_visible_multiplayer(unit_object, source_player, inverted)
trigger.new_condition.objects_in_area(
    quantity, object_list, source_player, area_x1, area_y1, area_x2, area_y2, object_group, object_type,
    inverted, object_state, include_changeable_weapon_objects
)
trigger.new_condition.or_()
trigger.new_condition.own_fewer_objects(
    quantity, object_list, source_player, area_x1, area_y1, area_x2, area_y2, object_group, object_type,
    include_changeable_weapon_objects
)
trigger.new_condition.own_objects(
    quantity, object_list, source_player, object_group, object_type, include_changeable_weapon_objects
)
trigger.new_condition.player_defeated(source_player, inverted)
trigger.new_condition.research_technology(source_player, technology, inverted)
trigger.new_condition.researching_tech(source_player, technology, inverted)
trigger.new_condition.script_call(xs_function)
trigger.new_condition.technology_state(quantity, source_player, technology, inverted)
trigger.new_condition.timer(timer, inverted)
trigger.new_condition.trigger_active(trigger_id, inverted)
trigger.new_condition.units_garrisoned(quantity, unit_object, inverted)
trigger.new_condition.variable_value(quantity, inverted, variable, comparison)
trigger.new_condition.victory_timer(quantity, source_player, inverted, comparison, victory_timer_type)
```
