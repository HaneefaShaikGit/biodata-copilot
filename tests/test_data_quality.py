from pathlib import Path

import pandas as pd


DATA_DIR = Path("data/processed")


patient_df = pd.read_csv(DATA_DIR / "patient_analytics.csv")
sample_df = pd.read_csv(DATA_DIR / "sample_analytics.csv")
mutation_df = pd.read_csv(DATA_DIR / "mutation_analytics.csv")


def test_expected_row_counts():
    assert len(patient_df) == 1084
    assert len(sample_df) == 1084
    assert len(mutation_df) == 84226


def test_patient_ids_are_unique():
    assert patient_df["patientId"].is_unique


def test_sample_ids_are_unique():
    assert sample_df["sampleId"].is_unique


def test_patient_sample_relationship():
    patient_ids = set(patient_df["patientId"])
    sample_patient_ids = set(sample_df["patientId"])

    assert patient_ids == sample_patient_ids


def test_mutation_critical_fields_are_complete():
    critical_columns = [
        "patientId",
        "sampleId",
        "gene",
        "mutationType",
    ]

    assert mutation_df[critical_columns].isna().sum().sum() == 0


def test_mutation_patient_and_sample_counts():
    assert mutation_df["patientId"].nunique() == 1009
    assert mutation_df["sampleId"].nunique() == 1009