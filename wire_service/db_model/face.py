from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
    UnicodeText,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship

from wire_service.db_model.outlet import OutletDb

from .base import Base


class FaceDb(Base):
    __tablename__ = "faces"

    id: int = Column(Integer, primary_key=True)
    order_index: int = Column(Integer, nullable=False)

    short_name: str = Column(String(10), unique=True)
    name: str = Column(String(128))
    height: int = Column(Integer, nullable=False)
    width: int = Column(Integer, nullable=False)
    description: str = Column(UnicodeText)

    place_id: int = Column(Integer, ForeignKey("places.id"), nullable=False)

    outlets = relationship(
        OutletDb,
        backref="face",
        cascade="all, delete-orphan",
        uselist=True,
        enable_typechecks=False,
    )
    __table_args__ = (UniqueConstraint("place_id", "order_index"),)

    def __repr__(self):
        return f"Face({self.id!r}, {self.name!r} [{self.short_name!r}])"
