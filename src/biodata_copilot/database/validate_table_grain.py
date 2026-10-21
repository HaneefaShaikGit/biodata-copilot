import duckdb


connection = duckdb.connect("data/biodata.duckdb")


print("TABLE GRAIN VALIDATION")
print("=" * 50)


# Patient table
patient_result = connection.execute("""
    SELECT
        COUNT(*) AS total_rows,
        COUNT(DISTINCT patientId) AS unique_patients,
        COUNT(*) - COUNT(DISTINCT patientId) AS duplicate_patients
    FROM patient_analytics
""").fetchone()

print("\nPATIENT_ANALYTICS")
print("-" * 40)
print(f"Total rows: {patient_result[0]}")
print(f"Unique patients: {patient_result[1]}")
print(f"Duplicate patient IDs: {patient_result[2]}")


# Sample table
sample_result = connection.execute("""
    SELECT
        COUNT(*) AS total_rows,
        COUNT(DISTINCT sampleId) AS unique_samples,
        COUNT(*) - COUNT(DISTINCT sampleId) AS duplicate_samples
    FROM sample_analytics
""").fetchone()

print("\nSAMPLE_ANALYTICS")
print("-" * 40)
print(f"Total rows: {sample_result[0]}")
print(f"Unique samples: {sample_result[1]}")
print(f"Duplicate sample IDs: {sample_result[2]}")


# Mutation table
mutation_result = connection.execute("""
    SELECT
        COUNT(*) AS total_rows,
        COUNT(DISTINCT patientId) AS unique_patients,
        COUNT(DISTINCT sampleId) AS unique_samples
    FROM mutation_analytics
""").fetchone()

print("\nMUTATION_ANALYTICS")
print("-" * 40)
print(f"Total mutation rows: {mutation_result[0]}")
print(f"Unique patients: {mutation_result[1]}")
print(f"Unique samples: {mutation_result[2]}")


# Patient-to-sample relationship
patient_sample_join = connection.execute("""
    SELECT COUNT(*)
    FROM patient_analytics p
    LEFT JOIN sample_analytics s
        ON p.patientId = s.patientId
""").fetchone()[0]

print("\nPATIENT → SAMPLE JOIN")
print("-" * 40)
print(f"Joined rows: {patient_sample_join}")


# Check radiation values
radiation_values = connection.execute("""
    SELECT
        RADIATION_THERAPY,
        COUNT(*) AS patient_count
    FROM patient_analytics
    GROUP BY RADIATION_THERAPY
    ORDER BY patient_count DESC
""").fetchall()

print("\nRADIATION_THERAPY VALUES")
print("-" * 40)

for value, count in radiation_values:
    print(f"{value}: {count}")


connection.close()