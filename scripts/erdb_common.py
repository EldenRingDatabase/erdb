import json
import collections
from typing import List, Dict

def get_schema_properties(filename: str, path: List[str]=[]) -> Dict:
    with open(f"./schema/{filename}.schema.json") as f:
        schema = json.load(f)

    for part in path:
        schema = schema[part]

    return schema["properties"]

# update function which recursively updates subdictionaries
# borrowed from https://stackoverflow.com/a/3233356
def update_nested(d, u):
    for k, v in u.items():
        if isinstance(v, collections.abc.Mapping):
            d[k] = update_nested(d.get(k, {}), v)
        else:
            d[k] = v
    return d