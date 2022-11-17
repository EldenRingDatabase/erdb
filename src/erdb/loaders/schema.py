import json
from typing import Tuple, Dict

from erdb.loaders import PKG_DATA_PATH
from erdb.utils.common import update_nested


def load(filename: str, subdirectory: str="") -> Tuple[str, Dict]:
    subdirectory = f"{subdirectory}/" if len(subdirectory) > 0 else subdirectory
    filename = f"{subdirectory}{filename}.schema.json"
    with open(PKG_DATA_PATH / "schema" / filename, mode="r", encoding="utf-8") as f:
        return filename, json.load(f)

def load_enums(*enum_names: str) -> Dict[str, Dict]:
    enums = {}

    for enum_name in enum_names:
        filename, schema = load(enum_name, subdirectory="enums")
        enums[filename] = schema

    return enums

def load_properties(*references: str) -> Tuple[Dict, Dict[str, Dict]]:
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
        filename, schema = load(filename)

        obj = schema
        for part in path:
            obj = obj[part]

        update_nested(properties_full, obj)
        store[filename] = schema

    return properties_full, store