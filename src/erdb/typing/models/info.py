from pydantic import Field

from erdb.typing.models import dataclass
from erdb.typing.models.item import Item
from erdb.typing.categories import InfoCategory


@dataclass
class Info(Item):
    category: InfoCategory = Field(...,
        description="Info Item category to discern its use.",
        example=InfoCategory.NOTE,
    )