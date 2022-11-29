import re
from operator import add
from itertools import repeat
from pathlib import Path
from typing import Any, overload
from pydantic.json import pydantic_encoder

from erdb.typing.params import ParamDict


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