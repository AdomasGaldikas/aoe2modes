from __future__ import annotations

import pytest

from aoe2modes.config import ConfigError, load_mode_spec

TEMPLATE = """
[mode]
id = "{id}"
name = "Demo"

[map]
size = {size}

[players]
count = {count}
teams = {teams}
"""


def write_mode(tmp_path, *, mode_id="demo", size=120, count=4, teams="[[1,2],[3,4]]"):
    directory = tmp_path / mode_id
    directory.mkdir()
    (directory / "mode.toml").write_text(
        TEMPLATE.format(id=mode_id, size=size, count=count, teams=teams), encoding="utf-8"
    )
    return directory


def test_loads_defaults(tmp_path):
    spec = load_mode_spec(write_mode(tmp_path))
    assert spec.id == "demo"
    assert spec.map.size == 120
    assert spec.players.count == 4
    assert spec.output_name == "Demo.aoe2scenario"


def test_id_must_match_folder(tmp_path):
    directory = write_mode(tmp_path, mode_id="demo")
    (directory / "mode.toml").write_text('[mode]\nid = "other"\n', encoding="utf-8")
    with pytest.raises(ConfigError, match="must match its folder name"):
        load_mode_spec(directory)


def test_rejects_player_on_two_teams(tmp_path):
    with pytest.raises(ConfigError, match="more than one team"):
        load_mode_spec(write_mode(tmp_path, teams="[[1,2],[2,3]]"))


def test_rejects_out_of_range_map(tmp_path):
    with pytest.raises(ConfigError, match="map.size"):
        load_mode_spec(write_mode(tmp_path, size=2))


def test_team_lookup(tmp_path):
    spec = load_mode_spec(write_mode(tmp_path))
    one, three = spec.players.ids[0], spec.players.ids[2]
    assert spec.players.team_of(one) == 1
    assert spec.players.team_of(three) == 2
    assert set(spec.players.opponents_of(one)) == {spec.players.ids[2], spec.players.ids[3]}


def test_output_stem_interpolates_version(tmp_path):
    directory = write_mode(tmp_path)
    (directory / "mode.toml").write_text(
        '[mode]\nid = "demo"\nname = "Demo"\nversion = "2.1"\n'
        '\n[scenario]\nfilename = "{name} v{version}"\n',
        encoding="utf-8",
    )
    assert load_mode_spec(directory).output_name == "Demo v2.1.aoe2scenario"
