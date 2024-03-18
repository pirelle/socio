from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from config import get_test_postgresql_url
from utils.database import BaseWithId
from utils.models import *  # noqa

engine = create_engine(get_test_postgresql_url())
session = scoped_session(sessionmaker(bind=engine))

BaseWithId.metadata.create_all(engine)
