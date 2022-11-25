from typing import Literal
from pydantic import Field, PositiveInt
from pydantic.dataclasses import dataclass

from erdb.typing.models import dt_config, NonEmptyStr
from erdb.typing.enums import Region, Location, Currency


@dataclass(config=dt_config())
class LocationDetail:
    summary: str = Field("no summary",
        description="Short, consice summary of the location. To help concatenating with other data, there are no capital letters or periods at the end.",
        min_length=1, regex=r"^.+(?<!\\.)$",
        example="found on top a giant spear in Leyndell, Royal Capital",
    )
    quantity: PositiveInt | Literal["infinite"] | None = Field(None,
        description="Specifies the amount if an integer, otherwise `infinite` if the Item respawns or can be purchased infinitely.",
        example=1,
    )
    location: Location | None = Field(None,
        description="The specific location in which the Item is found.",
        example=Location.LEYNDELL_ROYAL_CAPITAL,
    )
    region: Region | None = Field(None,
        description="The generic region in which the Item is found.",
        example=Region.ALTUS_PLATEAU,
    )
    directions: NonEmptyStr | None =  Field(None,
        description="Exact description on where to find the Item if summary cannot be straightfoward enough.",
        example="From the East Capital Rampart Gate grace, take an elevator down towards the capital. Head alongside the railing to the left and jump onto the giant spear.",
    )
    price_bought: PositiveInt | None = Field(None,
        description="The amount of Currency the Item is bought for at this location, if applicable.",
        example=500,
    )
    currency: Currency | None =  Field(None,
        description="The type of currency this item is bought for, if applicable.",
        example=Currency.RUNES,
    )
    requirements: list[NonEmptyStr] | None = Field(None,
        description="List of requirements which make the item available in full sentences.",
        min_items=1,
        example=[
            "Two Great Runes must be acquired to access Leyndell, Royal Capital",
            "Godfrey, First ELden Lord (Golden Shade) must be defeated to gain access to the area with the Armament.",
        ],
    )
    blockers: list[NonEmptyStr] | None = Field(None,
        description="List of situations which cause the item to become unavailable in full sentences.",
        min_items=1,
        example=["Maliketh, the Black Blade is deafeated turning Leyndell, Royal Capital into Leyndell, Ashen Capital."]
    )