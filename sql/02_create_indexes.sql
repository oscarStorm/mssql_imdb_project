IF NOT EXISTS (SELECT 1 FROM sys.indexes 
WHERE name = 'IX_titles_primary_title')
CREATE INDEX IX_titles_primary_title 
ON titles(primary_title);


IF NOT EXISTS (SELECT 1 FROM sys.indexes 
WHERE name = 'IX_persons_primary_name')
CREATE INDEX IX_persons_primary_name 
ON persons(primary_name);


IF NOT EXISTS (SELECT 1 FROM sys.indexes 
WHERE name = 'IX_title_genres_tconst')
CREATE INDEX IX_title_genres_tconst 
ON title_genres(tconst);


IF NOT EXISTS (SELECT 1 FROM sys.indexes 
WHERE name = 'IX_title_directors_tconst')
CREATE INDEX IX_title_directors_tconst 
ON title_directors(tconst);


IF NOT EXISTS (SELECT 1 FROM sys.indexes 
WHERE name = 'IX_title_directors_nconst')
CREATE INDEX IX_title_directors_nconst 
ON title_directors(nconst);


IF NOT EXISTS (SELECT 1 FROM sys.indexes 
WHERE name = 'IX_title_writers_tconst')
CREATE INDEX IX_title_writers_tconst 
ON title_writers(tconst);


IF NOT EXISTS (SELECT 1 FROM sys.indexes 
WHERE name = 'IX_title_writers_nconst')
CREATE INDEX IX_title_writers_nconst 
ON title_writers(nconst);
