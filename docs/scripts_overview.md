# BioData Copilot — Scripts Overview

| Script | Purpose | Main Output | Stage |
|---|---|---|---|
| `explore_studies.py` | Explore cBioPortal studies | Candidate studies | Exploration |
| `compare_cancer_types.py` | Group studies into cancer families | Cancer-family summary | Exploration |
| `compare_candidate_studies.py` | Compare shortlisted studies | Study comparison | Exploration |
| `inspect_study.py` | Inspect one study in detail | Clinical + molecular metadata | Exploration |
| `fetch_clinical_data.py` | Retrieve clinical records | Raw patient/sample JSON | Ingestion |
| `check_patient_sample_relationship.py` | Check patient/sample relationship | Relationship summary | Validation |
| `profile_clinical_data.py` | Profile raw clinical data | Completeness + duplicate checks | Validation |
| `transform_patient_data.py` | Convert patient data to wide format | Patient wide CSV | Transformation |
| `transform_sample_data.py` | Convert sample data to wide format | Sample wide CSV | Transformation |
| `validate_wide_tables.py` | Validate transformed clinical tables | Validation results | Validation |
| `inspect_data_types.py` | Inspect inferred column types | Type summary | Validation |
| `inspect_values.py` | Inspect distributions and outliers | Value profile | Validation |
| `create_analytics_tables.py` | Create V1 clinical analytics datasets | Patient + sample analytics CSVs | Transformation |
| `fetch_mutation_data.py` | Retrieve mutation records | Raw mutation JSON | Ingestion |
| `profile_mutation_data.py` | Profile mutation dataset | Mutation/gene summaries | Validation |
| `validate_mutation_coverage.py` | Compare sequenced vs mutated samples | Coverage summary | Validation |
| `create_mutation_analytics.py` | Flatten mutation JSON | Mutation analytics CSV | Transformation |
| `validate_mutation_analytics.py` | Validate mutation analytics output | Validation summary | Validation |
| `upload_to_gcs.py` | Upload raw data to GCS | Raw GCS objects | Cloud Exploration |
| `upload_processed_to_gcs.py` | Upload processed data to GCS | Processed GCS objects | Cloud Exploration |
| `load_duckdb.py` | Load processed datasets into DuckDB | Local analytical database | Database |
| `inspect_duckdb.py` | Inspect DuckDB table schemas | Schema summary | Database |
| `validate_table_grain.py` | Confirm entity grain and relationships | Grain summary | Database |
| `create_models.py` | Create reusable analytical views | Patient/gene models | SQL Modeling |
---

## `explore_studies.py`

### Purpose

Fetch available studies from cBioPortal and understand the API response.

### API

`GET /api/studies`

### Main Result

Approximately 550 studies were returned.

### Concepts Learned

- HTTP GET
- `requests`
- JSON
- lists
- dictionaries
- loops
- conditions
- `raise_for_status()`

---

## `compare_cancer_types.py`

### Purpose

Compare study availability across broad cancer families.

### APIs

- `GET /api/studies`
- `GET /api/cancer-types`

### Important Finding

Related cancer types can appear under different IDs.

Example:

`brca → breast → tissue`

### Solution

Follow the parent hierarchy until the broad cancer family is reached.

### Output

For each cancer family:

- number of studies
- largest sample count
- largest study ID
- largest study name

---

## `compare_candidate_studies.py`

### Purpose

Compare shortlisted studies using their available clinical and molecular metadata.

### APIs

- `/clinical-attributes`
- `/molecular-profiles`

### Output

For each candidate study:

- number of clinical attributes
- number of molecular profiles

### Main Lesson

The largest dataset or the dataset with the most attributes is not automatically the most appropriate dataset.

Actual fields must be inspected.

---

## `inspect_study.py`

### Purpose

Inspect clinical attributes and molecular profiles for one study.

### Example Study

`brca_tcga_pan_can_atlas_2018`

### Main Result

The TCGA Breast PanCancer Atlas study contains broad clinical and molecular information and was selected for BioData Copilot V1.

---

## `fetch_clinical_data.py`

### Purpose

Retrieve actual patient-level and sample-level clinical records from cBioPortal.

### Outputs

- `data/raw/patient_clinical_data.json`
- `data/raw/sample_clinical_data.json`

### Results

Patient-level records:

- 41,497 records
- 1,084 unique patients

Sample-level records:

- 19,348 records
- 1,084 unique samples

