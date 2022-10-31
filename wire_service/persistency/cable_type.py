from sqlalchemy import Column, ForeignKey, Integer, String, UnicodeText
from sqlalchemy.orm import relationship

from .base import Base


class WireDb(Base):
    __tablename__ = "cable_types_wires"

    id: int = Column(Integer, primary_key=True)
    name: str = Column(String(128), nullable=False)
    color: str = Column(String(7), nullable=False)
    second_color: str = Column(String(7), nullable=True)

    cable_type_id: int = Column(Integer, ForeignKey("cable_types.id"), nullable=False)

    def __repr__(self):
        return f"Wire({self.name!r}, {self.color!r} [{self.second_color!r}])"


class CableTypeDb(Base):
    __tablename__ = "cable_types"

    id: int = Column(Integer, primary_key=True)

    name: str = Column(String(128), nullable=False)
    description: str = Column(UnicodeText, nullable=False)

    wires = relationship(
        WireDb,
        backref="cable_type",
        cascade="all, delete-orphan",
        uselist=True,
        enable_typechecks=False,
    )

    def __repr__(self):
        return f"CableType({self.id!r}, {self.name!r} [{self.wires!r}])"
