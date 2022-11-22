import uvicorn
from fastapi import FastAPI, APIRouter, Depends

from erdb.app_api.endpoints import DataEndpoint, ItemEndpoint
from erdb.app_api.common import precache_data
from erdb.generators import Table


def _get_router(table: Table) -> APIRouter:
    router = APIRouter(
        prefix="/{game_version}/" + table.value,
        tags=[table.title],
    )

    for Endpoint in [DataEndpoint, ItemEndpoint]:
        endpoint = Endpoint(table)
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

app = FastAPI()

for tb in sorted(Table.effective()):
    app.include_router(_get_router(tb))

def serve(port: int, *, bind: str = "0.0.0.0", precache: bool = False):
    if precache:
        precache_data()

    uvicorn.run(app, host=bind, port=port)
