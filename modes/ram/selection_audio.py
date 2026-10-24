"""Package source-owned selection voices and narrowly patch a pristine DE dataset.

genieutils is optional and imported only when DAT patching is requested. Every
asset needed for a subsequent build lives beside manifest.json under assets/;
generation paths within the manifest are archival provenance, never build inputs.
"""

from __future__ import annotations

import hashlib
import io
import json
import re
import wave
import zlib
from collections import Counter
from importlib.metadata import version
from pathlib import Path

ROLES = ("infantry", "archer", "cavalry", "leader")
SOUND_PATH = "resources/_common/drs/sounds"
ID_PATTERN = re.compile(r"[a-z0-9][a-z0-9_-]{0,63}\Z")
REQUIRED_LICENSES = {
    "HIGGS-LICENSE.txt", "ADAPTER-LICENSE.txt", "OMNIVOICE-LICENSE.txt",
    "OMNIVOICE-TOKENIZER-LICENSE.txt", "NATIVE_REFERENCE_ATTRIBUTION.txt",
    "VOXCPM-REFERENCE-CODE-LICENSE.txt",
}

# Native ObjectClass values. Keep noncombat objects and literal bow wording apart.
CLASS_ROLE = {
    0: "archer", 26: "archer", 44: "infantry", 23: "cavalry",
    6: "infantry", 28: "infantry", 45: "infantry", 46: "infantry",
    50: "infantry", 56: "infantry",
    12: "cavalry", 24: "cavalry", 36: "cavalry", 47: "cavalry", 57: "cavalry",
}
RAM_HERO_IDS = {168, 200, 424, 426, 432, 698, 731, 777}
RAM_CONTROL_IDS = {639}  # War Penguin is RAM's permanent noncombat controller.
BOW_PROJECTILE_IDS = {363, 364, 503, 507, 510, 511, 1971}
KING_IDS = {434}  # Other class59 objects include civilian merchants/carts/queens.


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _json_bytes(value: dict) -> bytes:
    return (json.dumps(value, indent=2, ensure_ascii=False) + "\n").encode("utf-8")


def _asset_path(directory: Path, relative: str) -> Path:
    if not isinstance(relative, str) or not relative or Path(relative).is_absolute():
        raise ValueError(f"Selection asset paths must be relative: {relative!r}")
    path = directory / relative
    if ".." in Path(relative).parts or not path.resolve().is_relative_to(directory.resolve()):
        raise ValueError(f"Selection asset escapes its source directory: {relative!r}")
    if path.is_symlink() or not path.is_file():
        raise ValueError(f"Missing regular selection asset: {relative!r}")
    return path


def civilization_catalog(manifest: dict) -> dict[int, dict]:
    """Require an explicit generated or stock decision for every catalog entry.

    This validates syntax without importing a DAT parser. The complete identity
    and coverage check is performed against the installed dataset when packaging.
    """
    entries = manifest.get("civilizations")
    if not isinstance(entries, list) or not entries:
        raise ValueError("Selection manifest requires a nonempty civilizations catalog")
    catalog = {}
    for row in entries:
        if not isinstance(row, dict):
            raise ValueError("Selection civilization catalog rows must be objects")
        civ_id, name = row.get("id"), row.get("name")
        if type(civ_id) is not int or civ_id <= 0 or civ_id in catalog:
            raise ValueError(f"Invalid or duplicate selection civilization id: {civ_id!r}")
        if not isinstance(name, str) or not name.strip() or name != name.strip():
            raise ValueError(f"Invalid selection civilization name: {civ_id}")
        profile = row.get("voice_profile")
        if not isinstance(profile, str) or not profile.strip():
            raise ValueError(f"Missing selection voice_profile for civilization: {civ_id}")
        mode = row.get("mode")
        if mode not in {"generated", "stock"}:
            raise ValueError(f"Invalid selection voice mode for civilization: {civ_id}/{mode!r}")
        if mode == "stock" and (not isinstance(row.get("reason"), str) or not row["reason"].strip()):
            raise ValueError(f"Stock selection fallback requires a reason: {civ_id}/{name}")
        catalog[civ_id] = dict(row)
    return dict(sorted(catalog.items()))


def validate_dataset_catalog(catalog: dict[int, dict], civilizations) -> None:
    """Match every non-Gaia installed DAT table, including newly added civs."""
    actual = {civ_id: civ.name for civ_id, civ in enumerate(civilizations) if civ_id > 0}
    missing, extra = actual.keys() - catalog.keys(), catalog.keys() - actual.keys()
    renamed = {civ_id: {"catalog": row["name"], "dataset": actual[civ_id]}
               for civ_id, row in catalog.items() if civ_id in actual and row["name"] != actual[civ_id]}
    if missing or extra or renamed:
        raise ValueError(
            "Selection civilization catalog does not match the installed dataset: "
            f"missing={sorted(missing)}, extra={sorted(extra)}, names={renamed}"
        )


