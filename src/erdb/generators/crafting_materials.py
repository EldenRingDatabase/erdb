from erdb.shop import Product, Material
from erdb.typing.models.crafting_material import CraftingMaterial
from erdb.typing.params import ParamDict, ParamRow
from erdb.typing.enums import GoodsType, ItemIDFlag
from erdb.typing.categories import CraftingMaterialCategory
from erdb.utils.common import strip_invalid_name
from erdb.generators._base import GeneratorDataBase


class CraftingMaterialGeneratorData(GeneratorDataBase):
    Base = GeneratorDataBase

    @staticmethod # override
    def output_file() -> str:
        return "crafting-materials.json"

    @staticmethod # override
    def element_name() -> str:
        return "CraftingMaterials"

    @staticmethod # override
    def model() -> CraftingMaterial:
        return CraftingMaterial

    # override
    def get_key_name(self, row: ParamRow) -> str:
        return strip_invalid_name(self.msgs["names"][row.index])

    main_param_retriever = Base.ParamDictRetriever("EquipParamGoods", ItemIDFlag.GOODS)

    param_retrievers = {}

    msgs_retrievers = {
        "names": Base.MsgsRetriever("GoodsName"),
        "armament_names": Base.MsgsRetriever("WeaponName"),
        "summaries": Base.MsgsRetriever("GoodsInfo"),
        "hints": Base.MsgsRetriever("GoodsInfo2"),
        "descriptions": Base.MsgsRetriever("GoodsCaption")
    }

    lookup_retrievers = {
        "crafting_lookup": Base.LookupRetriever(
            shop_lineup_id_min=None, shop_lineup_id_max=None,
            material_set_id_min=300000, material_set_id_max=400000,
            recipe=True
        )
    }

    def main_param_iterator(self, materials: ParamDict):
        for row in materials.values():
            if row.get("goodsType") == GoodsType.CRAFTING_MATERIAL:
                yield row

    def construct_object(self, row: ParamRow) -> CraftingMaterial:
        crafting_lookup = self.lookups["crafting_lookup"]

        names = {
            Product.Category.GOOD: self.msgs["names"],
            Product.Category.WEAPON: self.msgs["armament_names"]
        }

        material = Material(row.index, Material.Category.GOOD)
        lineups = crafting_lookup.get_lineups_from_material(material)
        assert len(lineups) > 0

        return CraftingMaterial(
            **self.get_fields_item(row),
            **self.get_fields_user_data(row, "locations", "remarks"),
            category=CraftingMaterialCategory.from_row(row),
            hint=self.msgs["hints"].get(row.index, ""),
            products=[strip_invalid_name(names[l.product.category][l.product.index]) for l in lineups]
        )