from pydantic import Field
from pydantic.dataclasses import dataclass

from erdb.typing.models import dt_config, NonEmptyStr
from erdb.typing.models.item import Item
from erdb.typing.categories import CraftingMaterialCategory


@dataclass(config=dt_config())
class CraftingMaterial(Item):
    category: CraftingMaterialCategory = Field(...,
        description="Crafting Material category to discern its use.",
        example=CraftingMaterialCategory.FAUNA,
    )
    hint: NonEmptyStr = Field(...,
        description="In-game hint on where to find the Crafting Material.",
        example="Found by hunting particularly large beasts",
    )
    products: list[NonEmptyStr] = Field(...,
        description="List of crafting products of the Crafting Material.",
        min_items=1,
        example=[
            "Beastlure Pot",
            "Exalted Flesh",
            "Bone Great Arrow (Fletched)",
            "Bone Great Arrow",
            "Bone Ballista Bolt",
        ]
    )