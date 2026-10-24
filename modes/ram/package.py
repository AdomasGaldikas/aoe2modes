"""Build a RAM mixed-content mod directory and an upload ZIP from the installed dataset.

Run with the project's Python: python modes/ram/package.py --game-dir /path/to/AoE2DE
"""

from __future__ import annotations

import argparse
import hashlib
import io
import json
import math
import shutil
import struct
import tomllib
import wave
import zipfile
from pathlib import Path

from aoe2modes.builder import build_mode
from aoe2modes.config import load_mode_spec
from aoe2modes.paths import paths

if __package__:
    from .civilization_leaders import leaders_enabled, package_civilization_leaders
    from .selection_audio import package_selection_audio
else:  # Support the documented python modes/ram/package.py entry point.
    from civilization_leaders import leaders_enabled, package_civilization_leaders
    from selection_audio import package_selection_audio


def startup_audio(settings: dict) -> bytes:
    """Original, deterministic mono PCM chime; no borrowed audio assets."""
    sample_rate = settings["sound_sample_rate"]
    note_samples = round(settings["sound_note_seconds"] * sample_rate)
    gap_samples = round(settings["sound_gap_seconds"] * sample_rate)
    samples = bytearray()
    for frequency in settings["sound_frequencies"]:
        for index in range(note_samples):
            # Smooth attack/release keeps the marker quiet and avoids clicks.
            envelope = math.sin(math.pi * index / (note_samples - 1)) ** 2
            value = round(32767 * settings["sound_amplitude"] * envelope
                          * math.sin(2 * math.pi * frequency * index / sample_rate))
            samples.extend(struct.pack("<h", value))
        samples.extend(b"\x00\x00" * gap_samples)
    output = io.BytesIO()
    with wave.open(output, "wb") as audio:
        audio.setnchannels(1)
        audio.setsampwidth(2)
        audio.setframerate(sample_rate)
        audio.writeframes(samples)
    return output.getvalue()


