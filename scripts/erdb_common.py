import json
import xml.etree.ElementTree as xmltree
import collections
import scripts.er_params as er_params
from operator import add
from itertools import repeat
from typing import Any, Callable, Iterator, NamedTuple, Optional, Tuple, Dict, List
from scripts.er_params import ParamDict, ParamRow
from scripts.er_params.enums import ItemIDFlag
from scripts.er_shop import Lookup

def _get_item_msg(filename: str, version: str) -> Dict[int, str]:
    tree = xmltree.parse(f"./source/{version}/{filename}.fmg.xml")
    entries = tree.getroot().findall(".//text")
    return {int(e.get("id")): e.text for e in entries if e.text != "%null%"}

class GeneratorDataBase(NamedTuple):

    class ParamDictRetriever(NamedTuple):
        file_name: str
        item_id_flag: ItemIDFlag
        id_min: Optional[int]=None
        id_max: Optional[int]=None

        def get(self, version: str) -> ParamDict:
            args = [self.file_name, version, self.item_id_flag]
            args += [arg for arg in [self.id_min, self.id_max] if arg is not None]
            return (er_params.load if len(args) <= 3 else er_params.load_ids)(*args)

    class MsgsRetriever(NamedTuple):
        file_name: str

        def get(self, version: str) -> Dict[str, str]:
            return _get_item_msg(self.file_name, version)

    class LookupRetriever(NamedTuple):
        shop_lineup_id_min: Optional[int]
        shop_lineup_id_max: Optional[int]
        material_set_id_min: Optional[int]
        material_set_id_max: Optional[int]

        def get(self, version: str) -> Lookup:
            Retr = GeneratorDataBase.ParamDictRetriever
            shop = Retr("ShopLineupParam", ItemIDFlag.NON_EQUIPABBLE, self.shop_lineup_id_min, self.shop_lineup_id_max)
            mats = Retr("EquipMtrlSetParam", ItemIDFlag.NON_EQUIPABBLE, self.material_set_id_min, self.material_set_id_max)
            return Lookup(shop.get(version), mats.get(version))

    main_param: ParamDict
    params: Dict[str, ParamDict]
    msgs: Dict[str, Dict[str, str]]
    lookups: Dict[str, Lookup]

    schema_properties: Dict
    schema_store: Dict[str, Dict]

    output_file: str = None
    schema_file: str = None
    element_name: str = None

    @staticmethod
    def get_key_name(row: ParamRow) -> str:
        return row.name

    @staticmethod
    def require_patching() -> bool:
        return True

    main_param_retriever: ParamDictRetriever = None
    param_retrievers: Dict[str, ParamDictRetriever] = None
    msgs_retrievers: Dict[str, MsgsRetriever] = None
    lookup_retrievers: Dict[str, LookupRetriever] = None

    schema_retriever: Callable[[], Tuple[Dict, Dict[str, Dict]]] = None

    main_param_iterator: Callable[["GeneratorDataBase", ParamDict], Iterator[ParamRow]] = None
    construct_object: Callable[["GeneratorDataBase", ParamRow], Dict] = None

    @classmethod
    def construct(cls, version: str) -> "GeneratorDataBase":
        def _retrieve_dict(retrievers):
            return {field_name: retrievers[field_name].get(version) for field_name in retrievers.keys()}

        main_param=cls.main_param_retriever.get(version)
        params=_retrieve_dict(cls.param_retrievers)
        msgs=_retrieve_dict(cls.msgs_retrievers)
        lookups=_retrieve_dict(cls.lookup_retrievers)
        properties, store = cls.schema_retriever()

        return cls(main_param, params, msgs, lookups, properties, store)

def load_schema(filename: str, subdirectory: str="") -> Tuple[str, Dict]:
    subdirectory = f"{subdirectory}/" if len(subdirectory) > 0 else subdirectory
    filename = f"{subdirectory}{filename}.schema.json"
    with open(f"./schema/{filename}", mode="r") as f:
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

def patch_keys(obj: Dict, schema: Dict) -> Dict:
    # delete excessive keys
    for key in (set(obj.keys()) - set(schema.keys())):
        del obj[key]

    # add missing base keys
    for key in (set(schema.keys()) - set(obj.keys())):
        obj[key] = schema[key].get("default", {})
    
    return obj

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

def find_offset_indices(base_index: int, params: ParamDict, possible_maxima: List[int], increment: int=1) -> Tuple[List[int], List[int]]:
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
    return [*map(add, repeat(base_index), levels)], levels