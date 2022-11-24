from functools import cache
from enum import Enum
from typing import Any

from erdb.generators import Table
from erdb.loaders import GAME_VERSIONS
from erdb.typing.game_version import GameVersion


GameVersionEnum = Enum("GameVersionEnum", {str(v).replace(".", "_"): str(v) for v in GAME_VERSIONS})

@cache
def generate(game_version: GameVersionEnum, table: Table) -> dict: # type: ignore
    ver = GameVersion.from_string(game_version.value)
    return table.make_generator(ver).generate()

def precache_data():
    for game_version in GameVersionEnum:
        print(f">>> Precaching version {game_version.value}:", flush=True)

        for tb in Table.effective():
            print(">", tb.title, flush=True)
            generate(game_version, tb)

        print()

def as_str(obj: Any, field: str) -> str:
    v = getattr(obj, field)
    return v.value if isinstance(v, Enum) else str(v)