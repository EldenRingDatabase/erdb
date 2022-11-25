from pydantic import Field, NonNegativeInt
from pydantic.dataclasses import dataclass

from erdb.typing.models import dt_config
from erdb.typing.models.item import Item
from erdb.typing.models.effect import Effect
from erdb.typing.categories import ToolCategory
from erdb.typing.enums import ToolAvailability


@dataclass(config=dt_config())
class Tool(Item):
    category: ToolCategory = Field(...,
        description="Tool category to discern its use.",
        example=ToolCategory.UTILITY,
    )
    availability: ToolAvailability = Field(...,
        description="Defines whether the Tool is available always, only during singleplayer or only during multiplayer.",
        example=ToolAvailability.ALWAYS,
    )
    fp_cost: NonNegativeInt = Field(...,
        description="Cost of FP to use.",
        example=0,
    )
    is_consumed: bool = Field(...,
        description="Specifies whether the Tool is consumed on use.",
        example=True,
    )
    is_ladder_usable: bool = Field(...,
        description="Specifies whether the Tool is available on ladders.",
        example=False,
    )
    is_horseback_usable: bool = Field(...,
        description="Specifies whether the Tool is available on horseback.",
        example=True,
    )
    effects: list[Effect] = Field(...,
        description="Effects of the Tool.",
        # example provided by Effects model
    )