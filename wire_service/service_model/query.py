from typing import List

import strawberry
from strawberry.types import Info

from wire_service.db_model import AreaDb
from wire_service.db_model.place import PlaceDb
from wire_service.service_model.place import Place
from wire_service.service_model.session_extension import db_query

from .area import Area


def get_areas(root: "Query", info: Info) -> List[Area]:
    areas = db_query(info)(AreaDb)

    return list(map(Area, areas))


def get_area(root: "Query", id: strawberry.ID, info: Info) -> Area:
    if (area := db_query(info)(AreaDb).filter_by(id=id).first()) is None:
        raise Exception(f"Area with ID {id} not found")

    return Area(area)


def get_places(root: "Query", info: Info) -> List[Place]:
    places = db_query(info)(PlaceDb)

    return list(map(Place, places))


def get_place(root: "Query", id: strawberry.ID, info: Info) -> Place:
    if (place := db_query(info)(PlaceDb).filter_by(id=id).first()) is None:
        raise Exception(f"Place with ID {id} not found")

    return Place(place)


@strawberry.type
class Query:
    areas: List[Area] = strawberry.field(resolver=get_areas)
    area: Area = strawberry.field(resolver=get_area)

    places: List[Place] = strawberry.field(resolver=get_places)
    place: Place = strawberry.field(resolver=get_place)
