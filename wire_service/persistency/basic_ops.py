from typing import Type

from strawberry.types import Info

from wire_service.service_model.session_extension import db_query

from .model import Base


def get_by_id(info: Info, db_class: Type[Base], id: str):
    if (db_object := db_query(info)(db_class).filter_by(id=id).first()) is None:
        raise Exception(f"{db_class.__name__[:-2]} with ID {id} not found")

    return db_object
