import logging
from dataclasses import asdict
from typing import TYPE_CHECKING
from xmlrpc.client import Boolean

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
class FaceInput:
    short_name: str
    height: int
    width: int
    name: str
    description: str


@strawberry.type
class FaceQuery:
    @strawberry.field
    def faces(self, info: Info) -> list[Face]:
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
        add_last: Boolean,
        new_face: FaceInput,
        info: Info,
    ) -> Face:
        with info.context["session"].begin():
            place = get_by_id(info, PlaceDb, place_id)
            new_db_face = FaceDb(**asdict(new_face))
            f = max if add_last else min
            order_index = f([p.order_index for p in place.faces], default=0)
            new_db_face.order_index = order_index + (1 if add_last else -1)
            logging.info(f"adding face {new_db_face}")
            place.faces.append(new_db_face)

        return Face.wrap(new_db_face)
