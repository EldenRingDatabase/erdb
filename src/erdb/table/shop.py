from erdb.typing.models.shop import Shop
from erdb.typing.params import ParamRow
from erdb.typing.enums import GoodsSortGroupID, GoodsType, ItemIDFlag
from erdb.typing.categories import ShopCategory
from erdb.typing.api_version import ApiVersion
from erdb.table._retrievers import ParamDictRetriever, MsgsRetriever, RetrieverData
from erdb.table._common import RowPredicate, TableSpecContext


class ShopTableSpec(TableSpecContext):
    model = {
        ApiVersion.VER_1: Shop,
    }

    main_param_retriever = ParamDictRetriever("EquipParamGoods", ItemIDFlag.GOODS)

    predicates: list[RowPredicate] = [
        lambda row: 1 <= row["sortId"].as_int < 999999,
        lambda row: row["goodsType"] == GoodsType.KEY_ITEM,
        lambda row: (row["sortGroupId"].as_int in [GoodsSortGroupID.GROUP_8, GoodsSortGroupID.GROUP_9, GoodsSortGroupID.GROUP_10] \
            or (row["sortGroupId"].as_int == GoodsSortGroupID.GROUP_6 and "Cookbook" in row.name)),
    ]

    msg_retrievers = {
        "names": MsgsRetriever("GoodsName"),
        "summaries": MsgsRetriever("GoodsInfo"),
        "descriptions": MsgsRetriever("GoodsCaption")
    }

    @classmethod
    def make_object(cls, api: ApiVersion, data: RetrieverData, row: ParamRow):
        return Shop(
            **cls.make_item(data, row),
            **cls.make_contrib(data, row, "locations", "remarks"),
            category=ShopCategory.from_row(row),
        )