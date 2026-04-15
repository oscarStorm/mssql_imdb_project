import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from db import get_connection
from config import SA

conn = get_connection(SA["user"], SA["password"])
cursor = conn.cursor()
# add person
cursor.execute(
    """
EXEC sp_add_person
    @nconst = ?,
    @primary_name = ?,
    @birth_year = ?,
    @death_year = ?
""",
    ("nm_test_1", "Test Person", 1990, None),
)

conn.commit()
# see if person added
cursor.execute(
    """
select nconst, primary_name, birth_year, death_year
from persons where nconst = ?
""",
    ("nm_test_1",),
)


print(cursor.fetchone())

conn.close()
