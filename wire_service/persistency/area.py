from sqlalchemy import Column, Integer, String, UnicodeText
from sqlalchemy.orm import relationship

from .base import Base
from .place import PlaceDb


class AreaDb(Base):
    __tablename__ = "areas"

    id: int = Column(Integer, primary_key=True)

    short_name: str = Column(String(10), nullable=False, unique=True)
    name: str = Column(String(128), nullable=False)
    description: str = Column(UnicodeText, nullable=False)

    places = relationship(
        PlaceDb,
        backref="area",
        cascade="all, delete-orphan",
        uselist=True,
        enable_typechecks=False,
    )

    def __repr__(self):
        return f"Area({self.id!r}, {self.name!r} [{self.short_name!r}])"
