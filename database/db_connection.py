import pyodbc

from database import config


def connect():
    if config.DB_USERNAME and config.DB_PASSWORD:
        return pyodbc.connect(
            f"DRIVER={{{config.DB_DRIVER}}};"
            f"SERVER={config.DB_SERVER};"
            f"UID={config.DB_USERNAME};"
            f"PWD={config.DB_PASSWORD};"
            f"DATABASE={config.DB_NAME};"
        )
    return pyodbc.connect(
        f"DRIVER={{{config.DB_DRIVER}}};"
        f"SERVER={config.DB_SERVER};"
        f"DATABASE={config.DB_NAME};"
    )


connection = connect()
