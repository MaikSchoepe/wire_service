from sqlalchemy import Column, Enum, ForeignKey, Integer, String, UnicodeText

from wire_service.service_model.outlet_kind import OutletKind

from . import Base


class OutletDb(Base):
    __tablename__ = "outlets"

    id = Column(Integer, primary_key=True)

    short_name: str = Column(String(10), unique=True)
    name: str = Column(String(128))
    description: str = Column(UnicodeText)
    kind: OutletKind = Column(Enum(OutletKind), nullable=False)

    face_id: int = Column(Integer, ForeignKey("faces.id"), nullable=False)

    def __repr__(self):
        return (
            f"Outlet({self.id!r}, {self.name!r} [{self.short_name!r}] - {self.kind!r})"
        )
