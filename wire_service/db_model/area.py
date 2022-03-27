from sqlalchemy import Column, Integer, String, UnicodeText
from sqlalchemy.orm import relationship

from .base import Base
from .place import PlaceDb


class AreaDb(Base):
    __tablename__ = "areas"

    id = Column(Integer, primary_key=True)

    short_name = Column(String(10), unique=True)
    name = Column(String(128))
    description = Column(UnicodeText)

    places = relationship(
        PlaceDb, backref="area", cascade="all, delete-orphan", uselist=True
    )

    def __repr__(self):
        return f"Area({self.id!r}, {self.name!r} [{self.short_name!r}])"
