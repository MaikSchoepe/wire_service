import typing

import strawberry

from wire_service.db_model.area import AreaDb

from .place import Place


@strawberry.type
class Area:
    # @classmethod
    # def marshal(cls, model: AreaDb) -> "Area":
    #     return cls(
    #         id=strawberry.ID(str(model.id)),
    #         name=model.name or "",
    #         short_name=model.short_name or "",
    #         description=model.description or "",
    #         # places=map(Place.marshal, model.places),
    #     )

    def __init__(self, model: AreaDb):
        self._model = model

    @strawberry.field
    def id(self) -> strawberry.ID:
        return strawberry.ID(str(self._model.id))

    @strawberry.field
    def name(self) -> str:
        return self._model.name or ""

    # name: str
    # short_name: str
    # description: str

    @strawberry.field
    def places(self) -> typing.List[Place]:
        return list(map(Place, self._model.places))
