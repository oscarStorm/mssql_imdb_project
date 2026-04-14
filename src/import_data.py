import csv
# built-in Python module for reading CSV/TSV files

from db import get_connection
# imports your helper function from db.py
# this function returns a pyodbc connection object

from config import SA
# imports the SA credentials dictionary from config.py
# SA["user"] and SA["password"] are used to connect as the super admin


def clean(value):
    """
    IMDB uses the string '\\N' to mean 'missing value'.

    This helper converts:
        '\\N'  -> None
        anything else -> unchanged

    Why:
    SQL Server should store missing values as NULL,
    and in Python that is represented by None.
    """
    return None if value == r"\N" else value


def to_int(value):
    """
    Convert an IMDB field to an integer.

    If the value is '\\N', return None instead of crashing.

    Examples:
        '1999' -> 1999
        '\\N'  -> None
        can also handle weird non integers from runtime_minutes
    """
    if value == r"\N":
        return None
    try:
        return int(value)
    except ValueError:
        return None


def to_bit(value):
    """
    Convert IMDB's isAdult field to a SQL Server BIT-compatible value.

    In the TSV file:
        '1' means true
        '0' means false

    convert:
        '1' -> 1
        everything else -> 0

    This matches SQL column type:
        is_adult BIT
    """
    return 1 if value == "1" else 0


####################################################################################################################
def import_persons(limit=None):
    """
    Import rows from name.basics.tsv into the persons table.

    Parameters:
        limit:
            - if None: import the whole file
            - if set to an integer: stop after that many rows
              useful for testing on a smaller sample

    High-level flow:
        1. connect to database
        2. open TSV file
        3. read each row
        4. clean/convert values
        5. batch rows in memory
        6. insert them into SQL Server with executemany()
    """

    # open a database connection using your SA credentials
    conn = get_connection(SA["user"], SA["password"])

    # create a cursor object
    # the cursor is what actually runs SQL commands
    cursor = conn.cursor()

    # pyodbc optimization:
    # this speeds up executemany() significantly for large batch inserts
    cursor.fast_executemany = True

    # parameterized insert query for the persons table
    # ? placeholders are filled with tuple values from Python
    insert_sql = """
        INSERT INTO persons (nconst, primary_name, birth_year, death_year)
        VALUES (?, ?, ?, ?)
    """

    # batch holds rows temporarily before writing them to the database
    batch = []

    # number of rows to insert at once
    # larger batches are usually much faster than row-by-row inserts
    batch_size = 10000

    # open the TSV file
    # encoding="utf-8" is needed because IMDB data contains non-ASCII names
    with open("../data/name.basics.tsv", "r", encoding="utf-8") as f:
        # DictReader reads each row as a dictionary using column names from the header
        # delimiter="\t" is important because the file is TSV, not CSV
        reader = csv.DictReader(f, delimiter="\t")

        # loop through each row in the file
        # start=1 makes the counter begin at 1 instead of 0
        for i, row in enumerate(reader, start=1):
            # clean the person's name
            # '\\N' becomes None
            primary_name = clean(row["primaryName"])

            # add one tuple to the batch
            # order must match the INSERT statement above
            batch.append(
                (
                    row["nconst"],
                    primary_name,
                    to_int(row["birthYear"]),
                    to_int(row["deathYear"]),
                )
            )

            # if the batch is full, insert it into the database
            if len(batch) >= batch_size:
                # insert all tuples in one call
                cursor.executemany(insert_sql, batch)

                # make the transaction permanent
                conn.commit()

                # progress output so you can see the import is moving
                print(f"persons: {i} rows processed")

                # empty the list so it can be reused for the next batch
                batch.clear()

            # optional stop condition for testing
            if limit is not None and i >= limit:
                break

    # after the loop ends, there may still be leftover rows in the batch
    # insert the remaining rows
    if batch:
        cursor.executemany(insert_sql, batch)
        conn.commit()

    # close the connection when done
    conn.close()

    print("Person import done.")


#######################################################################################################################


