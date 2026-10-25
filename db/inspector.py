from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import MetaData, Table, inspect, select

from .base import get_engine


def list_tables() -> list[str]:
    inspector = inspect(get_engine())
    return sorted(inspector.get_table_names(schema="public"))


def _serialize(value):
    if isinstance(value, Decimal):
        return float(value)
    if isinstance(value, (datetime, date)):
        return value.isoformat()
    return value


def fetch_table_rows(table_name: str, limit: int = 500):
    engine = get_engine()
    if table_name not in list_tables():
        raise ValueError(f"Unknown table: {table_name}")

    metadata = MetaData()
    table = Table(table_name, metadata, autoload_with=engine, schema="public")
    with engine.connect() as conn:
        result = conn.execute(select(table).limit(limit))
        rows = [dict(row) for row in result.mappings()]

    columns = [c.name for c in table.columns]
    serialized_rows = [{k: _serialize(v) for k, v in row.items()} for row in rows]
    return columns, serialized_rows
