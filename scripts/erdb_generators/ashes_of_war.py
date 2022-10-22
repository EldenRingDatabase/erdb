from typing import Dict, List, Tuple
from scripts.er_params import ParamDict, ParamRow
from scripts.er_params.enums import ItemIDFlag, Affinity, WeaponClass
from scripts.erdb_common import get_schema_properties, get_schema_enums, strip_invalid_name
from scripts.erdb_generators._base import GeneratorDataBase

def _is_elem_true(row: ParamRow, list_param: str, elem: str) -> bool:
    return row.get_bool(list_param + elem)

def _get_classes(row: ParamRow) -> List[WeaponClass]:
    return [c for c in list(WeaponClass) if _is_elem_true(row, "canMountWep_", c)]

def _get_affinities(row: ParamRow) -> List[Affinity]:
    return [a for a in list(Affinity) if _is_elem_true(row, "configurableWepAttr", a.zfill(2))]

class AshOfWarGeneratorData(GeneratorDataBase):
    Base = GeneratorDataBase

    @staticmethod # override
    def output_file() -> str:
        return "ashes-of-war.json"

    @staticmethod # override
    def schema_file() -> str:
        return "ashes-of-war.schema.json"

    @staticmethod # override
    def element_name() -> str:
        return "AshesOfWar"

    # override
    def get_key_name(self, row: ParamRow) -> str:
        return strip_invalid_name(self.msgs["names"][row.index])

    main_param_retriever = Base.ParamDictRetriever("EquipParamGem", ItemIDFlag.ACCESSORIES, id_min=10000)

    param_retrievers = {}

    msgs_retrievers = {
        "names": Base.MsgsRetriever("GemName"),
        "summaries": Base.MsgsRetriever("GemInfo"),
        "descriptions": Base.MsgsRetriever("GemCaption")
    }

    lookup_retrievers = {}

    @staticmethod
    def schema_retriever() -> Tuple[Dict, Dict[str, Dict]]:
        properties, store = get_schema_properties(
            "item/properties",
            "item/definitions/ItemUserData/properties",
            "ashes-of-war/definitions/AshOfWar/properties")
        store.update(get_schema_enums("ash-of-war-names", "affinity-names", "armament-class-names", "skill-names"))
        return properties, store

    def main_param_iterator(self, ashes_of_war: ParamDict):
        for row in ashes_of_war.values():
            yield row

    def construct_object(self, row: ParamRow) -> Dict:
        return self.get_fields_item(row) | self.get_fields_user_data(row, "locations", "remarks") | {
            "classes": [*map(str, _get_classes(row))],
            "default_affinity": str(Affinity(row.get("defaultWepAttr"))),
            "affinities": [*map(str, _get_affinities(row))],
            "skill_id": row.get_int("swordArtsParamId")
        }