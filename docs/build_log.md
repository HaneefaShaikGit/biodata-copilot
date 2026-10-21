# BioData Copilot — Build Log

This document records the major implementation steps, findings, mistakes, validations, and architectural decisions made while building BioData Copilot.

The goal is to preserve not only what was built, but also why each step was taken.

---

# Day 1 — Project Setup and Architecture

## Goal

Define the project, understand the problem, and create a clean Python development environment.

## Project Idea

BioData Copilot is a biomedical data platform that combines:

- biomedical data
- data engineering
- SQL analytics
- trustworthy AI explanations

The core principle is:

**The database calculates facts.**

**The LLM explains verified facts.**

The LLM should not invent numerical results or unsupported clinical conclusions.

---

## Initial Architecture

The first architecture considered was:

cBioPortal  
→ Python  
→ Raw Storage  
→ Validation  
→ Transformation  
→ Analytical Database  
→ SQL  
→ Verified Results  
→ OpenAI  
→ User Interface

The exact storage and analytical technologies were intentionally left open until the data requirements were better understood.

---

## Python Project Setup

The project was initialized using `uv`.

Project location:

`/Users/haneefa/Desktop/Job/biodata-copilot`

Python version:

`3.12.10`

Main project structure:

- `src/`
- `data/raw/`
- `data/processed/`
- `docs/`
- `tests/`
- `app/`
- `notebooks/`

---

## Git Setup

Git was initialized locally.

The main branch was renamed to:

`main`

A `.gitignore` file was added to exclude:

- virtual environments
- local environment files
- raw datasets
- processed datasets
- operating-system files
- editor-specific files

The project is being developed locally before being published to GitHub.

---

## Important Concepts Learned

### API

An API allows one application to request information or functionality from another application.

### JSON

JSON is a structured data-interchange format commonly returned by APIs.

It is not only a file format.

### Raw Data

Raw data should be preserved before transformation so that downstream datasets can be rebuilt and transformation errors can be investigated.

### Grounded AI

The LLM should explain verified results rather than calculate or invent the underlying facts.

---

# Day 2 — Dataset Exploration and Selection

## Goal

Choose a biomedical dataset using actual data coverage rather than randomly selecting a cancer type.

---

## cBioPortal API Check

The cBioPortal API was tested successfully.

API health returned:

`HTTP 200`

The studies endpoint returned approximately:

`550 studies`

---

## Initial Study Exploration

Created:

`explore_studies.py`

The script retrieved study metadata and helped understand the structure returned by the cBioPortal API.

Important Python concepts included:

- `requests.get()`
- `response.json()`
- lists
- dictionaries
- loops
- conditions
- `raise_for_status()`

---

## Problem with Keyword-Based Selection

An early approach searched for studies containing terms such as:

`breast`

This was rejected as the main selection method because the keyword itself was arbitrary.

The dataset should be chosen based on actual study coverage and available fields.

---

## Cancer-Family Comparison

Created:

`compare_cancer_types.py`

The script retrieved:

- studies
- cancer-type metadata

A problem was discovered:

related cancer types could appear under different identifiers.

Example:

`brca → breast → tissue`

A hierarchy-following function was created to group specific cancer types into broader cancer families.

---

## Cancer-Family Summary

Examples of broad study coverage included:

| Cancer Family | Approx. Studies |
|---|---:|
| Lung | 41 |
| Breast | 38 |
| CNS / Brain | 35 |
| Prostate | 31 |
| Lymphoid | 30 |
| Bowel | 29 |
| Skin | 28 |
| Bladder / Urinary | 28 |
| Soft Tissue | 27 |
| Kidney | 25 |
| Pancreas | 21 |

The exercise demonstrated that dataset selection should consider more than one study or disease area.

---

## Candidate Study Comparison

Created:

`compare_candidate_studies.py`

Candidate studies from several cancer families were compared using:

- number of clinical attributes
- number of molecular profiles
- sample count

Candidate examples included:

- Breast
- Lung
- Bowel
- Prostate
- Pancreas

---

## Important Finding

A larger dataset or a dataset with more fields is not automatically better.

The meaning of the fields must be inspected.

---

## Detailed Candidate Inspection

Created:

`inspect_study.py`

### Lung Study

The inspected lung dataset contained rich information including:

- survival
- stage
- treatment
- metastatic sites
- TMB
- MSI
- mutation data

However, it had a specialised metastatic organotropism focus.

### Pancreas Study

The pancreatic study contained:

