import requests


base_url = "https://www.cbioportal.org/api/studies"

study_ids = [
    "breast_msk_2026",
    "luad_mskcc_2023_met_organotropism",
    "crc_msk_2026",
    "prostate_msk_2024",
    "pdac_msk_2024",
]


for study_id in study_ids:

    clinical_url = f"{base_url}/{study_id}/clinical-attributes"
    molecular_url = f"{base_url}/{study_id}/molecular-profiles"

    clinical_response = requests.get(clinical_url, timeout=30)
    clinical_response.raise_for_status()

    molecular_response = requests.get(molecular_url, timeout=30)
    molecular_response.raise_for_status()

    clinical_attributes = clinical_response.json()
    molecular_profiles = molecular_response.json()

    print("\n", study_id)
    print("Clinical attributes:", len(clinical_attributes))
    print("Molecular profiles:", len(molecular_profiles))