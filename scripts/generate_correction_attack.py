from typing import Dict, Tuple
from scripts.er_params import ParamDict, ParamRow
from scripts.er_params.enums import ItemIDFlag
from scripts.erdb_common import GeneratorDataBase, get_schema_properties

_DAMAGE_TYPE: Dict[str, str] = {
    "physical": "Physics",
    "magic": "Magic",
    "fire": "Fire",
    "lightning": "Thunder",
    "holy": "Dark",
}

_ATTRIBUTE: Dict[str, str] = {
    "strength": "Strength",
    "dexterity": "Dexterity",
    "intelligence": "Magic",
    "faith": "Faith",
    "arcane": "Luck",
}

def _format_correction(attribute: str, damage_type: str) -> str:
    return f"is{attribute}Correct_by{damage_type}"

def _format_override(attribute: str, damage_type: str) -> str:
    return f"overwrite{attribute}CorrectRate_by{damage_type}"

def _format_ratio(attribute: str, damage_type: str) -> str:
    return f"Influence{attribute}CorrectRate_by{damage_type}"

def _get_attributes(row: ParamRow, damage_type: str, format_func) -> Dict[str, str]:
    def _get_field(row: ParamRow, attribute: str, damage_type: str, format_func) -> int:
        field = format_func(_ATTRIBUTE[attribute], _DAMAGE_TYPE[damage_type])

        if format_func == _format_correction:
            value = row.get_int(field)
            assert value in [0, 1], "Correction values should be boolean"
            return value

        elif format_func == _format_override:
            value = row.get_int(field)
            return None if value == -1 else float(value) / 100.0

        elif format_func == _format_ratio:
            return row.get_float(field) / 100.0

        assert False, "Invalid format function"

    ret = {attrib: _get_field(row, attrib, damage_type, format_func) for attrib in _ATTRIBUTE.keys()}
    return {k: v for k, v in ret.items() if v is not None}

def _get_damage_types(row: ParamRow, format_func) -> Dict[str, Dict[str, str]]:
    return {damage: _get_attributes(row, damage, format_func) for damage in _DAMAGE_TYPE.keys()}

class CorrectionAttackGeneratorData(GeneratorDataBase):
    Base = GeneratorDataBase

    @staticmethod # override
    def output_file() -> str:
        return "correction-attack.json"

    @staticmethod # override
    def schema_file() -> str:
        return "correction-attack.schema.json"

    @staticmethod # override
    def element_name() -> str:
        return "CorrectionAttack"

    @staticmethod # override
    def get_key_name(row: ParamRow) -> str:
        return str(row.index)

    main_param_retriever = Base.ParamDictRetriever("AttackElementCorrectParam", ItemIDFlag.NON_EQUIPABBLE)

    param_retrievers = {}
    msgs_retrievers = {}
    lookup_retrievers = {}

    @staticmethod
    def schema_retriever() -> Tuple[Dict, Dict[str, Dict]]:
        return get_schema_properties("correction-attack")

    def main_param_iterator(self, correct_attack: ParamDict):
        for row in correct_attack.values():
            yield row

    def construct_object(self, row: ParamRow) -> Dict:
        return {
            "correction": _get_damage_types(row, _format_correction),
            "override": _get_damage_types(row, _format_override),
            "ratio": _get_damage_types(row, _format_ratio),
        }