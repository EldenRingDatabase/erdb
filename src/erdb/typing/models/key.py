from pydantic import Field
from pydantic.dataclasses import dataclass

from erdb.typing.models import dt_config
from erdb.typing.models.item import Item
from erdb.typing.categories import KeyCategory


@dataclass(config=dt_config())
class Key(Item):
    category: KeyCategory = Field(...,
        description="Key category to discern its use.",
        example=KeyCategory.QUEST,
    )