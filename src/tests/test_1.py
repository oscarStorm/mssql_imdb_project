import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from db import get_connection
from config import SA

# Open a connection to the database using the super admin login from config.py.
conn = get_connection(SA["user"], SA["password"])

# A cursor is the object that sends SQL statements to the database.
cursor = conn.cursor()

# Ask SQL Server for every base table in the current database.
# INFORMATION_SCHEMA.TABLES is a system view that stores table metadata.
cursor.execute("""
SELECT
    TABLE_SCHEMA,
    TABLE_NAME
FROM INFORMATION_SCHEMA.TABLES
WHERE TABLE_TYPE = 'BASE TABLE'
ORDER BY TABLE_SCHEMA, TABLE_NAME;
""")

# fetchall() returns all rows from the SELECT statement above.
tables = cursor.fetchall()

# Print each table as "schema.table", for example: dbo.movies
for table in tables:
    print(f"{table.TABLE_SCHEMA}.{table.TABLE_NAME}")

# Close the database connection when the query is finished.
conn.close()
