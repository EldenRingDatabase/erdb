from erdb.typing.models.spirit_ash import SpiritAsh
from erdb.typing.params import ParamDict, ParamRow
from erdb.typing.enums import GoodsType, ItemIDFlag, SpiritAshUpgradeMaterial
from erdb.typing.api_version import ApiVersion
from erdb.utils.common import find_offset_indices
from erdb.table._retrievers import ParamDictRetriever, MsgsRetriever, RetrieverData
from erdb.table._common import RowPredicate, TableSpecContext


def _find_upgrade_costs(goods: ParamDict, base_item_id: int) -> list[int]:
    indices, _ = find_offset_indices(base_item_id, goods, possible_maxima=[9]) # not 10, ignore last one
    return [goods[i]["reinforcePrice"].as_int for i in indices]

class SpiritAshTableSpec(TableSpecContext):
    model = {
        ApiVersion.VER_1: SpiritAsh,
    }

    main_param_retriever = ParamDictRetriever("EquipParamGoods", ItemIDFlag.GOODS)

    predicates: list[RowPredicate] = [
        lambda row: row.is_base_item,
        lambda row: row["goodsType"] in [GoodsType.LESSER, GoodsType.GREATER],
    ]

    param_retrievers = {
        "upgrade_materials": ParamDictRetriever("EquipMtrlSetParam", ItemIDFlag.NON_EQUIPABBLE)
    }

    msg_retrievers = {
        "names": MsgsRetriever("GoodsName"),
        "summaries": MsgsRetriever("GoodsInfo"),
        "summon_names": MsgsRetriever("GoodsInfo2"),
        "descriptions": MsgsRetriever("GoodsCaption")
    }

    @classmethod
    def make_object(cls, api: ApiVersion, data: RetrieverData, row: ParamRow):
        upgrade_materials = data.params["upgrade_materials"]
        names = data.msgs["names"]
        summon_names = data.msgs["summon_names"]

        upgrade_material = upgrade_materials[row["reinforceMaterialId"].as_int]
        upgrade_material = names[upgrade_material["materialId01"].as_int].removesuffix("[1]").strip()
        upgrade_material = {
            "Grave Glovewort": SpiritAshUpgradeMaterial.GRAVE_GLOVEWORT,
            "Ghost Glovewort": SpiritAshUpgradeMaterial.GHOST_GLOVEWORT,
        }[upgrade_material]

        return SpiritAsh(
            **cls.make_item(data, row),
            **cls.make_contrib(data, row, "locations", "remarks", "summon_quantity", "abilities"),
            summon_name=summon_names[row.index].strip(), # sometimes trailing spaces
            fp_cost=row["consumeMP"].get_int(0),
            hp_cost=row["consumeHP"].get_int(0),
            upgrade_material=upgrade_material,
            upgrade_costs=_find_upgrade_costs(data.main_param, row.index)
        )