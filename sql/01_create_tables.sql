CREATE TABLE titles (
    tconst VARCHAR(20) PRIMARY KEY,
    title_type VARCHAR(50) NOT NULL,
    primary_title VARCHAR(500) NOT NULL,
    original_title VARCHAR(500),
    is_adult BIT,
    start_year INT,
    end_year INT,
    runtime_minutes INT
);

CREATE TABLE persons (
    nconst VARCHAR(20) PRIMARY KEY,
    primary_name VARCHAR(255) NOT NULL,
    birth_year INT,
    death_year INT
);

CREATE TABLE title_genres (
    tconst VARCHAR(20) NOT NULL,
    genre VARCHAR(100) NOT NULL,

    CONSTRAINT PK_title_genres 
        PRIMARY KEY (tconst, genre),

    CONSTRAINT FK_title_genres_titles 
        FOREIGN KEY (tconst) 
        REFERENCES titles(tconst)
);

CREATE TABLE title_directors (
    tconst VARCHAR(20) NOT NULL,
    nconst VARCHAR(20) NOT NULL,

    CONSTRAINT PK_title_directors 
        PRIMARY KEY (tconst, nconst),

    CONSTRAINT FK_title_directors_titles 
        FOREIGN KEY (tconst) 
        REFERENCES titles(tconst),

    CONSTRAINT FK_title_directors_persons 
        FOREIGN KEY (nconst) 
        REFERENCES persons(nconst)
);

CREATE TABLE title_writers (
    tconst VARCHAR(20) NOT NULL,
    nconst VARCHAR(20) NOT NULL,

    CONSTRAINT PK_title_writers 
        PRIMARY KEY (tconst, nconst),

    CONSTRAINT FK_title_writers_titles 
        FOREIGN KEY (tconst) 
        REFERENCES titles(tconst),

    CONSTRAINT FK_title_writers_persons 
        FOREIGN KEY (nconst) 
        REFERENCES persons(nconst)
);
