from pydantic import Field, PositiveFloat
from pydantic.dataclasses import dataclass

from erdb.typing.models import dt_config, NonEmptyStr
from erdb.typing.models.item import Item
from erdb.typing.models.effect import Effect


@dataclass(config=dt_config())
class Talisman(Item):
    weight: PositiveFloat = Field(...,
        description="Weight of the Talisman",
        example=0.3
    )
    effects: list[Effect] = Field(...,
        description="Effects of the Talisman",
        # example provided by Effect model
    )
    conflicts: list[NonEmptyStr] = Field(...,
        description="Array of other talismans this one conflicts with.",
        example=["Crimson Amber Medallion", "Crimson Amber Medallion +1", "Crimson Amber Medallion +2"]
    )