import logging

import strawberry
from strawberry.types import Info

from wire_service.db_model.area import AreaDb
from wire_service.service_model.area import Area


@strawberry.type
class Mutation:
    @strawberry.mutation
    def add_area(
        self, short_name: str, name: str, description: str, info: Info
    ) -> Area:
        session = info.context["session"]
        new_area = AreaDb(short_name=short_name, name=name, description=description)
        logging.info(f"adding area {new_area}")
        session.add(new_area)
        session.commit()
        return Area(new_area)
