from typing import Dict, Iterator, List, Tuple
from scripts.er_params import ParamDict, ParamRow
from scripts.er_params.enums import GoodsType, GoodsRarity, ItemIDFlag
from scripts.erdb_common import GeneratorDataBase, find_offset_indices, get_schema_properties, parse_description

def _is_base_spirit_ash(row: ParamRow) -> bool:
    return row.is_base_item() and row.get("goodsType") in [GoodsType.LESSER, GoodsType.GREATER]

def _find_upgrade_costs(goods: ParamDict, base_item_id: int) -> List[int]:
    indices, _ = find_offset_indices(base_item_id, goods, possible_maxima=[9]) # not 10, ignore last one
    return [goods[str(i)].get_int("reinforcePrice") for i in indices]

class SpiritAshGeneratorData(GeneratorDataBase):
    Base = GeneratorDataBase

    output_file: str = "spirit-ashes.json"
    schema_file: str = "spirit-ashes.schema.json"
    element_name: str = "SpiritAshes"

    main_param_retriever = Base.ParamDictRetriever("EquipParamGoods", ItemIDFlag.GOODS)

    param_retrievers = {
        "upgrade_materials": Base.ParamDictRetriever("EquipMtrlSetParam", ItemIDFlag.NON_EQUIPABBLE)
    }

    msgs_retrievers = {
        "summaries": Base.MsgsRetriever("GoodsInfo"),
        "summon_names": Base.MsgsRetriever("GoodsInfo2"),
        "descriptions": Base.MsgsRetriever("GoodsCaption")
    }

    lookup_retrievers = {}

    @staticmethod
    def schema_retriever() -> Tuple[Dict, Dict[str, Dict]]:
        return get_schema_properties("item/properties", "spirit-ashes/definitions/SpiritAsh/properties")

    def main_param_iterator(self, spirit_ashes: ParamDict) -> Iterator[ParamRow]:
        for row in spirit_ashes.values():
            if _is_base_spirit_ash(row):
                yield row

    def construct_object(self, row: ParamRow) -> Dict:
        goods = self.main_param
        upgrade_materials = self.params["upgrade_materials"]
        summaries = self.msgs["summaries"]
        summon_names = self.msgs["summon_names"]
        descriptions = self.msgs["descriptions"]

        upgrade_material = upgrade_materials[row.get("reinforceMaterialId")]
        upgrade_material = goods[upgrade_material.get("materialId01")].name.replace(" [1]", "")
        assert upgrade_material in ["Grave Glovewort", "Ghost Glovewort"]

        return {
            "full_hex_id": row.index_hex,
            "id": row.index,
            "name": row.name,
            "summary": summaries[row.index],
            "description": parse_description(descriptions[row.index]),
            "summon_name": summon_names[row.index].strip(), # sometimes trailing spaces
            "is_tradable": row.get("disableMultiDropShare") == "0",
            "price_sold": row.get_int_corrected("sellValue"),
            "max_held": row.get_int("maxNum"),
            "max_stored": row.get_int("maxRepositoryNum"),
            # locations -- cannot autogenerate, make sure not to overwrite
            # remarks -- cannot autogenerate, make sure not to overwrite
            "fp_cost": row.get_int_corrected("consumeMP"),
            "hp_cost": row.get_int_corrected("consumeHP"),
            "rarity": GoodsRarity(row.get_int("rarity")).name.lower(),
            # summon_quantity -- cannot autogenerate, make sure not to overwrite
            # abilities -- cannot autogenerate, make sure not to overwrite
            "upgrade_material": upgrade_material,
            "upgrade_costs": _find_upgrade_costs(goods, row.index)
        }