import strawberry
import uvicorn
from strawberry.asgi import GraphQL

from wire_service.service_model.mutation import Mutation
from wire_service.service_model.query import Query
from wire_service.service_model.session_extension import SessionExtension

schema = strawberry.Schema(
    query=Query, mutation=Mutation, extensions=[SessionExtension]
)
app = GraphQL(schema)

if __name__ == "__main__":
    uvicorn.run("wire_service.app:app", host="127.0.0.1", port=5000, log_level="info")
