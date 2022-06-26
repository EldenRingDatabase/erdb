import json
import collections
import scripts.config as cfg
from operator import add
from itertools import repeat
from typing import Any, Generator, Tuple, Dict, List
from scripts.er_params import ParamDict

IntGen = Generator[int, None, None]

def load_schema(filename: str, subdirectory: str="") -> Tuple[str, Dict]:
    subdirectory = f"{subdirectory}/" if len(subdirectory) > 0 else subdirectory
    filename = f"{subdirectory}{filename}.schema.json"
    with open(cfg.ROOT / "schema" / filename, mode="r") as f:
        return filename, json.load(f)

def get_schema_enums(*enum_names: str) -> Dict[str, Dict]:
    enums = {}

    for enum_name in enum_names:
        filename, schema = load_schema(enum_name, subdirectory="enums")
        enums[filename] = schema

    return enums

def get_schema_properties(*references: str) -> Tuple[Dict, Dict[str, Dict]]:
    """
    Parse and merge properties of individual schemas.
    Takes in references to objects containing the "properties" field of a schema.
    Becuase the properties get merged, the order of references matters.

    Format: "<base schema filename>/path/to/object", ex. "spirit-ashes/definitions/SpiritAsh"

    Returns the merged property dict and schemas that were parsed in full as a filename->schema dict.
    """
    properties_full = {}
    store = {}

    for ref in references:
        filename, *path = ref.split("/")
        filename, schema = load_schema(filename)

        obj = schema
        for part in path:
            obj = obj[part]

        update_nested(properties_full, obj)
        store[filename] = schema

    return properties_full, store

def parse_description(desc: str) -> List[str]:
    return desc.replace("—", " - ").split("\n")

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