def load_selection_assets(directory: Path) -> tuple[dict, list[dict], dict[str, bytes]]:
    """Validate catalog-driven source WAVs and full licenses, without a DAT parser."""
    manifest = json.loads((directory / "manifest.json").read_text(encoding="utf-8"))
    if not isinstance(manifest, dict) or manifest.get("schema_version") != 1:
        raise ValueError("RAM selection audio requires manifest schema_version 1")
    if manifest.get("fixture") or not isinstance(manifest.get("clips"), list):
        raise ValueError("RAM selection audio must contain actual source clips, not test fixtures")
    catalog = civilization_catalog(manifest)
    generated = {civ_id for civ_id, row in catalog.items() if row["mode"] == "generated"}
    clips, seen_ids, seen_pairs = [], set(), set()
    for item in manifest["clips"]:
        if not isinstance(item, dict):
            raise ValueError("Each selection clip must be an object")
        clip_id, civ_id, role = item.get("id"), item.get("civilization_id"), item.get("role")
        if not isinstance(clip_id, str) or not ID_PATTERN.fullmatch(clip_id) or clip_id in seen_ids:
            raise ValueError(f"Invalid or duplicate selection clip id: {clip_id!r}")
        if type(civ_id) is not int or civ_id not in generated or role not in ROLES:
            raise ValueError(f"Unsupported selection civilization/role: {civ_id!r}/{role!r}")
        if "voice_profile" in item and item["voice_profile"] != catalog[civ_id]["voice_profile"]:
            raise ValueError(f"Selection clip voice_profile differs from its civilization catalog: {clip_id}")
        if (civ_id, role) in seen_pairs or not isinstance(item.get("text"), str) or not item["text"].strip():
            raise ValueError(f"Duplicate civilization/role or missing spoken text: {clip_id}")
        source = _asset_path(directory, item.get("file"))
        data = source.read_bytes()
        if source.suffix.lower() != ".wav" or item.get("sha256") != _sha256(data):
            raise ValueError(f"Selection WAV SHA-256 mismatch or wrong extension: {clip_id}")
        try:
            with wave.open(io.BytesIO(data), "rb") as audio:
                params = audio.getnchannels(), audio.getsampwidth(), audio.getframerate(), audio.getcomptype()
                if params != (1, 2, 48000, "NONE"):
                    raise ValueError(f"Selection WAV must be mono 48 kHz PCM16: {clip_id}")
                frames = audio.getnframes()
                duration = frames / 48000
                pcm = audio.readframes(frames)
                if not 0.15 <= duration <= 12 or len(pcm) != frames * 2 or not any(pcm):
                    raise ValueError(f"Silent, truncated, or unreasonable selection WAV: {clip_id}")
        except (wave.Error, EOFError) as exc:
            raise ValueError(f"Invalid selection WAV: {clip_id}") from exc
        clips.append({**item, "duration_seconds": duration,
                      "filename": f"ram_select_{clip_id}_v1", "data": data})
        seen_ids.add(clip_id)
        seen_pairs.add((civ_id, role))
    expected = {(civ, role) for civ in generated for role in ROLES}
    if seen_pairs != expected:
        raise ValueError(
            f"Exactly {len(expected)} catalog-generated selection clips required; "
            f"missing: {sorted(expected - seen_pairs)}"
        )

    licenses = {}
    for item in manifest.get("license_files", []):
        if not isinstance(item, dict):
            raise ValueError("Selection license entries must be objects")
        name = item.get("name")
        if not isinstance(name, str) or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]{0,127}", name):
            raise ValueError(f"Unsafe selection license basename: {name!r}")
        if name in licenses:
            raise ValueError(f"Duplicate selection license basename: {name}")
        content = _asset_path(directory, item.get("file")).read_bytes()
        if not content.strip() or item.get("sha256") != _sha256(content):
            raise ValueError(f"Missing or changed selection license text: {name}")
        content.decode("utf-8")
        licenses[name] = content
    if not REQUIRED_LICENSES <= licenses.keys():
        missing = sorted(REQUIRED_LICENSES - licenses.keys())
        raise ValueError(f"Missing full selection license files: {missing}")
    clips.sort(key=lambda clip: (clip["civilization_id"], ROLES.index(clip["role"])))
    return manifest, clips, licenses


