import logging
from dataclasses import asdict

import strawberry
from strawberry.types import Info

from wire_service.persistency.area import AreaDb
from wire_service.persistency.basic_ops import get_by_id
from wire_service.service_model.place import Place
from wire_service.service_model.session_extension import db_query
from wire_service.service_model.wrapper import DbProxy


@strawberry.type
class Area(DbProxy):
    id: strawberry.ID
    name: str
    short_name: str
    description: str

    places: list[Place]


@strawberry.type
class AreaQuery:
    @strawberry.field
    def areas(self, info: Info) -> list[Area]:
        return list(map(Area.wrap, db_query(info)(AreaDb)))

    @strawberry.field
    def area(self, id: strawberry.ID, info: Info) -> Area:
        return Area.wrap(get_by_id(info, AreaDb, id))


@strawberry.input
class AreaInput:
    short_name: str
    name: str
    description: str


@strawberry.type
class AreaMutation:
    @strawberry.mutation
    def add_area(self, new_area: AreaInput, info: Info) -> Area:
        s = info.context["session"]
        with s.begin():
            new_db_area = AreaDb(**asdict(new_area))
            logging.info(f"adding area {new_db_area}")
            s.add(new_db_area)
        return Area.wrap(new_db_area)
