import os

DB_DRIVER = os.environ.get("ANALYZER_DB_DRIVER", "SQL Server")
DB_SERVER = os.environ.get("ANALYZER_DB_SERVER", ".")
DB_NAME = os.environ.get("ANALYZER_DB_NAME", "Users")
DB_USERNAME = os.environ.get("ANALYZER_DB_USERNAME")
DB_PASSWORD = os.environ.get("ANALYZER_DB_PASSWORD")

WINDOW_TITLE = "Analyze Data"
WINDOW_SIZE = "1000x620"
