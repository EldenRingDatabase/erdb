from typing import Iterator
import xml.etree.ElementTree as xmltree
from csv import DictReader
from zipfile import Path as ZipPath

from erdb.loaders import PKG_DATA_PATH
from erdb.typing.game_version import GameVersion
from erdb.typing.params import ParamRow, ParamDict
from erdb.typing.enums import ItemIDFlag


def _load(param: str, version: GameVersion) -> Iterator[dict[str, str]]:
    archive = PKG_DATA_PATH / "gamedata" / f"{version}.zip"
    with ZipPath(archive, at=f"{param}.csv").open(mode="r") as f:
        yield from DictReader(f, delimiter=";") # type: ignore

def load(param: str, version: GameVersion, item_id_flag: ItemIDFlag) -> ParamDict:
    return {int(row["Row ID"]): ParamRow.make(row, item_id_flag) for row in _load(param, version)}

# optimal variant for params with a lot of IDs like spEffects
def load_ids(param: str, version: GameVersion, item_id_flag: ItemIDFlag, id_min: int, id_max: int = 999999999) -> ParamDict:
    return {int(row["Row ID"]): ParamRow.make(row, item_id_flag) for row in _load(param, version) if id_min <= int(row["Row ID"]) <= id_max}

def load_msg(filename: str, version: GameVersion) -> dict[int, str]:
    archive = PKG_DATA_PATH / "gamedata" / f"{version}.zip"
    with ZipPath(archive, at=f"{filename}.fmg.xml").open(mode="r", encoding="utf-8") as f:
        tree = xmltree.fromstring(f.read())
        entries = tree.findall(".//text")

    return {int(str(e.get("id"))): str(e.text) for e in entries if e.text != "%null%"}