- survival
- treatment
- TMB
- MSI
- mutation data
- extensive KRAS-related variables

However, it was strongly KRAS-focused.

### Breast TCGA PanCancer Atlas

Study ID:

`brca_tcga_pan_can_atlas_2018`

It contained broad:

- demographic information
- tumour stage
- survival outcomes
- breast-cancer subtype
- mutation data
- mRNA data
- copy-number data
- methylation
- protein information
- structural variants

---

## Dataset Decision

Selected:

`brca_tcga_pan_can_atlas_2018`

Reason:

The dataset provides broad clinical and molecular coverage without being narrowly designed around one specific research question.

---

# Day 2 — Clinical Data Ingestion

## Goal

Retrieve actual patient-level and sample-level clinical records.

---

## Clinical API Structure

Clinical data was returned in long format.

Example structure:

`patientId | clinicalAttributeId | value`

Patient and sample clinical data were retrieved separately.

---

## Raw Clinical Data

Created:

`fetch_clinical_data.py`

Outputs:

- `data/raw/patient_clinical_data.json`
- `data/raw/sample_clinical_data.json`

### Patient Data

- 41,497 raw records
- 1,084 unique patients
- 40 unique clinical attributes

### Sample Data

- 19,348 raw records
- 1,084 unique samples
- 18 unique clinical attributes

---

## Patient–Sample Relationship

Created:

`check_patient_sample_relationship.py`

Result:

- Total patients: 1,084
- Patients with multiple samples: 0

Observed relationship:

`1 patient → 1 sample`

Both patient and sample identifiers are still retained because other biomedical studies may have one-to-many relationships.

---

## Clinical Data Profiling

Created:

`profile_clinical_data.py`

Checks included:

- record count
- entity count
- attribute count
- duplicate entity-attribute pairs
- completeness

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

---

## Important Data-Quality Lesson

Completeness means that an attribute is present for an entity.

It does not mean that the biological value is necessarily correct.

---

# Day 3 — Clinical Transformation and Validation

## Goal

Convert long-format clinical API data into structured analytical tables.

---

## Patient Transformation

Created:

`transform_patient_data.py`

Transformation:

Long format:

`patientId | clinicalAttributeId | value`

became wide format:

`patientId | AGE | SEX | RACE | SUBTYPE | OS_MONTHS | ...`

Output:

`data/processed/patient_clinical_wide.csv`

Result:

- 1,084 rows
- 42 columns

---

## Sample Transformation

Created:

`transform_sample_data.py`

Output:

`data/processed/sample_clinical_wide.csv`

Result:

- 1,084 rows
- 21 columns

---

## Wide-Table Validation

Created:

`validate_wide_tables.py`

### Patient Table

- 1,084 rows
- 1,084 unique patient IDs
- 0 duplicate patient IDs

### Sample Table

- 1,084 rows
- 1,084 unique sample IDs
- 0 duplicate sample IDs

Cross-table patient consistency checks also passed.

---

## Data-Type Inspection

Created:

`inspect_data_types.py`

Important types included:

- identifiers → string
- AGE → integer
- survival months → floating point
- clinical categories → string
- mutation count / TMB → numeric

A key lesson was:

Do not force data types before inspecting the actual values.

---

## Value Inspection

Created:

`inspect_values.py`

Examples observed:

### Sex

- Female: 1,072
- Male: 12

### Subtype

Examples:

- LumA
- LumB
- Basal
- Her2
- Normal
- missing values

### Overall Survival Status

- Living: 933
- Deceased: 151

### Age

- Count: 1,084
- Mean: approximately 58.4
- Minimum: 26
- Maximum: 90

---

## Outlier Review

Some samples had very high mutation counts.

Examples also showed correspondingly high TMB values.

Because the values were internally consistent, they were retained.

Important lesson:

**Outlier does not automatically mean error.**

---

## Clinical Analytics Tables

Created:

`create_analytics_tables.py`

### Patient Analytics

Output:

`data/processed/patient_analytics.csv`

Result:

- 1,084 rows
- 17 columns

Fields include:

- patient ID
- study ID
- age
- sex
- race
- ethnicity
- stage
- subtype
- survival fields
- radiation therapy

### Sample Analytics

Output:

`data/processed/sample_analytics.csv`

Result:

- 1,084 rows
- 12 columns

Fields include:

- sample ID
- patient ID
- study ID
- sample type
- cancer type
- OncoTree code
- mutation count
- TMB
- fraction genome altered
- aneuploidy score
- MSI measures

