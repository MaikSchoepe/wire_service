from dynaconf import settings  # type: ignore
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from wire_service.db_model import AreaDb, Base, PlaceDb

engine = create_engine(settings.DB_PATH, echo=True, future=True)

Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)


with Session(engine) as session:
    test_place = PlaceDb(
        name="Testplace", short_name="short2", description="Foobarplace"
    )

    test_area = AreaDb(name="Testarea", short_name="short1", description="Foobararea")

    test_area.places.append(test_place)

    session.add(test_area)
    session.commit()
