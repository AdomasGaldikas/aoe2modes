"""Native one-use backup state and compact combat-objective presentation."""

from AoE2ScenarioParser.datasets.conditions import ConditionId
from AoE2ScenarioParser.datasets.effects import EffectId
from AoE2ScenarioParser.datasets.players import PlayerId
from AoE2ScenarioParser.datasets.trigger_lists import Comparison, Operation
from AoE2ScenarioParser.datasets.units import UnitInfo

BACKUP_VARIABLE_BASE = 145
BACKUP_AVAILABLE = 1
BACKUP_ACTIVE = 2
BACKUP_SPENT = 0
BACKUP_HELP = (
    "Move to the marked side island to call six Scorpions for 50 seconds. One use."
)
SHARED_KING_HELP = (
    "Skorpion King: move to the marked side island for six Scorpions (50s, once). "
    "White King: displays live kills."
)


def configure_backup_hud(ctx, *, occupied_base, eliminated_base):
    """Toggle numeric/A rows using native state, independent of XS identity."""
    by_name = {trigger.name: trigger for trigger in ctx.tm.triggers}
    units = {unit.reference_id: unit for group in ctx.um.units for unit in group}
    initialize = ctx.tm.add_trigger("Scorpion Backup Initialize")
    for color in range(1, 9):
        state = BACKUP_VARIABLE_BASE + color - 1
        ctx.tm.add_variable(f"p{color}backup", variable_id=state)
        initialize.new_effect.change_variable(
            variable=state, quantity=BACKUP_AVAILABLE, operation=Operation.SET,
        )
        numeric = by_name[f"Combat HUD Live P{color}"]
        numeric.short_description += f" | <p{color}backup>"
        active = ctx.tm.add_trigger(
            f"Combat HUD Backup Active P{color}",
            description_stid=0, short_description_stid=0,
            short_description=numeric.short_description.replace(f"<p{color}backup>", "A"),
            display_on_screen=1, description_order=numeric.description_order,
            enabled=0, mute_objectives=1,
        )
        active.new_condition.player_defeated(source_player=PlayerId.GAIA)
        syncs = []
        for label, shown, hidden, comparison in (
            ("Numeric", numeric, active, Comparison.LESS),
            ("Active", active, numeric, Comparison.EQUAL),
        ):
            sync = ctx.tm.add_trigger(f"Scorpion Backup HUD {label} P{color}", enabled=0, looping=1)
            sync.new_condition.timer(timer=1)
            sync.new_condition.variable_value(
                variable=occupied_base + color - 1, quantity=1, comparison=Comparison.EQUAL,
            )
            sync.new_condition.variable_value(
                variable=state, quantity=BACKUP_ACTIVE, comparison=comparison,
            )
            sync.new_effect.deactivate_trigger(trigger_id=hidden.trigger_id)
            sync.new_effect.activate_trigger(trigger_id=shown.trigger_id)
            syncs.append(sync)

        # Defeat removes the deployed units early; preserve the final spent value.
        end = ctx.tm.add_trigger(f"Scorpion Backup Defeated P{color}")
        end.new_condition.timer(timer=1)
        end.new_condition.variable_value(variable=state, quantity=BACKUP_ACTIVE, comparison=Comparison.EQUAL)
        end.new_condition.variable_value(
            variable=eliminated_base + color - 1, quantity=1, comparison=Comparison.EQUAL,
        )
        end.new_effect.change_variable(variable=state, quantity=BACKUP_SPENT, operation=Operation.SET)

        for owner in range(1, 9):
            gate = by_name[f"Occupied Slot S{color} W{owner}"]
            activations = [effect for effect in gate.effects
                           if effect.effect_type == EffectId.ACTIVATE_TRIGGER
                           and effect.trigger_id == numeric.trigger_id]
            if len(activations) != 1:
                raise RuntimeError(f"missing unique backup HUD activation for {gate.name}")
            gate.effects.remove(activations[0])
            for sync in syncs:
                gate.new_effect.activate_trigger(trigger_id=sync.trigger_id)
            claim = by_name[f"King Island S{color} W{owner}"]
            references = [condition.unit_object for condition in claim.conditions
                          if condition.condition_type == ConditionId.BRING_OBJECT_TO_AREA]
            if len(references) != 1:
                raise RuntimeError(f"missing unique activation King for {claim.name}")
            gate.new_effect.change_object_name(
                source_player=owner, selected_object_ids=references, message="Skorpion King",
            )
            # DE descriptions target a type, not an instance. P1 uses King Sancho;
            # the other backup Kings share their type with the white kill counter.
            king_type = units[references[0]].unit_const
            gate.new_effect.change_object_description(
                source_player=owner, object_list_unit_id=king_type,
                message=SHARED_KING_HELP if king_type == UnitInfo.KING.ID else BACKUP_HELP,
            )
