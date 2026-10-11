import json


def profile_data(file_path, entity_key, label):

    with open(file_path, "r") as file:
        data = json.load(file)

    entities = set()
    attributes = set()
    attribute_entities = {}
    entity_attribute_pairs = set()

    duplicate_pairs = 0

    for record in data:
        entity_id = record[entity_key]
        attribute_id = record["clinicalAttributeId"]

        entities.add(entity_id)
        attributes.add(attribute_id)

        if attribute_id not in attribute_entities:
            attribute_entities[attribute_id] = set()

        attribute_entities[attribute_id].add(entity_id)

        pair = (entity_id, attribute_id)

        if pair in entity_attribute_pairs:
            duplicate_pairs += 1
        else:
            entity_attribute_pairs.add(pair)

    total_entities = len(entities)

    print(f"\n{label} DATA PROFILE")
    print("-" * 40)

    print("Total raw records:", len(data))
    print("Unique entities:", total_entities)
    print("Unique attributes:", len(attributes))
    print("Duplicate entity-attribute pairs:", duplicate_pairs)

    print("\nATTRIBUTE COMPLETENESS")
    print("-" * 40)

    completeness_results = []

    for attribute_id in attributes:

        entities_with_value = len(attribute_entities[attribute_id])

        completeness = (
            entities_with_value / total_entities
        ) * 100

        completeness_results.append(
            (
                attribute_id,
                entities_with_value,
                completeness
            )
        )

    completeness_results.sort(
        key=lambda item: item[2]
    )

    for attribute_id, count, completeness in completeness_results:

        print(
            f"{attribute_id:40} "
            f"{count:5}/{total_entities} "
            f"{completeness:6.2f}%"
        )


profile_data(
    "data/raw/patient_clinical_data.json",
    "patientId",
    "PATIENT"
)

profile_data(
    "data/raw/sample_clinical_data.json",
    "sampleId",
    "SAMPLE"
)