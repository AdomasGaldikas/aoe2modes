# Effect reference

Generated from AoE2ScenarioParser 0.8.4 (`AoE2ScenarioParser.objects.support.new_effect.NewEffectSupport`) by `scripts/dump_signatures.py`.

Every factory returns an `Effect` object whose attributes stay editable afterwards.
All parameters default to `None` (leave at the game's default) — always pass them by name.

```py
trigger.new_effect.acknowledge_ai_signal(ai_signal_value)
trigger.new_effect.acknowledge_multiplayer_ai_signal(ai_signal_value)
trigger.new_effect.activate_trigger(trigger_id)
trigger.new_effect.add_train_location(
    object_list_unit_id, source_player, object_list_unit_id_2, button_location, train_time, hotkey
)
trigger.new_effect.ai_script_goal(ai_script_goal)
trigger.new_effect.attack_move(
    object_list_unit_id, source_player, location_x, location_y, location_object_reference, area_x1, area_y1,
    area_x2, area_y2, object_group, object_type, selected_object_ids, max_units_affected
)
trigger.new_effect.build_object(
    object_list_unit_id, source_player, location_x, location_y, location_object_reference, area_x1, area_y1,
    area_x2, area_y2, wall_x1, wall_y1, wall_x2, wall_y2, object_group, object_type, building_list,
    selected_object_ids, disable_garrison_unload_sound, max_units_affected, issue_group_command, queue_action
)
trigger.new_effect.change_civilization_name(source_player, string_id, message)
trigger.new_effect.change_color_mood(quantity, color_mood)
trigger.new_effect.change_diplomacy(diplomacy, source_player, target_player, mutual_diplomacy)
trigger.new_effect.change_object_armor(
    armour_attack_quantity, armour_attack_class, object_list_unit_id, source_player, area_x1, area_y1, area_x2,
    area_y2, object_group, object_type, operation, selected_object_ids, max_units_affected
)
trigger.new_effect.change_object_attack(
    armour_attack_quantity, armour_attack_class, object_list_unit_id, source_player, area_x1, area_y1, area_x2,
    area_y2, object_group, object_type, operation, selected_object_ids, max_units_affected
)
trigger.new_effect.change_object_caption(
    object_list_unit_id, source_player, string_id, message, area_x1, area_y1, area_x2, area_y2,
    selected_object_ids
)
trigger.new_effect.change_object_civilization_name(
    source_player, string_id, area_x1, area_y1, area_x2, area_y2, message, selected_object_ids,
    max_units_affected
)
trigger.new_effect.change_object_cost(
    object_list_unit_id, source_player, resource_1, resource_1_quantity, resource_2, resource_2_quantity,
    resource_3, resource_3_quantity
)
trigger.new_effect.change_object_description(object_list_unit_id, source_player, string_id, message)
trigger.new_effect.change_object_hp(
    quantity, object_list_unit_id, source_player, area_x1, area_y1, area_x2, area_y2, object_group, object_type,
    operation, selected_object_ids, max_units_affected
)
trigger.new_effect.change_object_icon(
    object_list_unit_id, source_player, area_x1, area_y1, area_x2, area_y2, object_group, object_type,
    object_list_unit_id_2, selected_object_ids, max_units_affected
)
trigger.new_effect.change_object_name(
    object_list_unit_id, source_player, string_id, area_x1, area_y1, area_x2, area_y2, message,
    selected_object_ids, max_units_affected
)
trigger.new_effect.change_object_player_color(
    object_list_unit_id, source_player, area_x1, area_y1, area_x2, area_y2, player_color, selected_object_ids,
    max_units_affected
)
trigger.new_effect.change_object_player_name(
    object_list_unit_id, source_player, string_id, area_x1, area_y1, area_x2, area_y2, message,
    selected_object_ids, max_units_affected
)
trigger.new_effect.change_object_range(
    quantity, object_list_unit_id, source_player, area_x1, area_y1, area_x2, area_y2, object_group, object_type,
    operation, selected_object_ids, max_units_affected
)
trigger.new_effect.change_object_speed(
    quantity, object_list_unit_id, source_player, area_x1, area_y1, area_x2, area_y2, object_group, object_type,
    selected_object_ids, max_units_affected
)
trigger.new_effect.change_object_stance(
    object_list_unit_id, source_player, area_x1, area_y1, area_x2, area_y2, object_group, object_type,
    attack_stance, selected_object_ids, max_units_affected
)
trigger.new_effect.change_object_visibility(
    source_player, target_player, area_x1, area_y1, area_x2, area_y2, visibility_state, max_units_affected,
    selected_object_ids
)
trigger.new_effect.change_ownership(
    object_list_unit_id, source_player, target_player, area_x1, area_y1, area_x2, area_y2, object_group,
    object_type, flash_object, selected_object_ids, max_units_affected
)
trigger.new_effect.change_player_color(source_player, player_color)
trigger.new_effect.change_player_name(source_player, string_id, message)
trigger.new_effect.change_research_location(source_player, technology, object_list_unit_id_2, button_location)
trigger.new_effect.change_technology_cost(
    source_player, technology, resource_1, resource_1_quantity, resource_2, resource_2_quantity, resource_3,
    resource_3_quantity
)
trigger.new_effect.change_technology_description(source_player, technology, string_id, message)
trigger.new_effect.change_technology_hotkey(technology, source_player, quantity)
trigger.new_effect.change_technology_icon(technology, source_player, quantity)
trigger.new_effect.change_technology_location(source_player, technology, object_list_unit_id_2, button_location)
trigger.new_effect.change_technology_name(source_player, technology, string_id, message)
trigger.new_effect.change_technology_research_time(quantity, source_player, technology)
trigger.new_effect.change_train_location(object_list_unit_id, source_player, object_list_unit_id_2, button_location)
trigger.new_effect.change_variable(quantity, operation, variable, message)
trigger.new_effect.change_view(quantity, source_player, location_x, location_y, scroll)
trigger.new_effect.clear_instructions(instruction_panel_position)
trigger.new_effect.clear_timer(timer)
trigger.new_effect.count_units_into_variable(
    object_list_unit_id, source_player, area_x1, area_y1, area_x2, area_y2, object_group, variable2
)
trigger.new_effect.create_decision(
    decision_id, string_id, message, string_id_option1, message_option1, string_id_option2, message_option2
)
trigger.new_effect.create_garrisoned_object(
    object_list_unit_id, source_player, area_x1, area_y1, area_x2, area_y2, object_list_unit_id_2,
    selected_object_ids, max_units_affected, disable_sound
)
trigger.new_effect.create_object(object_list_unit_id, source_player, location_x, location_y, facet, disable_sound)
trigger.new_effect.create_object_armor(
    armour_attack_quantity, armour_attack_class, object_list_unit_id, source_player, area_x1, area_y1, area_x2,
    area_y2, object_group, object_type, operation, selected_object_ids, max_units_affected
)
trigger.new_effect.create_object_attack(
    armour_attack_quantity, armour_attack_class, object_list_unit_id, source_player, area_x1, area_y1, area_x2,
    area_y2, object_group, object_type, operation, selected_object_ids, max_units_affected
)
trigger.new_effect.damage_object(
    quantity, object_list_unit_id, source_player, area_x1, area_y1, area_x2, area_y2, object_group, object_type,
    selected_object_ids, max_units_affected
)
trigger.new_effect.deactivate_trigger(trigger_id)
trigger.new_effect.declare_victory(source_player, enabled)
trigger.new_effect.delete_key(message)
trigger.new_effect.disable_object_deletion(
    object_list_unit_id, source_player, area_x1, area_y1, area_x2, area_y2, selected_object_ids,
    max_units_affected
)
trigger.new_effect.disable_object_selection(
    object_list_unit_id, source_player, area_x1, area_y1, area_x2, area_y2, selected_object_ids,
    max_units_affected
)
trigger.new_effect.disable_technology_stacking(source_player, technology)
trigger.new_effect.disable_unit_attackable(
    object_list_unit_id, source_player, area_x1, area_y1, area_x2, area_y2, selected_object_ids,
    max_units_affected
)
trigger.new_effect.disable_unit_targeting(
    object_list_unit_id, source_player, area_x1, area_y1, area_x2, area_y2, selected_object_ids,
    max_units_affected
)
trigger.new_effect.display_instructions(
    object_list_unit_id, source_player, string_id, display_time, instruction_panel_position, play_sound, message,
    sound_name, use_tag_color_for_icon
)
trigger.new_effect.display_timer(string_id, display_time, time_unit, timer, reset_timer, message)
trigger.new_effect.enable_disable_object(object_list_unit_id, source_player, enabled)
trigger.new_effect.enable_disable_technology(source_player, technology, enabled)
trigger.new_effect.enable_object_deletion(
    object_list_unit_id, source_player, area_x1, area_y1, area_x2, area_y2, selected_object_ids,
    max_units_affected
)
trigger.new_effect.enable_object_selection(
    object_list_unit_id, source_player, area_x1, area_y1, area_x2, area_y2, selected_object_ids,
    max_units_affected
)
trigger.new_effect.enable_technology_stacking(source_player, technology, quantity)
trigger.new_effect.enable_unit_attackable(
    object_list_unit_id, source_player, area_x1, area_y1, area_x2, area_y2, selected_object_ids,
    max_units_affected
)
trigger.new_effect.enable_unit_targeting(
    object_list_unit_id, source_player, area_x1, area_y1, area_x2, area_y2, selected_object_ids,
    max_units_affected
)
trigger.new_effect.freeze_object(
    object_list_unit_id, source_player, area_x1, area_y1, area_x2, area_y2, object_group, object_type,
    selected_object_ids, max_units_affected
)
trigger.new_effect.heal_object(
    quantity, object_list_unit_id, source_player, area_x1, area_y1, area_x2, area_y2, object_group, object_type,
    selected_object_ids, max_units_affected
)
trigger.new_effect.initiate_research(source_player, technology, selected_object_ids)
trigger.new_effect.kill_object(
    object_list_unit_id, source_player, area_x1, area_y1, area_x2, area_y2, object_group, object_type,
    selected_object_ids, max_units_affected
)
trigger.new_effect.load_key_value(variable, message, quantity)
trigger.new_effect.lock_gate(selected_object_ids)
trigger.new_effect.mirror_diplomacy(source_player, target_player, enabled)
trigger.new_effect.modify_attribute(
    quantity, armour_attack_quantity, armour_attack_class, object_list_unit_id, source_player, operation,
    object_attributes, message
)
trigger.new_effect.modify_attribute_by_variable(
    object_list_unit_id, source_player, operation, object_attributes, variable, message, armour_attack_class
)
trigger.new_effect.modify_attribute_for_class(
    object_group2, object_type2, source_player, object_attributes, message, operation, quantity,
    armour_attack_quantity, armour_attack_class
)
trigger.new_effect.modify_object_attribute(
    object_list_unit_id, source_player, object_attributes, selected_object_ids, area_x1, area_y1, area_x2,
    area_y2, operation, message, quantity, armour_attack_quantity, armour_attack_class, object_filter
)
trigger.new_effect.modify_object_attribute_by_variable(
    object_list_unit_id, source_player, object_attributes, selected_object_ids, area_x1, area_y1, area_x2,
    area_y2, operation, message, variable, armour_attack_class
)
trigger.new_effect.modify_resource(quantity, tribute_list, source_player, operation)
trigger.new_effect.modify_resource_by_variable(tribute_list, source_player, operation, variable)
trigger.new_effect.modify_variable_by_attribute(
    object_list_unit_id, source_player, operation, object_attributes, variable, message, armour_attack_class
)
trigger.new_effect.modify_variable_by_resource(tribute_list, source_player, operation, variable)
trigger.new_effect.modify_variable_by_variable(variable, operation, variable2)
trigger.new_effect.none()
trigger.new_effect.patrol(
    object_list_unit_id, source_player, location_x, location_y, area_x1, area_y1, area_x2, area_y2, object_group,
    object_type, selected_object_ids, max_units_affected
)
trigger.new_effect.place_foundation(object_list_unit_id, source_player, location_x, location_y)
trigger.new_effect.play_sound(
    source_player, location_x, location_y, location_object_reference, global_sound, sound_name
)
trigger.new_effect.remove_object(
    object_list_unit_id, source_player, area_x1, area_y1, area_x2, area_y2, object_group, object_type,
    object_state, selected_object_ids, max_units_affected
)
trigger.new_effect.replace_object(
    object_list_unit_id, source_player, target_player, area_x1, area_y1, area_x2, area_y2, object_group,
    object_type, object_list_unit_id_2, selected_object_ids, facet2, max_units_affected
)
trigger.new_effect.research_local_technology(
    local_technology, source_player, selected_object_ids, area_x1, area_y1, area_x2, area_y2,
    object_list_unit_id_2
)
trigger.new_effect.research_technology(source_player, technology, force_research_technology)
trigger.new_effect.script_call(string_id, message)
trigger.new_effect.send_chat(source_player, string_id, message, sound_name)
trigger.new_effect.set_building_gather_point(
    object_list_unit_id, source_player, location_x, location_y, area_x1, area_y1, area_x2, area_y2,
    selected_object_ids, max_units_affected
)
trigger.new_effect.set_object_cost(object_list_unit_id, source_player, quantity, tribute_list)
trigger.new_effect.set_player_visibility(source_player, target_player, visibility_state)
trigger.new_effect.stop_object(
    object_list_unit_id, source_player, area_x1, area_y1, area_x2, area_y2, object_group, object_type,
    selected_object_ids, max_units_affected
)
trigger.new_effect.store_key_value(variable, message)
trigger.new_effect.task_object(
    object_list_unit_id, source_player, location_x, location_y, location_object_reference, area_x1, area_y1,
    area_x2, area_y2, object_group, object_type, action_type, selected_object_ids, disable_garrison_unload_sound,
    max_units_affected, issue_group_command, queue_action
)
trigger.new_effect.teleport_object(
    object_list_unit_id, source_player, location_x, location_y, area_x1, area_y1, area_x2, area_y2, object_group,
    object_type, selected_object_ids, max_units_affected
)
trigger.new_effect.train_unit(
    quantity, object_list_unit_id, source_player, location_x, location_y, area_x1, area_y1, area_x2, area_y2,
    selected_object_ids, max_units_affected
)
trigger.new_effect.tribute(quantity, tribute_list, source_player, target_player)
trigger.new_effect.unload(
    object_list_unit_id, source_player, location_x, location_y, location_object_reference, area_x1, area_y1,
    area_x2, area_y2, object_group, object_type, selected_object_ids, max_units_affected
)
trigger.new_effect.unlock_gate(selected_object_ids)
trigger.new_effect.use_advanced_buttons()
```
