import logging
from typing import List

import strawberry
from strawberry.types import Info

from wire_service.persistency.basic_ops import get_by_id
from wire_service.persistency.model.cable import CableDb
from wire_service.persistency.model.cable_type import CableTypeDb
from wire_service.persistency.model.outlet import OutletDb
from wire_service.service_model.cable_type import CableType
from wire_service.service_model.outlet import Outlet
from wire_service.service_model.session_extension import db_query
from wire_service.service_model.wrapper import DbProxy


@strawberry.type
class Cable(DbProxy):
    id: strawberry.ID

    cable_type_id: strawberry.ID
    start_outlet_id: strawberry.ID
    end_outlet_id: strawberry.ID

    @strawberry.field
    def cable_type(
        self,
    ) -> CableType:
        return CableType.resolve_type().wrap(self._model.cable_type)  # type: ignore

    @strawberry.field
    def start_outlet(
        self,
    ) -> Outlet:
        return Outlet.resolve_type().wrap(self._model.start_outlet)  # type: ignore

    @strawberry.field
    def end_outlet(
        self,
    ) -> Outlet:
        return Outlet.resolve_type().wrap(self._model.end_outlet)  # type: ignore


@strawberry.type
class CableQuery:
    @strawberry.field
    def cables(self, info: Info) -> List[Cable]:
        return list(map(Cable.wrap, db_query(info)(CableDb)))

    @strawberry.field
    def cable(self, id: strawberry.ID, info: Info) -> Cable:
        return Cable.wrap(get_by_id(info, CableDb, id))


@strawberry.type
class CableMutation:
    @strawberry.mutation
    def add_cable(
        self,
        cable_type_id: strawberry.ID,
        start_outlet_id: strawberry.ID,
        end_outlet_id: strawberry.ID,
        info: Info,
    ) -> Cable:
        s = info.context["session"]
        with s.begin():
            cable_type = get_by_id(info, CableTypeDb, cable_type_id)
            start_outlet = get_by_id(info, OutletDb, start_outlet_id)
            end_outlet = get_by_id(info, OutletDb, end_outlet_id)
            new_db_cable = CableDb()
            new_db_cable.cable_type = cable_type
            new_db_cable.start_outlet = start_outlet
            new_db_cable.end_outlet = end_outlet
            s.add(new_db_cable)
            logging.info(f"adding cable {new_db_cable}")

        return Cable.wrap(new_db_cable)
