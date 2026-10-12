import json
import pandas as pd


# File locations
input_file = "data/raw/patient_clinical_data.json"
output_file = "data/processed/patient_clinical_wide.csv"


# Step 1: Read the raw JSON file
with open(input_file, "r") as file:
    patient_data = json.load(file)


# Step 2: Convert JSON into a pandas table
df = pd.DataFrame(patient_data)

print("Raw shape:", df.shape)
print("Raw columns:", df.columns.tolist())


# Step 3: Pivot long data into wide data
patient_wide = df.pivot(
    index="patientId",
    columns="clinicalAttributeId",
    values="value"
)


# Step 4: Turn patientId back into a normal column
patient_wide = patient_wide.reset_index()


# Step 5: Save the transformed data
patient_wide.to_csv(output_file, index=False)


print("Wide shape:", patient_wide.shape)
print("Saved to:", output_file)