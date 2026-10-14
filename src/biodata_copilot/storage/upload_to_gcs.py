from google.cloud import storage


bucket_name = "biodata-copilot-haneefa-raw"

files_to_upload = [
    (
        "data/raw/patient_clinical_data.json",
        "raw/patient_clinical_data.json",
    ),
    (
        "data/raw/sample_clinical_data.json",
        "raw/sample_clinical_data.json",
    ),
    (
        "data/raw/mutation_data.json",
        "raw/mutation_data.json",
    ),
]


client = storage.Client()

bucket = client.bucket(bucket_name)

for local_file, gcs_file in files_to_upload:
    print(f"Uploading {local_file}")

    blob = bucket.blob(gcs_file)

    blob.upload_from_filename(local_file)

    print(f"Uploaded to gs://{bucket_name}/{gcs_file}")


print("All files uploaded successfully.")