---

# Day 4 — Mutation Data Ingestion and Profiling

## Goal

Retrieve and understand gene-level mutation data for the selected study.

---

## Mutation Profile

Molecular profile:

`brca_tcga_pan_can_atlas_2018_mutations`

Type:

`MUTATION_EXTENDED`

Datatype:

`MAF`

---

## Mutation Sample List

Selected:

`brca_tcga_pan_can_atlas_2018_sequenced`

This sample list represents samples profiled for mutation data.

Number of sequenced samples:

`1,066`

---

## API Trial and Correction

An initial GET mutation request was attempted.

The endpoint returned an error because:

`entrezGeneId`

was required.

This revealed that the GET endpoint was designed for querying specific genes.

The approach was corrected to use the POST mutation fetch endpoint:

`/api/molecular-profiles/{profile}/mutations/fetch`

This allowed mutation records to be retrieved across the sequenced cohort.

---

## Mutation Data Retrieval

Created:

`fetch_mutation_data.py`

Output:

`data/raw/mutation_data.json`

Result:

`84,226 mutation records`

---

## Mutation Profiling

Created:

`profile_mutation_data.py`

Results:

- 84,226 mutation records
- 1,009 unique samples
- 1,009 unique patients
- 16,488 unique genes

---

## Most Common Mutation Types

| Mutation Type | Records |
|---|---:|
| Missense Mutation | 64,473 |
| Frame Shift Deletion | 9,171 |
| Nonsense Mutation | 5,417 |
| Splice Site | 1,970 |
| Splice Region | 1,402 |
| Frame Shift Insertion | 913 |
| In Frame Deletion | 653 |
| Nonstop Mutation | 90 |
| Translation Start Site | 87 |
| In Frame Insertion | 50 |

---

## Mutation Coverage Validation

Created:

`validate_mutation_coverage.py`

Results:

- Sequenced samples: 1,066
- Samples with mutation records: 1,009
- Sequenced samples without mutation records: 57

Important distinction:

`sequenced sample ≠ sample with a mutation`

A sequenced sample can have zero returned mutation calls.

---

## Patient-Level Gene Frequency

Raw mutation-record count was initially used to rank genes.

This was improved because one patient can contribute multiple mutation records for the same gene.

Gene frequency was therefore calculated using unique:

`patientId + gene`

pairs.

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
| RYR2 | 66 |
| FLG | 66 |

Important lesson:

**Raw mutation records and patients with a mutation are different metrics.**

---

# Mutation Analytics Transformation

## Goal

Convert nested raw mutation JSON into a clean tabular dataset for analytical SQL.

Created:

`create_mutation_analytics.py`

Input:

`data/raw/mutation_data.json`

Output:

`data/processed/mutation_analytics.csv`

---

## Mutation Analytics Result

- 84,226 rows
- 19 columns
- 1,009 unique patients
- 1,009 unique samples
- 16,488 unique genes

Important fields include:

- `patientId`
- `sampleId`
- `studyId`
- `molecularProfileId`
- `gene`
- `entrezGeneId`
- `mutationType`
- `proteinChange`
- chromosome
- genomic position
- reference allele
- variant allele
- read counts

No aggregation was performed.

One row still represents one mutation record.

---

## Mutation Analytics Validation

Created:

`validate_mutation_analytics.py`

Results:

- Raw mutation records: 84,226
- Processed rows: 84,226
- Processed columns: 19
- Unique patients: 1,009
- Unique samples: 1,009
- Unique genes: 16,488

Critical missing-value checks:

- Missing `patientId`: 0
- Missing `sampleId`: 0
- Missing `gene`: 0
- Missing `mutationType`: 0

Row-count validation:

`PASSED`

---

# Day 5 — Google Cloud Storage Exploration

## Goal

Explore how the local BioData Copilot pipeline could integrate with Google Cloud.

---

## Google Cloud Setup

Google Cloud CLI was installed.

A Google account was authenticated.

A Google Cloud project was created.

Application Default Credentials were configured for local Python development.

---

## Authentication Learning

Three separate concepts became clearer.

### Authentication

Who are you?

### Authorization

What are you allowed to do?

### Application Logic

What operation should the program perform?

ADC handled authentication.

IAM controls authorization.

The Python SDK performs actions such as uploading files.

---

## Raw GCS Bucket

Created:

`biodata-copilot-haneefa-raw`

Configuration:

