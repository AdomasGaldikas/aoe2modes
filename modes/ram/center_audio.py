"""Native center announcer queue, sharing the Backup channel to prevent overlap."""

import hashlib
import json
import math
import re
import tomllib
import wave

from AoE2ScenarioParser.datasets.trigger_lists import Comparison, Operation

from .voice_lines import center_lines

# Center's existing pending kill amounts end at 187. Allocate audio before Backup,
# which discovers the next free ids and reuses the declared shared busy flag.
VOICE_BUSY = 188
PERSONAL_BASE = 189
WAVE_BASE = 197
STATUS = 205
STATUS_BUSY = 206


def declare_center_audio(ctx):
    settings = tomllib.loads((ctx.mode_dir / "mode.toml").read_text())["center_audio"]
    if not settings["enabled"]:
        return {"CENTER_AUDIO_ENABLED": 0, "CENTER_WAVE_VOICE_BASE": -1, "CENTER_STATUS_VOICE": -1}
    if max(v.variable_id for v in ctx.tm.variables) != 187:
        raise RuntimeError("RAM center audio must follow pending kill allocation")
    for name, identifier in (("ramvoicebusy", VOICE_BUSY), ("ramcentervoicestatus", STATUS),
                             ("ramcenterstatusbusy", STATUS_BUSY)):
        ctx.tm.add_variable(name, variable_id=identifier)
    for base, suffix in ((PERSONAL_BASE, "centervoice"), (WAVE_BASE, "centerwavevoice")):
        for player in range(1, 9):
            ctx.tm.add_variable(f"p{player}{suffix}", variable_id=base + player - 1)
    return {"CENTER_AUDIO_ENABLED": 1, "CENTER_WAVE_VOICE_BASE": WAVE_BASE, "CENTER_STATUS_VOICE": STATUS}


def configure_center_audio(ctx):
    config = tomllib.loads((ctx.mode_dir / "mode.toml").read_text())
    settings = config["center_audio"]
    if not settings["enabled"] or not config["center"]["enabled"]:
        return
    if config["center"]["credit_cap"] > 25:
        raise ValueError("The bundled center voice covers awards up to 25 kills")
    for option in ("queue_gap_seconds", "status_cooldown_seconds", "audio_game_time_scale"):
        if type(settings[option]) is not int or settings[option] < 1:
            raise ValueError(f"center_audio.{option} must be a positive integer")
    lines = center_lines()
    directory = ctx.mode_dir / "assets/audio"
    manifest = json.loads((directory / "manifest.json").read_text())
    longest = 0
    for name, metadata in lines.items():
        path = directory / f"{name}.wav"
        item = manifest["clips"][path.name]
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        if item["text"] != metadata["text"] or digest != item["sha256"]:
            raise ValueError(f"Center voice mismatch: {name}")
        with wave.open(str(path), "rb") as audio:
            if (audio.getnchannels(), audio.getsampwidth(), audio.getframerate()) != (1, 2, 48000):
                raise ValueError(f"Invalid center PCM format: {name}")
            seconds = audio.getnframes() / audio.getframerate()
        if not 0.5 < seconds < 8:
            raise ValueError(f"Invalid center clip duration: {name}")
        longest = max(longest, seconds)
    cooldown = ctx.tm.add_trigger("RAM Center voice cooldown", enabled=0)
    cooldown.new_condition.timer(
        timer=math.ceil(longest * settings["audio_game_time_scale"]) + settings["queue_gap_seconds"],
    )
    cooldown.new_effect.change_variable(variable=VOICE_BUSY, quantity=0, operation=Operation.SET)
    status_cooldown = ctx.tm.add_trigger("RAM Center status cooldown", enabled=0)
    status_cooldown.new_condition.timer(timer=settings["status_cooldown_seconds"])
    status_cooldown.new_effect.change_variable(variable=STATUS_BUSY, quantity=0, operation=Operation.SET)

    # Queue the exact awarded amount after the kill effect, before acknowledgement.
    for trigger in ctx.tm.triggers:
        match = re.fullmatch(r"RAM Center kills — P([1-8]) W([1-8])", trigger.name)
        if match is None:
            continue
        color, owner = map(int, match.groups())
        clear = trigger.effects.pop(-1)
        trigger.new_effect.modify_variable_by_variable(
            variable=PERSONAL_BASE + owner - 1, variable2=180 + color - 1, operation=Operation.SET,
        )
        trigger.effects.append(clear)
        trigger.effect_order = list(range(len(trigger.effects)))
    # A wave notice waits for the personal queue; a simultaneous kill payout wins.
    for color in range(1, 9):
        for owner in range(1, 9):
            request = ctx.tm.add_trigger(f"RAM Center wave notice — P{color} W{owner}", looping=1)
            request.new_condition.timer(timer=1)
            for variable, quantity in ((40 + color - 1, owner), (WAVE_BASE + color - 1, 1),
                                       (PERSONAL_BASE + owner - 1, 0)):
                request.new_condition.variable_value(variable=variable, quantity=quantity,
                                                     comparison=Comparison.EQUAL)
            request.new_effect.change_variable(variable=PERSONAL_BASE + owner - 1, quantity=26,
                                               operation=Operation.SET)
            request.new_effect.change_variable(variable=WAVE_BASE + color - 1, quantity=0,
                                               operation=Operation.SET)

    for name, metadata in lines.items():
        status = metadata["kind"] == "center_status"
        audiences = (0,) if status else range(1, 9)
        code = metadata["state"] if status else metadata.get("amount", 26)
        for owner in audiences:
            playback = ctx.tm.add_trigger(f"RAM Center voice — {name} W{owner}", looping=1)
            queued = STATUS if status else PERSONAL_BASE + owner - 1
            playback.new_condition.variable_value(variable=queued, quantity=code, comparison=Comparison.EQUAL)
            playback.new_condition.variable_value(variable=VOICE_BUSY, quantity=0,
                                                   comparison=Comparison.EQUAL)
            if status:
                playback.new_condition.variable_value(variable=STATUS_BUSY, quantity=0,
                                                       comparison=Comparison.EQUAL)
                playback.new_effect.change_variable(variable=STATUS_BUSY, quantity=1, operation=Operation.SET)
                playback.new_effect.activate_trigger(trigger_id=status_cooldown.trigger_id)
            playback.new_condition.timer(timer=1)
            playback.new_effect.change_variable(variable=VOICE_BUSY, quantity=1, operation=Operation.SET)
            for audience in range(1, 9) if status else (owner,):
                playback.new_effect.play_sound(source_player=audience, global_sound=True, sound_name=name)
                if status or code == 26:
                    playback.new_effect.send_chat(source_player=audience, message=metadata["text"])
            playback.new_effect.change_variable(variable=queued, quantity=0, operation=Operation.SET)
            playback.new_effect.activate_trigger(trigger_id=cooldown.trigger_id)
