import json
from pathlib import Path

import pandas as pd


RAW_DIR = Path("data/raw")
PROCESSED_DIR = Path("data/processed")


PATIENT_COLUMNS = [
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


SAMPLE_COLUMNS = [
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


def load_json(path):
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def transform_patient_data():
    data = load_json(RAW_DIR / "patient_clinical_data.json")
    df = pd.DataFrame(data)

    patient_wide = (
        df.pivot(
            index=["patientId", "studyId"],
            columns="clinicalAttributeId",
            values="value",
        )
        .reset_index()
    )

    patient_wide.to_csv(
        PROCESSED_DIR / "patient_clinical_wide.csv",
        index=False,
    )

    patient_analytics = patient_wide[PATIENT_COLUMNS].copy()

    patient_analytics.to_csv(
        PROCESSED_DIR / "patient_analytics.csv",
        index=False,
    )

    return patient_analytics


def transform_sample_data():
    data = load_json(RAW_DIR / "sample_clinical_data.json")
    df = pd.DataFrame(data)

    sample_wide = (
        df.pivot(
            index=["sampleId", "patientId", "studyId"],
            columns="clinicalAttributeId",
            values="value",
        )
        .reset_index()
    )

    sample_wide.to_csv(
        PROCESSED_DIR / "sample_clinical_wide.csv",
        index=False,
    )

    sample_analytics = sample_wide[SAMPLE_COLUMNS].copy()

    sample_analytics.to_csv(
        PROCESSED_DIR / "sample_analytics.csv",
        index=False,
    )

    return sample_analytics


def main():
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    patient_analytics = transform_patient_data()
    sample_analytics = transform_sample_data()

    print(f"Patient analytics: {patient_analytics.shape}")
    print(f"Sample analytics: {sample_analytics.shape}")
    print("Clinical data saved to data/processed/")


if __name__ == "__main__":
    main()