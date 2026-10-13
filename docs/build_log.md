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

## Day 3 — Clinical Data Transformation

### Goal

Convert raw long-format clinical data into structured and analytics-ready tables.

### Patient Transformation

Raw patient data:

- 41,497 long-format records
- 1,084 patients
- 40 clinical attributes

Transformed wide table:

- 1,084 rows
- 42 columns

### Sample Transformation

Raw sample data:

- 19,348 long-format records
- 1,084 samples
- 18 clinical attributes

Transformed wide table:

- 1,084 rows
- 21 columns

### Validation Results

Patient table:

- 1,084 rows
- 1,084 unique patients
- 0 duplicate patient IDs

Sample table:

- 1,084 rows
- 1,084 unique samples
- 0 duplicate sample IDs

Patient/sample relationship:

- 0 patient IDs missing from sample table
- 0 sample patient IDs missing from patient table

### Data-Type Inspection

Pandas correctly inferred most numeric and text fields.

Examples:

Numeric:
- AGE
- OS_MONTHS
- DFS_MONTHS
- MUTATION_COUNT
- TMB_NONSYNONYMOUS

Categorical/text:
- SEX
- RACE
- SUBTYPE
- OS_STATUS
- SAMPLE_TYPE

### Value Inspection

Important observations:

- AGE ranged from 26 to 90
- OS_STATUS was complete
- SUBTYPE contained missing values
- RACE contained missing values
- MUTATION_COUNT contained high outliers

High mutation-count samples also had high TMB values.

This suggests the extreme values are internally consistent and should not automatically be treated as errors.

### Key Lesson

An outlier is not automatically bad data.

### Analytics Tables Created

Patient analytics table:

- 1,084 rows
- 17 columns

Sample analytics table:

- 1,084 rows
- 12 columns

### Final Local Data Flow

Raw JSON
→ Wide Clinical Tables
→ Validation
→ Analytics-Ready Tables 

## Day 4 — Mutation Data Ingestion and Profiling

### Goal

Retrieve and understand gene-level mutation data for the selected study.

### Mutation Profile

Molecular profile:

`brca_tcga_pan_can_atlas_2018_mutations`

Mutation sample list:

`brca_tcga_pan_can_atlas_2018_sequenced`

### Important API Finding

The normal GET mutation endpoint required an `entrezGeneId`, meaning it was designed for querying specific genes.

To retrieve all mutations for the sequenced cohort, the POST fetch endpoint was used instead.

### Raw Mutation Data

The mutation API returned:

- 84,226 mutation records
- 1,009 samples with at least one mutation record
- 1,009 patients with at least one mutation record
- 16,488 unique genes represented

Raw data was saved to:

`data/raw/mutation_data.json`

### Mutation Coverage Validation

The mutation sample list contained:

- 1,066 sequenced samples

Mutation records were returned for:

- 1,009 samples

Therefore:

- 57 sequenced samples had no returned mutation records

This means:

`sequenced sample ≠ sample with at least one mutation`

### Most Common Mutation Types

| Mutation Type | Records |
|---|---:|
| Missense Mutation | 64,473 |
| Frame Shift Deletion | 9,171 |
| Nonsense Mutation | 5,417 |
| Splice Site | 1,970 |
| Splice Region | 1,402 |
| Frame Shift Insertion | 913 |
| In Frame Deletion | 653 |

### Most Frequently Mutated Genes by Patient

| Gene | Patients |
|---|---:|
| TP53 | 347 |
| PIK3CA | 347 |
| TTN | 187 |
| CDH1 | 130 |
| GATA3 | 127 |
| MUC16 | 109 |
| KMT2C | 99 |
| MAP3K1 | 89 |
| PTEN | 58 |

### Important Lesson

Raw mutation-record counts are not the same as the number of patients carrying a mutation in a gene.

A patient may have multiple mutation records for the same gene.

Therefore, patient-level gene frequency was calculated using unique:

`patientId + gene`

pairs.

EOF