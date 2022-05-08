import json
import collections
from typing import Tuple, Dict
from jsonschema import validate, RefResolver, ValidationError

def load_schema(filename: str) -> Tuple[str, Dict]:
    filename = f"{filename}.schema.json"
    with open(f"./schema/{filename}", mode="r") as f:
        return filename, json.load(f)

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

        update_nested(properties_full, obj["properties"])
        store[filename] = schema

    return properties_full, store

def patch_keys(obj: Dict, schema: Dict) -> Dict:
    # delete excessive keys
    for key in (set(obj.keys()) - set(schema.keys())):
        del obj[key]

    # add missing base keys
    for key in (set(schema.keys()) - set(obj.keys())):
        obj[key] = schema[key].get("default", {})
    
    return obj

def validate_and_write(file_path: str, schema_name: str, data: Dict, store: Dict[str, Dict]) -> bool:
    try:
        resolver = RefResolver(base_uri="unused", referrer="unused", store=store)
        validate(data, store[schema_name], resolver=resolver)

    except ValidationError as e:
        readable_path = "/".join(str(part) for part in e.path)
        print(f"Failed to validate \"{readable_path}\": {e.message}")
        return False

    finally:
        with open(file_path, mode="w") as f:
            json.dump(data, f, indent=4, sort_keys=True)

    return True

# update function which recursively updates subdictionaries
# borrowed from https://stackoverflow.com/a/3233356
def update_nested(d, u):
    for k, v in u.items():
        if isinstance(v, collections.abc.Mapping):
            d[k] = update_nested(d.get(k, {}), v)
        else:
            d[k] = v
    return d