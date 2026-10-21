import duckdb


database_path = "data/biodata.duckdb"

connection = duckdb.connect(database_path)


tables = [
    "patient_analytics",
    "sample_analytics",
    "mutation_analytics",
]


for table in tables:
    print()
    print("=" * 60)
    print(table.upper())
    print("=" * 60)

    print("\nSCHEMA")
    print("-" * 40)

    schema = connection.execute(
        f"DESCRIBE {table}"
    ).fetchdf()

    print(schema.to_string(index=False))

    print("\nROW COUNT")
    print("-" * 40)

    row_count = connection.execute(
        f"SELECT COUNT(*) FROM {table}"
    ).fetchone()[0]

    print(row_count)


connection.close()