from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
    UnicodeText,
    UniqueConstraint,
)

from .base import Base


class FaceDb(Base):
    __tablename__ = "faces"

    id = Column(Integer, primary_key=True)
    order_index = Column(Integer, nullable=False)

    short_name = Column(String(10), unique=True)
    name = Column(String(128))
    height = Column(Integer, nullable=False)
    width = Column(Integer, nullable=False)
    description = Column(UnicodeText)

    place_id = Column(Integer, ForeignKey("places.id"), nullable=False)

    __table_args__ = (UniqueConstraint("place_id", "order_index"),)

    def __repr__(self):
        return f"Face({self.id!r}, {self.name!r} [{self.short_name!r}])"
