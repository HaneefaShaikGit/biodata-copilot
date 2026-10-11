import json
import requests


study_id = "brca_tcga_pan_can_atlas_2018"

base_url = (
    f"https://www.cbioportal.org/api/studies/"
    f"{study_id}/clinical-data"
)


clinical_data_types = [
    "PATIENT",
    "SAMPLE",
]


for data_type in clinical_data_types:

    url = f"{base_url}?clinicalDataType={data_type}"

    response = requests.get(url, timeout=30)
    response.raise_for_status()

    clinical_data = response.json()

    print(f"\n{data_type} DATA")
    print("Total clinical records:", len(clinical_data))

    attribute_ids = set()

    for record in clinical_data:
        attribute_ids.add(record["clinicalAttributeId"])

    print("Unique clinical attributes:", len(attribute_ids))

    if data_type == "PATIENT":
        patient_ids = set()

        for record in clinical_data:
            patient_ids.add(record["patientId"])

        print("Unique patients:", len(patient_ids))

        output_file = "data/raw/patient_clinical_data.json"

    else:
        sample_ids = set()

        for record in clinical_data:
            sample_ids.add(record["sampleId"])

        print("Unique samples:", len(sample_ids))

        output_file = "data/raw/sample_clinical_data.json"

    with open(output_file, "w") as file:
        json.dump(clinical_data, file, indent=2)

    print("Raw data saved to:", output_file)