- Region: `asia-south1`
- Storage class: Standard
- Uniform bucket-level access enabled

---

## Raw Files Uploaded

Uploaded:

- `patient_clinical_data.json`
- `sample_clinical_data.json`
- `mutation_data.json`

Total uploaded size:

`106,711,324 bytes`

Approximately:

`101.77 MiB`

---

## Upload Validation

The local file sizes were compared with GCS.

Local total:

`106,711,324 bytes`

GCS total:

`106,711,324 bytes`

The sizes matched.

---

## Python GCS Integration

Installed:

`google-cloud-storage`

Created:

`upload_to_gcs.py`

The script demonstrated:

Python  
→ ADC authentication  
→ GCS client  
→ bucket  
→ blob/object  
→ upload

---

## Processed GCS Storage

A processed bucket was also created.

Processed files uploaded included:

- `patient_analytics.csv`
- `sample_analytics.csv`
- `mutation_analytics.csv`

Created:

`upload_processed_to_gcs.py`

---

# Architecture Reassessment

## Question

Does BioData Copilot actually require GCP for V1?

After reviewing the pipeline, the answer was:

**No.**

---

## Why

The current dataset is approximately:

- 100 MB raw
- 1,084 patients
- 84,226 mutation records

This data comfortably fits on a local machine.

Most ingestion, validation, profiling, and transformation already occur locally.

Using GCS and BigQuery as mandatory components would currently add infrastructure complexity without solving a real:

- scalability problem
- collaboration problem
- deployment problem
- availability requirement

---

## Decision

BioData Copilot V1 will use a local-first architecture.

Planned architecture:

cBioPortal  
→ Python ingestion  
→ Local raw data  
→ Validation and profiling  
→ Python transformation  
→ Processed analytical datasets  
→ DuckDB  
→ SQL analytics  
→ Verified results  
→ OpenAI  
→ User interface

---

## GCP Status

GCP is not being deleted from the project history.

The cloud work remains documented as:

**Cloud architecture exploration / optional Phase 2**

Possible future architecture:

cBioPortal  
→ Cloud-hosted ingestion  
→ GCS  
→ BigQuery  
→ SQL analytics  
→ deployed application

---

# Current Processed Data

The primary V1 analytical datasets are:

| Dataset | Rows | Purpose |
|---|---:|---|
| `patient_analytics.csv` | 1,084 | Patient clinical information |
| `sample_analytics.csv` | 1,084 | Sample/genomic summary information |
| `mutation_analytics.csv` | 84,226 | Mutation-level records |

Intermediate transformation datasets are also retained:

- `patient_clinical_wide.csv`
- `sample_clinical_wide.csv`

---

# Current Project Status

| Stage | Status |
|---|---|
| Project setup | ✅ |
| Dataset exploration | ✅ |
| Dataset selection | ✅ |
| Clinical ingestion | ✅ |
| Clinical profiling | ✅ |
| Clinical transformation | ✅ |
| Clinical validation | ✅ |
| Patient analytics | ✅ |
| Sample analytics | ✅ |
| Mutation ingestion | ✅ |
| Mutation profiling | ✅ |
| Mutation coverage validation | ✅ |
| Mutation analytics | ✅ |
| Mutation analytics validation | ✅ |
| GCP/GCS exploration | ✅ |
| Local analytical database | ⏳ |
| SQL modeling | ⏳ |
| AI explanation layer | ⏳ |
| User interface | ⏳ |

---

# Next Step

Introduce DuckDB as the local analytical database.

Planned next steps:

1. install DuckDB,
2. create the local database,
3. load `patient_analytics.csv`,
4. load `sample_analytics.csv`,
5. load `mutation_analytics.csv`,
6. validate table row counts,
7. begin SQL analytical modeling,
8. create reusable analytical tables/views,
9. connect verified SQL results to the LLM explanation layer.

# DuckDB Analytical Layer

## Goal

Introduce a local SQL analytical database and begin combining clinical and mutation data.

DuckDB was selected because the current dataset is small enough to process comfortably on a single machine and the project mainly requires analytical SQL rather than transactional database features.

---

## DuckDB Setup

Installed:

`duckdb`

Created local database:

`data/biodata.duckdb`

The database file is generated locally and excluded from Git.

The following processed datasets were loaded:

| Table | Rows | Grain |
|---|---:|---|
| `patient_analytics` | 1,084 | One row per patient |
| `sample_analytics` | 1,084 | One row per sample |
| `mutation_analytics` | 84,226 | One row per mutation record |

