from pydantic.dataclasses import dataclass

from erdb.typing.models import dt_config
from erdb.typing.models.item import Item


@dataclass(config=dt_config())
class Gesture(Item):
    pass