from typing import Any, Callable, Iterator, NamedTuple
from unicodedata import normalize, combining

from erdb.loaders.params import load as load_params, load_ids as load_param_ids, load_msg
from erdb.loaders.contrib import load as load_contrib
from erdb.typing.game_version import GameVersion
from erdb.typing.params import ParamDict, ParamRow
from erdb.typing.enums import ItemIDFlag, GoodsRarity
from erdb.shop import Lookup


def _remove_accents(string: str) -> str:
    nfkd_form = normalize("NFKD", string)
    return "".join(c for c in nfkd_form if not combining(c))

class GeneratorDataBase(NamedTuple):

    class ParamDictRetriever(NamedTuple):
        file_name: str
        item_id_flag: ItemIDFlag
        id_min: int | None = None
        id_max: int | None = None

        def get(self, version: GameVersion) -> ParamDict:
            args = [self.file_name, version, self.item_id_flag]
            args += [arg for arg in [self.id_min, self.id_max] if arg is not None]
            return (load_params if len(args) <= 3 else load_param_ids)(*args)

    class MsgsRetriever(NamedTuple):
        file_name: str

        def get(self, version: GameVersion) -> dict[int, str]:
            return load_msg(self.file_name, version)

    class LookupRetriever(NamedTuple):
        shop_lineup_id_min: int | None
        shop_lineup_id_max: int | None
        material_set_id_min: int | None
        material_set_id_max: int | None
        recipe: bool = False

        def get(self, version: GameVersion) -> Lookup:
            Retr = GeneratorDataBase.ParamDictRetriever
            shop_param = "ShopLineupParam_Recipe" if self.recipe else "ShopLineupParam"
            shop = Retr(shop_param, ItemIDFlag.NON_EQUIPABBLE, self.shop_lineup_id_min, self.shop_lineup_id_max)
            mats = Retr("EquipMtrlSetParam", ItemIDFlag.NON_EQUIPABBLE, self.material_set_id_min, self.material_set_id_max)
            return Lookup(shop.get(version), mats.get(version))

    class UserDataRetriever(NamedTuple):
        def get(self, element_name: str, version: GameVersion) -> dict[str, dict]:
            return load_contrib(element_name, version)

    main_param: ParamDict
    params: dict[str, ParamDict]
    msgs: dict[str, dict[int, str]]
    lookups: dict[str, Lookup]
    user_data: dict[str, dict]

    @staticmethod
    def output_file() -> str:
        assert False, "output_file must be overridden"

    @staticmethod
    def element_name() -> str:
        assert False, "element_name must be overridden"

    @staticmethod
    def model() -> Any:
        assert False, "model must be overridden"

    def get_key_name(self, row: ParamRow) -> str:
        assert False, "get_key_name must be overridden"

    main_param_retriever: ParamDictRetriever = None
    param_retrievers: dict[str, ParamDictRetriever] = None
    msgs_retrievers: dict[str, MsgsRetriever] = None
    lookup_retrievers: dict[str, LookupRetriever] = None

    main_param_iterator: Callable[["GeneratorDataBase", ParamDict], Iterator[ParamRow]] = None
    construct_object: Callable[["GeneratorDataBase", ParamRow], dict] = None

    def get_fields_item(self, row: ParamRow, *, summary: bool = True, description: bool = True) -> dict[str, Any]:
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
            "description": self.msgs["descriptions"][row.index].split("\n") if description else ["no description"],
            "is_tradable": row.get("disableMultiDropShare") == "0", # assumption this exists for every param table
            "price_sold": row.get_int_corrected("sellValue"),       # assumption this exists for every param table
            "rarity": GoodsRarity.from_id(row.get_int("rarity")),   # assumption this exists for every param table
            "max_held": row.get_int("maxNum") if "maxNum" in row.keys else 999,
            "max_stored": row.get_int("maxRepositoryNum") if "maxRepositoryNum" in row.keys else 999,
        }

    def get_fields_user_data(self, row: ParamRow, *fields: str) -> dict[str, Any]:
        """
        Covers every user data field
        """
        row_name = self.get_key_name(row)

        def get_user_value(field: str):
            return self.user_data.get(row_name.replace(":", ""), {}).get(field)

        user_data = {field: get_user_value(field) for field in fields}
        user_data = {k: v for k, v in user_data.items() if v is not None}

        return user_data

    @classmethod
    def construct(cls, version: GameVersion) -> "GeneratorDataBase":
        def _retrieve_dict(retrievers):
            return {field_name: retrievers[field_name].get(version) for field_name in retrievers.keys()}

        main_param=cls.main_param_retriever.get(version)
        params=_retrieve_dict(cls.param_retrievers)
        msgs=_retrieve_dict(cls.msgs_retrievers)
        lookups=_retrieve_dict(cls.lookup_retrievers)
        user_data=cls.UserDataRetriever().get(cls.element_name(), version)

        return cls(main_param, params, msgs, lookups, user_data)

    def generate(self) -> dict:
        main_iter = self.main_param_iterator(self.main_param)
        return {_remove_accents(self.get_key_name(row)): self.construct_object(row) for row in main_iter}