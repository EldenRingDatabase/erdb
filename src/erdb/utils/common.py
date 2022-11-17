import collections
from operator import add
from itertools import repeat
from pathlib import Path
from typing import Any, Generator, Tuple, Dict, List

from erdb.typing.params import ParamDict


IntGen = Generator[int, None, None]

def update_nested(d, u):
    """
    Update function which recursively updates subdictionaries.
    Borrowed from https://stackoverflow.com/a/3233356
    """
    for k, v in u.items():
        if isinstance(v, collections.abc.Mapping):
            d[k] = update_nested(d.get(k, {}), v)
        else:
            d[k] = v
    return d

def update_optional(d: Dict, key: str, value: Any, null_value: Any=None) -> Dict:
    if value != null_value:
        d[key] = value
    return d

def find_offset_indices(base_index: int, params: ParamDict, possible_maxima: List[int], increment: int=1) -> Tuple[IntGen, IntGen]:
    """
    Returns lists of valid indices from `base_index` value which offset
    until the highest possible maxima is reached.

    First list is possible indices and second is raw level integers.
    """
    def _find_offset_maxima():
        for maxima in sorted(possible_maxima, reverse=True): # from largest
            if str(base_index + maxima * increment) in params.keys():
                return maxima

    maxima = _find_offset_maxima()
    levels = range(0, (maxima + 1) * increment, increment)
    return map(add, repeat(base_index), levels), levels

def strip_invalid_name(name: str) -> str:
    return name.removeprefix("[ERROR]").strip()

def prepare_writable_path(path: Path, default_filename: str) -> Path:
    (path if path.suffix == "" else path.parent).mkdir(parents=True, exist_ok=True)
    return path / default_filename if path.is_dir() else path
