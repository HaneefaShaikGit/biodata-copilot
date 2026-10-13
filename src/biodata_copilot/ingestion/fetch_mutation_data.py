import json
import requests


molecular_profile_id = "brca_tcga_pan_can_atlas_2018_mutations"
sample_list_id = "brca_tcga_pan_can_atlas_2018_sequenced"


url = (
    f"https://www.cbioportal.org/api/molecular-profiles/"
    f"{molecular_profile_id}/mutations/fetch"
)


request_body = {
    "sampleListId": sample_list_id
}


response = requests.post(
    url,
    params={"projection": "DETAILED"},
    json=request_body,
    timeout=60,
)

response.raise_for_status()


mutation_data = response.json()


print("Total mutation records:", len(mutation_data))


output_file = "data/raw/mutation_data.json"


with open(output_file, "w") as file:
    json.dump(mutation_data, file, indent=2)


print("Raw mutation data saved to:", output_file)