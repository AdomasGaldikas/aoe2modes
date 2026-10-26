"""Protect existing user files and keep local/resource packages faithful to ZIPs."""

from __future__ import annotations

import importlib
import json
from pathlib import Path

import pytest

from aoe2modes import registry
from aoe2modes.builder import _load_build_module

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture
def packaged(tmp_path):
    package = importlib.import_module(_load_build_module(registry.get("ram")).__name__ + ".package")
    mode = tmp_path / "ram"
    mode.mkdir()
    original = (ROOT / "modes/ram/mode.toml").read_text()
    (mode / "mode.toml").write_text(original.replace("enabled = true", "enabled = false"))
    scenario = tmp_path / "source.aoe2scenario"
    scenario.write_bytes(b"scenario fixture")
    dataset = tmp_path / "source.dat"
    dataset.write_bytes(b"dataset fixture")
    output = tmp_path / "packages"
    folder, archive, manifest = package.package_mod(scenario, dataset, output, mode)
    return package, mode, scenario, dataset, output, folder, archive, manifest


def test_repackage_identical_or_partial_tree_is_idempotent(packaged):
    package, mode, scenario, dataset, output, folder, archive, manifest = packaged
    marker = folder / "info.json"
    old_inode, old_mtime = marker.stat().st_ino, marker.stat().st_mtime_ns
    old_archive = archive.read_bytes()
    missing = folder / "resources/_common/drs/sounds/ram_startup_v1.wav"
    missing.unlink()
    again, same_archive, repeated = package.package_mod(scenario, dataset, output, mode)
    assert again == folder and same_archive == archive and repeated == manifest
    assert archive.read_bytes() == old_archive and missing.is_file()
    assert marker.stat().st_ino == old_inode and marker.stat().st_mtime_ns == old_mtime


@pytest.mark.parametrize("conflict", ["extra", "changed", "directory", "symlink", "archive", "manifest"])
def test_repackage_rejects_conflicts_before_any_output_writes(packaged, tmp_path, conflict):
    package, mode, scenario, dataset, output, folder, archive, manifest = packaged
    marker = folder / "info.json"
    missing = folder / "resources/_common/drs/sounds/ram_startup_v1.wav"
    missing.unlink()  # Would be regenerated if checks were not completed before writing.
    if conflict == "extra":
        protected = folder / "resources/_common/drs/sounds/unknown.wav"
        protected.write_bytes(b"user-owned extra")
    elif conflict == "changed":
        protected = marker
        protected.write_bytes(b"user-owned edit")
    elif conflict == "directory":
        marker.unlink()
        marker.mkdir()
        protected = marker / "user-child.txt"
        protected.write_bytes(b"user-owned directory content")
    elif conflict == "symlink":
        protected = tmp_path / "outside.wav"
        protected.write_bytes(b"user-owned outside")
        (folder / "resources/_common/drs/sounds/link.wav").symlink_to(protected)
    elif conflict == "archive":
        protected = archive
        protected.write_bytes(b"user-owned archive")
    else:
        protected = output / f"RAM-v{manifest['version']}-manifest.json"
        protected.write_bytes(b"user-owned manifest")
    before = protected.read_bytes()
    with pytest.raises(ValueError, match="Unexpected|differs|symlink|overwrite|directory"):
        package.package_mod(scenario, dataset, output, mode)
    assert protected.read_bytes() == before
    assert not missing.exists()


def test_resource_package_rejects_stale_extra_and_preserves_it(packaged):
    package, mode, _scenario, _dataset, output, folder, _archive, _manifest = packaged
    extra = folder / "resources/_common/drs/sounds/stale.wav"
    extra.write_bytes(b"old unrelated sound")
    with pytest.raises(ValueError, match="Unexpected file"):
        package.package_resource_mod(folder, output / "resource", mode)
    assert extra.read_bytes() == b"old unrelated sound"
    assert not (output / "resource").exists()


def test_resource_package_rejects_missing_or_modified_mixed_file(packaged):
    package, mode, _scenario, _dataset, output, folder, _archive, _manifest = packaged
    source = folder / "resources/_common/dat/empires2_x2_p1.dat"
    source.write_bytes(b"changed data")
    with pytest.raises(ValueError, match="differs"):
        package.package_resource_mod(folder, output / "resource", mode)
    assert source.read_bytes() == b"changed data"
    assert not (output / "resource").exists()


def test_resource_package_is_idempotent_and_rejects_output_conflicts(packaged):
    package, mode, _scenario, _dataset, output, folder, _archive, _manifest = packaged
    resource = output / "resource"
    directory, archive = package.package_resource_mod(folder, resource, mode)
    before = archive.read_bytes()
    assert package.package_resource_mod(folder, resource, mode) == (directory, archive)
    assert archive.read_bytes() == before
    extra = directory / "user-file.txt"
    extra.write_text("keep me")
    with pytest.raises(ValueError, match="Unexpected file"):
        package.package_resource_mod(folder, resource, mode)
    assert extra.read_text() == "keep me" and archive.read_bytes() == before


def test_resource_package_requires_complete_matching_manifest(packaged):
    package, mode, _scenario, _dataset, output, folder, _archive, manifest = packaged
    path = output / f"RAM-v{manifest['version']}-manifest.json"
    data = json.loads(path.read_text())
    data["version"] = "0.0.0"
    path.write_text(json.dumps(data))
    with pytest.raises(ValueError, match="manifest does not match"):
        package.package_resource_mod(folder, output / "resource", mode)
