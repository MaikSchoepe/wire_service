from sqlalchemy import Column, ForeignKey, Integer, String, UnicodeText
from sqlalchemy.orm import relationship

from . import Base
from .face import FaceDb


class PlaceDb(Base):
    __tablename__ = "places"

    id = Column(Integer, primary_key=True)

    short_name: str = Column(String(10), unique=True)
    name: str = Column(String(128))
    description: str = Column(UnicodeText)

    area_id: int = Column(Integer, ForeignKey("areas.id"), nullable=False)

    faces = relationship(
        FaceDb,
        backref="place",
        cascade="all, delete-orphan",
        uselist=True,
        enable_typechecks=False,
    )

    def __repr__(self):
        return f"Place({self.id!r}, {self.name!r} [{self.short_name!r}])"
