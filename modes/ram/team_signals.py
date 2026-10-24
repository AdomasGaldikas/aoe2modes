"""Selectable map posts with synchronized input and owner-resolved team-only delivery."""

import hashlib
import json
import math
import tomllib
import wave

from AoE2ScenarioParser.datasets.buildings import BuildingInfo
from AoE2ScenarioParser.datasets.other import OtherInfo
from AoE2ScenarioParser.datasets.players import ColorId
from AoE2ScenarioParser.datasets.terrains import TerrainId
from AoE2ScenarioParser.datasets.trigger_lists import Comparison, Operation

from aoe2modes.lib.xs import substitute

from .v2_map import v2_cell_for_player, v2_position_for_player
from .voice_lines import signal_lines


def team_for(color):
    return 1 if color <= 4 else 2


def audience_for(metadata):
    team = team_for(metadata["target"])
    if metadata["signal"] == "attack":
        team = 3 - team
    return tuple(range(1, 5) if team == 1 else range(5, 9))


def commands_for(color, lines):
    return [(name, item) for name, item in lines.items()
            if (item["signal"] == "help" and item["target"] == color)
            or (item["signal"] == "attack" and team_for(item["target"]) != team_for(color))
            or (item["signal"] == "feed" and item["target"] != color
                and team_for(item["target"]) == team_for(color))]


