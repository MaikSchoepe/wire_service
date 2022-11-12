from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from wire_service.persistency.model.cable_type import CableTypeDb
from wire_service.persistency.model.outlet import OutletDb

from . import Base


class CableDb(Base):
    __tablename__ = "cables"

    id = Column(Integer, primary_key=True)

    cable_type_id: int = Column(Integer, ForeignKey("cable_types.id"), nullable=False)
    start_outlet_id: int = Column(Integer, ForeignKey("outlets.id"), nullable=False)
    end_outlet_id: int = Column(Integer, ForeignKey("outlets.id"), nullable=False)

    cable_type = relationship(CableTypeDb, uselist=False)
    start_outlet = relationship(OutletDb, uselist=False, foreign_keys=[start_outlet_id])
    end_outlet = relationship(OutletDb, uselist=False, foreign_keys=[end_outlet_id])

    def __repr__(self):
        return f"Cable({self.id!r}, From: {self.start_outlet} - To: {self.end_outlet} [{self.cable_type}]"
