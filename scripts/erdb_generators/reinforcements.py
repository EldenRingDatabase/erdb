from typing import Dict, Tuple
from scripts.er_params import ParamDict, ParamRow
from scripts.er_params.enums import ItemIDFlag, ReinforcementType
from scripts.erdb_common import get_schema_properties, get_schema_enums, find_offset_indices
from scripts.erdb_generators._base import GeneratorDataBase

def _is_base_index(index: int) -> bool:
    return index == 0 or index % 100 == 0

def _get_damages(row: ParamRow) -> Dict[str, float]:
    return {
        "base": row.get_float("baseAtkRate"),
        "physical": row.get_float("physicsAtkRate"),
        "magic": row.get_float("magicAtkRate"),
        "fire": row.get_float("fireAtkRate"),
        "lightning": row.get_float("thunderAtkRate"),
        "holy": row.get_float("darkAtkRate"),
        "stamina":row.get_float("staminaAtkRate") 
    }

def _get_scalings(row: ParamRow) -> Dict[str, float]:
    return {
        "strength": row.get_float("correctStrengthRate"),
        "dexterity": row.get_float("correctAgilityRate"),
        "intelligence": row.get_float("correctMagicRate"),
        "faith": row.get_float("correctFaithRate"),
        "arcane": row.get_float("correctLuckRate")
    }

def _get_guards(row: ParamRow) -> Dict[str, float]:
    return {
        "physical": row.get_float("physicsGuardCutRate"),
        "magic": row.get_float("magicGuardCutRate"),
        "fire": row.get_float("fireGuardCutRate"),
        "lightning": row.get_float("thunderGuardCutRate"),
        "holy": row.get_float("darkGuardCutRate"),
        "guard_boost": row.get_float("staminaGuardDefRate")
    }

def _get_resistances(row: ParamRow) -> Dict[str, float]:
    return {
        "poison": row.get_float("poisonGuardResistRate"),
        "scarlet_rot": row.get_float("diseaseGuardResistRate"),
        "forstbite": row.get_float("freezeGuardDefRate"),
        "bleed": row.get_float("bloodGuardResistRate"),
        "sleep": row.get_float("sleepGuardDefRate"),
        "madness": row.get_float("madnessGuardDefRate"),
        "death_blight": row.get_float("curseGuardResistRate")
    }

def _get_reinforcement(level: int, row: ParamRow) -> Dict:
    return {
        "level": level,
        "damage": _get_damages(row),
        "scaling": _get_scalings(row),
        "guard": _get_guards(row),
        "resistance": _get_resistances(row)
    }

class ReinforcementGeneratorData(GeneratorDataBase):
    Base = GeneratorDataBase

    @staticmethod # override
    def output_file() -> str:
        return "reinforcements.json"

    @staticmethod # override
    def schema_file() -> str:
        return "reinforcements.schema.json"

    @staticmethod # override
    def element_name() -> str:
        return "Reinforcements"

    # override
    def get_key_name(self, row: ParamRow) -> str:
        return str(ReinforcementType(str(row.index)))

    main_param_retriever = Base.ParamDictRetriever("ReinforceParamWeapon", ItemIDFlag.NON_EQUIPABBLE)

    param_retrievers = {}
    msgs_retrievers = {}
    lookup_retrievers = {}

    @staticmethod
    def schema_retriever() -> Tuple[Dict, Dict[str, Dict]]:
        properties, store = get_schema_properties("reinforcements")
        store.update(get_schema_enums("reinforcement-names"))
        return properties, store

    def main_param_iterator(self, reinforcements: ParamDict):
        for row in reinforcements.values():
            if _is_base_index(row.index) and len(row.name) > 0: # NOTE: Paramdex coupling (row.name)
                yield row

    def construct_object(self, row: ParamRow) -> Dict:
        reinforcementType = ReinforcementType(str(row.index))
        if reinforcementType == ReinforcementType.NO_REINFORCEMENT:
            return {"0": _get_reinforcement(0, row)}

        indices, offsets = find_offset_indices(row.index, self.main_param, possible_maxima=[10, 25])
        return {str(l): _get_reinforcement(l, self.main_param[str(i)]) for l, i in zip(offsets, indices)}