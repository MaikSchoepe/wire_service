import logging
from typing import TYPE_CHECKING, List

import strawberry
from strawberry.types import Info

from wire_service.db_model.basic_ops import get_by_id
from wire_service.db_model.face import FaceDb
from wire_service.db_model.place import PlaceDb
from wire_service.service_model.session_extension import db_query
from wire_service.service_model.wrapper import DbProxy

if TYPE_CHECKING:
    from wire_service.service_model.place import Place
else:
    Place = strawberry.LazyType["Place", "wire_service.service_model.place"]


@strawberry.type
class Face(DbProxy):
    place_id: strawberry.ID
    id: strawberry.ID
    order_index: int
    height: int
    width: int
    name: str
    short_name: str
    description: str

    @strawberry.field
    def parent_place(
        self,
    ) -> Place:
        return Place.resolve_type().wrap(self._model.place)  # type: ignore


@strawberry.input
class FaceInput(FaceDb):
    order_index: int = 0  # type: ignore
    short_name: str  # type: ignore
    height: int = 100  # type: ignore
    width: int = 100  # type: ignore
    name: str  # type: ignore
    description: str  # type: ignore


@strawberry.type
class FaceQuery:
    @strawberry.field
    def faces(self, info: Info) -> List[Face]:
        return list(map(Face.wrap, db_query(info)(FaceDb)))

    @strawberry.field
    def face(self, id: strawberry.ID, info: Info) -> Face:
        return Face.wrap(get_by_id(info, FaceDb, id))


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

        return Face.wrap(new_face)
