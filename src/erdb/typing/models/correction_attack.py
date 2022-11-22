from erdb.typing.models import dataclass


@dataclass
class AttributesCorrection:
    strength: bool
    dexterity: bool
    intelligence: bool
    faith: bool
    arcane: bool

@dataclass
class AttributesOverride:
    strength: float | None = None
    dexterity: float | None = None
    intelligence: float | None = None
    faith: float | None = None
    arcane: float | None = None

@dataclass
class AttributesRatio:
    strength: float
    dexterity: float
    intelligence: float
    faith: float
    arcane: float

@dataclass
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

@dataclass
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

@dataclass
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

@dataclass
class CorrectionAttack:
    correction: Correction
    override: Override
    ratio: Ratio