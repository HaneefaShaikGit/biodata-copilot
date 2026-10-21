import duckdb


connection = duckdb.connect("data/biodata.duckdb")


connection.execute("""
    CREATE OR REPLACE VIEW patient_gene_mutations AS

    SELECT DISTINCT
        p.patientId,
        p.SUBTYPE,
        m.gene

    FROM patient_analytics AS p

    INNER JOIN mutation_analytics AS m
        ON p.patientId = m.patientId

    WHERE p.SUBTYPE IS NOT NULL
""")


print("ANALYTICAL MODEL CREATED")
print("-" * 40)


row_count = connection.execute("""
    SELECT COUNT(*)
    FROM patient_gene_mutations
""").fetchone()[0]


patient_count = connection.execute("""
    SELECT COUNT(DISTINCT patientId)
    FROM patient_gene_mutations
""").fetchone()[0]


print(f"Patient-gene rows: {row_count}")
print(f"Unique patients: {patient_count}")

connection.execute("""
    CREATE OR REPLACE VIEW subtype_gene_mutation_summary AS

    SELECT
        SUBTYPE,
        gene,
        COUNT(*) AS mutated_patients

    FROM patient_gene_mutations

    GROUP BY
        SUBTYPE,
        gene
""")
connection.close()
