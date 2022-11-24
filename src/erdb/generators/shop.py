from erdb.typing.models.shop import Shop
from erdb.typing.params import ParamRow
from erdb.typing.enums import GoodsSortGroupID, GoodsType, ItemIDFlag
from erdb.typing.categories import ShopCategory
from erdb.generators._retrievers import ParamDictRetriever, MsgsRetriever, RetrieverData
from erdb.generators._common import RowPredicate, TableSpecContext


class ShopTableSpec(TableSpecContext):
    model = Shop

    main_param_retriever = ParamDictRetriever("EquipParamGoods", ItemIDFlag.GOODS)

    predicates: list[RowPredicate] = [
        lambda row: 1 <= row.get_int("sortId") < 999999,
        lambda row: row.get("goodsType") == GoodsType.KEY_ITEM,
        lambda row: (row.get_int("sortGroupId") in [GoodsSortGroupID.GROUP_8, GoodsSortGroupID.GROUP_9, GoodsSortGroupID.GROUP_10] \
            or (row.get_int("sortGroupId") == GoodsSortGroupID.GROUP_6 and "Cookbook" in row.name)),
    ]

    msg_retrievers = {
        "names": MsgsRetriever("GoodsName"),
        "summaries": MsgsRetriever("GoodsInfo"),
        "descriptions": MsgsRetriever("GoodsCaption")
    }

    @classmethod
    def make_object(cls, data: RetrieverData, row: ParamRow):
        return Shop(
            **cls.make_item(data, row),
            **cls.make_contrib(data, row, "locations", "remarks"),
            category=ShopCategory.from_row(row),
        )