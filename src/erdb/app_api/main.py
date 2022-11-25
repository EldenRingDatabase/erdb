import uvicorn
from fastapi import FastAPI, APIRouter, Depends
from fastapi_versioning import VersionedFastAPI, versioned_api_route

from erdb.app_api.endpoints import DataEndpoint, ItemEndpoint
from erdb.app_api.common import precache_data
from erdb.typing.api_version import ApiVersion
from erdb.table import Table


def _get_router(api: ApiVersion, table: Table) -> APIRouter:
    router = APIRouter(
        prefix="/{game_version}/" + table.value,
        route_class=versioned_api_route(api),
        tags=[table.title],
    )

    for Endpoint in [DataEndpoint, ItemEndpoint]:
        endpoint = Endpoint(api, table)
        router.add_api_route(
            endpoint.route,
            lambda dep = Depends(endpoint): dep,
            response_model=endpoint.model,
            response_model_exclude_none=True,
            responses=endpoint.responses,
            summary=endpoint.summary,
            description=endpoint.description
        )

    return router

def serve(port: int, *, bind: str = "0.0.0.0", precache: bool = False):
    if precache:
        precache_data()

    app = FastAPI(title="ERDB API Docs", description="RESTful API documentation for ERDB.")

    for tb in sorted(Table.effective()):
        for api in tb.spec.model.keys():
            app.include_router(_get_router(api, tb))

    app = VersionedFastAPI(app, version_format="API v{major}", prefix_format="/v{major}")

    uvicorn.run(app, host=bind, port=port)
