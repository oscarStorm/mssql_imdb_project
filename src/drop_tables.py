from db import get_connection
from config import SA

conn = get_connection(SA["user"], SA["password"])
cursor = conn.cursor()


cursor.execute("drop table if exists title_writers")

cursor.execute("drop table if exists title_directors")

cursor.execute("drop table if exists title_genres")

cursor.execute("drop table if exists titles")

cursor.execute("drop table if exists persons")


conn.commit()
conn.close()

print("tables are dropped")
