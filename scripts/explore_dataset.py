import requests


API_BASE = "https://www.cbioportal.org/api"

SELECTED_STUDY = "brca_tcga_pan_can_atlas_2018"

CANDIDATE_STUDIES = [
    "brca_tcga_pan_can_atlas_2018",
    "luad_mskcc_2023_met_organotropism",
    "crc_msk_2026",
    "prostate_msk_2024",
    "pdac_msk_2024",
]


def fetch_json(url):
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    return response.json()


def get_cancer_family(cancer_type_id, cancer_types):
    current_type = cancer_type_id

    while current_type in cancer_types:
        parent = cancer_types[current_type].get("parent")

        if parent == "tissue":
            return current_type

        current_type = parent

    return cancer_type_id


def show_cancer_families(studies, cancer_types):
    family_counts = {}
    largest_studies = {}

    for study in studies:
        family = get_cancer_family(
            study.get("cancerTypeId"),
            cancer_types,
        )

        family_counts[family] = family_counts.get(family, 0) + 1

        sample_count = study.get("allSampleCount", 0)

        if (
            family not in largest_studies
            or sample_count > largest_studies[family]["samples"]
        ):
            largest_studies[family] = {
                "samples": sample_count,
                "study_id": study["studyId"],
            }

    print("\nCANCER FAMILY SUMMARY")
    print("-" * 70)

    ranked_families = sorted(
        family_counts,
        key=family_counts.get,
        reverse=True,
    )

    for family in ranked_families[:15]:
        family_name = cancer_types.get(
            family,
            {},
        ).get("name", family)

        largest = largest_studies[family]

        print(
            f"{family_name:25} "
            f"studies={family_counts[family]:3} "
            f"largest={largest['samples']:5} "
            f"{largest['study_id']}"
        )


def compare_candidates():
    print("\nCANDIDATE STUDIES")
    print("-" * 70)

    for study_id in CANDIDATE_STUDIES:
        clinical = fetch_json(
            f"{API_BASE}/studies/{study_id}/clinical-attributes"
        )

        molecular = fetch_json(
            f"{API_BASE}/studies/{study_id}/molecular-profiles"
        )

        print(
            f"{study_id:45} "
            f"clinical={len(clinical):3} "
            f"molecular={len(molecular):2}"
        )


def inspect_selected_study():
    molecular_profiles = fetch_json(
        f"{API_BASE}/studies/{SELECTED_STUDY}/molecular-profiles"
    )

    print("\nSELECTED STUDY")
    print("-" * 70)
    print(SELECTED_STUDY)

    print("\nMolecular profiles:")

    for profile in molecular_profiles:
        print(
            "-",
            profile["molecularProfileId"],
            "|",
            profile["name"],
        )


def main():
    studies = fetch_json(f"{API_BASE}/studies")
    cancer_type_data = fetch_json(f"{API_BASE}/cancer-types")

    cancer_types = {
        item["cancerTypeId"]: item
        for item in cancer_type_data
    }

    print(f"Studies returned: {len(studies)}")

    show_cancer_families(
        studies,
        cancer_types,
    )

    compare_candidates()
    inspect_selected_study()


if __name__ == "__main__":
    main()