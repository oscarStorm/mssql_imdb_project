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

    # opens the sql file, read the file into a string
    with open(path, "r") as f:
        sql = f.read()
    # create cursor (cursor executes the sql command)
    cursor = conn.cursor()
    # execute the command
    # (sends the SQL string to to SQL server)
    cursor.execute(sql)
    # commits the changes to the database
    conn.commit()
