import pyodbc
from config import DB


# connects to the database
def get_connection(user, password):
    conn_str = (
        f"DRIVER={{{DB['driver']}}};"
        f"SERVER={DB['server']},{DB['port']};"
        f"DATABASE={DB['name']};"
        f"UID={user};"
        f"PWD={password};"
        "TrustServerCertificate=yes;"
    )
    return pyodbc.connect(conn_str)


# uses the conn (connection) from the pyodbc
# and the path to the sql file that is being
# executed.
def execute_sql_file(conn, path):
    with open(path, "r", encoding="utf-8") as f:
        sql = f.read()

    cursor = conn.cursor()

    # Split SQL batches on lines containing only GO
    batches = []
    current_batch = []

    for line in sql.splitlines():
        if line.strip().upper() == "GO":
            if current_batch:
                batches.append("\n".join(current_batch).strip())
                current_batch = []
        else:
            current_batch.append(line)

    if current_batch:
        batches.append("\n".join(current_batch).strip())

    for batch in batches:
        if batch:
            cursor.execute(batch)

    conn.commit()
