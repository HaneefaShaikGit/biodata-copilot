# BioData Copilot — Development Journey

This document summarizes how BioData Copilot evolved from an initial biomedical-data idea into a working analytics and grounded-AI application.

It focuses on the important technical decisions, mistakes, discoveries, and lessons rather than documenting every command used during development.

---

# 1. Project Idea

BioData Copilot started with a simple goal:

> Build a biomedical data platform that combines Data Engineering, cancer genomics, SQL analytics, and AI explanations.

The core principle was established early:

> **The database calculates facts. The LLM explains verified facts.**

The aim was not to use an LLM as a replacement for analytical computation.

Instead, the project would separate:

```text
Data ingestion
      ↓
Transformation
      ↓
Analytical computation
      ↓
Verified result
      ↓
AI explanation
```

---

# 2. Dataset Exploration

The first step was understanding what data was available through cBioPortal.

The public API returned more than 550 cancer studies.

An early approach searched for studies using keywords such as:

`breast`

This was rejected because choosing a dataset based only on a keyword or familiarity would be arbitrary.

Instead, the study-selection process became data-driven.

Studies were grouped into broader cancer families using the cBioPortal cancer-type hierarchy.

One important discovery was that related cancer types can appear under different identifiers.

Example:

`brca → breast → tissue`

This required following the hierarchy rather than treating every cancer-type ID as unrelated.

---

# 3. Candidate Study Comparison

Several large studies were compared using:

- sample size,
- clinical attributes,
- molecular profiles,
- survival information,
- study scope,
- degree of specialization.

Representative candidates included:

### Lung

`luad_mskcc_2023_met_organotropism`

Strengths:

- rich clinical data,
- survival data,
- mutation data,
- metastatic-site information.

Limitation:

The study is strongly focused on metastatic organotropism.

---

### Pancreas

`pdac_msk_2024`

Strengths:

- clinical data,
- survival,
- mutation information,
- TMB and MSI.

Limitation:

Many fields are strongly focused on KRAS biology.

---

### Breast

`brca_tcga_pan_can_atlas_2018`

Strengths:

- broad clinical information,
- tumour stage,
- subtype,
- survival,
- mutation data,
- copy-number data,
- gene expression,
- methylation,
- protein information,
- structural variants.

This study provided the best balance between breadth and flexibility.

---

# 4. Dataset Selection

The final study selected was:

`brca_tcga_pan_can_atlas_2018`

Breast Invasive Carcinoma — TCGA PanCancer Atlas.

The decision was not based on having the largest sample count.

It was selected because it provides broad clinical and molecular information without forcing the project into one narrow biological question.

To keep V1 manageable, only two domains were used:

1. clinical data,
2. mutation data.

---

# 5. Clinical Data Ingestion

Clinical records were retrieved separately at:

- patient level,
- sample level.

The API returned long-format records such as:

```text
patientId | clinicalAttributeId | value
```

Raw outputs included:

```text
patient_clinical_data.json
sample_clinical_data.json
```

Observed counts:

### Patient data

- 41,497 raw records,
- 1,084 unique patients,
- 40 clinical attributes.

### Sample data

- 19,348 raw records,
- 1,084 unique samples,
- 18 clinical attributes.

---

# 6. Patient–Sample Relationship

The selected study contained:

- 1,084 patients,
- 1,084 samples,
- 0 patients with multiple samples.

Observed relationship:

```text
1 patient → 1 sample
```

Both identifiers were still retained because this relationship is not guaranteed in other biomedical datasets.

This became an early lesson in understanding **data grain before performing joins**.

---

# 7. Clinical Transformation

Clinical API data was transformed from long format:

```text
patientId | clinicalAttributeId | value
```

into wide analytical structures such as:

```text
patientId | AGE | SEX | RACE | SUBTYPE | OS_MONTHS | ...
```

Intermediate outputs were created for traceability:

```text
patient_clinical_wide.csv
sample_clinical_wide.csv
```

Final clinical analytics datasets became:

```text
patient_analytics.csv
sample_analytics.csv
```

Resulting dimensions:

### Patient analytics

- 1,084 rows,
- 17 columns.

### Sample analytics

- 1,084 rows,
- 12 columns.

---

# 8. Data Profiling Lessons

Exploratory profiling was used to inspect:

- missing values,
- duplicate entity/attribute pairs,
- data types,
- categorical values,
- numerical distributions,
- possible outliers.

Two important lessons emerged.

## Missing does not mean false

