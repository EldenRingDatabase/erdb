from erdb.typing.models.bolstering_material import BolsteringMaterial
from erdb.typing.categories import BolsteringMaterialCategory
from erdb.typing.params import ParamRow
from erdb.typing.enums import GoodsType, ItemIDFlag
from erdb.generators._retrievers import ParamDictRetriever, MsgsRetriever, RetrieverData
from erdb.generators._common import RowPredicate, TableSpecContext


class BolsteringMaterialTableSpec(TableSpecContext):
    model = BolsteringMaterial

    predicates: list[RowPredicate] = [
        lambda row: row.get("goodsType") == GoodsType.REINFORCEMENT_MATERIAL,
    ]

    main_param_retriever = ParamDictRetriever("EquipParamGoods", ItemIDFlag.GOODS)

    msg_retrievers = {
        "names": MsgsRetriever("GoodsName"),
        "summaries": MsgsRetriever("GoodsInfo"),
        "descriptions": MsgsRetriever("GoodsCaption")
    }

    @classmethod
    def make_object(cls, data: RetrieverData, row: ParamRow):
        return BolsteringMaterial(
            **cls.make_item(data, row),
            **cls.make_contrib(data, row, "locations", "remarks"),
            category=BolsteringMaterialCategory.from_row(row),
        )