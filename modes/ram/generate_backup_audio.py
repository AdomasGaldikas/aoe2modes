"""Regenerate RAM's original, playful announcer using Piper and an explicit model.

Requires piper-tts==1.3.0 and ffmpeg with rubberband. No model is downloaded here.
Example: /tmp/ram-voice-env/bin/python modes/ram/generate_backup_audio.py \
    --model /tmp/ram-voice-model/en_US-joe-medium.onnx
"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import tempfile
import wave
from pathlib import Path

from voice_lines import center_lines, signal_lines


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", type=Path, required=True)
    parser.add_argument("--events", choices=("all", "backup", "center", "signals"), default="all")
    parser.add_argument("--clip", action="append", help="Generate only this event name; repeat as needed")
    parser.add_argument("--output", type=Path, help="Staging directory for generated assets")
    args = parser.parse_args()
    # Generation dependencies are optional; normal builds only copy finished PCM.
    import onnxruntime
    from piper import PiperVoice, SynthesisConfig

    onnxruntime.disable_telemetry_events()
    voice = PiperVoice.load(args.model)
    config = SynthesisConfig(length_scale=0.90, noise_scale=0.0, noise_w_scale=0.0)
    output = args.output or Path(__file__).parent / "assets" / "audio"
    output.mkdir(parents=True, exist_ok=True)
    filters = (
        "rubberband=pitch=1.15,highpass=f=100,equalizer=f=2800:t=q:w=0.7:g=2,"
        "loudnorm=I=-18:TP=-2:LRA=7,afade=t=in:st=0:d=0.015,apad=pad_dur=0.15,aresample=48000"
    )
    manifest_path = output / "manifest.json"
    clips = json.loads(manifest_path.read_text())["clips"] if manifest_path.exists() else {}
    lines = {}
    if args.events in {"all", "backup"}:
        for color, word in enumerate(("one", "two", "three", "four", "five", "six", "seven", "eight"), 1):
            text = f"Player {word} called Scorpion backup!"
            # Keep a small pause between the player number and the action.
            if color == 7:
                text = "Player seven, called Scorpion backup!"
            lines[f"ram_scorpion_p{color}_v3"] = {"kind": "backup", "color": color, "text": text}
    if args.events in {"all", "center"}:
        lines.update(center_lines())
    if args.events in {"all", "signals"}:
        lines.update(signal_lines())
    if args.clip:
        lines = {name: lines[name] for name in args.clip}
    with tempfile.TemporaryDirectory(prefix="ram-backup-voice-") as temporary:
        for name, metadata in lines.items():
            raw = Path(temporary) / f"{name}.wav"
            with wave.open(str(raw), "wb") as handle:
                voice.synthesize_wav(metadata["text"], handle, syn_config=config)
            destination = output / f"{name}.wav"
            subprocess.run([
                "ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", str(raw),
                "-af", filters, "-ar", "48000", "-ac", "1", "-c:a", "pcm_s16le", str(destination),
            ], check=True)
            # Match the canonical PCM container of RAM's working startup chime.
            with wave.open(str(destination), "rb") as handle:
                params = handle.getparams()
                frames = handle.readframes(handle.getnframes())
            with wave.open(str(destination), "wb") as handle:
                handle.setparams(params)
                handle.writeframes(frames)
            data = destination.read_bytes()
            with wave.open(str(destination), "rb") as handle:
                duration = handle.getnframes() / handle.getframerate()
            clips[destination.name] = {
                **metadata, "seconds": duration,
                "sha256": hashlib.sha256(data).hexdigest(),
                "pcm_sha256": hashlib.sha256(frames).hexdigest(),
            }
    manifest = {
        "wav_container": "Canonical RIFF PCM with fmt and data chunks only; no LIST metadata",
        "engine": "Piper 1.3.0 (GPL-3.0); generation tool only, not shipped with the mod",
        "voice": "en_US-joe-medium",
        "style": "Original playful game-show announcer; brighter pitch and brisk delivery",
        "model_card": "https://huggingface.co/rhasspy/piper-voices/blob/main/en/en_US/joe/medium/MODEL_CARD",
        "dataset_license": "CC0, as stated in the model card",
        "model_sha256": hashlib.sha256(args.model.read_bytes()).hexdigest(),
        "model_config_sha256": hashlib.sha256(Path(str(args.model) + ".json").read_bytes()).hexdigest(),
        "synthesis": {"length_scale": 0.90, "noise_scale": 0, "noise_w_scale": 0},
        "ffmpeg_filters": filters, "clips": clips,
    }
    (output / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(f"Generated {len(lines)} clips; {len(clips)} total in {output}")


if __name__ == "__main__":
    main()
