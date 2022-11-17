from typing import Dict, Iterator, Tuple

import erdb.loaders.schema as schema
from erdb.typing.params import ParamDict, ParamRow
from erdb.typing.enums import GoodsSortGroupID, ItemIDFlag
from erdb.utils.common import strip_invalid_name
from erdb.generators._base import GeneratorDataBase


class GestureGeneratorData(GeneratorDataBase):
    Base = GeneratorDataBase

    @staticmethod # override
    def output_file() -> str:
        return "gestures.json"

    @staticmethod # override
    def schema_file() -> str:
        return "gestures.schema.json"

    @staticmethod # override
    def element_name() -> str:
        return "Gestures"

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
            "gestures/definitions/Gesture/properties")
        store.update(schema.load_enums("item-names"))
        return properties, store

    def main_param_iterator(self, gestures: ParamDict) -> Iterator[ParamRow]:
        for row in gestures.values():
            if row.get_int("sortGroupId") == GoodsSortGroupID.GESTURES:
                yield row

    def construct_object(self, row: ParamRow) -> Dict:
        return self.get_fields_item(row) | self.get_fields_user_data(row, "locations", "remarks")