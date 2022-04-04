from typing import List

import strawberry
from strawberry.types import Info

from wire_service.db_model import AreaDb

from .area import Area


def get_areas(root: "Query", info: Info) -> List[Area]:
    areas = info.context["session"].query(AreaDb)

    return list(map(Area, areas))


@strawberry.type
class Query:
    areas: List[Area] = strawberry.field(resolver=get_areas)
