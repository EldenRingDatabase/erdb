from pydantic import Field

from erdb.typing.models import dataclass
from erdb.typing.models.item import Item
from erdb.typing.categories import BolsteringMaterialCategory


@dataclass
class BolsteringMaterial(Item):
    category: BolsteringMaterialCategory = Field(...,
        description="Bolstering Material category to discern its use.",
        example=BolsteringMaterialCategory.SMITHING_STONE,
    )