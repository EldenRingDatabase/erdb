from pydantic.dataclasses import dataclass

from erdb.typing.models import dt_config


@dataclass(config=dt_config())
class AttributesCorrection:
    strength: bool
    dexterity: bool
    intelligence: bool
    faith: bool
    arcane: bool

@dataclass(config=dt_config())
class AttributesOverride:
    strength: float | None = None
    dexterity: float | None = None
    intelligence: float | None = None
    faith: float | None = None
    arcane: float | None = None

@dataclass(config=dt_config())
class AttributesRatio:
    strength: float
    dexterity: float
    intelligence: float
    faith: float
    arcane: float

@dataclass(config=dt_config())
class Correction:
    physical: AttributesCorrection
    magic: AttributesCorrection
    fire: AttributesCorrection
    lightning: AttributesCorrection
    holy: AttributesCorrection

    @staticmethod
    def get_field_type():
        return AttributesCorrection

    @staticmethod
    def get_property(attribute: str, damage_type: str) -> str:
        return f"is{attribute}Correct_by{damage_type}"

@dataclass(config=dt_config())
class Override:
    physical: AttributesOverride | None = None
    magic: AttributesOverride | None = None
    fire: AttributesOverride | None = None
    lightning: AttributesOverride | None = None
    holy: AttributesOverride | None = None

    @staticmethod
    def get_field_type():
        return AttributesOverride

    @staticmethod
    def get_property(attribute: str, damage_type: str) -> str:
        return f"overwrite{attribute}CorrectRate_by{damage_type}"

@dataclass(config=dt_config())
class Ratio:
    physical: AttributesRatio
    magic: AttributesRatio
    fire: AttributesRatio
    lightning: AttributesRatio
    holy: AttributesRatio

    @staticmethod
    def get_property(attribute: str, damage_type: str) -> str:
        return f"Influence{attribute}CorrectRate_by{damage_type}"

    @staticmethod
    def get_field_type():
        return AttributesRatio

@dataclass(config=dt_config())
class CorrectionAttack:
    correction: Correction
    override: Override
    ratio: Ratio