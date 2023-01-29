import re
from enum import Enum
from operator import add
from itertools import repeat
from pathlib import Path
from typing import Any, NamedTuple, overload, Self
from urllib.parse import urlparse
from pydantic.json import pydantic_encoder

from erdb.typing.params import ParamDict


class Destination(NamedTuple):
    protocol: str
    path: Path
    netloc: str | None = None
    username: str | None = None
    password: str | None = None

    @property
    def is_local(self) -> bool:
        return self.protocol == "file"

    @classmethod
    def from_str(cls, value: str) -> Self:
        data = urlparse(value)

        if data.scheme in ["", "file"]:
            return cls("file", Path(value))

        return cls(data.scheme, Path(data.path), data.netloc, data.username, data.password)

def find_offset_indices(base_index: int, params: ParamDict, possible_maxima: list[int], increment: int = 1) -> tuple[map, range]:
    """
    Returns lists of valid indices from `base_index` value which offset
    until the highest possible maxima is reached.

    First list is possible indices and second is raw level integers.
    """
    def _find_offset_maxima() -> int | None:
        for maxima in sorted(possible_maxima, reverse=True): # from largest
            if (base_index + maxima * increment) in params.keys():
                return maxima
        return None

    maxima = _find_offset_maxima()
    assert maxima is not None

    levels = range(0, (maxima + 1) * increment, increment)
    return map(add, repeat(base_index), levels), levels

def prepare_writable_path(path: Path, default_filename: str) -> Path:
    (path if path.suffix == "" else path.parent).mkdir(parents=True, exist_ok=True)
    return path / default_filename if path.is_dir() else path

@overload
def remove_nulls(val: dict) -> dict: ...

@overload
def remove_nulls(val: list) -> list: ...

@overload
def remove_nulls(val: Any) -> Any: ...

def remove_nulls(val: dict | list | Any) -> dict | list | Any:
    """
    Recursively remove all None values from dictionaries and lists, and returns
    the result as a new dictionary or list.
    """
    if isinstance(val, list):
        return [remove_nulls(x) for x in val if x is not None]

    elif isinstance(val, dict):
        return {k: remove_nulls(v) for k, v in val.items() if v is not None}

    else:
        return val

def pydantic_encoder_no_nulls(obj: Any) -> Any:
    return remove_nulls(pydantic_encoder(obj))

def get_filename(name: str) -> str:
    return re.sub(r"(?u)[^-\w. &\[\]']", "", name)

def as_str(v: Any) -> str:
    return v.value if isinstance(v, Enum) else str(v)

def getattrstr(obj: Any, field: str) -> str:
    return as_str(getattr(obj, field))

def scaling_grade(value: float, null_value: str = "-") -> str:
    if value >= 1.75: return "S"
    if value >= 1.4: return "A"
    if value >= 0.9: return "B"
    if value >= 0.6: return "C"
    if value >= 0.25: return "D"
    if value > 0.0: return "E"
    return null_value

def to_somber(level: int) -> int:
    return {
        0: 0, 1: 0,
        2: 1, 3: 1, 4: 1,
        5: 2, 6: 2,
        7: 3, 8: 3, 9: 3,
        10: 4, 11: 4,
        12: 5, 13: 5, 14: 5,
        15: 6, 16: 6,
        17: 7, 18: 7, 19: 7,
        20: 8, 21: 8,
        22: 9, 23: 9, 24: 9,
        25: 10,
    }[level]