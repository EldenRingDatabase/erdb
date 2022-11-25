from pydantic import Field
from pydantic.dataclasses import dataclass

from erdb.typing.models import dt_config
from erdb.typing.models.item import Item
from erdb.typing.categories import ShopCategory


@dataclass(config=dt_config())
class Shop(Item):
    category: ShopCategory = Field(...,
        description="Shop Item category to discern its use.",
        example=ShopCategory.COOKBOOK,
    )