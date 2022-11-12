from typing import Dict, Iterator, Tuple
from scripts.er_params import ParamDict, ParamRow
from scripts.er_params.enums import GoodsType, GoodsSortGroupID, ItemIDFlag
from scripts.erdb_common import get_schema_enums, get_schema_properties, strip_invalid_name
from scripts.erdb_generators._base import GeneratorDataBase

def _get_category(row: ParamRow) -> str:
    G = GoodsSortGroupID
    return {
        G.GROUP_1: "Painting" if "Painting" in row.name else "Note" if "Note" in row.name else "Clue",
        G.GROUP_2: "Tutorial",
    }[row.get_int("sortGroupId")]

class InfoGeneratorData(GeneratorDataBase):
    Base = GeneratorDataBase

    @staticmethod # override
    def output_file() -> str:
        return "info.json"

    @staticmethod # override
    def schema_file() -> str:
        return "info.schema.json"

    @staticmethod # override
    def element_name() -> str:
        return "Info"

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
        properties, store = get_schema_properties(
            "item/properties",
            "item/definitions/ItemUserData/properties",
            "info/definitions/Info/properties")
        store.update(get_schema_enums("item-names"))
        return properties, store

    def main_param_iterator(self, info: ParamDict) -> Iterator[ParamRow]:
        Gsid = GoodsSortGroupID
        for row in info.values():
            if 1 <= row.get_int("sortId") < 999999 \
            and row.get("goodsType") == GoodsType.INFO_ITEM:
                yield row

    def construct_object(self, row: ParamRow) -> Dict:
        return self.get_fields_item(row) | self.get_fields_user_data(row, "locations", "remarks") | {
            "category": _get_category(row)
        }