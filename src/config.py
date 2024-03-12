import os

from dotenv import load_dotenv

load_dotenv()

POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
PG_HOST = os.getenv("PG_HOST")
PGPORT = os.getenv("PGPORT")
POSTGRES_DB = os.getenv("POSTGRES_DB")
