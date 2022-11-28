from erdb.typing.models.bolstering_material import BolsteringMaterial
from erdb.typing.categories import BolsteringMaterialCategory
from erdb.typing.params import ParamRow
from erdb.typing.enums import GoodsType, ItemIDFlag
from erdb.typing.api_version import ApiVersion
from erdb.table._retrievers import ParamDictRetriever, MsgsRetriever, RetrieverData
from erdb.table._common import RowPredicate, TableSpecContext


class BolsteringMaterialTableSpec(TableSpecContext):
    model = {
        ApiVersion.VER_1: BolsteringMaterial,
    }

    predicates: list[RowPredicate] = [
        lambda row: row["goodsType"] == GoodsType.REINFORCEMENT_MATERIAL,
    ]

    main_param_retriever = ParamDictRetriever("EquipParamGoods", ItemIDFlag.GOODS)

    msg_retrievers = {
        "names": MsgsRetriever("GoodsName"),
        "summaries": MsgsRetriever("GoodsInfo"),
        "descriptions": MsgsRetriever("GoodsCaption")
    }

    @classmethod
    def make_object(cls, api: ApiVersion, data: RetrieverData, row: ParamRow):
        return BolsteringMaterial(
            **cls.make_item(data, row),
            **cls.make_contrib(data, row, "locations", "remarks"),
            category=BolsteringMaterialCategory.from_row(row),
        )