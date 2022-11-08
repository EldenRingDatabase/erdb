from zipfile import Path as ZipPath
import xml.etree.ElementTree as xmltree
import scripts.config as cfg
import scripts.er_params as er_params
import scripts.user_data as user_data
from typing import Any, Callable, Iterator, List, NamedTuple, Optional, Tuple, Dict
from scripts.game_version import GameVersion
from scripts.er_params import ParamDict, ParamRow
from scripts.er_params.enums import ItemIDFlag
from scripts.er_shop import Lookup

def _get_item_msg(filename: str, version: GameVersion) -> Dict[int, str]:
    archive = cfg.ROOT / "gamedata" / "_Extracted" / f"{version}.zip"
    with ZipPath(archive, at=f"{filename}.fmg.xml").open(mode="r", encoding="utf-8") as f:
        tree = xmltree.fromstring(f.read())
        entries = tree.findall(".//text")

    return {int(e.get("id")): e.text for e in entries if e.text != "%null%"}

def _parse_description(desc: str) -> List[str]:
    return desc.replace("—", " - ").split("\n")

class GeneratorDataBase(NamedTuple):

    class ParamDictRetriever(NamedTuple):
        file_name: str
        item_id_flag: ItemIDFlag
        id_min: Optional[int]=None
        id_max: Optional[int]=None

        def get(self, version: GameVersion) -> ParamDict:
            args = [self.file_name, version, self.item_id_flag]
            args += [arg for arg in [self.id_min, self.id_max] if arg is not None]
            return (er_params.load if len(args) <= 3 else er_params.load_ids)(*args)

    class MsgsRetriever(NamedTuple):
        file_name: str

        def get(self, version: GameVersion) -> Dict[int, str]:
            return _get_item_msg(self.file_name, version)

    class LookupRetriever(NamedTuple):
        shop_lineup_id_min: Optional[int]
        shop_lineup_id_max: Optional[int]
        material_set_id_min: Optional[int]
        material_set_id_max: Optional[int]

        def get(self, version: GameVersion) -> Lookup:
            Retr = GeneratorDataBase.ParamDictRetriever
            shop = Retr("ShopLineupParam", ItemIDFlag.NON_EQUIPABBLE, self.shop_lineup_id_min, self.shop_lineup_id_max)
            mats = Retr("EquipMtrlSetParam", ItemIDFlag.NON_EQUIPABBLE, self.material_set_id_min, self.material_set_id_max)
            return Lookup(shop.get(version), mats.get(version))

    class UserDataRetriever(NamedTuple):
        def get(self, element_name: str, version: GameVersion) -> Dict[str, Dict]:
            return user_data.read(element_name, version)

    main_param: ParamDict
    params: Dict[str, ParamDict]
    msgs: Dict[str, Dict[int, str]]
    lookups: Dict[str, Lookup]
    user_data: Dict[str, Dict]

    schema_properties: Dict
    schema_store: Dict[str, Dict]

    @staticmethod
    def output_file() -> str:
        assert False, "output_file must be overridden"

    @staticmethod
    def schema_file() -> str:
        assert False, "schema_file must be overridden"

    @staticmethod
    def element_name() -> str:
        assert False, "element_name must be overridden"

    def get_key_name(self, row: ParamRow) -> str:
        assert False, "get_key_name must be overridden"

    main_param_retriever: ParamDictRetriever = None
    param_retrievers: Dict[str, ParamDictRetriever] = None
    msgs_retrievers: Dict[str, MsgsRetriever] = None
    lookup_retrievers: Dict[str, LookupRetriever] = None

    schema_retriever: Callable[[], Tuple[Dict, Dict[str, Dict]]] = None

    main_param_iterator: Callable[["GeneratorDataBase", ParamDict], Iterator[ParamRow]] = None
    construct_object: Callable[["GeneratorDataBase", ParamRow], Dict] = None

    def get_fields_item(self, row: ParamRow, *, summary: bool = True, description: bool = True) -> Dict[str, Any]:
        """
        Covers every common field specified in item.schema.json
        """

        assert not summary or "summaries" in self.msgs, "Summary specified, yet no summaries were parsed"
        assert not description or "descriptions" in self.msgs, "Description specified, yet no descriptions were parsed"

        # individual items might not have summaries or descriptions
        summary = summary and row.index in self.msgs["summaries"]
        description = description and row.index in self.msgs["descriptions"]

        return {
            "full_hex_id": row.index_hex,
            "id": row.index,
            "name": self.get_key_name(row),
            "summary": self.msgs["summaries"][row.index] if summary else "no summary",
            "description": _parse_description(self.msgs["descriptions"][row.index]) if description else "no description",
            "is_tradable": row.get("disableMultiDropShare") == "0", # assumption this exists for every param table
            "price_sold": row.get_int_corrected("sellValue"),       # assumption this exists for every param table
            "max_held": row.get_int("maxNum") if "maxNum" in row.keys else 999,
            "max_stored": row.get_int("maxRepositoryNum") if "maxRepositoryNum" in row.keys else 999,
        }

    def get_fields_user_data(self, row: ParamRow, *args: str) -> Dict[str, Any]:
        """
        Covers every user data field
        """
        def get_user_data(row: str, field: str):
            assert field in self.schema_properties
            return self.user_data.get(row.replace(":", ""), {}).get(field, self.schema_properties[field].get("default", {}))

        name = self.get_key_name(row)
        return {arg: get_user_data(name, arg) for arg in args}

    @classmethod
    def construct(cls, version: GameVersion) -> "GeneratorDataBase":
        def _retrieve_dict(retrievers):
            return {field_name: retrievers[field_name].get(version) for field_name in retrievers.keys()}

        main_param=cls.main_param_retriever.get(version)
        params=_retrieve_dict(cls.param_retrievers)
        msgs=_retrieve_dict(cls.msgs_retrievers)
        lookups=_retrieve_dict(cls.lookup_retrievers)
        user_data=cls.UserDataRetriever().get(cls.element_name(), version)
        properties, store = cls.schema_retriever()

        return cls(main_param, params, msgs, lookups, user_data, properties, store)

    def generate(self) -> Dict:
        main_iter = self.main_param_iterator(self.main_param)
        return {self.get_key_name(row): self.construct_object(row) for row in main_iter}