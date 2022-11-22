import pytest

from erdb.typing.game_version import GameVersion, GameVersionRange


def _make(major: str, minor: str, patch: str) -> GameVersion:
    assert len(minor) >= 2, "Minor part must be at least 2 digits"
    return GameVersion(major, minor, patch, [int(major), int(minor), int(patch)])

@pytest.fixture(scope="module")
def base() -> GameVersion:
    return _make("1", "02", "3")

@pytest.mark.parametrize("left,right", [
    (["1", "02", "3"], ["1", "02", "3"]),
    (["1", "03", "3"], ["1", "03", "3"]),
    (["3", "03", "3"], ["3", "03", "3"]),
])
def test_eq(left: list[str], right: list[str]):
    assert _make(*left) == _make(*right)

@pytest.mark.parametrize("left,right", [
    (["1", "02", "4"], ["1", "02", "3"]),
    (["1", "04", "3"], ["1", "03", "3"]),
    (["4", "03", "3"], ["3", "03", "3"]),
])
def test_ne(left: list[str], right: list[str]):
    assert _make(*left) != _make(*right)

@pytest.mark.parametrize("left", [["1", "02", "2"], ["1", "01", "9"], ["0", "09", "9"]])
def test_lt(base, left):
    assert _make(*left) < base

@pytest.mark.parametrize("left", [["1", "02", "4"], ["1", "03", "0"], ["2", "00", "0"]])
def test_gt(base, left):
    assert _make(*left) > base

@pytest.mark.parametrize("left", [["1", "02", "2"], ["1", "02", "3"]])
def test_le(base, left):
    assert _make(*left) <= base

@pytest.mark.parametrize("left", [["1", "02", "3"], ["1", "02", "4"]])
def test_ge(base, left):
    assert _make(*left) >= base

@pytest.mark.parametrize("string,expected", [
    ("1.04.1", _make("1", "04", "1")),
    ("2.64.9", _make("2", "64", "9")),
    ("0.03.9",  _make("0", "03", "9")),
])
def test_from_string(string: str, expected: GameVersion):
    assert GameVersion.from_string(string) == expected

@pytest.mark.parametrize("string,begin,end", [
    ("from 1.04.1 until 1.05.0", _make("1", "04", "1"), _make("1", "05", "0")),
    ("from 1.04.1", _make("1", "04", "1"), GameVersion.max()),
    ("until 1.05.0", GameVersion.min(), _make("1", "05", "0")),
    ("only 1.04.1", _make("1", "04", "1"), GameVersion.max()),
    ("any version", GameVersion.min(), GameVersion.max()),
])
def test_range_from_string(string: str, begin: GameVersion, end: GameVersion):
    version_range = GameVersionRange.from_string(string)
    assert version_range.begin == begin
    assert version_range.end == end

@pytest.mark.parametrize("string,version", [
    ("from 1.04.1 until 1.05.0", _make("1", "04", "1")),
    ("from 1.04.1 until 1.05.0", _make("1", "04", "2")),
    ("from 1.04.1 until 1.05.0", _make("1", "04", "99")),
    ("from 1.04.1", _make("1", "04", "99")),
    ("from 1.04.1", _make("1", "05", "0")),
    ("until 1.05.0", _make("1", "04", "99")),
    ("until 1.05.0", _make("1", "03", "0")),
    ("only 1.05.0", _make("1", "05", "0")),
    ("any version", _make("1", "04", "99")),
    ("any version", _make("1", "05", "99")),
])
def test_range_contains(string: str, version: GameVersion):
    assert version in GameVersionRange.from_string(string)

@pytest.mark.parametrize("string,version", [
    ("from 1.04.1 until 1.05.0", _make("1", "04", "0")),
    ("from 1.04.1 until 1.05.0", _make("1", "05", "0")),
    ("from 1.04.1 until 1.05.0", _make("1", "05", "99")),
    ("from 1.04.1", _make("1", "04", "0")),
    ("from 1.04.1", _make("1", "03", "99")),
    ("until 1.05.0", _make("1", "05", "0")),
    ("only 1.05.0", _make("1", "04", "99")),
    ("only 1.05.0", _make("1", "05", "1")),
])
def test_range_not_contains(string: str, version: GameVersion):
    assert version not in GameVersionRange.from_string(string)