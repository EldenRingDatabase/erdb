from typing import Any

from erdb.typing.models.correction_attack import CorrectionAttack, Correction, Override, Ratio
from erdb.typing.params import ParamDict, ParamRow
from erdb.typing.enums import ItemIDFlag
from erdb.generators._base import GeneratorDataBase

_DAMAGE_TYPE: dict[str, str] = {
    "physical": "Physics",
    "magic": "Magic",
    "fire": "Fire",
    "lightning": "Thunder",
    "holy": "Dark",
}

_ATTRIBUTE: dict[str, str] = {
    "strength": "Strength",
    "dexterity": "Dexterity",
    "intelligence": "Magic",
    "faith": "Faith",
    "arcane": "Luck",
}

def _get_attributes(row: ParamRow, damage_type: str, cls: Any) -> Any:
    def get_field(attribute: str, damage_type: str) -> int:
        field = cls.get_property(_ATTRIBUTE[attribute], _DAMAGE_TYPE[damage_type])

        return {
            Correction: row.get_bool(field),
            Override: None if (value := row.get_int(field)) == -1 else float(value) / 100.0,
            Ratio: row.get_float(field) / 100.0,
        }[cls]

    ret = {attrib: get_field(attrib, damage_type) for attrib in _ATTRIBUTE.keys()}
    ret = {k: v for k, v in ret.items() if v is not None}
    return cls.get_field_type()(**ret)

def _get_damage_types(row: ParamRow, cls: Any) -> Any:
    data = {damage: _get_attributes(row, damage, cls) for damage in _DAMAGE_TYPE.keys()}
    return cls(**data)

class CorrectionAttackGeneratorData(GeneratorDataBase):
    Base = GeneratorDataBase

    @staticmethod # override
    def output_file() -> str:
        return "correction-attack.json"

    @staticmethod # override
    def element_name() -> str:
        return "CorrectionAttack"

    @staticmethod # override
    def model() -> CorrectionAttack:
        return CorrectionAttack

    # override
    def get_key_name(self, row: ParamRow) -> str:
        return str(row.index)

    main_param_retriever = Base.ParamDictRetriever("AttackElementCorrectParam", ItemIDFlag.NON_EQUIPABBLE)

    param_retrievers = {}
    msgs_retrievers = {}
    lookup_retrievers = {}

    def main_param_iterator(self, correct_attack: ParamDict):
        for row in correct_attack.values():
            yield row

    def construct_object(self, row: ParamRow) -> CorrectionAttack:
        return CorrectionAttack(
            correction=_get_damage_types(row, Correction),
            override=_get_damage_types(row, Override),
            ratio=_get_damage_types(row, Ratio),
        )