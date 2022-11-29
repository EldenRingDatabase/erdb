from typing import NamedTuple

from erdb.typing.game_version import GameVersion
from erdb.loaders.params import load as load_params, load_ids as load_param_ids, load_msg
from erdb.loaders.contrib import load as load_contrib
from erdb.typing.params import ParamDict
from erdb.typing.enums import ItemIDFlag
from erdb.shop import Lookup


class RetrieverData(NamedTuple):
    main_param: ParamDict
    params: dict[str, ParamDict]
    msgs: dict[str, dict[int, str]]
    shops: dict[str, Lookup]
    contrib: dict[str, dict]

class ParamDictRetriever(NamedTuple):
    param_name: str
    item_id_flag: ItemIDFlag
    id_min: int | None = None
    id_max: int | None = None

    def get(self, version: GameVersion) -> ParamDict:
        args = [self.param_name, version, self.item_id_flag]
        args += [arg for arg in [self.id_min, self.id_max] if arg is not None]
        func = load_params if len(args) <= 3 else load_param_ids
        return func(*args) # type: ignore

    def __contains__(self, __x: object) -> bool:
        assert isinstance(__x, int), f"Can only check for integer range"
        return  (not self.id_min or self.id_min <= __x) \
            and (not self.id_max or self.id_max >= __x)

class MsgsRetriever(NamedTuple):
    file_name: str

    def get(self, version: GameVersion) -> dict[int, str]:
        return load_msg(self.file_name, version)

class ShopRetriever(NamedTuple):
    shop_lineup_id_min: int | None
    shop_lineup_id_max: int | None
    material_set_id_min: int | None
    material_set_id_max: int | None
    recipe: bool = False

    def get(self, version: GameVersion) -> Lookup:
        F = ParamDictRetriever
        shop_param = "ShopLineupParam_Recipe" if self.recipe else "ShopLineupParam"
        shop = F(shop_param, ItemIDFlag.NON_EQUIPABBLE, self.shop_lineup_id_min, self.shop_lineup_id_max)
        mats = F("EquipMtrlSetParam", ItemIDFlag.NON_EQUIPABBLE, self.material_set_id_min, self.material_set_id_max)
        return Lookup(shop.get(version), mats.get(version))

class ContribRetriever(NamedTuple):
    def get(self, element_name: str, version: GameVersion) -> dict[str, dict]:
        return load_contrib(element_name, version)