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
EXEC sp_add_movie
    @tconst = ?,
    @title_type = ?,
    @primary_title = ?,
    @original_title = ?,
    @is_adult = ?,
    @start_year = ?,
    @end_year = ?,
    @runtime_minutes = ?
""",
    (
        "testmovie123",
        "greatesMovie!",
        "greatest movie ever!",
        "greatest ever!",
        "0",
        "1738",
        "1922",
        "2031",
    ),
)

conn.commit()
# see if person added
cursor.execute(
    """
select tconst, title_type, primary_title, original_title, is_adult, start_year, end_year, runtime_minutes
from titles where tconst = ?
""",
    ("testmovie123",),
)


print(cursor.fetchone())

conn.close()
