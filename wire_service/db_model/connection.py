from dynaconf import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine(settings.DB_PATH, echo=True, future=True)
Session = sessionmaker(engine)
