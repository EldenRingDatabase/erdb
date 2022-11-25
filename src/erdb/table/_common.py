from typing import Any, Callable, Protocol
from unicodedata import normalize, combining

from erdb.typing.enums import GoodsRarity
from erdb.typing.params import ParamRow
from erdb.typing.api_version import ApiVersion
from erdb.table._retrievers import ParamDictRetriever, MsgsRetriever, ShopRetriever, ContribRetriever, RetrieverData


RowPredicate = Callable[[ParamRow], bool]

def _remove_accents(string: str) -> str:
    nfkd_form = normalize("NFKD", string)
    return "".join(c for c in nfkd_form if not combining(c))

class TableSpec(Protocol):
    model: dict[ApiVersion, Any]

    predicates: list[RowPredicate]

    main_param_retriever: ParamDictRetriever
    param_retrievers: dict[str, ParamDictRetriever]
    msg_retrievers: dict[str, MsgsRetriever]
    shop_retrievers: dict[str, ShopRetriever]
    contrib_retriever: ContribRetriever

    has_icons: bool

    @classmethod
    def title(cls) -> str:
        ...

    @classmethod
    def latest_api(cls) -> ApiVersion:
        ...

    @classmethod
    def get_pk(cls, data: RetrieverData, row: ParamRow) -> str:
        ...

    @classmethod
    def make_object(cls, api: ApiVersion, data: RetrieverData, row: ParamRow) -> Any:
        ...

class TableSpecContext:
    # specify defaults so providing everything isn't always necessary
    predicates: list[RowPredicate] = []
    param_retrievers: dict[str, ParamDictRetriever] = {}
    msg_retrievers: dict[str, MsgsRetriever] = {}
    shop_retrievers: dict[str, ShopRetriever] = {}
    contrib_retriever: ContribRetriever = ContribRetriever()
    has_icons = True

    @classmethod # override
    def title(cls) -> str:
        return cls.__name__.removesuffix("TableSpec")

    @classmethod # override
    def latest_api(cls: TableSpec) -> ApiVersion:
        return list(cls.model.keys())[-1]

    @classmethod # override
    def get_pk(cls, data: RetrieverData, row: ParamRow) -> str:
        assert "names" in data.msgs, "names were not parsed, override get_pk() for non-standard pk"
        return _remove_accents(cls.parse_name(data.msgs["names"][row.index]))

    @classmethod
    def parse_name(cls, name: str) -> str:
        return name.removeprefix("[ERROR]").strip()

    @classmethod
    def make_item(cls, data: RetrieverData, row: ParamRow, *, summary: bool = True, description: bool = True) -> dict[str, Any]:
        assert "names" in data.msgs, "make_item() cannot be called without names parsed"
        assert not summary or "summaries" in data.msgs, "Summary specified, yet no summaries were parsed"
        assert not description or "descriptions" in data.msgs, "Description specified, yet no descriptions were parsed"

        # individual items might not have summaries or descriptions
        summary = summary and row.index in data.msgs["summaries"]
        description = description and row.index in data.msgs["descriptions"]

        return {
            "full_hex_id": row.index_hex,
            "id": row.index,
            "name": cls.parse_name(data.msgs["names"][row.index]),
            "summary": data.msgs["summaries"][row.index] if summary else "no summary",
            "description": data.msgs["descriptions"][row.index].split("\n") if description else ["no description"],
            "is_tradable": row.get("disableMultiDropShare") == "0", # assumption this exists for every param table
            "price_sold": row.get_int_corrected("sellValue"),       # assumption this exists for every param table
            "rarity": GoodsRarity.from_id(row.get_int("rarity")),   # assumption this exists for every param table
            "max_held": row.get_int("maxNum") if "maxNum" in row.keys else 999,
            "max_stored": row.get_int("maxRepositoryNum") if "maxRepositoryNum" in row.keys else 999,
        }

    @classmethod
    def make_contrib(cls, data: RetrieverData, row: ParamRow, *fields: str) -> dict[str, Any]:
        row_name = cls.get_pk(data, row)

        def get_user_value(field: str):
            return data.contrib.get(row_name.replace(":", ""), {}).get(field)

        user_data = {field: get_user_value(field) for field in fields}
        user_data = {k: v for k, v in user_data.items() if v is not None}

        return user_data