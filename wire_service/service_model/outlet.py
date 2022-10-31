import logging
from dataclasses import asdict
from typing import TYPE_CHECKING, List

import strawberry
from strawberry.types import Info

from wire_service.persistency.basic_ops import get_by_id
from wire_service.persistency.model.face import FaceDb
from wire_service.persistency.model.outlet import OutletDb
from wire_service.service_model.outlet_kind import OutletKind
from wire_service.service_model.session_extension import db_query
from wire_service.service_model.wrapper import DbProxy

if TYPE_CHECKING:
    from wire_service.service_model.face import Face
else:
    Face = strawberry.LazyType["Face", "wire_service.service_model.face"]


@strawberry.type
class Outlet(DbProxy):
    face_id: strawberry.ID

    id: strawberry.ID
    name: str
    short_name: str
    description: str
    kind: OutletKind

    @strawberry.field
    def parent_face(
        self,
    ) -> Face:
        return Face.resolve_type().wrap(self._model.face)  # type: ignore


@strawberry.input
class OutletInput:
    short_name: str
    name: str
    description: str
    kind: OutletKind


@strawberry.type
class OutletQuery:
    @strawberry.field
    def outlets(self, info: Info) -> List[Outlet]:
        return list(map(Outlet.wrap, db_query(info)(OutletDb)))

    @strawberry.field
    def outlet(self, id: strawberry.ID, info: Info) -> Outlet:
        return Outlet.wrap(get_by_id(info, OutletDb, id))


@strawberry.type
class OutletMutation:
    @strawberry.mutation
    def add_outlet(
        self,
        face_id: strawberry.ID,
        new_outlet: OutletInput,
        info: Info,
    ) -> Outlet:
        with info.context["session"].begin():
            face = get_by_id(info, FaceDb, face_id)
            new_db_outlet = OutletDb(**asdict(new_outlet))
            logging.info(f"adding outlet {new_db_outlet}")
            face.outlets.append(new_db_outlet)

        return Outlet.wrap(new_db_outlet)
