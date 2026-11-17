import sys
from pathlib import Path

import duckdb


DATABASE_PATH = "data/biodata.duckdb"


def run_query(query_file):
    sql = Path(query_file).read_text(encoding="utf-8")

    connection = duckdb.connect(DATABASE_PATH)

    result = connection.execute(sql).fetchdf()

    connection.close()

    return result


def main():
    if len(sys.argv) != 2:
        print("Usage: python run_sql.py <sql_file>")
        raise SystemExit(1)

    result = run_query(sys.argv[1])

    print(result.to_string(index=False))


if __name__ == "__main__":
    main()