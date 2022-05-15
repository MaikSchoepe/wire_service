from sqlalchemy import Column, ForeignKey, Integer, String, UnicodeText

from .base import Base


class FaceDb(Base):
    __tablename__ = "faces"

    id = Column(Integer, primary_key=True)

    short_name = Column(String(10), unique=True)
    name = Column(String(128))
    description = Column(UnicodeText)

    place_id = Column(Integer, ForeignKey("places.id"), nullable=False)

    def __repr__(self):
        return f"Face({self.id!r}, {self.name!r} [{self.short_name!r}])"
