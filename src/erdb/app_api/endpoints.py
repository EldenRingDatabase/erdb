from typing import Any
from fastapi import Query, status
from fastapi.responses import JSONResponse
from pydantic.dataclasses import dataclass

from erdb.table import Table
from erdb.app_api.common import GameVersionEnum, generate, as_str
from erdb.typing.api_version import ApiVersion


@dataclass
class _Detail:
    detail: str

class DataEndpoint:
    api: ApiVersion
    table: Table

    def __init__(self, api: ApiVersion, table: Table) -> None:
        self.api = api
        self.table = table

    @property
    def route(self) -> str:
        return "/"

    @property
    def model(self) -> Any:
        return dict[str, self.table.spec.model[self.api]] # type: ignore

    @property
    def summary(self) -> str:
        return "multiple items"

    @property
    def description(self) -> str:
        return "Retrieve a dictionary of item's ascii name -> item properties."

    @property
    def responses(self) -> dict[int, dict]:
        return {
            status.HTTP_400_BAD_REQUEST: {
                "model": _Detail,
                "description": "Bad Request: `query` format is valid, but the specified field does not exist for this model."
            }
        }

    def __call__(self,
        game_version: GameVersionEnum,
        keys: list[str] | None = Query(None, alias="k", description="Specify a list of keys (ascii names) to retrieve specific items."),
        query: str | None = Query(None, description="Filter elements by field in format \"{field}:{value}\".", regex=r"^\w+\:.+$"),
    ) -> Any:
        data = generate(self.api, game_version, self.table)

        if keys is not None:
            data = {k: v for k, v in data.items() if k in keys}

        if query is not None:
            field, value = query.split(":", maxsplit=1)

            try:
                data = {k: v for k, v in data.items() if as_str(v, field) == value}
            
            except AttributeError:
                return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"detail": f"{self.table.title} has no field: \"{field}\"."})

        return data

class ItemEndpoint:
    api: ApiVersion
    table: Table

    def __init__(self, api: ApiVersion, table: Table) -> None:
        self.api = api
        self.table = table

    @property
    def route(self) -> str:
        return "/{key}"

    @property
    def model(self) -> Any:
        return self.table.spec.model[self.api]

    @property
    def summary(self) -> str:
        return "single item"

    @property
    def description(self) -> str:
        return "Retrieve properties of a single item."

    @property
    def responses(self) -> dict[int, dict]:
        return {
            status.HTTP_404_NOT_FOUND: {"model": _Detail}
        }

    def __call__(self, game_version: GameVersionEnum, key: str) -> Any:
        try:
            return generate(self.api, game_version, self.table)[key]

        except KeyError:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"detail": f"{self.table.title} has no key: \"{key}\""})