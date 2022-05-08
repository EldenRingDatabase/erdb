import json
import er_params
from typing import Dict, List
from er_params.enums import GoodsType, GoodsRarity, ItemIDFlag
from erdb_common import update_nested, get_schema_properties, patch_keys, validate_and_write

ParamRow = er_params.ParamRow
ParamDict = er_params.ParamDict

def is_base_spirit_ash(row: ParamRow) -> bool:
    return row.is_base_item() and row.get("goodsType") in [GoodsType.LESSER, GoodsType.GREATER]

def find_upgrade_costs(goods: ParamDict, base_item_id: int) -> List[int]:
    return [goods[str(item_id)].get_int("reinforcePrice") for item_id in range(base_item_id, base_item_id + 10)]

def make_spirit_ash_object(row: ParamRow, goods: ParamDict, upgrade_mats: ParamDict) -> Dict:
    # HACK: reinforceMaterialId links to EquipMtrlSetParam which THEN links to the actual EquipParamGoods
    # this simply checks if the name of EquipMtrlSetParam somewhat matches without following everything
    upgrade_material = upgrade_mats[row.get("reinforceMaterialId")].name.startswith("Grave")
    upgrade_material = "Grave Glovewort" if upgrade_material else "Ghost Glovewort"

    return {
        "full_hex_id": row.index_hex,
        "id": row.index,
        "name": row.name,
        # summary -- cannot autogenerate, make sure not to overwrite
        # description -- cannot autogenerate, make sure not to overwrite
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
        "upgrade_costs": find_upgrade_costs(goods, row.index)
    }

def main():
    with open("./spirit-ashes.json", mode="r") as f:
        spirit_ashes_full = json.load(f)

    spirit_ashes = spirit_ashes_full["SpiritAshes"]
    goods = er_params.load("EquipParamGoods", "1.04.1", ItemIDFlag.GOODS)
    upgrade_mats = er_params.load("EquipMtrlSetParam", "1.04.1", ItemIDFlag.NON_EQUIPABBLE)
    properties, store = get_schema_properties("item", "spirit-ashes/definitions/SpiritAsh")

    for row in goods.values():
        if is_base_spirit_ash(row):
            obj = make_spirit_ash_object(row, goods, upgrade_mats)
            ash = spirit_ashes.get(row.name, {})

            update_nested(ash, obj)
            spirit_ashes[row.name] = patch_keys(ash, properties)

    spirit_ashes_full["SpiritAshes"] = spirit_ashes
    ok = validate_and_write("./spirit-ashes.json", "spirit-ashes.schema.json", spirit_ashes_full, store)

    if not ok:
        raise RuntimeError("Validation failed")

if __name__ == "__main__":
    main()