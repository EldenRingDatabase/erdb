from erdb.typing.models.bolstering_material import BolsteringMaterial
from erdb.typing.categories import BolsteringMaterialCategory
from erdb.typing.params import ParamDict, ParamRow
from erdb.typing.enums import GoodsType, ItemIDFlag
from erdb.utils.common import strip_invalid_name
from erdb.generators._base import GeneratorDataBase


class BolsteringMaterialGeneratorData(GeneratorDataBase):
    Base = GeneratorDataBase

    @staticmethod # override
    def output_file() -> str:
        return "bolstering-materials.json"

    @staticmethod # override
    def element_name() -> str:
        return "BolsteringMaterials"

    @staticmethod # override
    def model() -> BolsteringMaterial:
        return BolsteringMaterial

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

    def main_param_iterator(self, materials: ParamDict):
        for row in materials.values():
            if row.get("goodsType") == GoodsType.REINFORCEMENT_MATERIAL:
                yield row

    def construct_object(self, row: ParamRow) -> BolsteringMaterial:
        return BolsteringMaterial(
            **self.get_fields_item(row),
            **self.get_fields_user_data(row, "locations", "remarks"),
            category=BolsteringMaterialCategory.from_row(row),
        )