from google.cloud import storage


bucket_name = "biodata-copilot-haneefa-processed"

files_to_upload = [
    "data/processed/patient_analytics.csv",
    "data/processed/sample_analytics.csv",
    "data/processed/mutation_analytics.csv",
]


client = storage.Client()
bucket = client.bucket(bucket_name)


for local_file in files_to_upload:
    file_name = local_file.split("/")[-1]

    print(f"Uploading {file_name}")

    blob = bucket.blob(file_name)
    blob.upload_from_filename(local_file)

    print(f"Uploaded to gs://{bucket_name}/{file_name}")


print("All processed files uploaded successfully.")