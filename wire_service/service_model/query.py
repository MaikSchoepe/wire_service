from typing import List

import strawberry
from strawberry.types import Info

from wire_service.db_model import AreaDb

from .area import Area


def get_areas(root: "Query", info: Info) -> List[Area]:
    areas = info.context["session"].query(AreaDb)

    return list(map(Area, areas))


def get_area(root: "Query", id: strawberry.ID, info: Info) -> Area:
    if (area := info.context["session"].query(AreaDb).filter_by(id=id).first()) is None:
        raise Exception(f"Area with ID {id} not found")

    return Area(area)


@strawberry.type
class Query:
    areas: List[Area] = strawberry.field(resolver=get_areas)
    area: Area = strawberry.field(resolver=get_area)
