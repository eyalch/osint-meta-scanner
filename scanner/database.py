import os

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

db_url = os.getenv("DATABASE_URL")

engine = create_engine(db_url)

Session = sessionmaker(engine)


class Base(DeclarativeBase):
    pass
