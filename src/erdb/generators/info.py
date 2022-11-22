from erdb.typing.models.info import Info
from erdb.typing.params import ParamDict, ParamRow
from erdb.typing.enums import GoodsType, ItemIDFlag
from erdb.typing.categories import InfoCategory
from erdb.utils.common import strip_invalid_name
from erdb.generators._base import GeneratorDataBase


class InfoGeneratorData(GeneratorDataBase):
    Base = GeneratorDataBase

    @staticmethod # override
    def output_file() -> str:
        return "info.json"

    @staticmethod # override
    def element_name() -> str:
        return "Info"

    @staticmethod # override
    def model() -> Info:
        return Info

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

    def main_param_iterator(self, info: ParamDict):
        for row in info.values():
            if 1 <= row.get_int("sortId") < 999999 \
            and row.get("goodsType") == GoodsType.INFO_ITEM:
                yield row

    def construct_object(self, row: ParamRow) -> Info:
        return Info(
            **self.get_fields_item(row),
            **self.get_fields_user_data(row, "locations", "remarks"),
            category=InfoCategory.from_row(row),
        )