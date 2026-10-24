"""Broadcast Backup speech through native triggers, independent of XS execution."""

import hashlib
import json
import math
import re
import tomllib
import wave

from AoE2ScenarioParser.datasets.trigger_lists import Comparison, Operation


def configure_backup_audio(ctx):
    settings = tomllib.loads((ctx.mode_dir / "mode.toml").read_text())["backup_audio"]
    if not settings["enabled"]:
        return
    if type(settings["queue_gap_seconds"]) is not int or settings["queue_gap_seconds"] < 0:
        raise ValueError("backup_audio.queue_gap_seconds must be a nonnegative integer")
    if type(settings["audio_game_time_scale"]) is not int or settings["audio_game_time_scale"] < 1:
        raise ValueError("backup_audio.audio_game_time_scale must be a positive integer")
    directory = ctx.mode_dir / "assets" / "audio"
    manifest = json.loads((directory / "manifest.json").read_text())
    base = max(v.variable_id for v in ctx.tm.variables) + 1
    existing = {v.name: v.variable_id for v in ctx.tm.variables}
    busy = existing.get("ramvoicebusy", base + 8)
    for color in range(1, 9):
        ctx.tm.add_variable(f"p{color}backupvoice", variable_id=base + color - 1)
        name = f"{settings['sound_prefix']}{color}{settings['sound_suffix']}"
        digest = hashlib.sha256((directory / f"{name}.wav").read_bytes()).hexdigest()
        if digest != manifest["clips"][f"{name}.wav"]["sha256"]:
            raise ValueError(f"Backup sound hash mismatch: {name}")
        with wave.open(str(directory / f"{name}.wav"), "rb") as audio:
            if (audio.getnchannels(), audio.getsampwidth(), audio.getframerate()) != (1, 2, 48000):
                raise ValueError(f"Backup sound {name} must be mono 48kHz 16-bit PCM")
            seconds = audio.getnframes() / audio.getframerate()
        if manifest["clips"][f"{name}.wav"]["color"] != color or not 1 < seconds < 10:
            raise ValueError(f"Invalid Backup clip metadata: {name}")
        claims = [t for t in ctx.tm.triggers if re.fullmatch(fr"King Island S{color} W[1-8]", t.name)]
        if len(claims) != 8:
            raise RuntimeError(f"Backup activation migration drift for P{color}")
        # Enqueue after the successful activation's native creation effects.
        # Every owner alias shares this color's one-use Backup state.
        for claim in claims:
            claim.new_effect.change_variable(
                variable=base + color - 1, quantity=1, operation=Operation.SET,
            )
        playback = ctx.tm.add_trigger(f"RAM Scorpion voice — P{color}", looping=0)
        playback.new_condition.variable_value(
            variable=base + color - 1, quantity=1, comparison=Comparison.EQUAL,
        )
        playback.new_condition.variable_value(variable=busy, quantity=0, comparison=Comparison.EQUAL)
        playback.new_effect.change_variable(variable=busy, quantity=1, operation=Operation.SET)
        for audience in range(1, 9):
            playback.new_effect.play_sound(source_player=audience, global_sound=True, sound_name=name)
            playback.new_effect.send_chat(
                source_player=audience, message=f"Player {color} called Scorpion backup!",
            )
        cooldown = ctx.tm.add_trigger(f"RAM Scorpion voice cooldown — P{color}", enabled=0)
        cooldown.new_condition.timer(
            timer=math.ceil(seconds * settings["audio_game_time_scale"]) + settings["queue_gap_seconds"],
        )
        cooldown.new_effect.change_variable(variable=busy, quantity=0, operation=Operation.SET)
        playback.new_effect.activate_trigger(trigger_id=cooldown.trigger_id)
        playback.new_effect.change_variable(
            variable=base + color - 1, quantity=3, operation=Operation.SET,
        )
    if "ramvoicebusy" not in existing:
        ctx.tm.add_variable("ramvoicebusy", variable_id=busy)
