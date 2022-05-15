import strawberry
import uvicorn
from starlette.applications import Starlette
from starlette.middleware.cors import CORSMiddleware
from strawberry.asgi import GraphQL

from wire_service.service_model.mutation import Mutation
from wire_service.service_model.query import Query
from wire_service.service_model.session_extension import SessionExtension

schema = strawberry.Schema(
    query=Query, mutation=Mutation, extensions=[SessionExtension]
)

graphql_app = GraphQL(schema)

app = Starlette()
app.add_route("/graphql", graphql_app)
app.add_websocket_route("/graphql", graphql_app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_headers=["*"],
    allow_methods=["*"],
)

if __name__ == "__main__":
    uvicorn.run("wire_service.app:app", host="127.0.0.1", port=5000, log_level="info")
