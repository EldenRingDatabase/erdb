import json
import math
import er_params
import er_shop
from typing import Dict
from er_params.enums import ItemIDFlag
from sp_effect_parser import parse_effects
from erdb_common import (
    get_schema_properties, get_schema_enums, get_item_msg,
    parse_description, update_nested, patch_keys, validate_and_write)

ParamRow = er_params.ParamRow
ParamDict = er_params.ParamDict

_EFFECT_FIELDS = ["residentSpEffectId", "residentSpEffectId2", "residentSpEffectId3"]

def iterate_armor(protectors: ParamDict):
    for row in protectors.values():
        if row.index >= 40000 and len(row.name) > 0:
            yield row

def get_category(category: int) -> str:
    """
    There is an unused category 4 (hair). It's not part of the schema,
    so let's have this throw an error in case it's ever used.
    """
    return {0: "head", 1: "body", 2: "arms", 3: "legs"}[category]

def get_absorptions(row: ParamRow) -> Dict[str, float]:
    def _parse(val: float):
        return round((1 - val) * 100, 1)

    return {
        "physical": _parse(row.get_float("neutralDamageCutRate")),
        "strike": _parse(row.get_float("blowDamageCutRate")),
        "slash": _parse(row.get_float("slashDamageCutRate")),
        "pierce": _parse(row.get_float("thrustDamageCutRate")),
        "magic": _parse(row.get_float("magicDamageCutRate")),
        "fire": _parse(row.get_float("fireDamageCutRate")),
        "lightning": _parse(row.get_float("thunderDamageCutRate")),
        "holy": _parse(row.get_float("darkDamageCutRate")),
    }

def get_resistances(row: ParamRow) -> Dict[str, int]:
    def _check_equal(*values: int):
        ret = values[0]
        for val in values:
            if ret != val:
                print(f"WARNING: Values mismatch for {row.name} resistances ({ret} != {val}), displaying the latter.")
            ret = val
        return ret

    return {
        "immunity": _check_equal(row.get_int("resistPoison"), row.get_int("resistDisease")),
        "robustness": _check_equal(row.get_int("resistFreeze"), row.get_int("resistBlood")),
        "focus": _check_equal(row.get_int("resistSleep"), row.get_int("resistMadness")),
        "vitality": _check_equal(row.get_int("resistCurse")),
        "poise": round(row.get_float("toughnessCorrectRate") * 1000)
    }

def make_armor_object(row: ParamRow, protectors: ParamDict, effects: ParamDict, armor_lookup: er_shop.Lookup, summaries: Dict[int, str], descriptions: Dict[int, str]) -> Dict:
    material = er_shop.Material(row.index, er_shop.Material.Category.PROTECTOR)
    lineups = armor_lookup.get_lineups_from_material(material)
    assert len(lineups) in [0, 2], "Each armor should have either none or self-/boc-made alterations"
    altered = "" if len(lineups) == 0 else protectors[str(lineups[0].product.index)].name

    return {
        "full_hex_id": row.index_hex,
        "id": row.index,
        "name": row.name,
        "summary": summaries.get(row.index, "no summary"),
        "description": parse_description(descriptions[row.index]),
        "is_tradable": row.get("disableMultiDropShare") == "0",
        "price_sold": row.get_int_corrected("sellValue"),
        "max_held": 999,
        "max_stored": 999,
        # locations -- cannot autogenerate, make sure not to overwrite
        # remarks -- cannot autogenerate, make sure not to overwrite
        "category": get_category(row.get_int("protectorCategory")),
        "altered": altered,
        "weight": row.get_float("weight"),
        "absorptions": get_absorptions(row),
        "resistances": get_resistances(row),
        "effects": parse_effects(row, effects, *_EFFECT_FIELDS),
    }

def main():
    with open("./armor.json", mode="r") as f:
        armor_full = json.load(f)

    armor = armor_full["ArmorPieces"]
    protectors = er_params.load("EquipParamProtector", "1.04.1", ItemIDFlag.PROTECTORS)

    effects = er_params.load("SpEffectParam", "1.04.1", ItemIDFlag.NON_EQUIPABBLE)

    properties, store = get_schema_properties("item", "armor/definitions/ArmorPiece")
    store.update(get_schema_properties("effect")[1])
    store.update(get_schema_enums("armor-names", "attribute-names", "attack-types", "effect-types", "health-conditions", "attack-conditions"))

    summaries = get_item_msg("ProtectorInfo", "1.04.1")
    descriptions = get_item_msg("ProtectorCaption", "1.04.1")

    shop_lineup = er_params.load_ids("ShopLineupParam", "1.04.1", ItemIDFlag.NON_EQUIPABBLE, id_min=110000, id_max=112000)
    material_sets = er_params.load_ids("EquipMtrlSetParam", "1.04.1", ItemIDFlag.NON_EQUIPABBLE, id_min=900100, id_max=901000)
    armor_lookup = er_shop.Lookup(shop_lineup, material_sets)

    for row in iterate_armor(protectors):
        new_obj = make_armor_object(row, protectors, effects, armor_lookup, summaries, descriptions)
        obj = armor.get(row.name, {})

        update_nested(obj, new_obj)
        armor[row.name] = patch_keys(obj, properties)

    armor_full["ArmorPieces"] = armor
    ok = validate_and_write("./armor.json", "armor.schema.json", armor_full, store)

    if not ok:
        raise RuntimeError("Validation failed")

if __name__ == "__main__":
    main()