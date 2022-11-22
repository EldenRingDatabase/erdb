from erdb.typing.models.shop import Shop
from erdb.typing.params import ParamDict, ParamRow
from erdb.typing.enums import GoodsSortGroupID, GoodsType, ItemIDFlag
from erdb.typing.categories import ShopCategory
from erdb.utils.common import strip_invalid_name
from erdb.generators._base import GeneratorDataBase


class ShopGeneratorData(GeneratorDataBase):
    Base = GeneratorDataBase

    @staticmethod # override
    def output_file() -> str:
        return "shop.json"

    @staticmethod # override
    def element_name() -> str:
        return "Shop"

    @staticmethod # override
    def model() -> Shop:
        return Shop

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

    def main_param_iterator(self, shop: ParamDict):
        Gsid = GoodsSortGroupID
        for row in shop.values():
            if 1 <= row.get_int("sortId") < 999999 \
            and row.get("goodsType") == GoodsType.KEY_ITEM \
            and (row.get_int("sortGroupId") in [Gsid.GROUP_8, Gsid.GROUP_9, Gsid.GROUP_10] \
            or (row.get_int("sortGroupId") == Gsid.GROUP_6 and "Cookbook" in row.name)):
                yield row

    def construct_object(self, row: ParamRow) -> Shop:
        return Shop(
            **self.get_fields_item(row),
            **self.get_fields_user_data(row, "locations", "remarks"),
            category=ShopCategory.from_row(row),
        )