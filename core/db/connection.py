import psycopg2

from psycopg2.extras import RealDictCursor
from psycopg2 import sql, errors
from core.config.config import (
    DB_HOST, DB_USER,
    DB_PASSWORD, DB_PORT
)

# BANCO
def get_connection(tenant_db):
    return psycopg2.connect(
        host=DB_HOST,
        database=tenant_db,
        user=DB_USER,
        password=DB_PASSWORD,
        port=DB_PORT
    )
