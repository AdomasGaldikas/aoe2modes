"""RAM startup audio and the current release's opening message."""

import tomllib

from AoE2ScenarioParser.datasets.players import PlayerId


def configure_mixed_content(ctx):
    with (ctx.mode_dir / "mode.toml").open("rb") as handle:
        settings = tomllib.load(handle)["ram_mod"]
    ctx.message_manager.victory = ctx.message_manager.victory.replace("RA VICTORY", "RAM VICTORY")
    trigger = ctx.tm.add_trigger("RAM — custom startup audio", enabled=True, looping=False)
    trigger.new_condition.timer(timer=settings["sound_delay_seconds"])
    for player in PlayerId.all(exclude_gaia=True):
        trigger.new_effect.play_sound(
            source_player=player, global_sound=True, sound_name=settings["sound_name"],
        )
        trigger.new_effect.display_instructions(
            source_player=player, display_time=8, instruction_panel_position=0,
            message=f"RAM v{ctx.spec.version}: control the center for team kill bonuses.",
        )
