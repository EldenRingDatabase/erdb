from pydantic import Field

from erdb.typing.models import dataclass
from erdb.typing.models.item import Item
from erdb.typing.categories import ShopCategory


@dataclass
class Shop(Item):
    category: ShopCategory = Field(...,
        description="Shop Item category to discern its use.",
        example=ShopCategory.COOKBOOK,
    )