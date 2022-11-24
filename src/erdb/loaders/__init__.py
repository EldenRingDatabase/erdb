import importlib.resources
from pathlib import Path

from erdb.typing.game_version import GameVersion


TOP_LEVEL_PKG = __name__.split(".")[0]
PKG_DATA_PATH = Path(str(importlib.resources.files(TOP_LEVEL_PKG))) / "data"
GAME_VERSIONS = sorted(
    [GameVersion.from_string(p.stem) for p in (PKG_DATA_PATH / "gamedata").glob("*zip")],
    reverse=True
)