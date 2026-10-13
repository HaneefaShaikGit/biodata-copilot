import json
import requests


sample_list_id = "brca_tcga_pan_can_atlas_2018_sequenced"

sample_list_url = (
    f"https://www.cbioportal.org/api/sample-lists/"
    f"{sample_list_id}/sample-ids"
)


# Step 1: Get all sequenced sample IDs
response = requests.get(sample_list_url, timeout=30)
response.raise_for_status()

sequenced_samples = set(response.json())


# Step 2: Read mutation data
with open("data/raw/mutation_data.json", "r") as file:
    mutation_data = json.load(file)


# Step 3: Find samples that actually have mutation records
mutated_samples = set()

for record in mutation_data:
    mutated_samples.add(record["sampleId"])


# Step 4: Compare the two sets
samples_without_mutation_records = (
    sequenced_samples - mutated_samples
)


print("Sequenced samples:", len(sequenced_samples))
print("Samples with mutation records:", len(mutated_samples))
print(
    "Sequenced samples with no mutation records:",
    len(samples_without_mutation_records)
)