def import_titles(limit=None):
    """
    Import rows from title.basics.tsv into:
        1. titles
        2. title_genres

    Why two tables?
    Because genres is a multi-valued field in the source file.
    Example:
        Action,Comedy

    In a normalized design, that should not stay inside titles.
    So:
        titles gets the main title data
        title_genres gets one row per (title, genre)

    Parameters:
        limit:
            - if None: import whole file
            - if integer: import only first N rows
    """

    # connect to database using SA credentials
    conn = get_connection(SA["user"], SA["password"])
    cursor = conn.cursor()

    # same batch insert speed optimization
    cursor.fast_executemany = True

    # insert SQL for the titles table
    title_sql = """
        INSERT INTO titles (
            tconst, title_type, primary_title, original_title,
            is_adult, start_year, end_year, runtime_minutes
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """

    # insert SQL for the bridge table title_genres
    # this table stores one genre per row
    genre_sql = """
        INSERT INTO title_genres (tconst, genre)
        VALUES (?, ?)
    """

    # one batch for titles rows
    title_batch = []

    # another batch for genre rows
    genre_batch = []

    batch_size = 10000

    # open the title basics file
    with open("../data/title.basics.tsv", "r", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter="\t")

        for i, row in enumerate(reader, start=1):
            # clean required fields
            primary_title = clean(row["primaryTitle"])
            title_type = clean(row["titleType"])

            # skip rows missing required values
            # your schema says these should not be NULL
            if primary_title is None or title_type is None:
                continue

            # save tconst once because it is used multiple times
            tconst = row["tconst"]

            # append one row to the titles batch
            title_batch.append(
                (
                    tconst,
                    title_type,
                    primary_title,
                    clean(row["originalTitle"]),
                    to_bit(row["isAdult"]),
                    to_int(row["startYear"]),
                    to_int(row["endYear"]),
                    to_int(row["runtimeMinutes"]),
                )
            )

            # handle genres separately
            # example source value: "Action,Comedy"
            genres = clean(row["genres"])

            if genres is not None:
                # split the comma-separated string into separate genre values
                for genre in genres.split(","):
                    # add one row per genre
                    genre_batch.append((tconst, genre))

            # when titles batch is full, insert it
            if len(title_batch) >= batch_size:
                cursor.executemany(title_sql, title_batch)
                conn.commit()

                if genre_batch:
                    cursor.executemany(genre_sql, genre_batch)
                    conn.commit()

                print(f"titles: {i} rows processed")
                title_batch.clear()
                genre_batch.clear()

            # optional stop point for testing
            if limit is not None and i >= limit:
                break

    # insert any remaining title rows
    if title_batch:
        cursor.executemany(title_sql, title_batch)
        conn.commit()

    # insert any remaining genre rows
    if genre_batch:
        cursor.executemany(genre_sql, genre_batch)
        conn.commit()

    # close database connection
    conn.close()

    print("Title import done.")


#########################################################################################################
def import_crews(limit=None):
    conn = get_connection(SA["user"], SA["password"])
    cursor = conn.cursor()
    cursor.fast_executemany = True

    director_sql = """
        INSERT INTO title_directors (tconst, nconst)
        VALUES (?, ?)
    """

    writer_sql = """
        INSERT INTO title_writers (tconst, nconst)
        VALUES (?, ?)
    """

    # load valid person IDs once
    cursor.execute("SELECT nconst FROM persons")
    valid_persons = {row[0] for row in cursor.fetchall()}

    director_batch = []
    writer_batch = []
    batch_size = 10000

    with open("../data/title.crew.tsv", "r", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter="\t")

        for i, row in enumerate(reader, start=1):
            tconst = row["tconst"]

            directors = clean(row["directors"])
            if directors is not None:
                for nconst in directors.split(","):
                    if nconst in valid_persons:
                        director_batch.append((tconst, nconst))

            writers = clean(row["writers"])
            if writers is not None:
                for nconst in writers.split(","):
                    if nconst in valid_persons:
                        writer_batch.append((tconst, nconst))

            if len(director_batch) >= batch_size:
                cursor.executemany(director_sql, director_batch)
                conn.commit()
                director_batch.clear()

            if len(writer_batch) >= batch_size:
                cursor.executemany(writer_sql, writer_batch)
                conn.commit()
                writer_batch.clear()

            if i % 100000 == 0:
                print(f"crew: {i} rows processed")

            if limit is not None and i >= limit:
                break

    if director_batch:
        cursor.executemany(director_sql, director_batch)
        conn.commit()

    if writer_batch:
        cursor.executemany(writer_sql, writer_batch)
        conn.commit()

    conn.close()
    print("Crew import done.")


if __name__ == "__main__":
    # import_persons()
    # import_titles()
    import_crews()
