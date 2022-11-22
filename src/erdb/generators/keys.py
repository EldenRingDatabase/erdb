from erdb.typing.models.key import Key
from erdb.typing.params import ParamDict, ParamRow
from erdb.typing.enums import GoodsSortGroupID, GoodsType, ItemIDFlag
from erdb.typing.categories import KeyCategory
from erdb.utils.common import strip_invalid_name
from erdb.generators._base import GeneratorDataBase


class KeyGeneratorData(GeneratorDataBase):
    Base = GeneratorDataBase

    @staticmethod # override
    def output_file() -> str:
        return "keys.json"

    @staticmethod # override
    def element_name() -> str:
        return "Keys"

    @staticmethod # override
    def model() -> Key:
        return Key

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

    def main_param_iterator(self, keys: ParamDict):
        Gsid = GoodsSortGroupID
        for row in keys.values():
            if 1 <= row.get_int("sortId") < 999999 \
            and row.get("goodsType") in [GoodsType.KEY_ITEM, GoodsType.REGENERATIVE_MATERIAL] \
            and row.get_int("sortGroupId") not in [Gsid.GROUP_8, Gsid.GROUP_9, Gsid.GROUP_10] \
            and "Cookbook" not in row.name:
                yield row

    def construct_object(self, row: ParamRow) -> Key:
        return Key(
            **self.get_fields_item(row),
            **self.get_fields_user_data(row, "locations", "remarks"),
            category=KeyCategory.from_row(row),
        )