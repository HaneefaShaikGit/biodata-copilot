import json
from pathlib import Path

import pandas as pd


INPUT_FILE = Path("data/raw/mutation_data.json")
OUTPUT_FILE = Path("data/processed/mutation_analytics.csv")


COLUMNS = [
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


def create_mutation_analytics():
    with INPUT_FILE.open("r", encoding="utf-8") as file:
        mutation_data = json.load(file)

    df = pd.json_normalize(mutation_data)

    mutation_analytics = df[COLUMNS].copy()

    mutation_analytics = mutation_analytics.rename(
        columns={
            "gene.hugoGeneSymbol": "gene",
            "gene.entrezGeneId": "entrezGeneId",
        }
    )

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    mutation_analytics.to_csv(
        OUTPUT_FILE,
        index=False,
    )

    return mutation_analytics


def main():
    mutation_analytics = create_mutation_analytics()

    print(f"Mutation analytics: {mutation_analytics.shape}")
    print(f"Saved to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()