---

## `check_patient_sample_relationship.py`

### Purpose

Check whether patients in the selected study have one or multiple biological samples.

### Input

`data/raw/sample_clinical_data.json`

### Result

- Total patients: 1,084
- Patients with multiple samples: 0

Observed relationship:

`1 patient → 1 sample`

### Why It Matters

This simplifies future joins between patient-level and sample-level data.

---

## `profile_clinical_data.py`

### Purpose

Profile the raw patient and sample clinical datasets before transformation.

### Inputs

- `data/raw/patient_clinical_data.json`
- `data/raw/sample_clinical_data.json`

### Checks

- total raw records
- unique entities
- unique attributes
- duplicate entity-attribute pairs
- attribute completeness

### Patient Results

- 41,497 records
- 1,084 patients
- 40 attributes
- 0 duplicate patient-attribute pairs

### Sample Results

- 19,348 records
- 1,084 samples
- 18 attributes
- 0 duplicate sample-attribute pairs

### Conclusion

The clinical datasets were suitable for transformation.

Patient-level attributes showed more variable completeness than sample-level attributes.

---

## `transform_patient_data.py`

### Purpose

Convert patient clinical data from long format to wide format.

### Input

`data/raw/patient_clinical_data.json`

### Output

`data/processed/patient_clinical_wide.csv`

### Result

- 1,084 rows
- 42 columns

### Transformation

Long format:

`patientId | clinicalAttributeId | value`

Wide format:

`patientId | AGE | SEX | RACE | SUBTYPE | OS_MONTHS | ...`

---

## `transform_sample_data.py`

### Purpose

Convert sample clinical data from long format to wide format.

### Input

`data/raw/sample_clinical_data.json`

### Output

`data/processed/sample_clinical_wide.csv`

### Result

- 1,084 rows
- 21 columns

---

## `validate_wide_tables.py`

### Purpose

Validate that the long-to-wide transformation did not create duplicate or missing entities.

### Checks

- row count
- unique patient IDs
- unique sample IDs
- duplicate IDs
- patient/sample consistency

### Results

Patient table:

- 1,084 rows
- 1,084 unique patients
- 0 duplicate patient IDs

Sample table:

- 1,084 rows
- 1,084 unique samples
- 0 duplicate sample IDs

Patient/sample consistency checks passed.

---

## `inspect_data_types.py`

### Purpose

Inspect pandas-inferred data types before changing any column types manually.

### Main Lesson

Data types should be inspected before forcing conversions.

For example, a numeric field may appear as a floating-point column because missing values are present.

---

## `inspect_values.py`

### Purpose

Inspect:

- categorical distributions
- numeric ranges
- missing values
- unusual values
- possible outliers

### Important Finding

Very high mutation-count values were also associated with very high TMB values.

Because they were internally consistent, they were retained rather than automatically removed as errors.

---

## `create_analytics_tables.py`

### Purpose

Create smaller V1 clinical analytics datasets containing only fields relevant to the application.

### Outputs

- `data/processed/patient_analytics.csv`
- `data/processed/sample_analytics.csv`

### Patient Analytics Result

- 1,084 rows
- 17 columns

### Sample Analytics Result

- 1,084 rows
- 12 columns

### Why

The original wide datasets contain more fields than V1 requires.

The analytics datasets keep the project focused while preserving the wider intermediate tables for traceability.

---

## `fetch_mutation_data.py`

### Purpose

Retrieve detailed mutation records for samples with mutation sequencing data.

### API

POST:

`/api/molecular-profiles/{molecularProfileId}/mutations/fetch`

### Molecular Profile

`brca_tcga_pan_can_atlas_2018_mutations`

### Sample List

`brca_tcga_pan_can_atlas_2018_sequenced`

### Output

`data/raw/mutation_data.json`

### Result

84,226 mutation records were retrieved.

### Important API Lesson

The normal GET mutation endpoint required an `entrezGeneId`.

The POST fetch endpoint was used because the project needed mutation records across the full sequenced cohort rather than for one specific gene.

---

## `profile_mutation_data.py`

### Purpose

Profile the raw mutation dataset.

### Checks

- total mutation records
- unique samples
- unique patients
- unique genes
- mutation-type frequencies
- most frequently mutated genes by patient

### Results

- 84,226 mutation records
- 1,009 unique samples
- 1,009 unique patients
- 16,488 unique genes

### Most Common Mutation Type

