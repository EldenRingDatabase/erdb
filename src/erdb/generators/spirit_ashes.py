from erdb.typing.models.spirit_ash import SpiritAsh
from erdb.typing.params import ParamDict, ParamRow
from erdb.typing.enums import GoodsType, ItemIDFlag, SpiritAshUpgradeMaterial
from erdb.utils.common import strip_invalid_name, find_offset_indices
from erdb.generators._base import GeneratorDataBase


def _is_base_spirit_ash(row: ParamRow) -> bool:
    return row.is_base_item() and row.get("goodsType") in [GoodsType.LESSER, GoodsType.GREATER]

def _find_upgrade_costs(goods: ParamDict, base_item_id: int) -> list[int]:
    indices, _ = find_offset_indices(base_item_id, goods, possible_maxima=[9]) # not 10, ignore last one
    return [goods[str(i)].get_int("reinforcePrice") for i in indices]

class SpiritAshGeneratorData(GeneratorDataBase):
    Base = GeneratorDataBase

    @staticmethod # override
    def output_file() -> str:
        return "spirit-ashes.json"

    @staticmethod # override
    def element_name() -> str:
        return "SpiritAshes"

    @staticmethod # override
    def model() -> SpiritAsh:
        return SpiritAsh

    # override
    def get_key_name(self, row: ParamRow) -> str:
        return strip_invalid_name(self.msgs["names"][row.index])

    main_param_retriever = Base.ParamDictRetriever("EquipParamGoods", ItemIDFlag.GOODS)

    param_retrievers = {
        "upgrade_materials": Base.ParamDictRetriever("EquipMtrlSetParam", ItemIDFlag.NON_EQUIPABBLE)
    }

    msgs_retrievers = {
        "names": Base.MsgsRetriever("GoodsName"),
        "summaries": Base.MsgsRetriever("GoodsInfo"),
        "summon_names": Base.MsgsRetriever("GoodsInfo2"),
        "descriptions": Base.MsgsRetriever("GoodsCaption")
    }

    lookup_retrievers = {}

    def main_param_iterator(self, spirit_ashes: ParamDict):
        for row in spirit_ashes.values():
            if _is_base_spirit_ash(row):
                yield row

    def construct_object(self, row: ParamRow) -> SpiritAsh:
        goods = self.main_param
        upgrade_materials = self.params["upgrade_materials"]
        names = self.msgs["names"]
        summon_names = self.msgs["summon_names"]

        upgrade_material = upgrade_materials[row.get("reinforceMaterialId")]
        upgrade_material = names[upgrade_material.get_int("materialId01")].removesuffix("[1]").strip()
        upgrade_material = {
            "Grave Glovewort": SpiritAshUpgradeMaterial.GRAVE_GLOVEWORT,
            "Ghost Glovewort": SpiritAshUpgradeMaterial.GHOST_GLOVEWORT,
        }[upgrade_material]

        return SpiritAsh(
            **self.get_fields_item(row),
            **self.get_fields_user_data(row, "locations", "remarks", "summon_quantity", "abilities"),
            summon_name=summon_names[row.index].strip(), # sometimes trailing spaces
            fp_cost=row.get_int_corrected("consumeMP"),
            hp_cost=row.get_int_corrected("consumeHP"),
            upgrade_material=upgrade_material,
            upgrade_costs=_find_upgrade_costs(goods, row.index)
        )