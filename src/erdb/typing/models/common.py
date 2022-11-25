from pydantic import Field
from pydantic.dataclasses import dataclass

from erdb.typing.models import dt_config


@dataclass(config=dt_config())
class Damage:
    physical: int | None = None
    magic: int | None = None
    fire: int | None = None
    lightning: int | None = None
    holy: int | None = None
    stamina: int | None = None

@dataclass(config=dt_config())
class StatRequirements:
    strength: int | None = Field(None, ge=0, le=99)
    dexterity: int | None = Field(None, ge=0, le=99)
    intelligence: int | None = Field(None, ge=0, le=99)
    faith: int | None = Field(None, ge=0, le=99)
    arcane: int | None = Field(None, ge=0, le=99)