cat > docs/scripts_overview.md <<'EOF'
# BioData Copilot — Scripts Overview

| Script | Purpose | Main Output | Status |
|---|---|---|---|
| `explore_studies.py` | Explore public cBioPortal studies | Candidate studies | Exploration |
| `compare_cancer_types.py` | Group studies into cancer families | Cancer-family summary | Exploration |
| `compare_candidate_studies.py` | Compare shortlisted studies | Attribute/profile counts | Exploration |
| `inspect_study.py` | Inspect one study in detail | Clinical + molecular fields | Exploration |

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
EOF