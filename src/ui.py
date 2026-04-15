import sys
from pathlib import Path

# allow imports when running ui.py directly from src/
sys.path.append(str(Path(__file__).resolve().parent))

from db import get_connection
from config import APP


def get_app_connection():
    return get_connection(APP["user"], APP["password"])


def search_movies():
    term = input("Enter movie title search term: ").strip()

    conn = get_app_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT TOP 20 tconst, primary_title, start_year, runtime_minutes, genres, directors
        FROM vw_movie_search
        WHERE primary_title LIKE ?
        ORDER BY 
            CASE
                WHEN primary_title = ? THEN 0
                WHEN primary_title LIKE ? THEN 1
                ELSE 2
            END,
            primary_title
        """,
        (f"%{term}%", term, f"{term}%"),
    )

    rows = cursor.fetchall()
    conn.close()

    if not rows:
        print("No movies found.")
        return

    for row in rows:
        print(row)


def search_persons():
    term = input("Enter person name search term: ").strip()

    conn = get_app_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT TOP 20 nconst, primary_name, birth_year, death_year
        FROM vw_person_search
        WHERE primary_name LIKE ?
        ORDER BY 
        CASE WHEN primary_name = ? THEN 0 ELSE 1 END
        """,
        (f"%{term}%", term),
    )

    rows = cursor.fetchall()
    conn.close()

    if not rows:
        print("No persons found.")
        return

    for row in rows:
        print(row)


def add_movie():
    tconst = input("tconst: ").strip()
    title_type = input("title type: ").strip()
    primary_title = input("primary title: ").strip()
    original_title = input("original title (optional): ").strip() or None
    is_adult = 1 if input("is adult? (0/1): ").strip() == "1" else 0
    start_year = input("start year (optional): ").strip()
    end_year = input("end year (optional): ").strip()
    runtime_minutes = input("runtime minutes (optional): ").strip()

    conn = get_app_connection()
    cursor = conn.cursor()

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
            tconst,
            title_type,
            primary_title,
            original_title,
            is_adult,
            int(start_year) if start_year else None,
            int(end_year) if end_year else None,
            int(runtime_minutes) if runtime_minutes else None,
        ),
    )

    conn.commit()
    conn.close()
    print("Movie added.")


def add_person():
    nconst = input("nconst: ").strip()
    primary_name = input("primary name (optional): ").strip() or None
    birth_year = input("birth year (optional): ").strip()
    death_year = input("death year (optional): ").strip()

    conn = get_app_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        EXEC sp_add_person
            @nconst = ?,
            @primary_name = ?,
            @birth_year = ?,
            @death_year = ?
        """,
        (
            nconst,
            primary_name,
            int(birth_year) if birth_year else None,
            int(death_year) if death_year else None,
        ),
    )

    conn.commit()
    conn.close()
    print("Person added.")


def update_movie():
    tconst = input("tconst of movie to update: ").strip()
    title_type = input("new title type: ").strip()
    primary_title = input("new primary title: ").strip()
    original_title = input("new original title (optional): ").strip() or None
    is_adult = 1 if input("is adult? (0/1): ").strip() == "1" else 0
    start_year = input("new start year (optional): ").strip()
    end_year = input("new end year (optional): ").strip()
    runtime_minutes = input("new runtime minutes (optional): ").strip()

    conn = get_app_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        EXEC sp_update_movie
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
            tconst,
            title_type,
            primary_title,
            original_title,
            is_adult,
            int(start_year) if start_year else None,
            int(end_year) if end_year else None,
            int(runtime_minutes) if runtime_minutes else None,
        ),
    )

    conn.commit()
    conn.close()
    print("Movie updated.")


def delete_movie():
    tconst = input("tconst of movie to delete: ").strip()

    conn = get_app_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        EXEC sp_delete_movie
            @tconst = ?
        """,
        (tconst,),
    )

    conn.commit()
    conn.close()
    print("Movie deleted.")


def delete_person():
    nconst = input("nconst of person to delete: ").strip()

    conn = get_app_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        EXEC sp_delete_person
            @nconst = ?
        """,
        (nconst,),
    )

    conn.commit()
    conn.close()
    print("Person deleted.")


def main():
    while True:
        print("\n=== IMDB Console UI ===")
        print("1. Search movie")
        print("2. Search person")
        print("3. Add movie")
        print("4. Add person")
        print("5. Update movie")
        print("6. Delete movie")
        print("7. Delete person")
        print("8. Exit")

        choice = input("Choose an option: ").strip()

        try:
            if choice == "1":
                search_movies()
            elif choice == "2":
                search_persons()
            elif choice == "3":
                add_movie()
            elif choice == "4":
                add_person()
            elif choice == "5":
                update_movie()
            elif choice == "6":
                delete_movie()
            elif choice == "7":
                delete_person()
            elif choice == "8":
                print("Goodbye.")
                break
            else:
                print("Invalid choice.")
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()
