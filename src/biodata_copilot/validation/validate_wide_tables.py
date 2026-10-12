import pandas as pd


# Read processed files
patient_df = pd.read_csv(
    "data/processed/patient_clinical_wide.csv"
)

sample_df = pd.read_csv(
    "data/processed/sample_clinical_wide.csv"
)


print("PATIENT TABLE")
print("-" * 30)

print("Rows:", len(patient_df))
print("Columns:", len(patient_df.columns))
print("Unique patients:", patient_df["patientId"].nunique())
print(
    "Duplicate patient IDs:",
    patient_df["patientId"].duplicated().sum()
)


print("\nSAMPLE TABLE")
print("-" * 30)

print("Rows:", len(sample_df))
print("Columns:", len(sample_df.columns))
print("Unique samples:", sample_df["sampleId"].nunique())
print(
    "Duplicate sample IDs:",
    sample_df["sampleId"].duplicated().sum()
)


print("\nPATIENT-SAMPLE CHECK")
print("-" * 30)

patient_ids = set(patient_df["patientId"])
sample_patient_ids = set(sample_df["patientId"])

print(
    "Patients missing from sample table:",
    len(patient_ids - sample_patient_ids)
)

print(
    "Sample patients missing from patient table:",
    len(sample_patient_ids - patient_ids)
)