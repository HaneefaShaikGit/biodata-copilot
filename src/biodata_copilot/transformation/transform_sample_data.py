import json
import pandas as pd


# File locations
input_file = "data/raw/sample_clinical_data.json"
output_file = "data/processed/sample_clinical_wide.csv"


# Step 1: Read raw JSON
with open(input_file, "r") as file:
    sample_data = json.load(file)


# Step 2: Convert JSON into a pandas table
df = pd.DataFrame(sample_data)

print("Raw shape:", df.shape)
print("Raw columns:", df.columns.tolist())


# Step 3: Convert long format to wide format
sample_wide = df.pivot(
    index=["sampleId", "patientId", "studyId"],
    columns="clinicalAttributeId",
    values="value"
)


# Step 4: Make IDs normal columns again
sample_wide = sample_wide.reset_index()


# Step 5: Save processed table
sample_wide.to_csv(output_file, index=False)


print("Wide shape:", sample_wide.shape)
print("Saved to:", output_file)