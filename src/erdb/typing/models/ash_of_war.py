from pydantic import Field
from pydantic.dataclasses import dataclass

from erdb.typing.models import dt_config
from erdb.typing.models.armament import Affinity
from erdb.typing.models.item import Item
from erdb.typing.categories import ArmamentCategory


@dataclass(config=dt_config())
class AshOfWar(Item):
    armament_categories: list[ArmamentCategory] = Field(...,
        description="Applicable weapons classes the Ash of War can be applied to.",
        min_items=1,
        example=[ArmamentCategory.GREATAXE, ArmamentCategory.GREAT_HAMMER, ArmamentCategory.COLOSSAL_WEAPON],
    )
    default_affinity: Affinity = Field(...,
        description="Default Affinity the Ash of War comes with.",
        example=Affinity.FLAME_ART,
    )
    possible_affinities: list[Affinity] = Field(...,
        description="List of Affinities the Ash of War can provide, assuming Whetblades are available.",
        min_items=1,
        example=[Affinity.STANDARD, Affinity.HEAVY, Affinity.KEEN, Affinity.QUALITY, Affinity.FIRE, Affinity.FLAME_ART]
    )
    skill_id: int = Field(...,
        description="Index of the Skill the Ash of War comes with.",
        ge=10,
        example=113,
    )
