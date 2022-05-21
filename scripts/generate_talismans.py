import json
import er_params
from typing import Dict, List, Tuple
from er_params.enums import ItemIDFlag
from sp_effect_parser import parse_effects
from erdb_common import (
    get_schema_properties, get_schema_enums,
    update_nested, patch_keys, validate_and_write)

ParamRow = er_params.ParamRow
ParamDict = er_params.ParamDict

_EFFECT_FIELDS = ["refId"]

def iterate_talismans(accessories: ParamDict):
    for row in accessories.values():
        if row.index >= 1000 and row.index < 999999:
            yield row

def find_min_max_effect_ids(accessories: ParamDict, *effect_fields: str) -> Tuple[int, int]:
    min_id: int = 999999999
    max_id: int = 0

    for row in iterate_talismans(accessories):
        for field in effect_fields:
            this_id = row.get_int_corrected(field)
            min_id = min(min_id, this_id)
            max_id = max(max_id, this_id)

    return min_id, (max_id + 1000) # account for potential variants mentioned inside spEffectParam itself

def find_conflicts(group: int, accessories: ParamDict) -> List[str]:
    return [t.name for t in accessories.values() if t.get_int("accessoryGroup") == group and len(t.name) > 0]

def make_talisman_object(row: ParamRow, accessories: ParamDict, effects: ParamDict) -> Dict:
    return {
        "full_hex_id": row.index_hex,
        "id": row.index,
        "name": row.name,
        # summary -- cannot autogenerate, make sure not to overwrite
        # description -- cannot autogenerate, make sure not to overwrite
        "is_tradable": row.get("disableMultiDropShare") == "0",
        "price_sold": row.get_int_corrected("sellValue"),
        "max_held": 999,
        "max_stored": 999,
        # locations -- cannot autogenerate, make sure not to overwrite
        # remarks -- cannot autogenerate, make sure not to overwrite
        "weight": float(row.get("weight")),
        "effects": parse_effects(row, effects, *_EFFECT_FIELDS),
        "conflicts": find_conflicts(row.get_int("accessoryGroup"), accessories),
    }

def main():
    with open("./talismans.json", mode="r") as f:
        talismans_full = json.load(f)

    talismans = talismans_full["Talismans"]
    accessories = er_params.load("EquipParamAccessory", "1.04.1", ItemIDFlag.ACCESSORIES)

    effect_id_min, effect_id_max = find_min_max_effect_ids(accessories, *_EFFECT_FIELDS)
    effects = er_params.load_ids("SpEffectParam", "1.04.1", ItemIDFlag.NON_EQUIPABBLE, effect_id_min, effect_id_max)

    properties, store = get_schema_properties("item", "talismans/definitions/Talisman")
    store.update(get_schema_enums("talisman-names", "attribute-names", "attack-types", "effect-types", "health-conditions", "attack-conditions"))

    for row in iterate_talismans(accessories):
        new_obj = make_talisman_object(row, accessories, effects)
        obj = talismans.get(row.name, {})

        update_nested(obj, new_obj)
        talismans[row.name] = patch_keys(obj, properties)

    talismans_full["Talismans"] = talismans
    ok = validate_and_write("./talismans.json", "talismans.schema.json", talismans_full, store)

    if not ok:
        raise RuntimeError("Validation failed")

if __name__ == "__main__":
    main()