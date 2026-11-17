# BioData Copilot — Design Decisions

This document records the main technical and architectural decisions behind BioData Copilot V1.

The goal is to explain not only what technologies were used, but why they were appropriate for the problem.

---

## 1. Use cBioPortal as the biomedical data source

### Decision

Use the cBioPortal REST API as the primary biomedical data source.

### Why

cBioPortal provides:

- public cancer studies,
- structured clinical data,
- mutation data,
- molecular profiles,
- REST API access,
- study metadata.

It allows the project to work with real biomedical data without requiring access to private clinical records.

---

## 2. Select the dataset using data coverage rather than choosing a disease arbitrarily

### Decision

Explore available studies before selecting the final dataset.

### Why

The largest study is not necessarily the most suitable study.

Candidate studies were compared using:

- sample size,
- clinical attributes,
- molecular profiles,
- study scope,
- degree of specialization.

The selected study was:

`brca_tcga_pan_can_atlas_2018`

because it provides broad clinical and molecular coverage while still supporting a manageable V1 scope.

---

## 3. Limit V1 to clinical and mutation data

### Decision

Use only:

1. clinical data,
2. mutation data.

### Why

The selected study also contains:

- gene expression,
- methylation,
- protein data,
- copy-number alterations,
- structural variants.

Including every available molecular profile would increase complexity without being necessary for the initial analytical questions.

Additional molecular profiles should only be introduced when they support a clear analytical or research requirement.

---

## 4. Preserve the original API responses

### Decision

Store raw API responses before transformation.

### Why

Raw data provides:

- traceability,
- reproducibility,
- debugging capability,
- the ability to rebuild processed datasets.

Transformation errors can therefore be investigated against the original source.

---

## 5. Use Python for ingestion and structural transformation

### Decision

Use Python and pandas for:

- REST API ingestion,
- JSON parsing,
- long-to-wide transformation,
- nested mutation-data flattening,
- creation of processed analytical datasets.

### Why

The source data is semi-structured and contains nested JSON.

Python provides a flexible way to prepare this data before analytical SQL is applied.

---

## 6. Make table grain explicit before performing joins

### Decision

Define the grain of each analytical table.

The main tables are:

```text
patient_analytics
1 row = 1 patient

sample_analytics
1 row = 1 sample

mutation_analytics
1 row = 1 mutation record
```

### Why

Different table grains can cause incorrect counts when data is joined.

For example, one patient can have multiple mutation records.

Therefore:

`COUNT(*)`

and:

`COUNT(DISTINCT patientId)`

can answer very different questions.

Understanding grain is required before interpreting analytical results.

---

## 7. Use DuckDB as the V1 analytical database

### Decision

Use DuckDB instead of a managed cloud warehouse.

### Why

The current dataset contains approximately:

- 1,084 patients,
- 84,226 mutation records,
- around 100 MB of raw data.

This workload fits comfortably on a single machine.

DuckDB provides:

- analytical SQL,
- joins,
- aggregations,
- CSV integration,
- a lightweight local database,

without requiring database-server or cloud infrastructure.

---

## 8. Use SQL for deterministic analytical calculations

### Decision

Use reviewed SQL queries to calculate dataset-specific results.

Examples include:

- patient counts,
- subtype distribution,
- mutation prevalence,
- gene frequency,
- mutation burden,
- data completeness.

### Why

SQL makes analytical logic:

- explicit,
- reproducible,
- reviewable,
- independently verifiable.

For the same input data and query, the database produces the same analytical result.

---

## 9. Use the LLM for explanation rather than numerical computation

### Decision

Calculate analytical results before sending information to the LLM.

The application flow is:

```text
User Question
      ↓
Reviewed SQL
      ↓
DuckDB
      ↓
Verified Result
      ↓
OpenAI
      ↓
Natural-language Explanation
```

### Why

Biomedical analysis can involve:

- duplicate records,
- different table grains,
- missing values,
- ambiguous denominators,
- joins across multiple tables.

These calculations are handled by explicit analytical logic rather than delegated entirely to the language model.

The LLM is responsible for explaining the verified result clearly.

---

## 10. Use predefined analytical questions in V1

### Decision

Map each supported user question to a reviewed SQL query.

### Why

V1 prioritizes:

- correctness,
- reproducibility,
- clear analytical scope.

Unrestricted natural-language-to-SQL would introduce additional uncertainty and is not necessary for the initial version.

It remains a possible future research direction.

---

## 11. Preserve missing values and investigate outliers before modifying them

### Decision

Do not automatically:

- fill missing biomedical values,
- remove unusual observations.

### Why

A missing value does not necessarily mean `False` or `0`.

Similarly, an extreme value is not automatically an error.

For example, very high mutation counts were accompanied by correspondingly high TMB values, so they were retained rather than automatically removed.

---

## 12. Convert stable data-quality expectations into automated tests

### Decision

Use pytest for stable pipeline checks instead of maintaining many one-off validation scripts.

### Current Checks

Tests currently verify:

- expected table sizes,
- patient ID uniqueness,
- sample ID uniqueness,
- patient/sample consistency,
- completeness of critical mutation fields,
- expected mutation patient/sample counts.

### Why

Exploratory profiling is useful while understanding a dataset.

Once expectations become stable, automated pass/fail tests provide a cleaner and more maintainable implementation.

---

## 13. Keep V1 local-first

### Decision

Do not make cloud infrastructure mandatory for V1.

### Why

Google Cloud Storage and BigQuery were successfully explored during development.

However, most ingestion and transformation already occur locally, and the current data volume does not require managed cloud infrastructure.

Adding cloud services solely for portfolio breadth would increase complexity without solving a current engineering requirement.

A future deployed version could use:

```text
cBioPortal
→ Cloud-hosted ingestion
→ GCS
→ BigQuery
→ SQL analytics
→ AI explanation
→ deployed application
```

Cloud infrastructure remains an extension rather than a requirement.

---

## 14. Keep the UI intentionally lightweight

### Decision

Use Streamlit as a thin presentation layer.

### Why

BioData Copilot is primarily a data and AI project rather than a frontend project.

The UI only needs to allow users to:

- select a supported analytical question,
- view the verified SQL result,
- view the AI explanation.

This keeps development effort focused on the data pipeline, analytical logic, and trustworthy-AI design.

---

# Engineering Principle

The main architectural principle behind BioData Copilot is:

> **Choose technology because it solves a requirement, not because it looks impressive in the technology stack.**

The project therefore favors:

- explicit data grain,
- reproducible transformations,
- reviewed SQL,
- automated tests,
- grounded AI explanations,
- and a deliberately simple architecture.