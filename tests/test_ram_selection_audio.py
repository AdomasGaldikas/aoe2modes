"""Dynamic civilization coverage plus the original reviewed voice-byte contract."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import shutil
from pathlib import Path
from types import SimpleNamespace

import pytest

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "modes/ram/assets/selection_audio"
# These hashes deliberately freeze the reviewed build inputs independently of
# their editable manifest. Replacement recordings must update this contract.
EXPECTED_CLIPS = {
    "khmer-archer": (
        "ធ្នូរួចរាល់ហើយ លោកមេបញ្ជាការ!",
        "55ac8e2440802f97384e4c0327fbe9f5e25b14b2ce328d8cec366c73212916f5",
    ),
    "khmer-cavalry": (
        "ត្រៀមរួចហើយ លោកមេបញ្ជាការ!",
        "1223ff6fb9f058341f8526210beaa03594aa89d778a3b18b5c0aa7a59af12f68",
    ),
    "khmer-infantry": (
        "បាទ លោកមេបញ្ជាការ!",
        "0531e4d30783a157c77e3b66b60a6bd5bcf0e442d4b927dd01c0900e6484db6b",
    ),
    "khmer-leader": (
        "តាមព្រះរាជបញ្ជា ព្រះករុណា!",
        "8d8460e88be25af66e5f7957d29263eb11b91fa90b292bcab3a02bf1148a840c",
    ),
    "lithuanian-archer": (
        "Lankas paruoštas, vade!",
        "db8fbea3c4304b014b39382838a119ac69ac58d680a4847640760690801626c2",
    ),
    "lithuanian-cavalry": (
        "Pasiruošęs joti, valdove!",
        "74c5c84d96fe7c4753cf9eab2692533e7b3548ed7bfdb9c980284aed5b356f52",
    ),
    "lithuanian-hero": (
        "Klausau, didysis kunigaikšti!",
        "3f96a06cebad6f4876033190b226aaada19b66d134f6f7f074b238d4f8496239",
    ),
    "lithuanian-infantry": (
        "Laukiu įsakymų, vade!",
        "a65a62fa90c1dd1e944a0bb0a24b815c70e614e9c3068302f04657a897bf68c9",
    ),
    "persian-archer": (
        "کمان آماده است، فرمانده!",
        "fef53b6905f240f323b7582555313b1c1257a1d5e4cf245c1f9e2a54b7d16270",
    ),
    "persian-cavalry": (
        "برای تاختن آماده\u200cام، سرورم!",
        "74197d65178b1c4df3aaa3b8adef436f2021feef9e98d6a56b425aa36b4e1374",
    ),
    "persian-hero": (
        "در خدمتم، شاهنشاه!",
        "68e4d475d08c805cd8a89b55d46517cd8b3de48d202e665891e911a7739a48e5",
    ),
    "persian-infantry": ("چشم، فرمانده!", "f72ba1080cb61e4855fe06623abd232ec8b45b20f984d965f728502f4a723bbe"),
    "spanish-archer": (
        "Arco listo, comandante.",
        "b0d32b188fd30747b039e3e482c79deca2c9b5bb3940f8ddff2aa45881202531",
    ),
    "spanish-cavalry": (
        "Montura lista, mi señor.",
        "205439bb915e070abac5fd8c7ec77b577e6e855111c76f28f665efef48b67720",
    ),
    "spanish-infantry": (
        "A sus órdenes, comandante.",
        "5076d59e5eab9aae21b190ab37d70c3f03d9d510a11e99d001759fb4aac2dbcf",
    ),
    "spanish-leader": (
        "A sus órdenes, majestad.",
        "8da0d7f39c23ea3d0e906606952429c2395059fa88afe036ff23cad57b9e1238",
    ),
    "turkish-archer": (
        "Yayım hazır, komutanım!",
        "6c38088062b003299f6592f44fb220658a2fd3ccb7bdc9c10240bb1c0c186b38",
    ),
    "turkish-cavalry": (
        "Hazırım, sultanım!",
        "bfc8c9de7290f4fd98573e3af57216e1813a4b2d9a7eaf1c02150f56ff4c54ee",
    ),
    "turkish-infantry": (
        "Emredin, komutanım!",
        "fec31924aba10ceef926c6d319a37641c723f0ebae8015fe8a5f84a96bb6fe17",
    ),
    "turkish-leader": (
        "Emrinizdeyim, sultanım!",
        "d9fd4960ba8c68e12431672bede211b294ba5212af8fb2416856befd658252bf",
    ),
}

EXPECTED_LICENSES = {
    "ADAPTER-LICENSE.txt": "bccb9e9fa28644216f919d1f80567e49a41990705d3c3b036c334dc03e00dd31",
    "HIGGS-LICENSE.txt": "0382189330b87c38517530e4e5bf0c9dfeb6c7bfbe62812577ddcb73e09a60c5",
    "NATIVE_REFERENCE_ATTRIBUTION.txt": "01880a1e2d5a058529631344462ed2b7fc2b66afc749acffcdb2a053c015fbb8",
    "OMNIVOICE-LICENSE.txt": "0f50c18894979bc783e58fc3b00d1cdc66f1dbcf9441e506b4c7a6fde65ae536",
    "OMNIVOICE-TOKENIZER-LICENSE.txt": "ac933dc084d119bd20401956b90d11ae87c248b2da62622cd580d82cdf2fa049",
    "VOXCPM-REFERENCE-CODE-LICENSE.txt": "4f10acc209addacfad28293315c74c4cd648f771ee1263a748f1781d1e0265e4",
}

# Independently captured from the installed DAT, not the editable voice manifest.
# Production verifies the catalog against the actual DAT again when packaging.
INSTALLED_CIV_NAMES = (
    "British", "French", "Goths", "Teutons", "Japanese", "Chinese", "Byzantine", "Persians",
    "Saracens", "Turks", "Vikings", "Mongols", "Celts", "Spanish", "Aztecs", "Mayan", "Huns",
    "Koreans", "Italians", "Hindustanis", "Incas", "Magyars", "Slavs", "Portuguese", "Ethiopians",
    "Malians", "Berbers", "Khmer", "Malay", "Burmese", "Vietnamese", "Bulgarians", "Tatars",
    "Cumans", "Lithuanians", "Burgundians", "Sicilians", "Poles", "Bohemians", "Dravidians",
    "Bengalis", "Gurjaras", "Romans", "Armenians", "Georgians", "Achaemenids", "Athenians",
    "Spartans", "Shu", "Wu", "Wei", "Jurchens", "Khitans", "Macedonians", "Thracians", "Puru",
    "Muisca", "Mapuche", "Tupi", "Saxons", "Varangians", "Danes",
)


def _catalog(generated=(8, 10, 14, 28, 35)):
    rows = []
    for civ_id, name in enumerate(INSTALLED_CIV_NAMES, start=1):
        row = {"id": civ_id, "name": name, "voice_profile": f"profile-{civ_id}",
               "mode": "generated" if civ_id in generated else "stock"}
        if row["mode"] == "stock":
            row["reason"] = "Archived five-civilization regression fixture retains stock audio."
        rows.append(row)
    return rows


def _archived_source_copy(tmp_path):
    """Keep the original twenty-byte regression runnable after expansion."""
    copied = tmp_path / "selection_audio"
    shutil.copytree(ASSETS, copied)
    path = copied / "manifest.json"
    manifest = json.loads(path.read_text())
    manifest["clips"] = [clip for clip in manifest["clips"] if clip["id"] in EXPECTED_CLIPS]
    manifest["civilizations"] = _catalog()
    for clip in manifest["clips"]:
        clip.pop("voice_profile", None)
    path.write_text(json.dumps(manifest, ensure_ascii=False))
    return copied


@pytest.fixture(scope="module")
def selection_audio():
    spec = importlib.util.spec_from_file_location(
        "ram_selection_audio_contract", ROOT / "modes/ram/selection_audio.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_ram_selection_source_assets_are_exact_current_native_voices(selection_audio):
    manifest, clips, licenses = selection_audio.load_selection_assets(ASSETS)
    catalog = selection_audio.civilization_catalog(manifest)
    assert {civ_id: row["name"] for civ_id, row in catalog.items()} == {
        civ_id: name for civ_id, name in enumerate(INSTALLED_CIV_NAMES, start=1)
    }
    generated = {civ_id for civ_id, row in catalog.items() if row["mode"] == "generated"}
    assert len(clips) == len(generated) * len(selection_audio.ROLES)
    assert {(clip["civilization_id"], clip["role"]) for clip in clips} == {
        (civ, role) for civ in generated for role in selection_audio.ROLES
    }
    reviewed = [clip for clip in clips if clip["id"] in EXPECTED_CLIPS]
    assert {clip["id"] for clip in reviewed} == EXPECTED_CLIPS.keys()
    for clip in reviewed:
        text, expected_hash = EXPECTED_CLIPS[clip["id"]]
        assert clip["text"] == text
        assert hashlib.sha256(clip["data"]).hexdigest() == expected_hash == clip["sha256"]
        assert not Path(clip["file"]).is_absolute()
        assert clip["file"] == f"audio/{clip['id']}.wav"
        model = clip["model"] if isinstance(clip["model"], str) else clip["model"]["repo"]
        expected_model = (
            "bosonai/higgs-tts-3-4b" if clip["language"] in ("lithuanian", "persian") else "k2-fsa/OmniVoice"
        )
        assert model == expected_model
        assert clip["model_revision"] == (
            "239f63fb7b02b1aa085f98d9efae5e35cc5523e8"
            if expected_model == "bosonai/higgs-tts-3-4b"
            else "c5fdb5ccb189668d56333f77ba2629f4cd7535f4"
        )
    original_licenses = {name: hashlib.sha256(licenses[name]).hexdigest() for name in EXPECTED_LICENSES}
    assert original_licenses == EXPECTED_LICENSES
    assert all(not Path(item["file"]).is_absolute() for item in manifest["license_files"])
    assert b"non-commercial" in licenses["HIGGS-LICENSE.txt"].lower()
    assert b"CC-BY-NC" in licenses["OMNIVOICE-LICENSE.txt"]
    assert b"CC BY 4.0" in licenses["NATIVE_REFERENCE_ATTRIBUTION.txt"]
    assert "This audio was created with Boson AI's Higgs Audio" in (ASSETS / "LICENSES.txt").read_text()


def test_ram_selection_assets_rebuild_from_isolated_source_copy(selection_audio, tmp_path):
    copied = _archived_source_copy(tmp_path)
    _, clips, licenses = selection_audio.load_selection_assets(copied)
    assert {clip["id"] for clip in clips} == EXPECTED_CLIPS.keys()
    assert EXPECTED_LICENSES.keys() <= licenses.keys()
    assert all((copied / clip["file"]).is_file() for clip in clips)
    for clip in clips:
        expected_text, expected_hash = EXPECTED_CLIPS[clip["id"]]
        assert clip["text"] == expected_text
        assert hashlib.sha256(clip["data"]).hexdigest() == expected_hash


@pytest.mark.parametrize(
    "corruption, message",
    [
        ("wav", "SHA-256 mismatch"),
        ("missing_role", "catalog-generated selection clips required"),
        ("escape", "escapes its source directory"),
        ("absolute", "paths must be relative"),
        ("license", "changed selection license"),
    ],
)
def test_ram_selection_assets_reject_corruption(selection_audio, tmp_path, corruption, message):
    copied = _archived_source_copy(tmp_path)
    manifest_path = copied / "manifest.json"
    manifest = json.loads(manifest_path.read_text())
    if corruption == "wav":
        (copied / manifest["clips"][0]["file"]).write_bytes(b"corrupted WAV")
    elif corruption == "missing_role":
        manifest["clips"].pop()
    elif corruption == "escape":
        manifest["clips"][0]["file"] = "../escaped.wav"
    elif corruption == "absolute":
        manifest["clips"][0]["file"] = str((copied / "audio/absolute.wav").resolve())
    elif corruption == "license":
        (copied / manifest["license_files"][0]["file"]).write_text("truncated license")
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False))
    with pytest.raises(ValueError, match=message):
        selection_audio.load_selection_assets(copied)


def test_complete_dataset_catalog_rejects_new_unknown_or_renamed_civs(selection_audio):
    rows = _catalog()
    catalog = selection_audio.civilization_catalog({"civilizations": rows})
    dataset = [SimpleNamespace(name="Gaia")] + [SimpleNamespace(name=name) for name in INSTALLED_CIV_NAMES]
    selection_audio.validate_dataset_catalog(catalog, dataset)
    with pytest.raises(ValueError, match="missing"):
        expanded = dataset + [SimpleNamespace(name="New civilization")]
        selection_audio.validate_dataset_catalog(catalog, expanded)
    with pytest.raises(ValueError, match="extra"):
        selection_audio.validate_dataset_catalog(catalog, dataset[:-1])
    dataset[1] = SimpleNamespace(name="Renamed civilization")
    with pytest.raises(ValueError, match="Renamed civilization"):
        selection_audio.validate_dataset_catalog(catalog, dataset)


@pytest.mark.parametrize("corruption", ["missing_catalog", "duplicate", "gaia", "stock_reason", "mode"])
def test_civilization_catalog_rejects_ambiguous_coverage(selection_audio, corruption):
    rows = _catalog()
    manifest = {"civilizations": rows}
    if corruption == "missing_catalog":
        manifest = {}
    elif corruption == "duplicate":
        rows.append(dict(rows[0]))
    elif corruption == "gaia":
        rows[0]["id"] = 0
    elif corruption == "stock_reason":
        rows[0].pop("reason")
    elif corruption == "mode":
        rows[0]["mode"] = "best_effort"
    with pytest.raises(ValueError):
        selection_audio.civilization_catalog(manifest)


def test_stock_fallback_cannot_accidentally_receive_generated_clips(selection_audio, tmp_path):
    copied = _archived_source_copy(tmp_path)
    path = copied / "manifest.json"
    manifest = json.loads(path.read_text())
    civ_id = manifest["clips"][0]["civilization_id"]
    row = next(row for row in manifest["civilizations"] if row["id"] == civ_id)
    row.update(mode="stock", reason="Native-language pronunciation is not accepted for this civilization.")
    path.write_text(json.dumps(manifest, ensure_ascii=False))
    with pytest.raises(ValueError, match="Unsupported selection civilization/role"):
        selection_audio.load_selection_assets(copied)


def test_all_stock_catalog_is_explicit_and_needs_no_clip_bindings(selection_audio, tmp_path):
    copied = _archived_source_copy(tmp_path)
    path = copied / "manifest.json"
    manifest = json.loads(path.read_text())
    manifest.update(civilizations=_catalog(generated=()), clips=[])
    path.write_text(json.dumps(manifest, ensure_ascii=False))
    loaded, clips, _licenses = selection_audio.load_selection_assets(copied)
    assert clips == []
    assert all(row["mode"] == "stock" and row["reason"] for row in loaded["civilizations"])


def test_generated_bindings_leave_stock_tables_and_civilians_untouched(selection_audio):
    def unit(name, kind, selection):
        return SimpleNamespace(
            type=70, class_=kind, name=name, selection_sound=selection, wwise_selection_sound_id=12345,
            bird=SimpleNamespace(run_pattern=255), creatable=SimpleNamespace(hero_mode=0),
            type_50=SimpleNamespace(projectile_unit_id=363),
        )

    generated_archer = unit("generated archer", 0, 100)
    generated_civilian = unit("generated civ's villager", 4, 101)
    stock_archer = unit("stock archer", 0, 102)
    civilizations = [SimpleNamespace(units=[]),
                     SimpleNamespace(units=[generated_archer, generated_civilian]),
                     SimpleNamespace(units=[stock_archer])]
    catalog = {1: {"mode": "generated"}, 2: {"mode": "stock"}}
    changes = selection_audio._apply_selection_bindings(civilizations, catalog, {(1, "archer"): 900})
    assert len(changes) == 1 and changes[0]["civilization_id"] == 1
    assert generated_archer.selection_sound == 900
    assert stock_archer.selection_sound == 102 and generated_civilian.selection_sound == 101
    assert all(u.wwise_selection_sound_id == 12345 and u.bird.run_pattern == 255
               for u in (generated_archer, generated_civilian, stock_archer))
