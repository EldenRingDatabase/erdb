from pydantic.dataclasses import dataclass as pydantic_dataclass
from pydantic import ConfigDict, Extra

dataclass = pydantic_dataclass(config=ConfigDict(extra=Extra.forbid))