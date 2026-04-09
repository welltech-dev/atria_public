from flask import (
    session, abort
)

from core.db.connection import get_connection

def get_tenant_connection():
    tenant_db = session.get("tenant_db")
    if not tenant_db:
        abort(403)
    return get_connection(tenant_db)