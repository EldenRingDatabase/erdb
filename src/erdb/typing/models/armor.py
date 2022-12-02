from pydantic import Field, PositiveFloat, NonNegativeInt
from pydantic.dataclasses import dataclass

from erdb.typing.models import dt_config
from erdb.typing.models.item import Item
from erdb.typing.models.effect import Effect
from erdb.typing.categories import ArmorCategory


@dataclass(config=dt_config())
class Absorptions:
    physical: float
    strike: float
    slash: float
    pierce: float
    magic: float
    fire: float
    lightning: float
    holy: float

@dataclass(config=dt_config())
class Resistances:
    immunity: int
    robustness: int
    focus: int
    vitality: int
    poise: int

@dataclass(config=dt_config())
class Armor(Item):
    category: ArmorCategory = Field(...,
        description="Category of the Armor.",
        example=ArmorCategory.BODY,
    )
    altered: str = Field(...,
        description="Name of the altered (or reversed) armor piece, empty if unalterable.",
        example="Elden Lord Armor (Altered)",
    )
    weight: PositiveFloat = Field(...,
        description="Weight of the Armor.",
        example=9.2,
    )
    icon_fem: NonNegativeInt = Field(...,
        description="Icon ID to the female version of the Armor, `icon` field specifies the male version which is usually the same.",
        example=584,
    )
    absorptions: Absorptions = Field(...,
        description="Absorption values for the Armor.",
        example=Absorptions(
            physical=11.9, strike=10.9, slash=11.4, pierce=12.4,
            magic=8.8, fire=11.4, lightning=7.1, holy=8.,
        ),
    )
    resistances: Resistances = Field(...,
        description="Resistance values for the Armor.",
        example=Resistances(immunity=32, robustness=55, focus=18, vitality=21, poise=19),
    )
    effects: list[Effect] = Field(...,
        description="Additional effects of the Armor."
        # example provided by Effect model
    )