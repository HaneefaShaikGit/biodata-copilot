cat > docs/build_log.md <<'EOF'
# BioData Copilot — Build Log

## Day 1 — Project Foundation

### Goal
Set up the Python project locally and understand the architecture before building.

### What we did
- Created the project using `uv`
- Confirmed Python 3.12.10
- Created the Python package under `src/biodata_copilot`
- Created folders for ingestion, validation, transformation, analytics and AI
- Initialized local Git
- Created initial project documentation

### Concepts learned
- API = interface used by software systems to communicate
- JSON = structured data-interchange format
- GCS = object/file storage
- BigQuery = analytical data warehouse
- Raw data should be preserved for traceability
- BigQuery should calculate factual results
- LLM should explain verified results

### Project Flow

Public Biomedical Data
→ REST API
→ Python
→ GCS
→ Validation / Transformation
→ BigQuery
→ SQL
→ Verified Result
→ OpenAI
→ User

### Result
The package entry point worked successfully:

`uv run biodata-copilot`

Output:

`Hello from biodata-copilot!`

---

## Day 2 — Dataset Exploration

### Goal
Explore cBioPortal and select a suitable biomedical dataset.

### API health check

Endpoint:

`https://www.cbioportal.org/api/health`

Result:

`{"status":"UP"}`

HTTP status:

`200`

### Study exploration

Endpoint:

`/api/studies`

Result:

`550 studies`

### What we discovered
- cBioPortal contains hundreds of cancer studies
- Studies have different sample counts
- Raw cancer IDs do not always represent separate disease families
- Example: `brca` belongs under `breast`
- Dataset size alone is not enough for dataset selection

### Cancer-family comparison

Examples:

| Family | Studies | Largest Study |
|---|---:|---:|
| Lung | 41 | 2,653 |
| Breast | 38 | 6,318 |
| CNS/Brain | 35 | 1,122 |
| Prostate | 31 | 2,260 |
| Bowel | 29 | 7,237 |
| Pancreas | 21 | 2,336 |

### Candidate comparison

| Study | Clinical Attributes | Molecular Profiles |
|---|---:|---:|
| Breast MSK 2026 | 36 | 3 |
| Lung MSK 2023 | 91 | 3 |
| Colorectal MSK 2026 | 23 | 3 |
| Prostate MSK 2024 | 24 | 3 |
| Pancreas MSK 2024 | 52 | 3 |

### Important finding
The biggest study is not automatically the best dataset.

Examples:
- Lung dataset was focused on metastatic organotropism
- Pancreas dataset was strongly focused on KRAS

### Selected dataset

Study ID:

`brca_tcga_pan_can_atlas_2018`

Reason:
- broad clinical information
- stage and subtype information
- survival outcomes
- mutation data
- mRNA expression
- copy-number data
- methylation
- protein data
- structural variants

### V1 scope

Initially use:
1. Clinical data
2. Mutation data

### Next step
Retrieve actual clinical records from the selected study.

### Patient–Sample Relationship Check

The selected study returned:

- 1,084 unique patients
- 1,084 unique samples
- 0 patients with multiple samples

This means the observed relationship in this study is:

`1 patient → 1 sample`

This simplifies future joins between patient-level and sample-level clinical data.

### Raw Clinical Data Profiling

The patient-level clinical dataset contains:

- 41,497 raw records
- 1,084 unique patients
- 40 unique clinical attributes
- 0 duplicate patient-attribute pairs

The sample-level clinical dataset contains:

- 19,348 raw records
- 1,084 unique samples
- 18 unique clinical attributes
- 0 duplicate sample-attribute pairs

The lowest patient-level completeness was observed for:

| Attribute | Completeness |
|---|---:|
| PRIMARY_LYMPH_NODE_PRESENTATION_ASSESSMENT | 66.42% |
| NEW_TUMOR_EVENT_AFTER_INITIAL_TREATMENT | 81.64% |
| ETHNICITY | 84.41% |
| DFS_MONTHS | 86.81% |
| DFS_STATUS | 86.90% |

The sample-level dataset was generally more complete. Its lowest completeness values were:

| Attribute | Completeness |
|---|---:|
| MSI_SCORE_MANTIS | 95.39% |
| ANEUPLOIDY_SCORE | 96.03% |
| MUTATION_COUNT | 98.34% |
| TMB_NONSYNONYMOUS | 98.34% |
| FRACTION_GENOME_ALTERED | 98.52% |

### Interpretation

Completeness here measures whether an attribute is present for an entity.

It does not yet validate whether the actual value is biologically or logically correct.

No duplicate entity-attribute pairs were found.

This means the long-format clinical data is suitable for transformation into wider analytical tables.

EOF