def configure_team_signals(ctx):
    settings = tomllib.loads((ctx.mode_dir / "mode.toml").read_text())["team_signals"]
    if not settings["enabled"]:
        return
    for name, value in settings.items():
        if name != "enabled" and (type(value) is not int or value < 1):
            raise ValueError(f"team_signals.{name} must be a positive integer")
    lines = signal_lines()
    directory = ctx.mode_dir / "assets/audio"
    manifest = json.loads((directory / "manifest.json").read_text())["clips"]
    longest = 0
    for name, item in lines.items():
        path = directory / f"{name}.wav"
        if (hashlib.sha256(path.read_bytes()).hexdigest() != manifest[path.name]["sha256"]
                or item["text"] != manifest[path.name]["text"]):
            raise ValueError(f"Team signal audio mismatch: {name}")
        with wave.open(str(path), "rb") as audio:
            if (audio.getnchannels(), audio.getsampwidth(), audio.getframerate()) != (1, 2, 48000):
                raise ValueError(f"Invalid team signal PCM format: {name}")
            seconds = audio.getnframes() / audio.getframerate()
        if not 0.5 < seconds < 8:
            raise ValueError(f"Invalid team signal duration: {name}")
        longest = max(longest, seconds)

    base = max(v.variable_id for v in ctx.tm.variables) + 1
    queue_base, delivery, ack_base, cursor = base, base + 8, base + 9, base + 17
    for offset, suffix in ((0, "signalrequest"), (9, "signalack")):
        for color in range(1, 9):
            ctx.tm.add_variable(f"p{color}{suffix}", variable_id=base + offset + color - 1)
    ctx.tm.add_variable("ramsignaldelivery", variable_id=delivery)
    ctx.tm.add_variable("ramsignalcursor", variable_id=cursor)
    variables = {v.name: v.variable_id for v in ctx.tm.variables}
    busy = variables.get("ramvoicebusy")
    if busy is None:
        busy = cursor + 1
        ctx.tm.add_variable("ramvoicebusy", variable_id=busy)
    # Tactical requests take the next free slot ahead of queued center notices.
    # Native variable gates preserve Backup/center playback without an XS guard.
    for trigger in ctx.tm.triggers:
        if trigger.name.startswith("RAM Center voice — "):
            for color in range(1, 9):
                trigger.new_condition.variable_value(variable=queue_base + color - 1, quantity=0,
                                                       comparison=Comparison.EQUAL)
    cooldown = ctx.tm.add_trigger("RAM Team signal voice cooldown", enabled=0)
    cooldown.new_condition.timer(
        timer=math.ceil(longest * settings["audio_game_time_scale"]) + settings["queue_gap_seconds"],
    )
    cooldown.new_effect.change_variable(variable=busy, quantity=0, operation=Operation.SET)

    # New isolated pads use previously empty water, with a water moat. They do
    # not connect to Castle routes, selector lanes, or the vote/Backup islands.
    water = {int(t) for t in TerrainId.water_terrains()}
    pad_cells = set()
    original_units = list(ctx.um.get_all_units())
    x1, y1 = settings["pad_x1"], settings["pad_y1"]
    x2, y2 = settings["pad_x2"], settings["pad_y2"]
    if x1 >= x2 or y1 >= y2:
        raise ValueError("Team signal island bounds must be ordered")
    for color in range(1, 9):
        cells = {v2_cell_for_player(color, x, y)
                 for y in range(y1, y2 + 1) for x in range(x1, x2 + 1)}
        if cells & pad_cells:
            raise RuntimeError("Team signal islands overlap")
        moat = {v2_cell_for_player(color, x, y)
                for y in range(y1 - 1, y2 + 2) for x in range(x1 - 1, x2 + 2)} - cells
        if any(int(ctx.mm.get_tile(x=x, y=y).terrain_id) not in water for x, y in moat):
            raise RuntimeError(f"P{color} signal island would connect to existing land")
        for x, y in cells:
            if int(ctx.mm.get_tile(x=x, y=y).terrain_id) not in water:
                raise RuntimeError(f"Signal island would replace existing land at {(x, y)}")
        if any((int(u.x), int(u.y)) in cells for u in original_units):
            raise RuntimeError(f"Signal island would overlap an existing P{color} object")
        pad_cells.update(cells)
        for x, y in cells:
            tile = ctx.mm.get_tile(x=x, y=y)
            tile.terrain_id = TerrainId.ROAD_GRAVEL
            tile.elevation = 1
            tile.layer = -1

    protect = ctx.tm.add_trigger("RAM — protect team signal posts")
    wrappers = []
    for color in range(1, 9):
        commands = commands_for(color, lines)
        if len(commands) != 8:
            raise RuntimeError(f"Expected eight signal commands for P{color}")
        reveal_x, reveal_y = v2_position_for_player(color, (x1 + x2 + 1) / 2, (y1 + y2 + 1) / 2)
        revealer = ctx.um.add_unit(player=color, unit_const=OtherInfo.MAP_REVEALER.ID,
                                   x=reveal_x, y=reveal_y)
        protect.new_effect.disable_unit_attackable(source_player=-1,
                                                   selected_object_ids=[revealer.reference_id])
        protect.new_effect.disable_object_deletion(source_player=-1,
                                                    selected_object_ids=[revealer.reference_id])
        for slot, (_name, item) in enumerate(commands):
            source_x = settings["post_x"] + (slot % 2) * settings["column_spacing"] + 0.5
            source_y = settings["post_y"] + (slot // 2) * settings["row_spacing"] + 0.5
            x, y = v2_position_for_player(color, source_x, source_y)
            post = ctx.um.add_unit(player=0, unit_const=BuildingInfo.OUTPOST.ID, x=x, y=y)
            reference = post.reference_id
            label = (f"HELP P{color}" if item["signal"] == "help" else
                     f"ATTACK P{item['target']}" if item["signal"] == "attack" else
                     f"P{item['target']} DON'T FEED")
            protect.new_effect.change_object_name(source_player=0, selected_object_ids=[reference],
                                                  message=f"{label} — P{color} TEAM SIGNAL")
            protect.new_effect.change_object_player_color(
                source_player=0, selected_object_ids=[reference],
                player_color=int(ColorId(item["target"] - 1)),
            )
            protect.new_effect.enable_object_selection(source_player=0, selected_object_ids=[reference])
            protect.new_effect.disable_unit_attackable(source_player=0, selected_object_ids=[reference])
            protect.new_effect.disable_object_deletion(source_player=0, selected_object_ids=[reference])
            function = f"ramSignalSelectP{color}E{item['event']}"
            wrappers.append(f"void {function}() {{ ramRequestSignal({color}, {item['event']}); }}")
            for owner in range(1, 9):
                press = ctx.tm.add_trigger(f"RAM Signal select — P{color} E{item['event']} W{owner}")
                release = ctx.tm.add_trigger(f"RAM Signal release — P{color} E{item['event']} W{owner}",
                                             enabled=0)
                press.new_condition.variable_value(variable=40 + color - 1, quantity=owner,
                                                    comparison=Comparison.EQUAL)
                press.new_condition.variable_value(variable=32 + color - 1, quantity=1,
                                                    comparison=Comparison.EQUAL)
                # The local-only Object Selected condition would desynchronize.
                press.new_condition.object_selected_multiplayer(unit_object=reference, source_player=owner)
                press.new_effect.script_call(message=function)
                press.new_effect.activate_trigger(trigger_id=release.trigger_id)
                release.new_condition.object_selected_multiplayer(unit_object=reference,
                                                                  source_player=owner, inverted=1)
                release.new_effect.activate_trigger(trigger_id=press.trigger_id)
        function = f"ramSignalDispatchP{color}"
        wrappers.append(f"bool {function}() {{ return(ramSignalCanDispatch({color})); }}")
        dispatch = ctx.tm.add_trigger(f"RAM Signal dispatch — P{color}", looping=1)
        dispatch.new_condition.timer(timer=1)
        dispatch.new_condition.script_call(xs_function=function)
        dispatch.new_effect.change_variable(variable=busy, quantity=1, operation=Operation.SET)
        dispatch.new_effect.modify_variable_by_variable(variable=delivery, variable2=queue_base + color - 1,
                                                        operation=Operation.SET)
        dispatch.new_effect.change_variable(variable=queue_base + color - 1,
                                             quantity=0, operation=Operation.SET)
        dispatch.new_effect.change_variable(variable=cursor, quantity=color, operation=Operation.SET)
        for recipient in range(1, 9):
            dispatch.new_effect.change_variable(variable=ack_base + recipient - 1,
                                                 quantity=0, operation=Operation.SET)
        dispatch.new_effect.activate_trigger(trigger_id=cooldown.trigger_id)

    protect.new_effect.change_object_description(
        source_player=0, object_list_unit_id=BuildingInfo.OUTPOST.ID,
        message=f"Select a post on your signal island to speak to your team. "
                f"Deselect/reselect to repeat. {settings['cooldown_seconds']}s cooldown per player.",
    )
    for name, item in lines.items():
        for recipient in audience_for(item):
            for owner in range(1, 9):
                playback = ctx.tm.add_trigger(
                    f"RAM Signal hear — E{item['event']} P{recipient} W{owner}", looping=1,
                )
                playback.new_condition.timer(timer=1)
                for variable, quantity in ((delivery, item["event"]), (ack_base + recipient - 1, 0),
                                           (121 + recipient - 1, 1), (40 + recipient - 1, owner)):
                    playback.new_condition.variable_value(variable=variable, quantity=quantity,
                                                          comparison=Comparison.EQUAL)
                playback.new_effect.play_sound(source_player=owner, global_sound=True, sound_name=name)
                playback.new_effect.send_chat(source_player=owner, message=f"[TEAM] {item['text']}")
                playback.new_effect.change_variable(variable=ack_base + recipient - 1,
                                                     quantity=1, operation=Operation.SET)

    source = substitute((ctx.mode_dir / "team_signals.xs").read_text(), {
        "COOLDOWN_SECONDS": settings["cooldown_seconds"], "QUEUE_BASE": queue_base,
        "VOICE_BUSY": busy, "CURSOR": cursor,
    })
    ctx.add_xs(source + "\n" + "\n".join(wrappers), label="RAM team-only map signals")
    ctx.message_manager.instructions += (
        "\nTEAM SIGNALS: Each player has an outer signal island with eight colored Outposts. "
        "Select HELP, ATTACK an enemy, or DON'T FEED for a teammate. Only your team receives "
        f"the voice and text. Deselect/reselect to repeat; "
        f"{settings['cooldown_seconds']}s personal cooldown. "
        "Commands are queued and holding a post selected does not repeat it."
    )
