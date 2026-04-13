from db import get_connection
from config import SA

conn = get_connection(SA["user"], SA["password"])
cursor = conn.cursor()

row = cursor.fetchone()
if row is not None:
    print(row[0])

conn.close()
