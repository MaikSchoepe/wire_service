import strawberry

from wire_service.db_model.place import PlaceDb


@strawberry.type
class Place:
    # @classmethod
    # def marshal(cls, model: PlaceDb) -> "Place":
    #     return cls(
    #         id=strawberry.ID(str(model.id)),
    #         name=model.name or "",
    #         short_name=model.short_name or "",
    #         description=model.description or "",
    #     )
    def __init__(self, model: PlaceDb):
        self._model = model

    @strawberry.field
    def id(self) -> strawberry.ID:
        return strawberry.ID(str(self._model.id))

    @strawberry.field
    def name(self) -> str:
        return self._model.name or ""

    # short_name: str
    # description: str
