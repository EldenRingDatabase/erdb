from erdb.typing.models.key import Key
from erdb.typing.params import ParamRow
from erdb.typing.enums import GoodsSortGroupID, GoodsType, ItemIDFlag
from erdb.typing.categories import KeyCategory
from erdb.typing.api_version import ApiVersion
from erdb.table._retrievers import ParamDictRetriever, MsgsRetriever, RetrieverData
from erdb.table._common import RowPredicate, TableSpecContext


class KeyTableSpec(TableSpecContext):
    model = {
        ApiVersion.VER_1: Key,
    }

    main_param_retriever = ParamDictRetriever("EquipParamGoods", ItemIDFlag.GOODS)

    predicates: list[RowPredicate] = [
        lambda row: 1 <= row["sortId"].as_int < 999999,
        lambda row: row["goodsType"] in [GoodsType.KEY_ITEM, GoodsType.REGENERATIVE_MATERIAL],
        lambda row: row["sortGroupId"].as_int not in [GoodsSortGroupID.GROUP_8, GoodsSortGroupID.GROUP_9, GoodsSortGroupID.GROUP_10],
        lambda row: "Cookbook" not in row.name,
    ]

    msg_retrievers = {
        "names": MsgsRetriever("GoodsName"),
        "summaries": MsgsRetriever("GoodsInfo"),
        "descriptions": MsgsRetriever("GoodsCaption")
    }

    @classmethod
    def make_object(cls, api: ApiVersion, data: RetrieverData, row: ParamRow):
        return Key(
            **cls.make_item(data, row),
            **cls.make_contrib(data, row, "locations", "remarks"),
            category=KeyCategory.from_row(row),
        )