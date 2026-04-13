import csv
from db import get_connection
from config import SA


def clean(value):
    return None if value == r"\N" else value


def to_int(value):
    return None if value == r"\N" else int(value)


def import_persons(limit=None):
    conn = get_connection(SA["user"], SA["password"])
    cursor = conn.cursor()
    cursor.fast_executemany = True

    insert_sql = """
        INSERT INTO persons (nconst, primary_name, birth_year, death_year)
        VALUES (?, ?, ?, ?)
    """
    batch = []
    batch_size = 10000

    with open("../data/name.basics.tsv", "r", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter="\t")

        for i, row in enumerate(reader, start=1):
            primary_name = clean(row["primaryName"])

            if primary_name is None:
                continue

            batch.append(
                (
                    row["nconst"],
                    primary_name,
                    to_int(row["birthYear"]),
                    to_int(row["deathYear"]),
                )
            )
            if len(batch) >= batch_size:
                cursor.executemany(insert_sql, batch)
                conn.commit()
                print(f"{i} rows processed")
                batch.clear()

            if limit is not None and i >= limit:
                break

    if batch:
        cursor.executemany(insert_sql, batch)
        conn.commit()

    conn.close()
    print("Person import done.")


if __name__ == "__main__":
    import_persons()
