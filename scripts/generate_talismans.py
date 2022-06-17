from typing import Dict, List, Tuple
from scripts.er_params import ParamDict, ParamRow
from scripts.er_params.enums import ItemIDFlag
from scripts.sp_effect_parser import parse_effects
from scripts.erdb_common import GeneratorDataBase, get_schema_properties, get_schema_enums, parse_description

def _find_conflicts(group: int, accessories: ParamDict) -> List[str]:
    return [t.name for t in accessories.values() if t.get_int("accessoryGroup") == group and len(t.name) > 0]

class TalismanGeneratorData(GeneratorDataBase):
    Base = GeneratorDataBase

    @staticmethod
    def output_file() -> str:
        return "talismans.json"

    @staticmethod
    def schema_file() -> str:
        return "talismans.schema.json"

    @staticmethod
    def element_name() -> str:
        return "Talismans"

    main_param_retriever = Base.ParamDictRetriever("EquipParamAccessory", ItemIDFlag.ACCESSORIES)

    param_retrievers = {
        "effects": Base.ParamDictRetriever("SpEffectParam", ItemIDFlag.NON_EQUIPABBLE, id_min=310000, id_max=400000)
    }

    msgs_retrievers = {
        "summaries": Base.MsgsRetriever("AccessoryInfo"),
        "descriptions": Base.MsgsRetriever("AccessoryCaption")
    }

    lookup_retrievers = {}

    @staticmethod
    def schema_retriever() -> Tuple[Dict, Dict[str, Dict]]:
        properties, store = get_schema_properties(
            "item/properties",
            "item/definitions/ItemUserData/properties",
            "talismans/definitions/Talisman/properties")
        store.update(get_schema_properties("effect")[1])
        store.update(get_schema_enums("talisman-names", "attribute-names", "attack-types", "effect-types", "health-conditions", "attack-conditions"))
        return properties, store

    def main_param_iterator(self, talismans: ParamDict):
        for row in talismans.values():
            if row.index >= 1000 and row.index < 999999:
                yield row

    def construct_object(self, row: ParamRow) -> Dict:
        talismans = self.main_param
        effects = self.params["effects"]
        summaries = self.msgs["summaries"]
        descriptions = self.msgs["descriptions"]

        return {
            "full_hex_id": row.index_hex,
            "id": row.index,
            "name": row.name,
            "summary": summaries[row.index],
            "description": parse_description(descriptions[row.index]),
            "is_tradable": row.get("disableMultiDropShare") == "0",
            "price_sold": row.get_int_corrected("sellValue"),
            "max_held": 999,
            "max_stored": 999,
            "locations": self.get_user_data(row.name, "locations"),
            "remarks": self.get_user_data(row.name, "remarks"),
            "weight": row.get_float("weight"),
            "effects": parse_effects(row, effects, "refId"),
            "conflicts": _find_conflicts(row.get_int("accessoryGroup"), talismans),
        }