def package_mod(scenario: Path, dataset: Path, output: Path, mode_dir: Path) -> tuple[Path, Path, dict]:
    """Package explicit files only; never alter the installed game dataset."""
    spec = load_mode_spec(mode_dir)
    with (mode_dir / "mode.toml").open("rb") as handle:
        config = tomllib.load(handle)
    settings = config["ram_mod"]
    if not scenario.is_file() or not dataset.is_file():
        raise FileNotFoundError("A built RAM scenario and the installed empires2_x2_p1.dat are required")
    folder = output / f"RAM-v{spec.version}"
    dataset_bytes = dataset.read_bytes()
    selection_files, selection_report = {}, None
    if config.get("selection_audio", {}).get("enabled", False):
        dataset_bytes, selection_files, selection_report = package_selection_audio(
            dataset, mode_dir / "assets" / "selection_audio",
        )
    leader_files, leader_report = {}, None
    if leaders_enabled(mode_dir):
        dataset_bytes, leader_files, leader_report = package_civilization_leaders(dataset_bytes, mode_dir)
    files = {
        "info.json": (json.dumps({
            "Author": ", ".join(spec.authors),
            "Title": f"{settings['title']} v{spec.version}",
            "Description": (
                "A 4v4 arena battle with center bonuses, reinforcements, "
                "custom voice announcements and private team signals."
            ),
        }, indent=2) + "\n").encode(),
        f"resources/_common/scenario/{spec.output_name}": scenario.read_bytes(),
        "resources/_common/dat/empires2_x2_p1.dat": dataset_bytes,
        f"resources/_common/drs/sounds/{settings['sound_name']}.wav": startup_audio(settings),
    }
    audio = config["backup_audio"]
    if audio["enabled"]:
        source = mode_dir / "assets" / "audio"
        for color in range(1, 9):
            name = f"{audio['sound_prefix']}{color}{audio['sound_suffix']}.wav"
            files[f"resources/_common/drs/sounds/{name}"] = (source / name).read_bytes()
        files["RAM_AUDIO_LICENSES.txt"] = (source / "LICENSES.txt").read_bytes()
        files["RAM_AUDIO_MANIFEST.json"] = (source / "manifest.json").read_bytes()
    if config["team_signals"]["enabled"]:
        source = mode_dir / "assets" / "audio"
        metadata = json.loads((source / "manifest.json").read_text())
        for name, item in metadata["clips"].items():
            if item.get("kind") == "team_signal":
                files[f"resources/_common/drs/sounds/{name}"] = (source / name).read_bytes()
        files["RAM_AUDIO_LICENSES.txt"] = (source / "LICENSES.txt").read_bytes()
        files["RAM_AUDIO_MANIFEST.json"] = (source / "manifest.json").read_bytes()
    if config["center"]["enabled"] and config["center_audio"]["enabled"]:
        source = mode_dir / "assets" / "audio"
        metadata = json.loads((source / "manifest.json").read_text())
        for name, item in metadata["clips"].items():
            if item.get("kind", "").startswith("center_"):
                files[f"resources/_common/drs/sounds/{name}"] = (source / name).read_bytes()
        files["RAM_AUDIO_LICENSES.txt"] = (source / "LICENSES.txt").read_bytes()
        files["RAM_AUDIO_MANIFEST.json"] = (source / "manifest.json").read_bytes()
    if files.keys() & selection_files.keys():
        raise ValueError("Selection audio package filenames collide with existing RAM files")
    files.update(selection_files)
    if files.keys() & leader_files.keys():
        raise ValueError("Leader package filenames collide with existing RAM files")
    files.update(leader_files)
    # DE 185872 accepts PCM WAV data with a .wem extension and prefers that
    # extension during sound lookup. Ship both names for native speech effects.
    for name, data in list(files.items()):
        if name.endswith(".wav") and not name.endswith(f"/{settings['sound_name']}.wav"):
            files[name[:-4] + ".wem"] = data
    for name, data in files.items():
        destination = folder / name
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(data)
    archive = output / f"RAM-v{spec.version}-mixed-content.zip"
    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED) as bundle:
        for name, data in sorted(files.items()):
            entry = zipfile.ZipInfo(name, date_time=(2026, 10, 17, 0, 0, 0))
            entry.compress_type = zipfile.ZIP_DEFLATED
            entry.external_attr = 0o100644 << 16
            bundle.writestr(entry, data)
    manifest = {
        "mode": spec.id, "version": spec.version, "base_mode": "normal RA v1.9",
        "dataset": (
            "Installed game dataset with native selection voices and one new civilization-specific "
            "starting-leader definition per civilization. Both patch stages prove all previous "
            "definitions unchanged outside their explicit changes. Rebuild after a game update."
            if leader_report is not None else
            "Installed game dataset with native selection-sound bindings and "
            f"{selection_report['proof']['new_sound_groups']} appended Sound groups; "
            "all other raw DAT bytes proven unchanged. Rebuild after a game data update."
            if selection_report is not None else
            "Unmodified copy of the installed game dataset; rebuild after a game data update."
        ),
        "files": {name: {"bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}
                  for name, data in sorted(files.items())},
        "archive_sha256": hashlib.sha256(archive.read_bytes()).hexdigest(),
    }
    if selection_report is not None:
        manifest["selection_audio"] = {
            "source_dataset_sha256": selection_report["source_dataset_sha256"],
            "output_dataset_sha256": selection_report["output_dataset_sha256"],
            "changed_unit_rows": selection_report["changed_unit_rows"],
            "proof": selection_report["proof"],
            "coverage_summary": selection_report["coverage_summary"],
        }
    if leader_report is not None:
        manifest["civilization_leaders"] = leader_report
    manifest["civilization_balance"] = config.get("civilization_balance", {})
    (output / f"RAM-v{spec.version}-manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    return folder, archive, manifest


def package_resource_mod(mixed_folder: Path, output: Path, mode_dir: Path) -> tuple[Path, Path]:
    """Carry the same scenario and voices as an enabled resource mod, without a dataset."""
    if leaders_enabled(mode_dir):
        raise ValueError("Civilization-specific starting leaders require the matching Data Mod")
    spec = load_mode_spec(mode_dir)
    output.mkdir(parents=True, exist_ok=True)
    folder = output / f"RAM-Sounds-v{spec.version}"
    files = {path.relative_to(mixed_folder).as_posix(): path.read_bytes()
             for path in mixed_folder.rglob("*") if path.is_file() and path.suffix != ".dat"}
    info = json.loads(files["info.json"])
    info["Title"] = f"RAM Scenario and Sounds v{spec.version}"
    info["Description"] = (
        "Enable this resource mod and restart DE. Select the RAM custom scenario with Definitive Set. "
        "Includes all playful announcer lines and the scenario; every player needs the sound assets."
    )
    if "RAM_SELECTION_VOICE_MANIFEST.json" in files:
        info["Description"] += (
            " Native unit-selection replies require the matching RAM Data Mod; "
            "this resource-only package carries their audio but cannot bind units to it."
        )
    files["info.json"] = (json.dumps(info, indent=2) + "\n").encode()
    archive = output / f"RAM-Sounds-v{spec.version}.zip"
    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED) as bundle:
        for name, data in sorted(files.items()):
            path = folder / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
            entry = zipfile.ZipInfo(name, date_time=(2026, 10, 17, 0, 0, 0))
            entry.compress_type = zipfile.ZIP_DEFLATED
            entry.external_attr = 0o100644 << 16
            bundle.writestr(entry, data)
    return folder, archive


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--game-dir", type=Path, required=True, help="Installed AoE2DE directory")
    parser.add_argument("--out", type=Path, default=paths().dist / "ram-mod")
    parser.add_argument("--install-local", type=Path, help="Explicit mods/local parent; game must be closed")
    args = parser.parse_args()
    mode_dir = Path(__file__).resolve().parent
    dataset = args.game_dir / "resources/_common/dat/empires2_x2_p1.dat"
    if not dataset.is_file():
        parser.error(f"Installed dataset not found: {dataset}")
    result = build_mode(load_mode_spec(mode_dir))
    folder, archive, manifest = package_mod(result.output, dataset, args.out, mode_dir)
    resource_archive = None
    if not leaders_enabled(mode_dir):
        _, resource_archive = package_resource_mod(folder, args.out, mode_dir)
    if args.install_local:
        # A new versioned folder avoids overwriting existing mods or releases.
        destination = args.install_local / folder.name
        shutil.copytree(folder, destination)
        print(f"Installed local mod: {destination}")
    print(f"Mod directory: {folder}\nUpload ZIP: {archive}\nSHA-256: {manifest['archive_sha256']}")
    if resource_archive is not None:
        print(f"Scenario and sounds resource mod: {resource_archive}")


if __name__ == "__main__":
    main()
