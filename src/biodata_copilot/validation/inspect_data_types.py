import pandas as pd


patient_df = pd.read_csv(
    "data/processed/patient_clinical_wide.csv"
)

sample_df = pd.read_csv(
    "data/processed/sample_clinical_wide.csv"
)


print("\nPATIENT DATA TYPES")
print("-" * 40)

print(patient_df.dtypes)


print("\nSAMPLE DATA TYPES")
print("-" * 40)

print(sample_df.dtypes)