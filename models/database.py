from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config import DATABASE

db_string = DATABASE

db = create_engine(db_string)
base = declarative_base()

Session = sessionmaker(db)
session = Session()


def create_db():
    base.metadata.create_all(db)

