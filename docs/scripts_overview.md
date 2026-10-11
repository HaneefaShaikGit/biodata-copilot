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

EOF