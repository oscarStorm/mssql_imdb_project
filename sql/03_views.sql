DROP VIEW IF EXISTS vw_movie_search;
GO  
DROP VIEW IF EXISTS vw_person_search;
GO

CREATE VIEW vw_movie_search AS
SELECT
    t.tconst,
    t.primary_title,
    t.start_year,
    t.runtime_minutes,
    STRING_AGG(g.genre, ', ') AS genres
FROM titles t
LEFT JOIN title_genres g
    ON t.tconst = g.tconst
GROUP BY
    t.tconst,
    t.primary_title,
    t.start_year,
    t.runtime_minutes;
GO  

CREATE VIEW vw_person_search AS
SELECT
    n.nconst,
    n.primary_name,
    n.birth_year,
    n.death_year
FROM persons n;
GO

