import logging
from typing import List

import strawberry
from strawberry.types import Info

from wire_service.db_model.area import AreaDb
from wire_service.db_model.basic_ops import get_by_id
from wire_service.db_model.place import PlaceDb
from wire_service.service_model.session_extension import db_query


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
        short_name: str,
        name: str,
        description: str,
        info: Info,
    ) -> Place:
        with info.context["session"].begin():
            if (area := get_by_id(info, AreaDb, area_id)) is None:
                raise Exception(f"Area with ID {id} not found")

            new_place = PlaceDb(
                short_name=short_name, name=name, description=description
            )
            logging.info(f"adding place {new_place}")
            area.places.append(new_place)

        return Place(new_place)
