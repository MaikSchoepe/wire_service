import logging

import strawberry
from strawberry.types import Info

from wire_service.db_model.area import AreaDb
from wire_service.db_model.place import PlaceDb
from wire_service.service_model.area import Area
from wire_service.service_model.place import Place


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

    @strawberry.mutation
    def add_place(
        self,
        area_id: strawberry.ID,
        short_name: str,
        name: str,
        description: str,
        info: Info,
    ) -> Place:
        session = info.context["session"]
        if (area := session.query(AreaDb).filter_by(id=area_id).first()) is None:
            raise Exception(f"Area with ID {id} not found")

        new_place = PlaceDb(short_name=short_name, name=name, description=description)
        logging.info(f"adding place {new_place}")
        area.places.append(new_place)
        session.commit()

        return Place(new_place)
