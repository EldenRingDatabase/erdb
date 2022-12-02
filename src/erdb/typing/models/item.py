from pydantic import Field, PositiveInt, NonNegativeInt
from pydantic.dataclasses import dataclass

from erdb.typing.models import dt_config, NonEmptyStr
from erdb.typing.models.location import LocationDetail
from erdb.typing.enums import GoodsRarity


@dataclass(config=dt_config())
class Item:
    full_hex_id: str = Field(...,
        description="Full ID of the Item in capital hexadecimal form. IDs differ per affinity or upgrade level.",
        regex=r"^[0-9A-F]+$",
        min_length=8, max_length=8,
        example="400000BE",
    )
    id: PositiveInt = Field(...,
        description="ID of the Item in its individual class. IDs differ per affinity or upgrade level.",
        example=190,
    )
    name: str = Field(...,
        description="Name of the Item.",
        min_length=1,
        example="Rune Arc",
    )
    summary: str = Field(...,
        description="Short description of the Item.",
        min_length=1,
        example="Grants the blessing of an equipped Great Rune upon use",
    )
    description: list[str] = Field(...,
        description="Array of lines of the in-game description, each element is separated by a new line. A line may contain multiple sentences, or be empty if in between paragraphs.",
        min_items=1,
        example=[
            "A shard of the shattered Elden Ring.",
            "Grants the blessing of an equipped Great Rune upon use.",
            "",
            "Even if no Great Rune is equipped, it will slightly increase maximum HP upon use.",
            "",
            "The lower arc of the Elden Ring is held to be the basin in which its blessings pool. Perhaps this shard originates from that very arc.",
        ],
    )
    is_tradable: bool = Field(...,
        description="Specifies whether the Item is visible to other players if dropped.",
    )
    price_sold: NonNegativeInt = Field(...,
        description="The amount of Runes the Item is sold for, 0 if not applicabe.",
        example=200,
    )
    rarity: GoodsRarity = Field(...,
        description="Rarity of the Item.",
        example=GoodsRarity.COMMON,
    )
    icon: NonNegativeInt = Field(...,
        description="ID of the icon which can be shared across many items. Icons can be sourced from the game files using ERDB.",
        example=584,
    )
    max_held: NonNegativeInt = Field(...,
        description="The maximum amount of the Item that a player can have on them.",
        example=99,
    )
    max_stored: NonNegativeInt = Field(...,
        description="The maximum amount of the Item that can be stored in the sort chest.",
        example=600,
    )
    locations: list[LocationDetail] = Field([LocationDetail()],
        description="List of locations in which this Item appears.",
        min_items=1,
        # example provided by LocationDetail model
    )
    remarks: list[NonEmptyStr] = Field([],
        description="List of remarks and trivia about this item.",
        example=[
            "Activates the equipped Great Rune until death.",
            "Use animation is long and leaves you open to attacks.",
        ],
    )