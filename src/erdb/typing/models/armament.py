from pydantic import Field, NonNegativeInt, NonNegativeFloat, PositiveInt
from pydantic.dataclasses import dataclass

from erdb.typing.models import dt_config
from erdb.typing.models.item import Item
from erdb.typing.models.common import Damage, StatRequirements
from erdb.typing.models.effect import Effect, StatusEffects
from erdb.typing.categories import ArmamentCategory
from erdb.typing.enums import Affinity, ArmamentUpgradeMaterial, AttackAttribute


@dataclass(config=dt_config())
class CorrectionCalcID:
    physical: NonNegativeInt
    magic: NonNegativeInt
    fire: NonNegativeInt
    lightning: NonNegativeInt
    holy: NonNegativeInt
    poison: NonNegativeInt
    bleed: NonNegativeInt
    sleep: NonNegativeInt
    madness: NonNegativeInt

@dataclass(config=dt_config())
class Scaling:
    strength: NonNegativeFloat | None = None
    dexterity: NonNegativeFloat | None = None
    intelligence: NonNegativeFloat | None = None
    faith: NonNegativeFloat | None = None
    arcane: NonNegativeFloat | None = None

@dataclass(config=dt_config())
class Guard:
    physical: NonNegativeInt | None = None
    magic: NonNegativeInt | None = None
    fire: NonNegativeInt | None = None
    lightning: NonNegativeInt | None = None
    holy: NonNegativeInt | None = None
    guard_boost: NonNegativeInt | None = None

@dataclass(config=dt_config())
class AffinityProperties:
    full_hex_id: str = Field(...,
        description="Full hex ID override for the Armament with Affinity applied.",
        regex=r"^[0-9A-F]+$",
        min_length=8, max_length=8,
        example="003085E0",
    )
    id: PositiveInt = Field(...,
        description="ID override for the Armament with Affinity applied.",
        exampe=3180000,
    )
    reinforcement_id: NonNegativeInt = Field(...,
        description="ID of reinforcement, refer to the `Reinforcements` table to look up value changes per level.",
        example=100,
    )
    correction_attack_id: NonNegativeInt = Field(...,
        description="ID of attack element correction, refer to the `Correction Attack` table to look up definitions.",
        example=10000,
    )
    correction_calc_id: CorrectionCalcID = Field(...,
        description="ID of calc correction for each damage type, refer to the `Correction Graph` table to look up value multipliers.",
        example=CorrectionCalcID(
            physical=0, magic=0, fire=0, lightning=0, holy=0,
            poison=6, bleed=6, sleep=6, madness=6,
        )
    )
    damage: Damage = Field(...,
        description="Base attack power values.",
        example=Damage(physical=138, stamina=63),
    )
    scaling: Scaling = Field(...,
        description="Base attribute scaling values.",
        example=Scaling(strength=0.49, dexterity=0.34)
    )
    guard: Guard = Field(...,
        description="Base guarded damage negation values.",
        example=Guard(physical=65, magic=35, fire=35, lightning=35, holy=35, guard_boost=42)
    )
    resistance: StatusEffects = Field(...,
        description="Base guarded resistances values.",
        example=StatusEffects(
            bleed=20, frostbite=20, poison=20, scarlet_rot=20,
            sleep=20, madness=20, death_blight=20
        ),
    )
    status_effects: StatusEffects = Field(...,
        description="Status effects of the Armament, dealt on hit.",
        example=StatusEffects(poison=80),
    )
    status_effect_overlay: list[StatusEffects] = Field(...,
        description="Array of status effects per Armament level which get upgraded alongside. Given the Armament level as the index to this array, the value should be overlaid on the `status_effects` property. In practice, only a single effect is set to be upgradable, but technically game params can do up to three.",
        max_items=26,
        example=[
            StatusEffects(poison=80), StatusEffects(poison=81), StatusEffects(poison=82),
            StatusEffects(poison=84), StatusEffects(poison=85), StatusEffects(poison=87),
            StatusEffects(poison=88), StatusEffects(poison=89), StatusEffects(poison=91),
            StatusEffects(poison=92), StatusEffects(poison=94), StatusEffects(poison=95),
            StatusEffects(poison=96), StatusEffects(poison=98), StatusEffects(poison=99),
            StatusEffects(poison=101), StatusEffects(poison=102), StatusEffects(poison=103),
            StatusEffects(poison=105), StatusEffects(poison=106), StatusEffects(poison=108),
            StatusEffects(poison=109), StatusEffects(poison=110), StatusEffects(poison=112),
            StatusEffects(poison=113), StatusEffects(poison=115),
        ]
    )

@dataclass(config=dt_config())
class Armament(Item):
    behavior_variation_id: NonNegativeInt = Field(...,
        description="Behavior variation ID used to identify attack params.",
        example=318
    )
    category: ArmamentCategory = Field(...,
        description="Class of the Armament.",
        example=ArmamentCategory.GREATSWORD,
    )
    weight: NonNegativeFloat = Field(...,
        description="Weight of the Armament.",
        example=9.,
    )
    default_skill_id: int = Field(...,
        description="Index of the default Skill the Armament comes with.",
        ge=10,
        example=100,
    )
    allow_ash_of_war: bool = Field(...,
        description="Specifies whether other Ashes of War can be put on the Armament and its affinity potentially changed.",
        example=True,
    )
    is_buffable: bool = Field(...,
        description="Specifies whether the Armament is buffable.",
        example=True,
    )
    is_l1_guard: bool = Field(...,
        description="Specifies whether the Armament is used for guarding when equipped in left hand.",
        example=True,
    )
    upgrade_material: ArmamentUpgradeMaterial = Field(...,
        description="Stones the Armament upgrades with, if upgradable.",
        example=ArmamentUpgradeMaterial.SMITHING_STONE,
    )
    upgrade_costs: list[NonNegativeInt] = Field(...,
        description="Array of Rune costs to upgrade to each level, +1 starting at position 0. Empty if the Armament is non-upgradable, otherwise it contains either 10 or 25 integers. `upgrade_material` can be used to tell the actual length.",
        min_items=0, max_items=25,
        example=[530, 636, 742, 848, 954, 1060, 1166, 1272, 1378, 1484],
    )
    attack_attributes: list[AttackAttribute] = Field(...,
        description="List of attack attributes the Armament can deal, usually 2.",
        min_items=1, max_items=2, unique_items=True,
        example=[AttackAttribute.PIERCE, AttackAttribute.STANDARD],
    )
    sp_consumption_rate: NonNegativeFloat = Field(...,
        description="Multiplier used for calculating the effective stamina consumption from the Skill's base stamina cost.",
        example=1.
    )
    requirements: StatRequirements = Field(...,
        description="Attribute requirements of the Armament.",
        example=StatRequirements(strength=16, dexterity=13),
    )
    effects: list[Effect] = Field(...,
        description="Effects of the Armament.",
        # example provided by Effect model
    )
    affinity: dict[Affinity, AffinityProperties] = Field(...,
        description="Mapping of possible affinities to their individual properties. `Standard` is always present.",
    )