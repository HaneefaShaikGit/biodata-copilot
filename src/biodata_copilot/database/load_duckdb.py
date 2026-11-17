from pathlib import Path

import duckdb


DATABASE_PATH = Path("data/biodata.duckdb")
PROCESSED_DIR = Path("data/processed")


TABLES = {
    "patient_analytics": "patient_analytics.csv",
    "sample_analytics": "sample_analytics.csv",
    "mutation_analytics": "mutation_analytics.csv",
}


def load_tables():
    connection = duckdb.connect(str(DATABASE_PATH))

    for table_name, file_name in TABLES.items():
        csv_path = PROCESSED_DIR / file_name

        connection.execute(
            f"""
            CREATE OR REPLACE TABLE {table_name} AS
            SELECT *
            FROM read_csv_auto('{csv_path}', header=True)
            """
        )

    connection.close()


def main():
    load_tables()

    print(f"DuckDB database created at {DATABASE_PATH}")


if __name__ == "__main__":
    main()