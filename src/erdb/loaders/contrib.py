import json
from pathlib import Path

from erdb.typing.game_version import GameVersion, GameVersionRange
from erdb.loaders import PKG_DATA_PATH


def _overlay_properties(ret: dict, source: dict):
    """
    Append to lists and sets, override scalars and dictionaries
    """
    for key, value in source.items():
        if isinstance(value, list):
            ret[key] = ret.get(key, list()) + value
        elif isinstance(value, set):
            ret[key] = ret.get(key, set()) + value # type: ignore
        else:
            ret[key] = value

def _parse_user_file(path: Path, version: GameVersion) -> dict:
    assert path.is_file
    assert path.suffix == ".json"

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    ret = dict()

    for version_range, properties in data.items():
        if version in GameVersionRange.from_string(version_range):
            _overlay_properties(ret, properties)

    return ret

def load(element: str, version: GameVersion) -> dict[str, dict]:
    path = PKG_DATA_PATH / "contrib" / element
    files = path.iterdir() if path.is_dir() else []
    return {f.stem: _parse_user_file(f, version) for f in files}