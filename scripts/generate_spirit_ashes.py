from scripts import er_params
from typing import Dict, Iterator, List, Tuple
from scripts.er_params.enums import GoodsType, GoodsRarity, ItemIDFlag
from scripts.erdb_common import GeneratorDataBase, get_schema_properties, parse_description

ParamRow = er_params.ParamRow
ParamDict = er_params.ParamDict

def _is_base_spirit_ash(row: ParamRow) -> bool:
    return row.is_base_item() and row.get("goodsType") in [GoodsType.LESSER, GoodsType.GREATER]

def _find_upgrade_costs(goods: ParamDict, base_item_id: int) -> List[int]:
    return [goods[str(item_id)].get_int("reinforcePrice") for item_id in range(base_item_id, base_item_id + 10)]

def iterate_spirit_ashes(self: GeneratorDataBase, spirit_ashes: ParamDict) -> Iterator[ParamRow]:
    for row in spirit_ashes.values():
        if _is_base_spirit_ash(row):
            yield row

def make_spirit_ash_object(self: GeneratorDataBase, row: ParamRow) -> Dict:
    goods = self.main_param
    upgrade_materials = self.params["upgrade_materials"]
    summaries = self.msgs["summaries"]
    summon_names = self.msgs["summon_names"]
    descriptions = self.msgs["descriptions"]

    # HACK: reinforceMaterialId links to EquipMtrlSetParam which THEN links to the actual EquipParamGoods
    # this simply checks if the name of EquipMtrlSetParam somewhat matches without following everything
    upgrade_material = upgrade_materials[row.get("reinforceMaterialId")].name.startswith("Grave")
    upgrade_material = "Grave Glovewort" if upgrade_material else "Ghost Glovewort"

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

def get_spirit_ash_schema() -> Tuple[Dict, Dict[str, Dict]]:
    return get_schema_properties("item", "spirit-ashes/definitions/SpiritAsh")

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

    schema_retriever = get_spirit_ash_schema
    main_param_iterator = iterate_spirit_ashes
    construct_object = make_spirit_ash_object