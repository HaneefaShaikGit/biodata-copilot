import duckdb


database_path = "data/biodata.duckdb"

connection = duckdb.connect(database_path)


connection.execute("""
    CREATE OR REPLACE TABLE patient_analytics AS
    SELECT *
    FROM read_csv_auto(
        'data/processed/patient_analytics.csv',
        header=True
    )
""")


connection.execute("""
    CREATE OR REPLACE TABLE sample_analytics AS
    SELECT *
    FROM read_csv_auto(
        'data/processed/sample_analytics.csv',
        header=True
    )
""")


connection.execute("""
    CREATE OR REPLACE TABLE mutation_analytics AS
    SELECT *
    FROM read_csv_auto(
        'data/processed/mutation_analytics.csv',
        header=True
    )
""")


print("DUCKDB TABLE LOAD")
print("-" * 40)

tables = [
    "patient_analytics",
    "sample_analytics",
    "mutation_analytics",
]

for table in tables:
    row_count = connection.execute(
        f"SELECT COUNT(*) FROM {table}"
    ).fetchone()[0]

    print(f"{table}: {row_count} rows")


connection.close()

print()
print(f"Database created: {database_path}")