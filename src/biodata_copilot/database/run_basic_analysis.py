import duckdb


connection = duckdb.connect("data/biodata.duckdb")


queries = {
    "TOTAL PATIENTS": """
        SELECT
            COUNT(*) AS total_patients
        FROM patient_analytics
    """,

    "PATIENTS BY SUBTYPE": """
        SELECT
            SUBTYPE,
            COUNT(*) AS patient_count
        FROM patient_analytics
        GROUP BY SUBTYPE
        ORDER BY patient_count DESC
    """,

    "AVERAGE AGE BY SUBTYPE": """
        SELECT
            SUBTYPE,
            COUNT(*) AS patient_count,
            ROUND(AVG(AGE), 2) AS average_age
        FROM patient_analytics
        WHERE SUBTYPE IS NOT NULL
        GROUP BY SUBTYPE
        ORDER BY patient_count DESC
    """,

    "TOP MUTATED GENES": """
        SELECT
            gene,
            COUNT(DISTINCT patientId) AS mutated_patients
        FROM mutation_analytics
        GROUP BY gene
        ORDER BY mutated_patients DESC
        LIMIT 20
    """,

    "MUTATION TYPES": """
        SELECT
            mutationType,
            COUNT(*) AS mutation_count
        FROM mutation_analytics
        GROUP BY mutationType
        ORDER BY mutation_count DESC
    """,
}


for title, query in queries.items():

    print()
    print("=" * 60)
    print(title)
    print("=" * 60)

    result = connection.execute(query).fetchdf()

    print(result.to_string(index=False))


connection.close()