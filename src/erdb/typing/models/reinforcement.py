from pydantic import NonNegativeFloat, conlist, conint

from erdb.typing.models import dataclass


@dataclass
class DamageMultiplier:
    physical: NonNegativeFloat
    magic: NonNegativeFloat
    fire: NonNegativeFloat
    lightning: NonNegativeFloat
    holy: NonNegativeFloat
    stamina: NonNegativeFloat

@dataclass
class ScalingMultiplier:
    strength: NonNegativeFloat
    dexterity: NonNegativeFloat
    intelligence: NonNegativeFloat
    faith: NonNegativeFloat
    arcane: NonNegativeFloat

@dataclass
class GuardMultiplier:
    physical: NonNegativeFloat
    magic: NonNegativeFloat
    fire: NonNegativeFloat
    lightning: NonNegativeFloat
    holy: NonNegativeFloat
    guard_boost: NonNegativeFloat

@dataclass
class ResistanceMultiplier:
    bleed: NonNegativeFloat
    frostbite: NonNegativeFloat
    poison: NonNegativeFloat
    scarlet_rot: NonNegativeFloat
    sleep: NonNegativeFloat
    madness: NonNegativeFloat
    death_blight: NonNegativeFloat

@dataclass
class ReinforcementLevel:
    level: conint(ge=0, le=25)
    damage: DamageMultiplier
    scaling: ScalingMultiplier
    guard: GuardMultiplier
    resistance: ResistanceMultiplier

Reinforcement = conlist(ReinforcementLevel, min_items=1, max_items=26)