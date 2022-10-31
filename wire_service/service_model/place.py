import logging
from dataclasses import asdict
from typing import TYPE_CHECKING, List

import strawberry
from strawberry.types import Info

from wire_service.persistency.basic_ops import get_by_id
from wire_service.persistency.model.area import AreaDb
from wire_service.persistency.model.place import PlaceDb
from wire_service.service_model.session_extension import db_query
from wire_service.service_model.wrapper import DbProxy

if TYPE_CHECKING:
    from wire_service.service_model.area import Area
else:
    Area = strawberry.LazyType["Area", "wire_service.service_model.area"]


@strawberry.type
class Place(DbProxy):
    area_id: strawberry.ID

    id: strawberry.ID
    name: str
    short_name: str
    description: str

    @strawberry.field
    def parent_area(
        self,
    ) -> Area:
        return Area.resolve_type().wrap(self._model.area)  # type: ignore


@strawberry.input
class PlaceInput:
    short_name: str
    name: str
    description: str


@strawberry.type
class PlaceQuery:
    @strawberry.field
    def places(self, info: Info) -> List[Place]:
        return list(map(Place.wrap, db_query(info)(PlaceDb)))

    @strawberry.field
    def place(self, id: strawberry.ID, info: Info) -> Place:
        return Place.wrap(get_by_id(info, PlaceDb, id))


@strawberry.type
class PlaceMutation:
    @strawberry.mutation
    def add_place(
        self,
        area_id: strawberry.ID,
        new_place: PlaceInput,
        info: Info,
    ) -> Place:
        with info.context["session"].begin():
            area = get_by_id(info, AreaDb, area_id)
            new_db_place = PlaceDb(**asdict(new_place))
            logging.info(f"adding place {new_db_place}")
            area.places.append(new_db_place)

        return Place.wrap(new_db_place)
