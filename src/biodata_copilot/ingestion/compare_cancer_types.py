import requests


studies_url = "https://www.cbioportal.org/api/studies"
cancer_types_url = "https://www.cbioportal.org/api/cancer-types"


studies_response = requests.get(studies_url, timeout=30)
studies_response.raise_for_status()
studies = studies_response.json()


cancer_types_response = requests.get(cancer_types_url, timeout=30)
cancer_types_response.raise_for_status()
cancer_types = cancer_types_response.json()


cancer_type_lookup = {}

for cancer_type in cancer_types:
    cancer_type_lookup[cancer_type["cancerTypeId"]] = cancer_type


def get_cancer_family(cancer_type_id):
    current_type = cancer_type_id

    while current_type in cancer_type_lookup:

        parent = cancer_type_lookup[current_type].get("parent")

        if parent == "tissue":
            return current_type

        current_type = parent

    return cancer_type_id


family_study_counts = {}
largest_sample_count = {}
largest_study_name = {}
largest_study_id = {}


for study in studies:

    cancer_type_id = study.get("cancerTypeId")
    sample_count = study.get("allSampleCount", 0)
    study_name = study.get("name", "")

    cancer_family = get_cancer_family(cancer_type_id)

    if cancer_family not in family_study_counts:
        family_study_counts[cancer_family] = 0
        largest_sample_count[cancer_family] = 0
        largest_study_name[cancer_family] = ""
        largest_study_id[cancer_family] = ""

    family_study_counts[cancer_family] += 1

    if sample_count > largest_sample_count[cancer_family]:
        largest_sample_count[cancer_family] = sample_count
        largest_study_name[cancer_family] = study_name
        largest_study_id[cancer_family] = study["studyId"]


families = sorted(
    family_study_counts,
    key=family_study_counts.get,
    reverse=True
)


print("\nCancer Family Summary\n")


for family in families[:20]:

    family_name = cancer_type_lookup.get(family, {}).get("name", family)

    print(
        family_name,
        "| studies:", family_study_counts[family],
        "| largest study:", largest_sample_count[family],
        "| study ID:", largest_study_id[family],
        "|", largest_study_name[family]
    )