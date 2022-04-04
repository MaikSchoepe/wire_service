from typing import Any, Optional, Union

from starlette.requests import Request
from starlette.responses import Response
from starlette.websockets import WebSocket
from strawberry.asgi import GraphQL
from strawberry.http import GraphQLHTTPResponse, process_result
from strawberry.types import ExecutionResult

from wire_service.db_model.connection import Session


class GraphQLApplication(GraphQL):
    async def get_context(
        self,
        request: Union[Request, WebSocket],
        response: Optional[Response] = None,
    ) -> Optional[Any]:
        self._session = Session()
        return {"request": request, "response": response, "session": self._session}

    async def process_result(
        self, request: Request, result: ExecutionResult
    ) -> GraphQLHTTPResponse:
        if self._session.is_active:
            self._session.close()
        return process_result(result)