def role_for(unit_id: int, unit) -> str | None:
    """Choose a spoken role while leaving civilians, siege, ships, and controllers stock."""
    if unit_id in RAM_CONTROL_IDS or unit is None or int(unit.type) != 70:
        return None
    if unit_id in KING_IDS:
        return "leader"
    if unit.class_ not in CLASS_ROLE and unit.class_ != 25:
        return None
    if unit_id in RAM_HERO_IDS or unit.class_ == 25 or (
        unit.creatable is not None and unit.creatable.hero_mode & 1
    ):
        return "leader"
    if unit.class_ == 0 and (
        unit.type_50 is None or unit.type_50.projectile_unit_id not in BOW_PROJECTILE_IDS
    ):
        return "infantry"
    return CLASS_ROLE.get(unit.class_)


def _apply_selection_bindings(civilizations, catalog: dict[int, dict], groups: dict) -> list[dict]:
    """Patch only explicitly generated tables; stock decisions never reach a unit."""
    changes = []
    for civ_id, row in catalog.items():
        if row["mode"] != "generated":
            continue
        for unit_id, unit in enumerate(civilizations[civ_id].units):
            role = role_for(unit_id, unit)
            if role is None:
                continue
            new = groups[(civ_id, role)]
            changes.append({
                "civilization_id": civ_id, "unit_id": unit_id, "unit_name": unit.name,
                "class": unit.class_, "role": role, "selection_sound_before": unit.selection_sound,
                "selection_sound_after": new, "wwise_selection_sound_id": unit.wwise_selection_sound_id,
                "run_pattern": unit.bird.run_pattern if unit.bird else None,
            })
            unit.selection_sound = new
    return changes


