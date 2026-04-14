from db import get_connection
from config import SA

conn = get_connection(SA["user"], SA["password"])
cursor = conn.cursor()

cursor.execute("""
SELECT TOP 5 *
FROM vw_person_search
WHERE primary_name LIKE '%nolan%'
ORDER BY primary_name
""")

for row in cursor.fetchall():
    print(row)

cursor.execute("""
SELECT TOP 5 *
FROM vw_movie_search
WHERE primary_title LIKE '%matrix%'
ORDER BY primary_title
""")

for row in cursor.fetchall():
    print(row)
conn.close()

print("done")