---

## Table Grain Validation

### Patient Table

- Total rows: 1,084
- Unique patients: 1,084
- Duplicate patient IDs: 0

Grain:

`1 row = 1 patient`

### Sample Table

- Total rows: 1,084
- Unique samples: 1,084
- Duplicate sample IDs: 0

Grain:

`1 row = 1 sample`

### Mutation Table

- Total mutation rows: 84,226
- Unique patients: 1,009
- Unique samples: 1,009

Grain:

`1 row = 1 mutation record`

---

## Patient–Sample Join

Joining patient and sample data using `patientId` produced:

`1,084 rows`

This confirms the observed one-to-one patient/sample relationship for the selected study.

---

## Radiation Therapy Field

DuckDB inferred `RADIATION_THERAPY` as a Boolean field.

Observed values:

- True: 549
- False: 434
- Missing: 101

Missing values were retained rather than being interpreted as False.

---

## First SQL Analysis

Initial SQL queries calculated:

- total patient count
- patient distribution by subtype
- average age by subtype
- most frequently mutated genes
- mutation-type distribution

### Patient Distribution by Subtype

| Subtype | Patients |
|---|---:|
| BRCA_LumA | 499 |
| BRCA_LumB | 197 |
| BRCA_Basal | 171 |
| Missing | 103 |
| BRCA_Her2 | 78 |
| BRCA_Normal | 36 |

---

## Most Frequently Mutated Genes

Patient-level mutation frequency used:

`COUNT(DISTINCT patientId)`

rather than raw mutation-row count.

Top examples:

| Gene | Patients |
|---|---:|
| TP53 | 347 |
| PIK3CA | 347 |
| TTN | 187 |
| CDH1 | 130 |
| GATA3 | 127 |

This reproduced the earlier Python profiling results and confirmed that the DuckDB analytical layer preserved the expected data.

---

## Patient–Gene Analytical Model

Created:

`patient_gene_mutations`

Grain:

`1 row = 1 patient + 1 mutated gene`

The model combines:

- patient subtype
- patient ID
- mutated gene

Duplicate patient/gene mutation records are removed using `DISTINCT`.

Result:

- 76,407 patient-gene rows
- 981 unique patients with known subtype

---

## Subtype–Gene Mutation Summary

Created:

`subtype_gene_mutation_summary`

Grain:

`1 row = 1 subtype + 1 gene`

The model stores the number of patients in each subtype with a mutation in each gene.

---

## Mutation Prevalence by Subtype

Raw mutation counts were converted into percentages because subtype sizes differ.

Examples:

| Subtype | Gene | Mutated Patients | Subtype Patients | Prevalence |
|---|---|---:|---:|---:|
| BRCA_Basal | TP53 | 153 | 171 | 89.47% |
| BRCA_Her2 | TP53 | 55 | 78 | 70.51% |
| BRCA_LumA | PIK3CA | 237 | 499 | 47.49% |
| BRCA_LumB | TP53 | 71 | 197 | 36.04% |
| BRCA_Normal | TP53 | 11 | 36 | 30.56% |

These values describe the selected dataset and should not automatically be generalized beyond it.

---

## Mutation Burden by Subtype

Patient and sample tables were joined to compare TMB and mutation count across subtypes.

| Subtype | Avg TMB | Median TMB | Avg Mutation Count | Median Mutation Count |
|---|---:|---:|---:|---:|
| BRCA_Basal | 3.35 | 2.37 | 96.36 | 66 |
| BRCA_Her2 | 5.50 | 2.42 | 163.28 | 71 |
| BRCA_LumA | 2.54 | 1.03 | 72.13 | 30 |
| BRCA_LumB | 2.54 | 1.67 | 74.95 | 48 |
| BRCA_Normal | 1.93 | 1.28 | 57.33 | 38 |

The difference between average and median, particularly for HER2, shows the effect of high-value observations on the mean.

Therefore, both average and median are useful when describing mutation burden.

---

## Key Lessons

- Table grain must be understood before performing joins.
- Patient counts and mutation-row counts represent different things.
- `COUNT(DISTINCT patientId)` is required for patient-level mutation frequency.
- Raw counts should not be compared across groups of very different sizes without context.
- Percentages allow more meaningful subtype comparisons.
- Average values can be strongly influenced by outliers.
- Median values provide a useful complementary measure.
- SQL is now being used for analytical modeling rather than repeating Python transformations.