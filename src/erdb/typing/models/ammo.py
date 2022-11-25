from pydantic import Field
from pydantic.dataclasses import dataclass

from erdb.typing.models import dt_config
from erdb.typing.models.item import Item
from erdb.typing.models.common import Damage
from erdb.typing.models.effect import Effect, StatusEffects
from erdb.typing.categories import AmmoCategory


@dataclass(config=dt_config())
class Ammo(Item):
    damage: Damage = Field(...,
        description="Base attack power values.",
        example=Damage(physical=10, fire=90, stamina=5),
    )
    category: AmmoCategory = Field(...,
        description="Category of the Ammo.",
        example=AmmoCategory.BOLT,
    )
    effects: list[Effect] = Field(...,
        description="Effects of the Ammo.",
        # example provided by Effect model
    )
    status_effects: StatusEffects = Field(...,
        description="Status effects of the Ammo, dealt on hit."
        # example provided by StatusEffects model
    )