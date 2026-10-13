import json
import pandas as pd


input_file = "data/raw/mutation_data.json"


# Step 1: Read raw mutation JSON
with open(input_file, "r") as file:
    mutation_data = json.load(file)


# Step 2: Convert JSON into a table
df = pd.json_normalize(mutation_data)


print("MUTATION DATA PROFILE")
print("-" * 40)

print("Total mutation records:", len(df))
print("Unique samples:", df["sampleId"].nunique())
print("Unique patients:", df["patientId"].nunique())
print("Unique genes:", df["gene.hugoGeneSymbol"].nunique())


print("\nMOST COMMON MUTATION TYPES")
print("-" * 40)

print(
    df["mutationType"]
    .value_counts()
    .head(10)
)


print("\nMOST FREQUENTLY MUTATED GENES BY PATIENT")
print("-" * 40)


patient_gene_pairs = df[
    ["patientId", "gene.hugoGeneSymbol"]
].drop_duplicates()


print(
    patient_gene_pairs["gene.hugoGeneSymbol"]
    .value_counts()
    .head(20)
)