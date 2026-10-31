# IMDb Data Normalization — SQL Server

A database project exploring how to transform [IMDb's TSV datasets](https://datasets.imdbws.com/) into a normalized relational database using **Microsoft SQL Server**.

The focus is on relational schema design, handling relationships between records, and working with SQL Server from Python.

## Tech stack

- **Microsoft SQL Server / T-SQL** — database design and SQL scripts
- **Python** — database connectivity
- **pyodbc** — SQL Server connection via ODBC
- **python-dotenv** — local configuration

## Project structure

```
sql/              SQL scripts
src/              Python source code
requirements.txt  Python dependencies
README.txt        Arch Linux ODBC dependency notes
```

## Getting started

**Prerequisites:** Python 3, a running SQL Server instance, a compatible SQL Server ODBC driver, and the required IMDb TSV files.

```bash
git clone https://github.com/oscarStorm/mssql_imdb_project.git
cd mssql_imdb_project
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
## Data source
IMDb's [non-commercial datasets](https://developer.imdb.com/non-commercial-datasets/) are used as the source. Consult IMDb's terms before redistributing the data.
