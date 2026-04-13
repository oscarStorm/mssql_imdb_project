from db import get_connection
from config import SA

conn = get_connection(SA["user"], SA["password"])
cursor = conn.cursor()

cursor.execute("""
SELECT 
    t.name AS table_name,
    i.name AS index_name
FROM sys.indexes i
JOIN sys.tables t ON i.object_id = t.object_id
WHERE i.type_desc = 'NONCLUSTERED'
ORDER BY t.name
""")

for row in cursor.fetchall():
    print(f"{row[0]} -> {row[1]}")

conn.close()
