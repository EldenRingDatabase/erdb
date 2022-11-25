from pydantic import Field, PositiveInt, NonNegativeInt
from pydantic.dataclasses import dataclass

from erdb.typing.models import dt_config, NonEmptyStr
from erdb.typing.models.item import Item
from erdb.typing.enums import SpiritAshUpgradeMaterial


@dataclass(config=dt_config())
class SpiritAshUserData:
    summon_quantity: PositiveInt = Field(1,
        description="The number of spririts this Spirit Ash summons.",
        example=1,
    )
    abilities: list[NonEmptyStr] = Field([],
        description="Strenghts of the Spirit Ash. Each briefly described with minimum amount of words.",
        example=[
            "Highly mobile",
            "Casts Blade of Death",
            "Jump and charged attacks can knock enemies down",
        ],
    )

@dataclass(config=dt_config())
class SpiritAsh(SpiritAshUserData, Item):
    summon_name: str = Field(...,
        description="Specific name of the summoned spirit(s). Rarely differs from Item name.",
        min_length=1,
        example="Black Knife Tiche"
    )
    fp_cost: NonNegativeInt = Field(...,
        description="Cost of FP to summon, 0 if not applicable.",
        example=132,
    )
    hp_cost: NonNegativeInt = Field(...,
        description="Cost of HP to summon, 0 if not applicable.",
        example=0,
    )
    upgrade_material: SpiritAshUpgradeMaterial = Field(...,
        description="Glovewort the Spirit Ash upgrades with.",
        example=SpiritAshUpgradeMaterial.GHOST_GLOVEWORT,
    )
    upgrade_costs: list[NonNegativeInt] = Field(...,
        description="Array of Rune costs to upgrade to each level, +1 starting at position 0.",
        min_items=10, max_items=10,
        example=[2000, 3200, 4400, 5600, 6800, 8000, 9200, 10400, 11600, 14000]
    )