from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
    UnicodeText,
    UniqueConstraint,
)

from .base import Base


def mydefault():
    global i
    i += 1
    return i


class FaceDb(Base):
    __tablename__ = "faces"

    id: int = Column(Integer, primary_key=True)
    order_index: int = Column(Integer, nullable=False, default=mydefault)

    short_name: str = Column(String(10), unique=True)
    name: str = Column(String(128))
    height: int = Column(Integer, nullable=False)
    width: int = Column(Integer, nullable=False)
    description: str = Column(UnicodeText)

    place_id: int = Column(Integer, ForeignKey("places.id"), nullable=False)

    __table_args__ = (UniqueConstraint("place_id", "order_index"),)

    def __repr__(self):
        return f"Face({self.id!r}, {self.name!r} [{self.short_name!r}])"
