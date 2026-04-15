import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))


from db import get_connection
from config import SA

conn = get_connection(SA["user"], SA["password"])
cursor = conn.cursor()
# delete person
cursor.execute(
    """
EXEC sp_delete_person
    @nconst = ? 
""",
    ("nm_test_1",),
)

conn.commit()
# see if person deleted
cursor.execute(
    """
select nconst, primary_name, birth_year, death_year
from persons where nconst = ?
""",
    ("nm_test_1",),
)


print(cursor.fetchone())
print("person not there")
conn.close()
