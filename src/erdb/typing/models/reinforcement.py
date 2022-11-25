from pydantic import Field, NonNegativeFloat, conlist
from pydantic.dataclasses import dataclass

from erdb.typing.models import dt_config


@dataclass(config=dt_config())
class DamageMultiplier:
    physical: NonNegativeFloat
    magic: NonNegativeFloat
    fire: NonNegativeFloat
    lightning: NonNegativeFloat
    holy: NonNegativeFloat
    stamina: NonNegativeFloat

@dataclass(config=dt_config())
class ScalingMultiplier:
    strength: NonNegativeFloat
    dexterity: NonNegativeFloat
    intelligence: NonNegativeFloat
    faith: NonNegativeFloat
    arcane: NonNegativeFloat

@dataclass(config=dt_config())
class GuardMultiplier:
    physical: NonNegativeFloat
    magic: NonNegativeFloat
    fire: NonNegativeFloat
    lightning: NonNegativeFloat
    holy: NonNegativeFloat
    guard_boost: NonNegativeFloat

@dataclass(config=dt_config())
class ResistanceMultiplier:
    bleed: NonNegativeFloat
    frostbite: NonNegativeFloat
    poison: NonNegativeFloat
    scarlet_rot: NonNegativeFloat
    sleep: NonNegativeFloat
    madness: NonNegativeFloat
    death_blight: NonNegativeFloat

@dataclass(config=dt_config())
class ReinforcementLevel:
    level: int = Field(..., ge=0, le=25)
    damage: DamageMultiplier = Field(...)
    scaling: ScalingMultiplier = Field(...)
    guard: GuardMultiplier = Field(...)
    resistance: ResistanceMultiplier = Field(...)

Reinforcement = conlist(ReinforcementLevel, min_items=1, max_items=26)