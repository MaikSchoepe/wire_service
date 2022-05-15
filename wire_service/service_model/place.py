import logging
from typing import TYPE_CHECKING, List

import strawberry
from strawberry.types import Info

from wire_service.db_model.area import AreaDb
from wire_service.db_model.basic_ops import get_by_id
from wire_service.db_model.place import PlaceDb
from wire_service.service_model.session_extension import db_query

if TYPE_CHECKING:
    from wire_service.service_model.area import Area
else:
    Area = strawberry.LazyType["Area", "wire_service.service_model.area"]


@strawberry.type
class Place:
    def __init__(self, model: PlaceDb):
        self._model = model

    @strawberry.field
    def id(self) -> strawberry.ID:
        return strawberry.ID(str(self._model.id))

    @strawberry.field
    def name(self) -> str:
        return self._model.name

    @strawberry.field
    def short_name(self) -> str:
        return self._model.short_name

    @strawberry.field
    def description(self) -> str:
        return self._model.description

    @strawberry.field
    def area_id(self) -> strawberry.ID:
        return strawberry.ID(str(self._model.area_id))

    @strawberry.field
    def parent_area(
        self,
    ) -> Area:
        return Area.resolve_type().wrap(self._model.area)  # type: ignore


@strawberry.input
class PlaceInput(PlaceDb):
    short_name: str  # type: ignore
    name: str  # type: ignore
    description: str  # type: ignore


@strawberry.type
class PlaceQuery:
    @strawberry.field
    def places(self, info: Info) -> List[Place]:
        return list(map(Place, db_query(info)(PlaceDb)))

    @strawberry.field
    def place(self, id: strawberry.ID, info: Info) -> Place:
        return Place(get_by_id(info, PlaceDb, id))


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
            logging.info(f"adding place {new_place}")
            area.places.append(new_place)

        return Place(new_place)
