from db import get_connection, execute_sql_file
from config import SA

conn = get_connection(SA["user"], SA["password"])

# execute_sql_file(conn, "../sql/01_create_tables.sql")
# execute_sql_file(conn, "../sql/02_create_indexes.sql")
# execute_sql_file(conn, "../sql/03_views.sql")
# execute_sql_file(conn, "../sql/04_procedures.sql")
execute_sql_file(conn, "../sql/05_security.sql")

conn.close()

print("login and users added")
# print("procedures created")
# print("Tables created and indexes created")
