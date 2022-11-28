from erdb.shop import Product, Material
from erdb.typing.models.crafting_material import CraftingMaterial
from erdb.typing.models import NonEmptyStr
from erdb.typing.params import ParamRow
from erdb.typing.enums import GoodsType, ItemIDFlag
from erdb.typing.categories import CraftingMaterialCategory
from erdb.typing.api_version import ApiVersion
from erdb.table._retrievers import ParamDictRetriever, MsgsRetriever, RetrieverData, ShopRetriever
from erdb.table._common import RowPredicate, TableSpecContext


class CraftingMaterialTableSpec(TableSpecContext):
    model = {
        ApiVersion.VER_1: CraftingMaterial,
    }

    main_param_retriever = ParamDictRetriever("EquipParamGoods", ItemIDFlag.GOODS)

    predicates: list[RowPredicate] = [
        lambda row: row["goodsType"] == GoodsType.CRAFTING_MATERIAL
    ]

    msg_retrievers = {
        "names": MsgsRetriever("GoodsName"),
        "armament_names": MsgsRetriever("WeaponName"),
        "summaries": MsgsRetriever("GoodsInfo"),
        "hints": MsgsRetriever("GoodsInfo2"),
        "descriptions": MsgsRetriever("GoodsCaption")
    }

    shop_retrievers = {
        "crafting_shop": ShopRetriever(
            shop_lineup_id_min=None, shop_lineup_id_max=None,
            material_set_id_min=300000, material_set_id_max=400000,
            recipe=True
        )
    }

    @classmethod
    def make_object(cls, api: ApiVersion, data: RetrieverData, row: ParamRow):
        crafting_shop = data.shops["crafting_shop"]

        names = {
            Product.Category.GOOD: data.msgs["names"],
            Product.Category.WEAPON: data.msgs["armament_names"]
        }

        material = Material(row.index, Material.Category.GOOD)
        lineups = crafting_shop.get_lineups_from_material(material)
        assert len(lineups) > 0

        return CraftingMaterial(
            **cls.make_item(data, row),
            **cls.make_contrib(data, row, "locations", "remarks"),
            category=CraftingMaterialCategory.from_row(row),
            hint=NonEmptyStr(data.msgs["hints"].get(row.index, "")),
            products=[NonEmptyStr(cls.parse_name(names[l.product.category][l.product.index])) for l in lineups]
        )