import xml.etree.ElementTree as xmltree
from csv import DictReader
from typing import Dict
from zipfile import Path as ZipPath

from erdb.loaders import PKG_DATA_PATH
from erdb.typing.game_version import GameVersion
from erdb.typing.params import ParamRow, ParamDict
from erdb.typing.enums import ItemIDFlag


def _in_range(row_id: str, id_min: int, id_max: int):
    index = int(row_id)
    return id_min <= index and index <= id_max

def _load(param: str, version: GameVersion) -> DictReader:
    archive = PKG_DATA_PATH / "gamedata" / f"{version}.zip"
    with ZipPath(archive, at=f"{param}.csv").open(mode="r") as f:
        yield from DictReader(f, delimiter=";")

def load(param: str, version: GameVersion, item_id_flag: ItemIDFlag) -> ParamDict:
    return {row["Row ID"]: ParamRow(row, item_id_flag) for row in _load(param, version)}

# optimal variant for params with a lot of IDs like spEffects
def load_ids(param: str, version: GameVersion, item_id_flag: ItemIDFlag, id_min: int, id_max: int=999999999) -> ParamDict:
    return {row["Row ID"]: ParamRow(row, item_id_flag) for row in _load(param, version) if _in_range(row["Row ID"], id_min, id_max)}

def load_msg(filename: str, version: GameVersion) -> Dict[int, str]:
    archive = PKG_DATA_PATH / "gamedata" / f"{version}.zip"
    with ZipPath(archive, at=f"{filename}.fmg.xml").open(mode="r", encoding="utf-8") as f:
        tree = xmltree.fromstring(f.read())
        entries = tree.findall(".//text")

    return {int(e.get("id")): e.text for e in entries if e.text != "%null%"}