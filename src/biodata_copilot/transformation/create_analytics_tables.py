import pandas as pd


patient_file = "data/processed/patient_clinical_wide.csv"
sample_file = "data/processed/sample_clinical_wide.csv"


patient_df = pd.read_csv(patient_file)
sample_df = pd.read_csv(sample_file)


patient_columns = [
    "patientId",
    "studyId",
    "AGE",
    "SEX",
    "RACE",
    "ETHNICITY",
    "AJCC_PATHOLOGIC_TUMOR_STAGE",
    "SUBTYPE",
    "OS_MONTHS",
    "OS_STATUS",
    "DFS_MONTHS",
    "DFS_STATUS",
    "PFS_MONTHS",
    "PFS_STATUS",
    "DSS_MONTHS",
    "DSS_STATUS",
    "RADIATION_THERAPY",
]


sample_columns = [
    "sampleId",
    "patientId",
    "studyId",
    "SAMPLE_TYPE",
    "CANCER_TYPE_DETAILED",
    "ONCOTREE_CODE",
    "MUTATION_COUNT",
    "TMB_NONSYNONYMOUS",
    "FRACTION_GENOME_ALTERED",
    "ANEUPLOIDY_SCORE",
    "MSI_SCORE_MANTIS",
    "MSI_SENSOR_SCORE",
]


patient_analytics = patient_df[patient_columns]

sample_analytics = sample_df[sample_columns]


patient_analytics.to_csv(
    "data/processed/patient_analytics.csv",
    index=False,
)

sample_analytics.to_csv(
    "data/processed/sample_analytics.csv",
    index=False,
)


print("Patient analytics shape:", patient_analytics.shape)
print("Sample analytics shape:", sample_analytics.shape)