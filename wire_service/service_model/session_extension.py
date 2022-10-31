from typing import Callable

from strawberry.extensions import Extension
from strawberry.types import Info

from wire_service.persistency.connection import DbConnection


class SessionExtension(Extension):
    def on_request_start(self):
        if not self.execution_context.context:
            self.execution_context.context = {}
        self.execution_context.context["session"] = DbConnection.Session()

    def on_request_end(self):
        session = self.execution_context.context.get("session", None)
        if session and session.is_active:
            session.close()


# get session and query from info
def db_query(info: Info) -> Callable:
    return info.context["session"].query