`Missense_Mutation`

### Important Logic

Gene frequency is calculated using unique:

`patientId + gene`

pairs.

This avoids counting multiple mutation records from the same patient and gene as separate patients.

---

## `validate_mutation_coverage.py`

### Purpose

Compare samples listed as mutation-sequenced with samples that actually have returned mutation records.

### Results

- Sequenced samples: 1,066
- Samples with mutation records: 1,009
- Sequenced samples without mutation records: 57

### Conclusion

Being sequenced does not necessarily mean that a sample has at least one returned mutation record.

Therefore:

`sequenced sample ≠ sample with a mutation`

---

## `create_mutation_analytics.py`

### Purpose

Flatten nested mutation JSON into a tabular analytics dataset.

### Input

`data/raw/mutation_data.json`

### Output

`data/processed/mutation_analytics.csv`

### Result

- 84,226 rows
- 19 columns
- 1,009 unique patients
- 1,009 unique samples
- 16,488 unique genes

### Important Transformation

Nested fields such as:

`gene.hugoGeneSymbol`

are flattened and renamed to:

`gene`

The transformation does not aggregate mutation records.

One output row still represents one mutation record.

---

## `validate_mutation_analytics.py`

### Purpose

Validate that mutation flattening preserved the expected records and critical identifiers.

### Results

- Raw mutation records: 84,226
- Processed rows: 84,226
- Processed columns: 19
- Unique patients: 1,009
- Unique samples: 1,009
- Unique genes: 16,488

### Missing Critical Values

- Missing `patientId`: 0
- Missing `sampleId`: 0
- Missing `gene`: 0
- Missing `mutationType`: 0

### Result

Row-count validation:

`PASSED`

---

## `upload_to_gcs.py`

### Purpose

Upload raw biomedical datasets to Google Cloud Storage during cloud architecture exploration.

### Inputs

- `data/raw/patient_clinical_data.json`
- `data/raw/sample_clinical_data.json`
- `data/raw/mutation_data.json`

### Authentication

Uses Google Application Default Credentials.

No credential files are stored inside the repository.

### Library

`google-cloud-storage`

### Status

Cloud exploration / optional Phase 2.

GCS is not required by the current local-first V1 architecture.

---

## `upload_processed_to_gcs.py`

### Purpose

Upload processed analytics datasets to a processed Google Cloud Storage bucket.

### Inputs

- `data/processed/patient_analytics.csv`
- `data/processed/sample_analytics.csv`
- `data/processed/mutation_analytics.csv`

### Why It Was Built

The script demonstrated how pipeline outputs can be uploaded programmatically rather than manually through the Google Cloud Console.

### Status

Cloud exploration / optional Phase 2.

The current V1 architecture will continue locally using DuckDB.

---

## `load_duckdb.py`

### Purpose

Load the processed BioData Copilot datasets into the local DuckDB analytical database.

### Inputs

- `patient_analytics.csv`
- `sample_analytics.csv`
- `mutation_analytics.csv`

### Output

`data/biodata.duckdb`

### Tables

- `patient_analytics`
- `sample_analytics`
- `mutation_analytics`

### Results

- Patient rows: 1,084
- Sample rows: 1,084
- Mutation rows: 84,226

---

## `inspect_duckdb.py`

### Purpose

Inspect DuckDB table schemas and confirm the imported data types.

### Main Finding

DuckDB correctly inferred the main analytical types, including:

- identifiers as `VARCHAR`
- age and genomic positions as integer types
- survival and TMB measures as numeric types
- radiation therapy as Boolean

---

## `validate_table_grain.py`

### Purpose

Confirm the grain of the three main analytical tables.

### Results

`patient_analytics`

`1 row = 1 patient`

`sample_analytics`

`1 row = 1 sample`

`mutation_analytics`

`1 row = 1 mutation record`

The patient-to-sample join returned 1,084 rows, confirming the one-to-one relationship observed earlier.

### Status

This is an exploratory validation script and may later be merged or removed during project cleanup.

---

## `create_models.py`

### Purpose

Create reusable DuckDB analytical views combining clinical and genomic information.

### Models

`patient_gene_mutations`

Grain:

`1 patient + 1 gene`

`subtype_gene_mutation_summary`

Grain:

`1 subtype + 1 gene`

### Note

During final cleanup, SQL model definitions will be kept in the `sql/` directory and Python execution code will be simplified to avoid duplicated SQL logic.