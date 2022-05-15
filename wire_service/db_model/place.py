from sqlalchemy import Column, ForeignKey, Integer, String, UnicodeText
from sqlalchemy.orm import relationship

from wire_service.db_model.face import FaceDb

from .base import Base


class PlaceDb(Base):
    __tablename__ = "places"

    id = Column(Integer, primary_key=True)

    short_name = Column(String(10), unique=True)
    name = Column(String(128))
    description = Column(UnicodeText)

    area_id = Column(Integer, ForeignKey("areas.id"), nullable=False)

    faces = relationship(
        FaceDb,
        backref="place",
        cascade="all, delete-orphan",
        uselist=True,
        enable_typechecks=False,
    )

    def __repr__(self):
        return f"Place({self.id!r}, {self.name!r} [{self.short_name!r}])"
