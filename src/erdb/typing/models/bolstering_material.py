from pydantic import Field
from pydantic.dataclasses import dataclass

from erdb.typing.models import dt_config
from erdb.typing.models.item import Item
from erdb.typing.categories import BolsteringMaterialCategory


@dataclass(config=dt_config())
class BolsteringMaterial(Item):
    category: BolsteringMaterialCategory = Field(...,
        description="Bolstering Material category to discern its use.",
        example=BolsteringMaterialCategory.SMITHING_STONE,
    )