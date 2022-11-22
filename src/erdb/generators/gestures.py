from erdb.typing.models.gesture import Gesture
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
    def element_name() -> str:
        return "Gestures"

    @staticmethod # override
    def model() -> Gesture:
        return Gesture

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

    def main_param_iterator(self, gestures: ParamDict):
        for row in gestures.values():
            if row.get_int("sortGroupId") == GoodsSortGroupID.GESTURES:
                yield row

    def construct_object(self, row: ParamRow) -> Gesture:
        return Gesture(
            **self.get_fields_item(row),
            **self.get_fields_user_data(row, "locations", "remarks")
        )