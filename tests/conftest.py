from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from config import get_test_postgresql_url
from utils.models import *
from utils.database import BaseWithId

engine = create_engine(get_test_postgresql_url())
session = scoped_session(sessionmaker(bind=engine))

BaseWithId.metadata.create_all(engine)
