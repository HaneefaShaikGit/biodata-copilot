import json


input_file = "data/raw/sample_clinical_data.json"


with open(input_file, "r") as file:
    sample_data = json.load(file)


patient_samples = {}


for record in sample_data:
    patient_id = record["patientId"]
    sample_id = record["sampleId"]

    if patient_id not in patient_samples:
        patient_samples[patient_id] = set()

    patient_samples[patient_id].add(sample_id)


patients_with_multiple_samples = 0


for patient_id in patient_samples:
    sample_count = len(patient_samples[patient_id])

    if sample_count > 1:
        patients_with_multiple_samples += 1
        print(patient_id, "→", sample_count, "samples")


print()
print("Total patients:", len(patient_samples))
print("Patients with multiple samples:", patients_with_multiple_samples)