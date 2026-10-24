"""The complete leader catalog must select land combat units and flag proxies."""

import importlib.util
import json
from pathlib import Path
from types import SimpleNamespace

import pytest

ROOT = Path(__file__).resolve().parents[1]
MODE = ROOT / "modes/ram"
SPEC = importlib.util.spec_from_file_location("ram_leaders", MODE / "civilization_leaders.py")
leaders = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(leaders)


def test_every_leader_keeps_the_original_population_cost_without_economic_prices():
    original = (SimpleNamespace(type=1, amount=55, flag=1), SimpleNamespace(type=3, amount=65, flag=1),
                SimpleNamespace(type=4, amount=1, flag=0))
    costs = leaders._leader_costs(original)
    assert [(cost.type, cost.amount, cost.flag) for cost in costs] == [(1, 0, 1), (3, 0, 1), (4, 1, 0)]
    assert original[0].amount == 55 and original[1].amount == 65


def test_complete_catalog_and_requested_native_leaders():
    rows = leaders.load_leader_catalog(MODE)
    catalog = {row["civilization"]: row for row in rows}
    assert set(catalog) == set(range(1, 63))
    assert (catalog[1]["leader_name"], catalog[1]["source_unit_id"]) == ("King Arthur", 173)
    assert (catalog[35]["leader_name"], catalog[35]["source_unit_id"]) == ("Vytautas the Great", 1281)
    assert catalog[12]["source_unit_id"] == 731
    assert catalog[60]["source_unit_id"] == 2724
    assert catalog[61]["source_unit_id"] == 2721
    assert not {203, 844} & {row["source_unit_id"] for row in rows}  # Both are ships.
    assert all(row["note"] for row in rows if row["fallback"])
    assert {row["role"] for row in rows} == leaders.ROLES
    voices = json.loads((MODE / "assets/selection_audio/manifest.json").read_text())
    assert {row["civilization"]: row["civilization_name"] for row in rows} == {
        row["id"]: row["name"] for row in voices["civilizations"]
    }


@pytest.mark.parametrize("change", ["duplicate", "invalid_role", "missing_note"])
def test_rejects_ambiguous_or_undocumented_catalog(tmp_path, change):
    data = json.loads((MODE / "assets/leaders/catalog.json").read_text())
    if change == "duplicate":
        data["civilizations"].append(data["civilizations"][0])
    elif change == "invalid_role":
        data["civilizations"][0]["role"] = "ship"
    else:
        data["civilizations"][0]["note"] = ""
    path = tmp_path / "assets/leaders/catalog.json"
    path.parent.mkdir(parents=True)
    path.write_text(json.dumps(data))
    with pytest.raises(ValueError):
        leaders.load_leader_catalog(tmp_path)
