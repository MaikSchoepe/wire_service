import strawberry

from wire_service.db_model.place import PlaceDb


@strawberry.type
class Place:
    def __init__(self, model: PlaceDb):
        self._model = model

    @strawberry.field
    def id(self) -> strawberry.ID:
        return strawberry.ID(str(self._model.id))

    @strawberry.field
    def area_id(self) -> strawberry.ID:
        return strawberry.ID(str(self._model.area_id))

    @strawberry.field
    def name(self) -> str:
        return self._model.name or ""

    @strawberry.field
    def short_name(self) -> str:
        return self._model.short_name or ""

    @strawberry.field
    def description(self) -> str:
        return self._model.description or ""
