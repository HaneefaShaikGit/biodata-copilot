import json

import pandas as pd


raw_file = "data/raw/mutation_data.json"
processed_file = "data/processed/mutation_analytics.csv"


with open(raw_file, "r") as file:
    raw_data = json.load(file)


df = pd.read_csv(processed_file)


print("MUTATION ANALYTICS VALIDATION")
print("-" * 40)

print(f"Raw mutation records: {len(raw_data)}")
print(f"Processed rows: {len(df)}")

print()

print(f"Processed columns: {len(df.columns)}")
print(f"Unique patients: {df['patientId'].nunique()}")
print(f"Unique samples: {df['sampleId'].nunique()}")
print(f"Unique genes: {df['gene'].nunique()}")

print()

print("MISSING CRITICAL VALUES")
print("-" * 40)

print(f"Missing patientId: {df['patientId'].isna().sum()}")
print(f"Missing sampleId: {df['sampleId'].isna().sum()}")
print(f"Missing gene: {df['gene'].isna().sum()}")
print(f"Missing mutationType: {df['mutationType'].isna().sum()}")

print()

if len(raw_data) == len(df):
    print("Row count validation: PASSED")
else:
    print("Row count validation: FAILED")