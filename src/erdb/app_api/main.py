import uvicorn
from fastapi import FastAPI, APIRouter, Depends
from fastapi_versioning import VersionedFastAPI, versioned_api_route
from fastapi.middleware.cors import CORSMiddleware

from erdb.app_api.endpoints import DataEndpoint, ItemEndpoint
from erdb.app_api.common import DataProxy
from erdb.typing.api_version import ApiVersion
from erdb.table import Table


def _get_router(data_proxy: DataProxy, api: ApiVersion, table: Table) -> APIRouter:
    router = APIRouter(
        prefix="/{game_version}/" + table.value,
        route_class=versioned_api_route(api),
        tags=[table.title],
    )

    for Endpoint in [DataEndpoint, ItemEndpoint]:
        endpoint = Endpoint(data_proxy, api, table)
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
    with DataProxy.in_temp_dir(prefix="erdb-cache-") as data_proxy:
        if precache:
            data_proxy.precache()

        app = FastAPI(title="ERDB API Docs", description="RESTful API documentation for ERDB.")

        for tb in sorted(Table.effective()):
            for api in tb.spec.model.keys():
                app.include_router(_get_router(data_proxy, api, tb))

        app = VersionedFastAPI(app, version_format="API v{major}", prefix_format="/v{major}")
        app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["GET"], allow_headers=["*"])

        uvicorn.run(app, host=bind, port=port)
