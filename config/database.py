import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import (scoped_session, sessionmaker)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

engine = create_engine("sqlite:///" + os.path.join(BASE_DIR, "db.sqlite"), convert_unicode=True)

db_session = scoped_session(sessionmaker(bind=engine, autoflush=False, autocommit=False))

Base = declarative_base()
Base.query = db_session.query_property()

Base.metadata.create_all(bind=engine)
