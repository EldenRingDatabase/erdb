from pydantic import Field
from pydantic.dataclasses import dataclass

from erdb.typing.models import dt_config
from erdb.typing.models.item import Item
from erdb.typing.categories import InfoCategory


@dataclass(config=dt_config())
class Info(Item):
    category: InfoCategory = Field(...,
        description="Info Item category to discern its use.",
        example=InfoCategory.NOTE,
    )