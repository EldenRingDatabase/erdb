from typing import Dict, Iterator, Tuple
from scripts import er_shop
from scripts.er_params import ParamDict, ParamRow
from scripts.er_params.enums import GoodsSortGroupID, GoodsType, ItemIDFlag
from scripts.erdb_common import get_schema_enums, get_schema_properties, strip_invalid_name
from scripts.erdb_generators._base import GeneratorDataBase

def _get_category(row: ParamRow) -> str:
    G = GoodsSortGroupID
    return {
        G.GROUP_1: "Fauna",
        G.GROUP_2: "Flora",
        G.GROUP_3: "Object",
    }[row.get_int("sortGroupId")]

class CraftingMaterialGeneratorData(GeneratorDataBase):
    Base = GeneratorDataBase

    @staticmethod # override
    def output_file() -> str:
        return "crafting-materials.json"

    @staticmethod # override
    def schema_file() -> str:
        return "crafting-materials.schema.json"

    @staticmethod # override
    def element_name() -> str:
        return "CraftingMaterials"

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

    @staticmethod
    def schema_retriever() -> Tuple[Dict, Dict[str, Dict]]:
        properties, store = get_schema_properties(
            "item/properties",
            "item/definitions/ItemUserData/properties",
            "crafting-materials/definitions/CraftingMaterial/properties")
        store.update(get_schema_enums("item-names", "ammo-names"))
        return properties, store

    def main_param_iterator(self, materials: ParamDict) -> Iterator[ParamRow]:
        for row in materials.values():
            if row.get("goodsType") == GoodsType.CRAFTING_MATERIAL:
                yield row

    def construct_object(self, row: ParamRow) -> Dict:
        crafting_lookup = self.lookups["crafting_lookup"]

        Cat = er_shop.Product.Category
        names = {
            Cat.GOOD: self.msgs["names"],
            Cat.WEAPON: self.msgs["armament_names"]
        }

        material = er_shop.Material(row.index, er_shop.Material.Category.GOOD)
        lineups = crafting_lookup.get_lineups_from_material(material)
        assert len(lineups) > 0

        return self.get_fields_item(row) | self.get_fields_user_data(row, "locations", "remarks") | {
            "category": _get_category(row),
            "hint": self.msgs["hints"].get(row.index, ""),
            "products": [strip_invalid_name(names[l.product.category][l.product.index]) for l in lineups]
        }