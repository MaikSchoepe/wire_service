from wire_service.persistency.connection import DbConnection
from wire_service.persistency.model.cable_type import CableTypeDb, WireDb
from wire_service.settings import load_cable_types


def config_wire_types():
    cable_types_config = load_cable_types()
    with DbConnection.Session.begin() as s:
        for cable_type in cable_types_config:
            cable_type_db = (
                s.query(CableTypeDb).filter_by(name=cable_type["name"]).first()
            )
            if cable_type_db is None:
                new_cable_type = CableTypeDb(
                    name=cable_type["name"], description=cable_type["description"]
                )
                for wire in cable_type["wires"]:
                    new_cable_type.wires.append(WireDb(**wire))
                s.add(new_cable_type)
