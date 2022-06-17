from typing import List
from pathlib import Path
from scripts.game_version import GameVersion

"""
Project root directory.
"""
ROOT: Path = None

"""
List of game version from latest to oldest.
"""
VERSIONS: List[GameVersion] = None