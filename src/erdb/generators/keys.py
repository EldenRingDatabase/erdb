from typing import Dict, Iterator, Tuple

import erdb.loaders.schema as schema
from erdb.typing.params import ParamDict, ParamRow
from erdb.typing.enums import GoodsSortGroupID, GoodsType, ItemIDFlag
from erdb.utils.common import strip_invalid_name
from erdb.generators._base import GeneratorDataBase


def _get_category(row: ParamRow) -> str:
    for custom in ("Great Rune", "Meding Rune", "Whetblade"):
        if custom in row.name:
            return custom

    G = GoodsSortGroupID
    return {
        G.GROUP_3: "Container",
        G.GROUP_4: "Exploration",
        G.GROUP_5: "Exchange" if row.get_bool("isConsume") else "Quest",
        G.GROUP_6: "Feature",
        G.GROUP_7: "Map",
    }[row.get_int("sortGroupId")]

class KeyGeneratorData(GeneratorDataBase):
    Base = GeneratorDataBase

    @staticmethod # override
    def output_file() -> str:
        return "keys.json"

    @staticmethod # override
    def schema_file() -> str:
        return "keys.schema.json"

    @staticmethod # override
    def element_name() -> str:
        return "Keys"

    # override
    def get_key_name(self, row: ParamRow) -> str:
        return strip_invalid_name(self.msgs["names"][row.index])

    main_param_retriever = Base.ParamDictRetriever("EquipParamGoods", ItemIDFlag.GOODS)

    param_retrievers = {}

    msgs_retrievers = {
        "names": Base.MsgsRetriever("GoodsName"),
        "summaries": Base.MsgsRetriever("GoodsInfo"),
        "descriptions": Base.MsgsRetriever("GoodsCaption")
    }

    lookup_retrievers = {}

    @staticmethod
    def schema_retriever() -> Tuple[Dict, Dict[str, Dict]]:
        properties, store = schema.load_properties(
            "item/properties",
            "item/definitions/ItemUserData/properties",
            "keys/definitions/Key/properties")
        store.update(schema.load_enums("item-names"))
        return properties, store

    def main_param_iterator(self, keys: ParamDict) -> Iterator[ParamRow]:
        Gsid = GoodsSortGroupID
        for row in keys.values():
            if 1 <= row.get_int("sortId") < 999999 \
            and row.get("goodsType") in [GoodsType.KEY_ITEM, GoodsType.REGENERATIVE_MATERIAL] \
            and row.get_int("sortGroupId") not in [Gsid.GROUP_8, Gsid.GROUP_9, Gsid.GROUP_10] \
            and "Cookbook" not in row.name:
                yield row

    def construct_object(self, row: ParamRow) -> Dict:
        return self.get_fields_item(row) | self.get_fields_user_data(row, "locations", "remarks") | {
            "category": _get_category(row)
        }