import json
from pathlib import Path

import requests


MOLECULAR_PROFILE_ID = "brca_tcga_pan_can_atlas_2018_mutations"
SAMPLE_LIST_ID = "brca_tcga_pan_can_atlas_2018_sequenced"

API_URL = (
    "https://www.cbioportal.org/api/molecular-profiles/"
    f"{MOLECULAR_PROFILE_ID}/mutations/fetch"
)

OUTPUT_FILE = Path("data/raw/mutation_data.json")


def fetch_mutation_data():
    response = requests.post(
        API_URL,
        params={"projection": "DETAILED"},
        json={"sampleListId": SAMPLE_LIST_ID},
        timeout=60,
    )

    response.raise_for_status()

    return response.json()


def save_json(data):
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    with OUTPUT_FILE.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=2)


def main():
    mutation_data = fetch_mutation_data()

    save_json(mutation_data)

    print(f"Mutation records: {len(mutation_data)}")
    print(f"Mutation data saved to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()