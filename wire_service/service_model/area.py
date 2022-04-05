import typing

import strawberry

from wire_service.db_model.area import AreaDb

from .place import Place


@strawberry.type
class Area:
    def __init__(self, model: AreaDb):
        self._model = model

    @strawberry.field
    def id(self) -> strawberry.ID:
        return strawberry.ID(str(self._model.id))

    @strawberry.field
    def name(self) -> str:
        return self._model.name or ""

    @strawberry.field
    def short_name(self) -> str:
        return self._model.short_name or ""

    @strawberry.field
    def description(self) -> str:
        return self._model.description or ""

    @strawberry.field
    def places(self) -> typing.List[Place]:
        return list(map(Place, self._model.places))
