import json
from pathlib import Path

import requests


STUDY_ID = "brca_tcga_pan_can_atlas_2018"
API_URL = f"https://www.cbioportal.org/api/studies/{STUDY_ID}/clinical-data"

RAW_DATA_DIR = Path("data/raw")


def fetch_clinical_data(data_type):
    response = requests.get(
        API_URL,
        params={"clinicalDataType": data_type},
        timeout=30,
    )
    response.raise_for_status()

    return response.json()


def save_json(data, output_file):
    RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)

    with output_file.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=2)


def main():
    patient_data = fetch_clinical_data("PATIENT")
    sample_data = fetch_clinical_data("SAMPLE")

    save_json(
        patient_data,
        RAW_DATA_DIR / "patient_clinical_data.json",
    )

    save_json(
        sample_data,
        RAW_DATA_DIR / "sample_clinical_data.json",
    )

    print(f"Patient clinical records: {len(patient_data)}")
    print(f"Sample clinical records: {len(sample_data)}")
    print("Clinical data saved to data/raw/")


if __name__ == "__main__":
    main()