import pandas as pd


patient_df = pd.read_csv(
    "data/processed/patient_clinical_wide.csv"
)

sample_df = pd.read_csv(
    "data/processed/sample_clinical_wide.csv"
)



print("\nPATIENT CATEGORICAL VALUES")
print("-" * 40)

columns = [
    "SEX",
    "RACE",
    "AJCC_PATHOLOGIC_TUMOR_STAGE",
    "SUBTYPE",
    "OS_STATUS",
]

for column in columns:
    print(f"\n{column}")
    print(patient_df[column].value_counts(dropna=False))


print("\nPATIENT NUMERIC SUMMARY")
print("-" * 40)

print(
    patient_df[
        [
            "AGE",
            "OS_MONTHS",
            "DFS_MONTHS",
            "PFS_MONTHS",
        ]
    ].describe()
)


print("\nSAMPLE NUMERIC SUMMARY")
print("-" * 40)

print(
    sample_df[
        [
            "MUTATION_COUNT",
            "TMB_NONSYNONYMOUS",
            "FRACTION_GENOME_ALTERED",
        ]
    ].describe()
)

print("\nTOP MUTATION COUNTS")
print("-" * 40)

print(
    sample_df[
        ["sampleId", "patientId", "MUTATION_COUNT", "TMB_NONSYNONYMOUS"]
    ]
    .sort_values(
        "MUTATION_COUNT",
        ascending=False
    )
    .head(10)
)