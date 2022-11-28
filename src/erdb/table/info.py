from erdb.typing.models.info import Info
from erdb.typing.params import ParamRow
from erdb.typing.enums import GoodsType, ItemIDFlag
from erdb.typing.categories import InfoCategory
from erdb.typing.api_version import ApiVersion
from erdb.table._retrievers import ParamDictRetriever, MsgsRetriever, RetrieverData
from erdb.table._common import RowPredicate, TableSpecContext


class InfoTableSpec(TableSpecContext):
    model = {
        ApiVersion.VER_1: Info,
    }

    main_param_retriever = ParamDictRetriever("EquipParamGoods", ItemIDFlag.GOODS)

    predicates: list[RowPredicate] = [
        lambda row: 1 <= row["sortId"].as_int < 999999,
        lambda row: row["goodsType"] == GoodsType.INFO_ITEM,
    ]

    msg_retrievers = {
        "names": MsgsRetriever("GoodsName"),
        "summaries": MsgsRetriever("GoodsInfo"),
        "descriptions": MsgsRetriever("GoodsCaption")
    }

    @classmethod
    def make_object(cls, api: ApiVersion, data: RetrieverData, row: ParamRow):
        return Info(
            **cls.make_item(data, row),
            **cls.make_contrib(data, row, "locations", "remarks"),
            category=InfoCategory.from_row(row),
        )