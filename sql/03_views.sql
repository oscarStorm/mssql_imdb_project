CREATE OR ALTER VIEW vw_movie_search AS
SELECT
    t.tconst,
    t.primary_title,
    t.start_year,
    t.runtime_minutes,

    (
        SELECT STRING_AGG(g.genre, ', ')
        FROM title_genres g
        WHERE g.tconst = t.tconst
    ) AS genres,

    (
        SELECT STRING_AGG(p.primary_name, ', ')
        FROM title_directors d
        JOIN persons p
            ON d.nconst = p.nconst
        WHERE d.tconst = t.tconst
    ) AS directors

FROM titles t;
GO
CREATE OR ALTER VIEW vw_person_search AS
SELECT
    n.nconst,
    n.primary_name,
    n.birth_year,
    n.death_year
FROM persons n;
GO
