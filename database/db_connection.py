import logging

import pyodbc

from database import config

logger = logging.getLogger(__name__)

_connection = None


class DatabaseConnectionError(Exception):
    pass


def _build_connection_string() -> str:
    parts = [f"DRIVER={{{config.DB_DRIVER}}}", f"SERVER={config.DB_SERVER}"]
    if config.DB_USERNAME and config.DB_PASSWORD:
        parts += [f"UID={config.DB_USERNAME}", f"PWD={config.DB_PASSWORD}"]
    parts.append(f"DATABASE={config.DB_NAME}")
    return ";".join(parts) + ";"


def get_connection() -> pyodbc.Connection:
    global _connection
    if _connection is None:
        logger.info("Connecting to database %s on %s", config.DB_NAME, config.DB_SERVER)
        try:
            _connection = pyodbc.connect(_build_connection_string())
        except pyodbc.Error as error:
            logger.exception("Database connection failed")
            raise DatabaseConnectionError(str(error)) from error
    return _connection
