from typing import Any

from erdb.typing.models.correction_attack import CorrectionAttack, Correction, Override, Ratio
from erdb.typing.params import ParamRow
from erdb.typing.enums import ItemIDFlag
from erdb.typing.api_version import ApiVersion
from erdb.table._retrievers import ParamDictRetriever, RetrieverData
from erdb.table._common import TableSpecContext


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
            Correction: row[field].as_bool,
            Override: value / 100.0 if (value := row[field].get_float()) else None,
            Ratio: row[field].as_float / 100.0,
        }[cls]

    ret = {attrib: get_field(attrib, damage_type) for attrib in _ATTRIBUTE.keys()}
    ret = {k: v for k, v in ret.items() if v is not None}
    return cls.get_field_type()(**ret)

def _get_damage_types(row: ParamRow, cls: Any) -> Any:
    data = {damage: _get_attributes(row, damage, cls) for damage in _DAMAGE_TYPE.keys()}
    return cls(**data)

class CorrectionAttackTableSpec(TableSpecContext):
    model = {
        ApiVersion.VER_1: CorrectionAttack,
    }

    main_param_retriever = ParamDictRetriever("AttackElementCorrectParam", ItemIDFlag.NON_EQUIPABBLE)

    @classmethod # override
    def get_pk(cls, data: RetrieverData, row: ParamRow) -> str:
        return str(row.index)

    @classmethod
    def make_object(cls, api: ApiVersion, data: RetrieverData, row: ParamRow):
        return CorrectionAttack(
            correction=_get_damage_types(row, Correction),
            override=_get_damage_types(row, Override),
            ratio=_get_damage_types(row, Ratio),
        )