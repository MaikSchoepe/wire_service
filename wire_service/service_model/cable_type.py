from typing import Optional

import strawberry
from strawberry.types import Info

# from wire_service.persistency.basic_ops import get_by_id
from wire_service.persistency.model.cable_type import CableTypeDb
from wire_service.service_model.cable_kind import CableKind
from wire_service.service_model.session_extension import db_query
from wire_service.service_model.wrapper import DbProxy


@strawberry.type
class Wire:
    name: str
    color: str
    second_color: Optional[str]


@strawberry.type
class CableType(DbProxy):
    id: strawberry.ID
    name: str
    description: str
    kind: CableKind

    wires: list[Wire]


@strawberry.type
class CableTypeQuery:
    @strawberry.field
    def cable_types(self, info: Info) -> list[CableType]:
        return list(map(CableType.wrap, db_query(info)(CableTypeDb)))

    # @strawberry.field
    # def cable_type(self, id: strawberry.ID, info: Info) -> CableType:
    #     return CableType.wrap(get_by_id(info, CableTypeDb, id))
