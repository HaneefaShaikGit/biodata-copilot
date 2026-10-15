import json

import pandas as pd


input_file = "data/raw/mutation_data.json"
output_file = "data/processed/mutation_analytics.csv"


with open(input_file, "r") as file:
    mutation_data = json.load(file)


df = pd.json_normalize(mutation_data)


columns_to_keep = [
    "patientId",
    "sampleId",
    "studyId",
    "molecularProfileId",
    "gene.hugoGeneSymbol",
    "gene.entrezGeneId",
    "mutationType",
    "proteinChange",
    "chr",
    "startPosition",
    "endPosition",
    "referenceAllele",
    "variantAllele",
    "variantType",
    "ncbiBuild",
    "tumorRefCount",
    "tumorAltCount",
    "normalRefCount",
    "normalAltCount",
]


mutation_analytics = df[columns_to_keep].copy()


mutation_analytics = mutation_analytics.rename(
    columns={
        "gene.hugoGeneSymbol": "gene",
        "gene.entrezGeneId": "entrezGeneId",
    }
)


mutation_analytics.to_csv(output_file, index=False)


print("MUTATION ANALYTICS TABLE")
print("-" * 40)
print(f"Rows: {len(mutation_analytics)}")
print(f"Columns: {len(mutation_analytics.columns)}")
print(f"Unique patients: {mutation_analytics['patientId'].nunique()}")
print(f"Unique samples: {mutation_analytics['sampleId'].nunique()}")
print(f"Unique genes: {mutation_analytics['gene'].nunique()}")
print()
print(f"Saved to: {output_file}")