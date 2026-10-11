import requests


study_id = "brca_tcga_pan_can_atlas_2018" #"pdac_msk_2024" #"luad_mskcc_2023_met_organotropism"

base_url = "https://www.cbioportal.org/api/studies"

clinical_url = f"{base_url}/{study_id}/clinical-attributes"
molecular_url = f"{base_url}/{study_id}/molecular-profiles"


clinical_response = requests.get(clinical_url, timeout=30)
clinical_response.raise_for_status()

molecular_response = requests.get(molecular_url, timeout=30)
molecular_response.raise_for_status()


clinical_attributes = clinical_response.json()
molecular_profiles = molecular_response.json()


print("\nCLINICAL ATTRIBUTES\n")

for attribute in clinical_attributes:
    print(
        attribute["clinicalAttributeId"],
        "|",
        attribute["displayName"]
    )


print("\nMOLECULAR PROFILES\n")

for profile in molecular_profiles:
    print(
        profile["molecularProfileId"],
        "|",
        profile["name"]
    )