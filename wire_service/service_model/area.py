import logging
from typing import List

import strawberry
from strawberry.types import Info

from wire_service.db_model.area import AreaDb
from wire_service.db_model.basic_ops import get_by_id
from wire_service.service_model.session_extension import db_query

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
    def places(self) -> List[Place]:
        return list(map(Place, self._model.places))


@strawberry.type
class AreaQuery:
    @strawberry.field
    def areas(self, info: Info) -> List[Area]:
        return list(map(Area, db_query(info)(AreaDb)))

    @strawberry.field
    def area(self, id: strawberry.ID, info: Info) -> Area:
        return Area(get_by_id(info, AreaDb, id))


@strawberry.input
class AreaInput(AreaDb):
    short_name: str  # type: ignore
    name: str  # type: ignore
    description: str  # type: ignore


@strawberry.type
class AreaMutation:
    @strawberry.mutation
    def add_area(self, new_area: AreaInput, info: Info) -> Area:
        s = info.context["session"]
        with s.begin():
            logging.info(f"adding area {new_area}")
            s.add(new_area)
        return Area(new_area)
