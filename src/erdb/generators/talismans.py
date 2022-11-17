from typing import Dict, List, Tuple

import erdb.loaders.schema as schema
from erdb.effect_parser import parse_effects
from erdb.typing.params import ParamDict, ParamRow
from erdb.typing.enums import ItemIDFlag
from erdb.utils.common import strip_invalid_name
from erdb.generators._base import GeneratorDataBase


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

    # override
    def get_key_name(self, row: ParamRow) -> str:
        return strip_invalid_name(self.msgs["names"][row.index])

    def _find_conflicts(self, group: int, accessories: ParamDict) -> List[str]:
        return [self.get_key_name(t) for t in accessories.values() if t.get_int("accessoryGroup") == group and t.get_int("sortId") < 9999999]

    main_param_retriever = Base.ParamDictRetriever("EquipParamAccessory", ItemIDFlag.ACCESSORIES)

    param_retrievers = {
        "effects": Base.ParamDictRetriever("SpEffectParam", ItemIDFlag.NON_EQUIPABBLE, id_min=310000, id_max=400000)
    }

    msgs_retrievers = {
        "names": Base.MsgsRetriever("AccessoryName"),
        "summaries": Base.MsgsRetriever("AccessoryInfo"),
        "descriptions": Base.MsgsRetriever("AccessoryCaption")
    }

    lookup_retrievers = {}

    @staticmethod
    def schema_retriever() -> Tuple[Dict, Dict[str, Dict]]:
        properties, store = schema.load_properties(
            "item/properties",
            "item/definitions/ItemUserData/properties",
            "talismans/definitions/Talisman/properties")
        store.update(schema.load_properties("effect")[1])
        store.update(schema.load_enums("talisman-names", "attribute-names", "attack-types", "effect-types", "health-conditions", "attack-conditions"))
        return properties, store

    def main_param_iterator(self, talismans: ParamDict):
        for row in talismans.values():
            if row.index >= 1000 and row.index < 999999:
                yield row

    def construct_object(self, row: ParamRow) -> Dict:
        talismans = self.main_param
        effects = self.params["effects"]

        return self.get_fields_item(row) | self.get_fields_user_data(row, "locations", "remarks") | {
            "weight": row.get_float("weight"),
            "effects": parse_effects(row, effects, "refId"),
            "conflicts": self._find_conflicts(row.get_int("accessoryGroup"), talismans),
        }