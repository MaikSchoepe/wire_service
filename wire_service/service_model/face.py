import logging
from typing import TYPE_CHECKING, List

import strawberry
from strawberry.types import Info

from wire_service.db_model.basic_ops import get_by_id
from wire_service.db_model.face import FaceDb
from wire_service.db_model.place import PlaceDb
from wire_service.service_model.session_extension import db_query

if TYPE_CHECKING:
    from wire_service.service_model.place import Place
else:
    Place = strawberry.LazyType["Place", "wire_service.service_model.place"]


@strawberry.type
class Face:
    def __init__(self, model: FaceDb):
        self._model = model

    @strawberry.field
    def id(self) -> strawberry.ID:
        return strawberry.ID(str(self._model.id))

    @strawberry.field
    def name(self) -> str:
        return self._model.name

    @strawberry.field
    def order_index(self) -> int:
        return self._model.order_index

    @strawberry.field
    def height(self) -> int:
        return self._model.height

    @strawberry.field
    def width(self) -> int:
        return self._model.width

    @strawberry.field
    def short_name(self) -> str:
        return self._model.short_name

    @strawberry.field
    def description(self) -> str:
        return self._model.description

    @strawberry.field
    def place_id(self) -> strawberry.ID:
        return strawberry.ID(str(self._model.place_id))

    @strawberry.field
    def parent_place(
        self,
    ) -> Place:
        return Place.resolve_type()(self._model.place)  # type: ignore


@strawberry.input
class FaceInput(FaceDb):
    order_index: int  # type: ignore
    short_name: str  # type: ignore
    height: int  # type: ignore
    width: int  # type: ignore
    name: str  # type: ignore
    description: str  # type: ignore


@strawberry.type
class FaceQuery:
    @strawberry.field
    def faces(self, info: Info) -> List[Face]:
        return list(map(Face, db_query(info)(FaceDb)))

    @strawberry.field
    def face(self, id: strawberry.ID, info: Info) -> Face:
        return Face(get_by_id(info, FaceDb, id))


@strawberry.type
class FaceMutation:
    @strawberry.mutation
    def add_face(
        self,
        place_id: strawberry.ID,
        new_face: FaceInput,
        info: Info,
    ) -> Face:
        with info.context["session"].begin():
            place = get_by_id(info, PlaceDb, place_id)
            logging.info(f"adding face {new_face}")
            place.faces.append(new_face)

        return Face(new_face)
