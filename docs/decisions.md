# BioData Copilot — Decisions

## 1. Use `uv`

### Decision

Use `uv` for Python project and dependency management.

### Why

It provides:

- dependency management
- virtual environments
- `pyproject.toml`
- reproducible `uv.lock`

---

## 2. Build locally before publishing to GitHub

### Decision

Develop and test the project locally first.

### Why

The project can be cleaned, tested, and documented before publication.

Git is still used locally for version control.

---

## 3. Keep Python simple first

### Decision

Prefer simple and explicit Python during the initial implementation.

### Why

The project is also being used to strengthen Python fundamentals.

Development approach:

Simple code  
→ Understand it  
→ Test it  
→ Find repetition  
→ Refactor later

---

## 4. Use cBioPortal

### Decision

Use cBioPortal as the biomedical data source.

### Why

It provides:

- public cancer studies
- REST APIs
- clinical data
- genomic data
- structured study metadata

---

## 5. Do not choose a cancer type randomly

### Decision

Compare available studies before selecting the dataset.

### Why

The dataset should be chosen based on actual data coverage rather than personal preference.

---

## 6. Group studies by cancer family

### Problem

Related cancer types appeared under different identifiers.

Example:

`brca → breast → tissue`

### Decision

Follow the cBioPortal cancer-type hierarchy to group specific cancer types into broader families.

---

## 7. Do not select a study only by sample size

### Why

Large studies may be highly specialised.

Examples inspected:

- Lung MSK study — metastatic organotropism focus
- Pancreas MSK study — KRAS-focused
- Breast TCGA PanCancer Atlas — broad clinical and molecular coverage

---

## 8. Selected dataset

Study ID:

`brca_tcga_pan_can_atlas_2018`

### Why

It provides broad:

- demographic information
- tumour stage
- molecular subtype
- survival data
- mutation data
- gene expression
- copy-number information
- methylation
- protein information
- structural variants

This makes it suitable for a general biomedical data exploration platform.

---

## 9. Limit V1 data scope

### Decision

Initially use:

1. Clinical data
2. Mutation data

### Why

The selected study contains many additional molecular profiles, but using everything in V1 would unnecessarily increase project complexity.

---

## 10. Separate facts from interpretation

### Decision

Use deterministic SQL/database operations to calculate numerical results.

Use the LLM only to explain those verified results.

### Rule

Observed association does not automatically imply:

- causation
- diagnosis
- prognosis
- treatment recommendation

---

## 11. Preserve raw source data

### Decision

Keep the original API responses before transformation.

### Why

Raw data allows:

- traceability
- debugging
- rebuilding processed datasets
- checking whether transformation logic introduced errors

---

## 12. Use Python for structural biomedical-data preparation

### Decision

Use Python and pandas for:

- API ingestion
- JSON handling
- validation
- profiling
- long-to-wide transformation
- nested mutation-data flattening
- creation of processed analytical datasets

### Why

Python is well suited to working with nested API responses and biomedical data structures.

---

## 13. Use SQL for analytical modeling

### Decision

After processed datasets are loaded into the analytical database, use SQL for:

- joins
- aggregations
- mutation-frequency calculations
- subtype summaries
- patient-level analytical models
- final application-facing results

### Why

This creates a clear separation between structural data preparation and analytical modeling.

---

## 14. Use a local-first architecture for V1

### Decision

Use DuckDB as the analytical database for V1 instead of requiring BigQuery.

### Why

The current dataset is small:

- approximately 100 MB of raw data
- 1,084 patients
- 84,226 mutation records

The dataset can comfortably be processed on a single machine.

Using a managed cloud warehouse would currently add infrastructure complexity without solving a real scale or collaboration problem.

---

## 15. Do not force GCP into the core architecture

### Decision

GCP is treated as an explored deployment option rather than a required V1 component.

### Why

The initial pipeline performs ingestion and transformation locally.

Uploading already-processed local data to cloud services solely to demonstrate GCP would not materially improve the current project.

Technology should be selected because it solves a requirement, not simply because it is available.

---

## 16. Retain the GCP work as a Phase 2 option

### Work Completed

The project successfully tested:

- Google Cloud CLI
- Google Cloud project setup
- Application Default Credentials
- GCS raw bucket
- GCS processed bucket
- Python GCS uploads
- raw and processed file storage

### Future Use

If BioData Copilot is deployed or scaled later, the architecture could evolve to:

cBioPortal  
→ cloud-hosted ingestion  
→ GCS  
→ BigQuery  
→ SQL analytics  
→ deployed application

---

## 17. Use Application Default Credentials for local GCP experimentation

### Decision

Use ADC instead of storing service-account keys inside the repository.

### Why

Google Cloud libraries can discover local credentials automatically without hardcoding secrets into the application.

---

## 18. Use `asia-south1` for GCP experimentation

### Decision

Cloud Storage resources created during the GCP exploration use:

`asia-south1`

### Why

The resources were created for development from India and colocating related cloud services would simplify a future cloud architecture.