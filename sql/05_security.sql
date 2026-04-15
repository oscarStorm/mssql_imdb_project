IF NOT EXISTS (SELECT * FROM sys.server_principals WHERE name = 'imdb_app_user')
    CREATE LOGIN imdb_app_user WITH PASSWORD = 'AppPassword123';
GO

IF NOT EXISTS (SELECT * FROM sys.database_principals WHERE name = 'imdb_app_user')
    CREATE USER imdb_app_user FOR LOGIN imdb_app_user;
GO

GRANT SELECT ON vw_movie_search TO imdb_app_user;
GRANT SELECT ON vw_person_search TO imdb_app_user;

GRANT EXECUTE ON sp_add_movie TO imdb_app_user;
GRANT EXECUTE ON sp_update_movie TO imdb_app_user;
GRANT EXECUTE ON sp_delete_movie TO imdb_app_user;
GRANT EXECUTE ON sp_add_person TO imdb_app_user;
GRANT EXECUTE ON sp_delete_person TO imdb_app_user;
GO
