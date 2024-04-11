import os

from dotenv import load_dotenv

load_dotenv()

POSTGRES_USER = os.getenv("POSTGRES_USER", "")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "")
PG_HOST = os.getenv("PG_HOST", "")
PGPORT = os.getenv("PGPORT", "")
POSTGRES_DB = os.getenv("POSTGRES_DB", "")
SECRET_KEY = os.getenv("SECRET_KEY", "")


def get_postgresql_url():
    return f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{PG_HOST}:{PGPORT}/{POSTGRES_DB}"


def get_async_mssql_url():
    return "mssql+aioodbc://sa:1q2w3eRR!%40@localhost/FirstDB?charset=utf8&driver=ODBC+Driver+18+for+SQL+Server&TrustServerCertificate=yes"


def get_mssql_url():
    return "mssql+pymssql://sa:1q2w3eRR!%40@127.0.0.1:1433/FirstDB?charset=utf8"


def get_sync_postgresql_url():
    return f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{PG_HOST}:{PGPORT}/{POSTGRES_DB}"


def get_test_async_postgresql_url():
    return f"postgresql+asyncpg://test_{POSTGRES_USER}:test_{POSTGRES_PASSWORD}@{PG_HOST}:{PGPORT}/test_{POSTGRES_DB}"


def get_test_postgresql_url():
    return f"postgresql://test_{POSTGRES_USER}:test_{POSTGRES_PASSWORD}@{PG_HOST}:{PGPORT}/test_{POSTGRES_DB}"
