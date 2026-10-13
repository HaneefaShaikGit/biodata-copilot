cat > docs/scripts_overview.md <<'EOF'
# BioData Copilot — Scripts Overview

| Script | Purpose | Main Output | Status |
|---|---|---|---|
| `explore_studies.py` | Explore public cBioPortal studies | Candidate studies | Exploration |
| `compare_cancer_types.py` | Group studies into cancer families | Cancer-family summary | Exploration |
| `compare_candidate_studies.py` | Compare shortlisted studies | Attribute/profile counts | Exploration |
| `inspect_study.py` | Inspect one study in detail | Clinical + molecular fields | Exploration |
| `check_patient_sample_relationship.py` | Check patient-to-sample relationship | 1 patient → 1 sample | Exploration |
| `profile_clinical_data.py` | Profile raw clinical data quality | Completeness + duplicate checks | Validation |
| `transform_patient_data.py` | Transform patient data to wide format | Wide patient table | Transformation |
| `transform_sample_data.py` | Transform sample data to wide format | Wide sample table | Transformation |
| `validate_wide_tables.py` | Validate transformed tables | Duplicate/link checks | Validation |
| `inspect_data_types.py` | Inspect inferred data types | Type summary | Validation |
| `inspect_values.py` | Inspect distributions and outliers | Value profile | Validation |
| `create_analytics_tables.py` | Create V1 analytics-ready tables | Patient + sample analytics CSVs | Transformation |
| `fetch_mutation_data.py` | Retrieve mutation records | Raw mutation JSON | Ingestion |
| `profile_mutation_data.py` | Profile mutation dataset | Mutation/gene summaries | Validation |
| `validate_mutation_coverage.py` | Check sequenced vs mutated samples | Coverage comparison | Validation |

---

## 1. `explore_studies.py`

### Purpose
Fetch all studies from cBioPortal and understand the API response.

### API
`GET /api/studies`

### Input
cBioPortal study metadata.

### Output
- study ID
- study name
- sample count
- reference genome

### Concepts learned
- `requests.get()`
- HTTP GET
- `raise_for_status()`
- JSON
- lists
- dictionaries
- loops
- conditions

### Main result
Approximately 550 studies were returned.

---

## 2. `compare_cancer_types.py`

### Purpose
Compare study availability across broad cancer families.

### APIs
- `GET /api/studies`
- `GET /api/cancer-types`

### Problem discovered
Related cancer types could appear under different IDs.

Example:

`brca → breast → tissue`

### Solution
Follow the parent hierarchy until the broad cancer family is reached.

### Output
For each family:
- number of studies
- largest sample count
- largest study ID
- largest study name

---

## 3. `compare_candidate_studies.py`

### Purpose
Compare several large candidate studies.

### APIs
- `/clinical-attributes`
- `/molecular-profiles`

### Output
Number of:
- clinical attributes
- molecular profiles

### Main lesson
More attributes does not automatically mean a better dataset.

The actual fields must be inspected.

---

## 4. `inspect_study.py`

### Purpose
Inspect the actual metadata available within one study.

### Input
One `study_id`.

Example:

`brca_tcga_pan_can_atlas_2018`

### Output
Clinical attributes and molecular profiles.

### Main result
The TCGA Breast PanCancer Atlas study contains broad clinical and molecular information.

## `check_patient_sample_relationship.py`

### Purpose
Check whether patients in the selected study have one or multiple biological samples.

### Input
`data/raw/sample_clinical_data.json`

### Output
- total patients
- number of patients with multiple samples

### Result
- Total patients: 1,084
- Patients with multiple samples: 0

### Conclusion
The study currently behaves as a one-patient-to-one-sample dataset.

### Status
Validation / exploration script.

## `profile_clinical_data.py`

### Purpose
Profile the raw patient and sample clinical datasets before transformation.

### Input
- `data/raw/patient_clinical_data.json`
- `data/raw/sample_clinical_data.json`

### Checks Performed
- total raw records
- unique entities
- unique attributes
- duplicate entity-attribute pairs
- attribute completeness

### Main Results

Patient:
- 41,497 records
- 1,084 patients
- 40 attributes
- 0 duplicate patient-attribute pairs

Sample:
- 19,348 records
- 1,084 samples
- 18 attributes
- 0 duplicate sample-attribute pairs

### Conclusion
The raw clinical datasets are suitable for transformation.

Patient-level completeness varies more than sample-level completeness.

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
Validate that the pivot transformation did not create duplicate or missing entities.

### Checks
- row count
- unique IDs
- duplicate IDs
- patient/sample consistency

### Result
All checks passed.

---

## `inspect_data_types.py`

### Purpose
Inspect pandas data types before changing any column types.

### Result
Most types were inferred correctly.

---

## `inspect_values.py`

### Purpose
Inspect category values, numeric distributions, and extreme values.

### Important Finding
High mutation-count outliers were also associated with high TMB values.

They were retained.

---

## `create_analytics_tables.py`

### Purpose
Create smaller V1 analytics tables containing only relevant fields.

### Outputs
- `patient_analytics.csv`
- `sample_analytics.csv`

### Result

Patient analytics:
- 1,084 rows
- 17 columns

Sample analytics:
- 1,084 rows
- 12 columns

## `fetch_mutation_data.py`

### Purpose

Retrieve all detailed mutation records for samples with mutation sequencing data.

### API

POST:

`/api/molecular-profiles/{molecularProfileId}/mutations/fetch`

### Input

Mutation molecular profile:

`brca_tcga_pan_can_atlas_2018_mutations`

Sample list:

`brca_tcga_pan_can_atlas_2018_sequenced`

### Output

`data/raw/mutation_data.json`

### Result

84,226 mutation records were retrieved.

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

### Result

- 84,226 mutation records
- 1,009 unique samples
- 1,009 unique patients
- 16,488 unique genes

### Important Logic

Gene frequency is calculated using unique:

`patientId + gene`

pairs rather than raw mutation-record counts.

---

## `validate_mutation_coverage.py`

### Purpose

Compare the mutation sequencing sample list with samples that actually have mutation records.

### Result

- Sequenced samples: 1,066
- Samples with mutation records: 1,009
- Sequenced samples with no mutation records: 57

### Conclusion

Being sequenced does not necessarily mean a sample has a called mutation.


EOF