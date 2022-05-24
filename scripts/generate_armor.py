from typing import Dict, Tuple, Iterator
from scripts import er_params, er_shop
from scripts.er_params.enums import ItemIDFlag
from scripts.sp_effect_parser import parse_effects
from scripts.erdb_common import GeneratorDataBase, get_schema_properties, get_schema_enums, parse_description

ParamRow = er_params.ParamRow
ParamDict = er_params.ParamDict

def _get_category(category: int) -> str:
    """
    There is an unused category 4 (hair). It's not part of the schema,
    so let's have this throw an error in case it's ever used.
    """
    return {0: "head", 1: "body", 2: "arms", 3: "legs"}[category]

def _get_absorptions(row: ParamRow) -> Dict[str, float]:
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

def _get_resistances(row: ParamRow) -> Dict[str, int]:
    def _check_equal(*values: int):
        ret = values[0]
        for val in values:
            if ret != val:
                print(f"WARNING: Values mismatch for {row.name} resistances ({ret} != {val}), displaying the latter.", flush=True)
            ret = val
        return ret

    return {
        "immunity": _check_equal(row.get_int("resistPoison"), row.get_int("resistDisease")),
        "robustness": _check_equal(row.get_int("resistFreeze"), row.get_int("resistBlood")),
        "focus": _check_equal(row.get_int("resistSleep"), row.get_int("resistMadness")),
        "vitality": _check_equal(row.get_int("resistCurse")),
        "poise": round(row.get_float("toughnessCorrectRate") * 1000)
    }

def iterate_armor(self: GeneratorDataBase, armor: ParamDict) -> Iterator[ParamRow]:
    for row in armor.values():
        if row.index >= 40000 and len(row.name) > 0:
            yield row

def make_armor_object(self: GeneratorDataBase, row: ParamRow) -> Dict:
    armor = self.main_param
    effects = self.params["effects"]
    summaries = self.msgs["summaries"]
    descriptions = self.msgs["descriptions"]
    armor_lookup = self.lookups["armor_lookup"]

    material = er_shop.Material(row.index, er_shop.Material.Category.PROTECTOR)
    lineups = armor_lookup.get_lineups_from_material(material)
    assert len(lineups) in [0, 2], "Each armor should have either none or self-/boc-made alterations"
    altered = "" if len(lineups) == 0 else armor[str(lineups[0].product.index)].name

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
        "category": _get_category(row.get_int("protectorCategory")),
        "altered": altered,
        "weight": row.get_float("weight"),
        "absorptions": _get_absorptions(row),
        "resistances": _get_resistances(row),
        "effects": parse_effects(row, effects, "residentSpEffectId", "residentSpEffectId2", "residentSpEffectId3"),
    }

def get_armor_schema() -> Tuple[Dict, Dict[str, Dict]]:
    properties, store = get_schema_properties("item", "armor/definitions/ArmorPiece")
    store.update(get_schema_properties("effect")[1])
    store.update(get_schema_enums("armor-names", "attribute-names", "attack-types", "effect-types", "health-conditions", "attack-conditions"))
    return properties, store

class ArmorGeneratorData(GeneratorDataBase):
    Base = GeneratorDataBase

    output_file: str = "armor.json"
    schema_file: str = "armor.schema.json"
    element_name: str = "ArmorPieces"

    main_param_retriever = Base.ParamDictRetriever("EquipParamProtector", ItemIDFlag.PROTECTORS)

    param_retrievers = {
        "effects": Base.ParamDictRetriever("SpEffectParam", ItemIDFlag.NON_EQUIPABBLE)
    }

    msgs_retrievers = {
        "summaries": Base.MsgsRetriever("ProtectorInfo"),
        "descriptions": Base.MsgsRetriever("ProtectorCaption")
    }

    lookup_retrievers = {
        "armor_lookup": Base.LookupRetriever(
            shop_lineup_id_min=110000, shop_lineup_id_max=112000,
            material_set_id_min=900100, material_set_id_max=901000,
        )
    }

    schema_retriever = get_armor_schema
    main_param_iterator = iterate_armor
    construct_object = make_armor_object