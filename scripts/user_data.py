import json
import scripts.config as cfg
from pathlib import Path
from scripts.game_version import GameVersion, GameVersionRange
from typing import Dict

def _overlay_properties(ret: Dict, source: Dict):
    """
    Append to lists and sets, override scalars and dictionaries
    """
    for key, value in source.items():
        if isinstance(value, list):
            ret[key] = ret.get(key, list()) + value
        elif isinstance(value, set):
            ret[key] = ret.get(key, set()) + value
        else:
            ret[key] = value

def _parse_user_file(path: Path, version: GameVersion) -> Dict:
    assert path.is_file
    assert path.suffix == ".json"

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    del data["$schema"]

    ret = dict()

    for version_range, properties in data.items():
        if version in GameVersionRange.from_string(version_range):
            _overlay_properties(ret, properties)

    return ret

def read(element: str, version: GameVersion) -> Dict[str, Dict]:
    path = cfg.ROOT / "gamedata" / element
    files = path.iterdir() if path.is_dir() else []
    return {f.stem: _parse_user_file(f, version) for f in files}