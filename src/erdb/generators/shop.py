from typing import Dict, Iterator, Tuple

import erdb.loaders.schema as schema
from erdb.typing.params import ParamDict, ParamRow
from erdb.typing.enums import GoodsSortGroupID, GoodsType, ItemIDFlag
from erdb.utils.common import strip_invalid_name
from erdb.generators._base import GeneratorDataBase


def _get_category(row: ParamRow) -> str:
    G = GoodsSortGroupID
    return {
        G.GROUP_6: "Cookbook",
        G.GROUP_8: "Bell Bearing",
        G.GROUP_9: "Bell Bearing",
        G.GROUP_10: "Spellbook",
    }[row.get_int("sortGroupId")]

class ShopGeneratorData(GeneratorDataBase):
    Base = GeneratorDataBase

    @staticmethod # override
    def output_file() -> str:
        return "shop.json"

    @staticmethod # override
    def schema_file() -> str:
        return "shop.schema.json"

    @staticmethod # override
    def element_name() -> str:
        return "Shop"

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
            "shop/definitions/Shop/properties")
        store.update(schema.load_enums("item-names"))
        return properties, store

    def main_param_iterator(self, shop: ParamDict) -> Iterator[ParamRow]:
        Gsid = GoodsSortGroupID
        for row in shop.values():
            if 1 <= row.get_int("sortId") < 999999 \
            and row.get("goodsType") == GoodsType.KEY_ITEM \
            and (row.get_int("sortGroupId") in [Gsid.GROUP_8, Gsid.GROUP_9, Gsid.GROUP_10] \
            or (row.get_int("sortGroupId") == Gsid.GROUP_6 and "Cookbook" in row.name)):
                yield row

    def construct_object(self, row: ParamRow) -> Dict:
        return self.get_fields_item(row) | self.get_fields_user_data(row, "locations", "remarks") | {
            "category": _get_category(row)
        }