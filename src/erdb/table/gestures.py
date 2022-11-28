from erdb.typing.models.gesture import Gesture
from erdb.typing.params import ParamRow
from erdb.typing.enums import GoodsSortGroupID, ItemIDFlag
from erdb.typing.api_version import ApiVersion
from erdb.table._retrievers import ParamDictRetriever, MsgsRetriever, RetrieverData
from erdb.table._common import RowPredicate, TableSpecContext


class GestureTableSpec(TableSpecContext):
    model = {
        ApiVersion.VER_1: Gesture,
    }

    predicates: list[RowPredicate] = [
        lambda row: row["sortGroupId"].as_int == GoodsSortGroupID.GESTURES,
    ]

    main_param_retriever = ParamDictRetriever("EquipParamGoods", ItemIDFlag.GOODS)

    msg_retrievers = {
        "names": MsgsRetriever("GoodsName"),
        "summaries": MsgsRetriever("GoodsInfo"),
        "descriptions": MsgsRetriever("GoodsCaption")
    }

    @classmethod
    def make_object(cls, api: ApiVersion, data: RetrieverData, row: ParamRow):
        return Gesture(
            **cls.make_item(data, row),
            **cls.make_contrib(data, row, "locations", "remarks")
        )