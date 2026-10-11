""" import requests


API_URL = "https://www.cbioportal.org/api/studies"


def fetch_studies():
    response = requests.get(API_URL, timeout=30)
    response.raise_for_status()
    studies = response.json()

    return studies


def search_studies(studies, keyword, min_samples=100):
    matches = []

    for study in studies:
        name = study.get("name", "")
        description = study.get("description", "")
        sample_count = study.get("allSampleCount", 0)

        searchable_text = f"{name} {description}".lower()

        if keyword.lower() in searchable_text and sample_count >= min_samples:
            matches.append(study)

    matches = sorted(
        matches,
        key=lambda study: study.get("allSampleCount", 0),
        reverse=True,
    )

    return matches


def print_studies(studies):
    for study in studies:
        print(
            f"{study['studyId']:40} "
            f"{study['allSampleCount']:6} samples | "
            f"{study['name']}"
        )


def main():
    studies = fetch_studies()

    print(f"Total studies returned: {len(studies)}")

    keywords = [
        "breast",
        "lung",
        "colorectal",
    ]

    for keyword in keywords:
        print(f"\n--- {keyword.upper()} ---")

        matches = search_studies(
            studies,
            keyword=keyword,
            min_samples=100,
        )

        print_studies(matches[:10])


if __name__ == "__main__":
    main() """

import requests

url = "https://www.cbioportal.org/api/studies"

response = requests.get(url, timeout=30)

response.raise_for_status()

studies = response.json()

print(f"Total studies: {len(studies)}")

for study in studies:
    name = study.get("name", "")
    sample_count = study.get("allSampleCount", 0)

    if "breast" in name.lower() and sample_count >= 100:
        print(
            study["studyId"],
            sample_count,
            name
        )