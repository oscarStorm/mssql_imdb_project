import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from db import get_connection
from config import APP

conn = get_connection(APP["user"], APP["password"])
cursor = conn.cursor()

cursor.execute("""
    select top 5 *
    from vw_movie_search
    """)

for row in cursor.fetchall():
    print(row)

cursor.execute("select top 5 * from titles")
print("should be and error")
conn.close()
