import pickle
from tempfile import TemporaryDirectory
from contextlib import contextmanager
from pathlib import Path
from functools import cache, lru_cache
from enum import Enum
from typing import IO, Any, Generator, NamedTuple, Self

from erdb.table import Table
from erdb.loaders import GAME_VERSIONS
from erdb.typing.game_version import GameVersion
from erdb.typing.api_version import ApiVersion


GameVersionEnum = Enum("GameVersionEnum", {"latest": "latest"} | {str(v).replace(".", "_"): str(v) for v in GAME_VERSIONS})
LATEST_VERSION = list(GameVersionEnum)[1]

class DataProxy(NamedTuple):
    cache_dir: Path

    def precache(self):
        for game_version in GameVersionEnum:
            print(f">>> Precaching version {game_version.value}:", flush=True)

            for tb in Table.effective():
                for api in tb.spec.model.keys():
                    print(f"> {tb.title} [v{api}]", flush=True)
                    self.generate(api, game_version, tb)

            print(flush=True)

    def generate(self, api: ApiVersion, game_version: GameVersionEnum, table: Table) -> dict: # type: ignore
        return \
            self._generate_latest(api, table) if game_version == GameVersionEnum.latest else \
            self._generate_specific(api, game_version, table)

    @cache # always in memory
    def _generate_latest(self, api: ApiVersion, table: Table) -> dict:
        return self._generate_specific(api, LATEST_VERSION, table)

    @lru_cache(maxsize=8) # up to 8 tables, single item access caches an entire table
    def _generate_specific(self, api: ApiVersion, game_version: GameVersionEnum, table: Table) -> dict: # type: ignore
        try:
            with self._open_cache(api, game_version, table, mode="rb") as f:
                return pickle.load(f)

        except FileNotFoundError:
            ver = GameVersion.from_string(game_version.value)
            data = table.make_generator(ver).generate(api)

            with self._open_cache(api, game_version, table, mode="wb") as f:
                pickle.dump(data, f)

            return data

    def _open_cache(self, api: ApiVersion, game_version: GameVersionEnum, table: Table, mode: str) -> IO[Any]: # type: ignore
        return open(self.cache_dir / f"{api}-{game_version.value}-{table}.bin", mode=mode)

    @classmethod
    @contextmanager
    def in_temp_dir(cls, **kwargs) -> Generator[Self, None, None]:
        with TemporaryDirectory(**kwargs) as temp_dir:
            yield cls(Path(temp_dir))