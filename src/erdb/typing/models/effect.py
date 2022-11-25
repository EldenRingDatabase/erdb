from pydantic import Field
from pydantic.dataclasses import dataclass

from erdb.typing.models import dt_config
from erdb.typing.effects import AttributeName, EffectModel, EffectType

@dataclass(config=dt_config())
class StatusEffects:
    bleed: int | None = None
    frostbite: int | None = None
    poison: int | None = None
    scarlet_rot: int | None = None
    sleep: int | None = None
    madness: int | None = None
    death_blight: int | None = None

@dataclass(config=dt_config())
class Effect:
    attribute: AttributeName = Field(...,
        description="Specific attribute this effect alters.",
        example=AttributeName.ATTACK_POWER,
    )
    value: float = Field(...,
        description="Value modifying the attribute.",
        example=1.2,
    )
    model: EffectModel = Field(EffectModel.MULTIPLICATIVE,
        description="Specifies whether the value is multiplicative (ex. rune acquisition) or additive (ex. +5 strength).",
        example=EffectModel.MULTIPLICATIVE,
    )
    type: EffectType = Field(EffectType.POSITIVE,
        description="The kind of the effect, considering the whole context (`value` *alone* can mean different things depending on `attribute` and `model`).",
        example=EffectType.POSITIVE,
    )
    value_pvp: float | None = Field(None,
        description="Optional modifying value when used in PvP scenario.",
        example=1.2,
    )
    conditions: list[str] | None = Field(None,
        description="List of conditions which trigger the effect, none for passive effects.",
        example=["HP below 20%"],
    )
    tick_interval: float | None = Field(None,
        description="Interval in seconds on how often the effect gets applied.",
        example=2
    )
