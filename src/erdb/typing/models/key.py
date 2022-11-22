from pydantic import Field

from erdb.typing.models import dataclass
from erdb.typing.models.item import Item
from erdb.typing.categories import KeyCategory


@dataclass
class Key(Item):
    category: KeyCategory = Field(...,
        description="Key category to discern its use.",
        example=KeyCategory.QUEST,
    )