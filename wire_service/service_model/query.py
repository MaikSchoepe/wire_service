from typing import Any, List, Optional, Union

import strawberry
from dynaconf import settings  # type: ignore
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from starlette.requests import Request
from starlette.responses import Response
from starlette.websockets import WebSocket
from strawberry.asgi import GraphQL
from strawberry.http import GraphQLHTTPResponse, process_result
from strawberry.types import ExecutionResult, Info

from wire_service.db_model import AreaDb

from .area import Area

engine = create_engine(settings.DB_PATH, echo=True, future=True)


class MyGraphQL(GraphQL):
    async def get_context(
        self,
        request: Union[Request, WebSocket],
        response: Optional[Response] = None,
    ) -> Optional[Any]:
        self._session = Session(engine)
        return {"request": request, "response": response, "session": self._session}

    async def process_result(
        self, request: Request, result: ExecutionResult
    ) -> GraphQLHTTPResponse:
        if self._session.is_active:
            self._session.close()
        return process_result(result)


def get_areas(root: "Query", info: Info) -> List[Area]:
    areas = info.context["session"].query(AreaDb)

    return list(map(Area, areas))


@strawberry.type
class Query:
    areas: List[Area] = strawberry.field(resolver=get_areas)