def package_selection_audio(dataset: Path, assets: Path) -> tuple[bytes, dict[str, bytes], dict]:
    """Return patched DAT bytes, extra package files, and the complete mutation proof.

    Only generated-civilization selection_sound fields and appended Sound groups
    may differ. Explicit stock tables and the installed source DAT stay unchanged.
    """
    try:
        from genieutils.common import ByteHandler
        from genieutils.datfile import DatFile
        from genieutils.sound import Sound, SoundItem
    except ImportError as exc:
        raise RuntimeError(
            "RAM selection voices require genieutils-py==0.1.2. "
            "Install the optional build dependency with: pip install -e '.[ram-data]'"
        ) from exc
    parser_version = version("genieutils-py")
    if parser_version != "0.1.2":
        raise RuntimeError(f"RAM selection DAT patching requires genieutils-py==0.1.2, got {parser_version}")
    manifest, clips, licenses = load_selection_assets(assets)
    catalog = civilization_catalog(manifest)
    generated = {civ_id: row for civ_id, row in catalog.items() if row["mode"] == "generated"}
    original_compressed = dataset.read_bytes()
    original_raw = zlib.decompress(original_compressed, wbits=-15)
    data = DatFile.parse(dataset)
    baseline = data.to_bytes()
    if baseline != original_raw:
        raise ValueError("DAT parser does not preserve all pristine bytes; refusing selection patch")
    validate_dataset_catalog(catalog, data.civs)
    sound_count = len(data.sounds)
    if sound_count + len(clips) > 32767:
        raise ValueError("Selection sound ids would exceed the signed 16-bit native field")

    new_groups, appended = {}, []
    for clip in clips:
        group_id = len(data.sounds)
        data.sounds.append(Sound(
            id=group_id, play_delay=0, cache_time=300000, total_probability=100,
            items=[SoundItem(filename=clip["filename"] + ".wav", resource_id=-1,
                             probability=100, civilization=-1, icon_set=-1)],
        ))
        new_groups[(clip["civilization_id"], clip["role"])] = group_id
        appended.append({"sound_id": group_id, "clip_id": clip["id"],
                         "civilization_id": clip["civilization_id"], "role": clip["role"],
                         "filename": clip["filename"] + ".wav"})
    changes = _apply_selection_bindings(data.civs, catalog, new_groups)
    by_unit = {(row["civilization_id"], row["unit_id"]): row for row in changes}
    for key, expected_role in {
        (8, 239): "cavalry", (10, 46): "infantry", (14, 771): "cavalry",
        (28, 1122): "cavalry", (35, 1236): "cavalry",
    }.items():
        if key[0] not in generated:
            continue
        if key not in by_unit or by_unit[key]["role"] != expected_role:
            raise ValueError(f"RAM wave selection voice is missing or misclassified: {key}")
    for civ_id in generated:
        for unit_id, expected_role in {
            731: "leader", 4: "archer", 24: "archer", 492: "archer", 6: "infantry",
            7: "infantry", 185: "infantry", 5: "infantry", 46: "infantry",
            771: "cavalry", 1126: "cavalry", 434: "leader",
        }.items():
            if (civ_id, unit_id) not in by_unit or by_unit[(civ_id, unit_id)]["role"] != expected_role:
                raise ValueError(f"Selection wording does not match unit type: {civ_id}/{unit_id}")

    patched = data.to_bytes()
    # Revert only permitted fields/groups. Complete raw-byte equality proves all
    # other civs, original sounds, stats, Wwise IDs, and RUN_PATTERN stay untouched.
    for row in changes:
        unit = data.civs[row["civilization_id"]].units[row["unit_id"]]
        unit.selection_sound = row["selection_sound_before"]
    del data.sounds[sound_count:]
    if data.to_bytes() != baseline:
        raise ValueError("Unexpected DAT mutation outside authorized selection fields/groups")
    reloaded = DatFile.from_bytes(ByteHandler(memoryview(patched)))
    if reloaded.to_bytes() != patched or len(reloaded.sounds) != sound_count + len(clips):
        raise ValueError("Selection-patched DAT is not stable after reload")
    for row in changes:
        unit = reloaded.civs[row["civilization_id"]].units[row["unit_id"]]
        if (unit.selection_sound != row["selection_sound_after"]
                or unit.wwise_selection_sound_id != row["wwise_selection_sound_id"]
                or (unit.bird.run_pattern if unit.bird else None) != row["run_pattern"]):
            raise ValueError("Reload changed selection binding, Wwise fallback, or double-click group")
    compressed = zlib.compress(patched, level=-1, wbits=-15) if clips else original_compressed
    if dataset.read_bytes() != original_compressed:
        raise ValueError("Source DAT changed while selection voices were being packaged")

    counts = Counter((row["civilization_id"], row["role"]) for row in changes)
    coverage = [
        {**row, "clip_count": sum(clip["civilization_id"] == civ_id for clip in clips),
         "changed_unit_rows": sum(count for (color, _role), count in counts.items() if color == civ_id)}
        for civ_id, row in catalog.items()
    ]
    report = {
        "source_dataset_sha256": _sha256(original_compressed),
        "output_dataset_sha256": _sha256(compressed),
        "source_audio_manifest_sha256": _sha256((assets / "manifest.json").read_bytes()),
        "parser": {"package": "genieutils-py", "version": parser_version},
        "dataset_version": str(data.version), "civilizations": len(data.civs),
        "sounds_before": sound_count, "sounds_after": sound_count + len(clips),
        "changed_unit_rows": len(changes),
        "civilization_coverage": coverage,
        "coverage_summary": {"installed_non_gaia": len(data.civs) - 1,
                             "catalogued": len(catalog), "generated": len(generated),
                             "stock": len(catalog) - len(generated)},
        "counts": [{"civilization_id": civ, "civilization": catalog[civ]["name"],
                    "role": role, "units": count}
                   for (civ, role), count in sorted(counts.items())],
        "proof": {
            "baseline_uncompressed_byte_equal": True, "authorized_field_restore_equals_baseline": True,
            "modified_roundtrip_stable": True, "wwise_fallbacks_unchanged": True,
            "run_patterns_unchanged": True, "uncovered_civs_units_and_original_sounds_unchanged": True,
            "new_sound_groups": len(clips), "native_gameplay_playback_verified": False,
        },
        "limitations": [
            "Fresh-match selection playback and second-client delivery still need live acceptance.",
            "Native pronunciation, perceived gender, and historical style need listening review.",
            "Selection voices require the patched Data Mod; resource-only audio does not bind them.",
            "Genghis type731 shares leader audio while RUN_PATTERN retains scenario selection grouping.",
        ],
        "license_files": [{"name": name, "sha256": _sha256(content), "bytes": len(content)}
                          for name, content in sorted(licenses.items())],
        "appended_sound_groups": appended, "changes": changes,
    }
    files = {}
    for clip in clips:
        for extension in (".wav", ".wem"):
            files[f"{SOUND_PATH}/{clip['filename']}{extension}"] = clip["data"]
    public_manifest = {**manifest, "clips": [
        {key: value for key, value in clip.items() if key != "data"} for clip in clips
    ]}
    files["RAM_SELECTION_VOICE_MANIFEST.json"] = _json_bytes(public_manifest)
    files["RAM_SELECTION_VOICE_LICENSES.txt"] = (assets / "LICENSES.txt").read_bytes()
    files["RAM_SELECTION_VOICE_README.txt"] = (assets / "README.txt").read_bytes()
    files["RAM_SELECTION_VOICE_REPORT.json"] = _json_bytes(report)
    for name, content in licenses.items():
        files[f"RAM_SELECTION_LICENSES/{name}"] = content
    return compressed, files, report
