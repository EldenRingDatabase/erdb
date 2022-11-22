import json
from pathlib import Path
import pytest

from erdb.utils.attack_power import Attributes, CalculatorData, ArmamentCalculator


"""
Version of the game the sample data has been explicitly collected for
"""
_GAME_VERSION: str = "1.05.0"

_TEST_DIR = Path(__file__).parent.resolve()
_DATA_DIR = _TEST_DIR / "attack_values"
_GAMEDATA_DIR = _TEST_DIR.parent / _GAME_VERSION
_ATTRIBUTE_SETS = [Attributes.from_string(f.stem) for f in _DATA_DIR.glob("*")]

def pytest_generate_tests(metafunc):
    assert "armament" in metafunc.fixturenames
    assert "attribs" in metafunc.fixturenames

    with open(_GAMEDATA_DIR / "armaments.json") as f:
        armaments = json.load(f)["Armaments"]

    armament_data: list[tuple[str, str]] = []
    armament_ids: list[str] = []

    for armament, properties in armaments.items():
        for affinity in properties["affinity"].keys():
            armament_data.append((affinity, armament))
            armament_ids.append(f"{affinity} {armament}")

    metafunc.parametrize("armament", armament_data, ids=armament_ids)
    metafunc.parametrize("attribs", _ATTRIBUTE_SETS, ids=[*map(str, _ATTRIBUTE_SETS)])

@pytest.fixture(scope="module")
def calc_data() -> CalculatorData:
    return CalculatorData.create(_GAMEDATA_DIR)

@pytest.fixture(scope="module")
def results_data() -> dict[str, dict]:
    def load(attribs):
        with open(_DATA_DIR / f"{attribs}.json") as f:
            return json.load(f)

    return {attribs: load(attribs) for attribs in _ATTRIBUTE_SETS}

def test_attack_power(calc_data, armament, attribs, results_data):
    affinity, name = armament
    level = "0" if name == "Meteorite Staff" else "10"

    expected = results_data[attribs][name][affinity]["attack_power"]
    calc = ArmamentCalculator(calc_data, name, affinity, level)
    ap = calc.attack_power(attribs)

    if ap.physical.total > 0:
        assert len(expected["physical"]) == 4
        assert expected["physical"][3] == ap.physical.total

    if ap.magic.total > 0:
        assert len(expected["magic"]) == 4
        assert expected["magic"][3] == ap.magic.total

    if ap.fire.total > 0:
        assert len(expected["fire"]) == 4
        assert expected["fire"][3] == ap.fire.total

    if ap.lightning.total > 0:
        assert len(expected["lightning"]) == 4
        assert expected["lightning"][3] == ap.lightning.total

    if ap.holy.total > 0:
        assert len(expected["holy"]) == 4
        assert expected["holy"][3] == ap.holy.total