Missing biomedical values were preserved unless there was a justified reason to transform them.

## Outlier does not mean error

Some samples showed unusually high mutation counts.

These observations also had correspondingly high TMB values.

Because the values were internally consistent, they were retained instead of being automatically removed.

---

# 9. Mutation Data Ingestion

Mutation data required a different cBioPortal API pattern.

An initial GET request failed because it required:

`entrezGeneId`

This revealed that the endpoint was designed for retrieving mutations for specific genes.

To retrieve mutations across the full sequenced cohort, the POST mutation fetch endpoint was used.

Mutation profile:

`brca_tcga_pan_can_atlas_2018_mutations`

Sample list:

`brca_tcga_pan_can_atlas_2018_sequenced`

Result:

`84,226 mutation records`

---

# 10. Mutation Coverage

The mutation sample list contained:

`1,066 sequenced samples`

Mutation records were returned for:

`1,009 samples`

Therefore:

`57 sequenced samples`

had no returned mutation records.

This produced an important distinction:

> **Sequenced sample ≠ sample with a mutation record**

A sequenced sample may have no called mutation.

---

# 11. Patient-Level Gene Frequency

An early mutation ranking used raw mutation-row counts.

This was corrected because a single patient can contribute multiple mutation records for the same gene.

Patient-level gene frequency therefore uses unique:

```text
patientId + gene
```

combinations.

Examples:

| Gene | Patients |
|---|---:|
| TP53 | 347 |
| PIK3CA | 347 |
| TTN | 187 |
| CDH1 | 130 |
| GATA3 | 127 |

This became another important grain lesson:

> **Mutation rows and patients with a mutation are different measures.**

---

# 12. Mutation Analytics Transformation

Nested mutation JSON was flattened into:

`mutation_analytics.csv`

Result:

- 84,226 rows,
- 19 columns,
- 1,009 unique patients,
- 1,009 unique samples,
- 16,488 genes.

The transformation preserved one row per mutation record.

Critical fields such as:

- `patientId`,
- `sampleId`,
- `gene`,
- `mutationType`

contained no missing values.

---

# 13. Cloud Architecture Exploration

Google Cloud was explored during development.

The project successfully tested:

- Google Cloud CLI,
- Google Cloud project setup,
- Application Default Credentials,
- Google Cloud Storage,
- raw-data upload,
- processed-data upload,
- Python GCS integration.

This helped clarify the difference between:

### Authentication

Who are you?

### Authorization

What are you allowed to do?

### Application logic

What operation should the program perform?

---

# 14. Architecture Reassessment

After the GCP experiment, the architecture was reconsidered.

The dataset contains approximately:

- 1,084 patients,
- 84,226 mutation records,
- around 100 MB of raw data.

This workload comfortably fits on one machine.

Most ingestion and transformation already happened locally.

Making GCS and BigQuery mandatory would therefore add infrastructure complexity without solving a current:

- scale problem,
- availability problem,
- collaboration problem,
- deployment requirement.

The V1 architecture was changed to local-first.

This led to an important engineering principle:

> **Problem → Requirements → Architecture → Technology**

rather than:

> **Technology → Find somewhere to use it**

---

# 15. DuckDB Analytical Layer

DuckDB was selected as the V1 analytical database.

Three processed datasets were loaded:

| Table | Rows | Grain |
|---|---:|---|
| `patient_analytics` | 1,084 | One row per patient |
| `sample_analytics` | 1,084 | One row per sample |
| `mutation_analytics` | 84,226 | One row per mutation record |

DuckDB provided:

- analytical SQL,
- joins,
- aggregations,
- local execution,
- no database server requirement.

---

# 16. Understanding Table Grain

Table grain became one of the most important lessons in the project.

```text
patient_analytics
1 row = 1 patient

sample_analytics
1 row = 1 sample

mutation_analytics
1 row = 1 mutation
```

This means:

```text
Patient
   |
   | 1 : 1
   v
Sample

Patient
   |
   | 1 : many
   v
Mutation records
```

Failing to understand these relationships could produce inflated counts after joins.

---

# 17. SQL Analytical Questions

The SQL layer was reduced to five official V1 questions.

1. How are patients distributed across breast-cancer subtypes?
2. Which genes are most frequently mutated?
3. Which genes are most frequently mutated within each subtype?
4. How does mutation burden differ across subtypes?
5. How complete are important clinical fields?

Each question maps to a reviewed SQL query.

---

# 18. Example Analytical Findings

## Patient Subtype Distribution

