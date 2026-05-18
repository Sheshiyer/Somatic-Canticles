from __future__ import annotations

import json
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Generator

import psycopg
from pgvector.psycopg import register_vector

from .config import settings


def _get_connection_string() -> str:
    return settings.database_url


@contextmanager
def get_db() -> Generator[psycopg.Connection, None, None]:
    conn = psycopg.connect(_get_connection_string(), autocommit=False)
    register_vector(conn)
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def get_db_readonly() -> psycopg.Connection:
    conn = psycopg.connect(_get_connection_string(), autocommit=True)
    register_vector(conn)
    return conn


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))