import strawberry
import uvicorn

from wire_service.application import GraphQLApplication
from wire_service.service_model.query import Query

# Base.metadata.drop_all(engine)
# Base.metadata.create_all(engine)


# with Session(engine) as session:
#     test_place = PlaceDb(
#         name="Testplace", short_name="short2", description="Foobarplace"
#     )

#     test_area = AreaDb(name="Testarea", short_name="short1", description="Foobararea")

#     test_area.places.append(test_place)

#     session.add(test_area)
#     session.commit()

schema = strawberry.Schema(query=Query)
app = GraphQLApplication(schema)

if __name__ == "__main__":
    uvicorn.run("wire_service.app:app", host="127.0.0.1", port=5000, log_level="info")