| Subtype | Patients | Percentage |
|---|---:|---:|
| LumA | 499 | 46.03% |
| LumB | 197 | 18.17% |
| Basal | 171 | 15.77% |
| Unknown | 103 | 9.50% |
| HER2 | 78 | 7.20% |
| Normal | 36 | 3.32% |

---

## Mutation Prevalence by Subtype

Examples from the selected dataset:

| Subtype | Gene | Prevalence |
|---|---|---:|
| Basal | TP53 | 89.47% |
| HER2 | TP53 | 70.51% |
| LumA | PIK3CA | 47.49% |
| LumB | TP53 | 36.04% |

Raw counts were converted to percentages because subtype populations differ in size.

---

# 19. Mean vs Median

Mutation burden analysis revealed large differences between mean and median values.

Example for HER2:

```text
Average mutation count = 163.28
Median mutation count  = 71
```

This suggests that high-value observations influence the mean.

Therefore, both mean and median are reported when describing mutation burden.

---

# 20. Grounded AI Layer

The next step was adding natural-language explanation.

The system does not ask the LLM to calculate dataset statistics.

Instead:

```text
User question
      ↓
Reviewed SQL
      ↓
DuckDB
      ↓
Verified result
      ↓
OpenAI
      ↓
Natural-language explanation
```

The LLM receives only:

- the selected question,
- the verified SQL output.

Prompt rules instruct the model to:

- not invent numbers,
- describe only the selected dataset,
- avoid causal claims,
- avoid diagnosis,
- avoid treatment recommendations.

---

# 21. Streamlit Interface

A small Streamlit interface was added to demonstrate the full pipeline.

The user can:

1. select one of the five supported questions,
2. run the SQL analysis,
3. view the verified result,
4. view the grounded AI explanation.

The UI was deliberately kept simple because the project focus is:

- biomedical data,
- data engineering,
- analytical modeling,
- trustworthy AI,

rather than frontend development.

---

# 22. Refactoring V1

During portfolio preparation, the repository was significantly simplified.

Early exploratory scripts were either:

- removed,
- merged,
- moved under `scripts/`,
- or converted into automated tests.

Examples include:

### Before

Multiple scripts for:

- profiling,
- schema inspection,
- table validation,
- mutation validation,
- SQL experimentation.

### After

A smaller structure centered around:

```text
ingestion/
transformation/
database/
ai/
sql/questions/
tests/
```

Stable data-quality expectations were converted into pytest tests.

The cleaned test suite currently verifies:

- expected dataset sizes,
- patient uniqueness,
- sample uniqueness,
- patient/sample consistency,
- completeness of critical mutation fields,
- mutation patient/sample counts.

---

# 23. Current V1 Architecture

```text
cBioPortal
    ↓
Python ingestion
    ↓
Raw JSON
    ↓
Python / pandas transformation
    ↓
Processed analytical datasets
    ↓
DuckDB
    ↓
Reviewed SQL questions
    ↓
Verified analytical result
    ↓
OpenAI explanation
    ↓
Streamlit
```

---

# 24. Key Lessons

The most important lessons from V1 were:

1. The largest dataset is not automatically the best dataset.
2. More columns do not automatically mean better data.
3. Preserve source data before transformation.
4. Missing does not automatically mean false.
5. An outlier does not automatically mean an error.
6. Table grain must be understood before joins.
7. `COUNT(*)` and `COUNT(DISTINCT patientId)` answer different questions.
8. Mutation records are not equivalent to mutated patients.
9. Raw counts should not be compared across groups of different sizes without context.
10. Mean and median can describe very different distributions.
11. Python is useful for semi-structured data preparation.
12. SQL is useful for deterministic analytical logic.
13. Stable expectations should become automated tests.
14. An LLM does not need to perform calculations that a database can perform deterministically.
15. Cloud infrastructure should only be introduced when it solves a real requirement.
16. A portfolio project benefits from removing exploratory clutter once the learning phase is complete.

---

# 25. Future Research Direction

V1 answers a practical engineering question:

> Can a biomedical analytics application separate deterministic computation from AI explanation?

A possible V2 would move toward a research-oriented question:

> **Can provenance-aware evidence constraints reduce scientific overclaiming in LLM explanations of structured cancer-genomics analyses?**

Potential evaluation dimensions include:

- numerical fidelity,
- unsupported claims,
- causal overreach,
- clinical overreach,
- appropriate abstention,
- provenance completeness.

This would extend BioData Copilot from a working data product into an experimental framework for trustworthy biomedical AI.