DROP PROCEDURE IF EXISTS sp_add_movie;
GO
DROP PROCEDURE IF EXISTS sp_update_movie;
GO
DROP PROCEDURE IF EXISTS sp_delete_movie;
GO
DROP PROCEDURE IF EXISTS sp_add_person;
GO
DROP PROCEDURE IF EXISTS sp_delete_person;
GO

CREATE PROCEDURE sp_add_movie
    @tconst VARCHAR(20),
    @title_type VARCHAR(50),
    @primary_title VARCHAR(500),
    @original_title VARCHAR(500) = NULL,
    @is_adult BIT = 0,
    @start_year INT = NULL,
    @end_year INT = NULL,
    @runtime_minutes INT = NULL
AS
BEGIN
    SET NOCOUNT ON;

    INSERT INTO titles (
        tconst,
        title_type,
        primary_title,
        original_title,
        is_adult,
        start_year,
        end_year,
        runtime_minutes
    )
    VALUES (
        @tconst,
        @title_type,
        @primary_title,
        @original_title,
        @is_adult,
        @start_year,
        @end_year,
        @runtime_minutes
    );
END;
GO

CREATE PROCEDURE sp_update_movie
    @tconst VARCHAR(20),
    @title_type VARCHAR(50),
    @primary_title VARCHAR(500),
    @original_title VARCHAR(500) = NULL,
    @is_adult BIT = 0,
    @start_year INT = NULL,
    @end_year INT = NULL,
    @runtime_minutes INT = NULL
AS
BEGIN
    SET NOCOUNT ON;

    UPDATE titles
    SET
        title_type = @title_type,
        primary_title = @primary_title,
        original_title = @original_title,
        is_adult = @is_adult,
        start_year = @start_year,
        end_year = @end_year,
        runtime_minutes = @runtime_minutes
    WHERE tconst = @tconst;
END;
GO

CREATE PROCEDURE sp_delete_movie
    @tconst VARCHAR(20)
AS
BEGIN
    SET NOCOUNT ON;

    DELETE FROM title_writers
    WHERE tconst = @tconst;

    DELETE FROM title_directors
    WHERE tconst = @tconst;

    DELETE FROM title_genres
    WHERE tconst = @tconst;

    DELETE FROM titles
    WHERE tconst = @tconst;
END;
GO

CREATE PROCEDURE sp_add_person
    @nconst VARCHAR(20),
    @primary_name VARCHAR(255) = NULL,
    @birth_year INT = NULL,
    @death_year INT = NULL
AS
BEGIN
    SET NOCOUNT ON;

    INSERT INTO persons (
        nconst,
        primary_name,
        birth_year,
        death_year
    )
    VALUES (
        @nconst,
        @primary_name,
        @birth_year,
        @death_year
    );
END;
GO


CREATE PROCEDURE sp_delete_person
    @nconst VARCHAR(20)
AS
BEGIN
    SET NOCOUNT ON;
    
    DELETE FROM title_directors
    WHERE nconst= @nconst;

    DELETE FROM title_writers 
    WHERE nconst = @nconst;

    DELETE FROM persons
    WHERE nconst = @nconst;

   END;
GO

