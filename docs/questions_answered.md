# BioData Copilot — Questions Answered

## Project Questions

### What are we building?

A biomedical data platform that retrieves, validates, transforms, analyzes, and explains public biomedical data.

---

### What is the core principle of the project?

The database calculates facts.

The LLM explains verified facts.

The LLM should not be the source of numerical truth.

---

### What should the LLM do?

The LLM should explain verified analytical results in understandable language.

---

### What should the LLM not do?

The LLM should not invent:

- patient counts
- mutation frequencies
- diagnoses
- clinical outcomes
- treatment recommendations
- unsupported biological conclusions
- causal conclusions that are not supported by the data

---

### Why are we using Python?

Python is used for:

- API ingestion
- JSON processing
- validation
- profiling
- nested biomedical data handling
- structural transformation
- preparation of analytical datasets

---

### Why are we using SQL as well as Python?

Python is useful for handling semi-structured source data.

SQL is better suited to:

- joins
- aggregations
- analytical summaries
- reusable data models
- application-facing query logic

The project intentionally uses both.

---

## Architecture Questions

### Why preserve raw data?

Raw data is preserved so that:

- transformations can be reproduced
- errors can be investigated
- processed datasets can be rebuilt
- source data remains traceable
- transformation logic can be validated

---

### Why do we have raw, wide, and analytics datasets?

Each layer has a different purpose.

Raw:

- preserves the original API response

Wide:

- converts long clinical records into a structured tabular format

Analytics:

- contains only the fields required for BioData Copilot V1

This gives the project traceability without forcing every intermediate dataset into the final application.

---

### Why are we using DuckDB?

The current dataset is small enough to run comfortably on one machine.

DuckDB provides:

- SQL
- joins
- aggregations
- analytical tables
- local execution
- no database server setup

This makes it suitable for the V1 analytical layer.

---

### Why not use Spark?

The current dataset is approximately 100 MB.

Distributed processing would add unnecessary complexity for data that fits comfortably on a single machine.

---

## Cloud Architecture Questions

### Is GCP required for BioData Copilot V1?

No.

The current dataset can comfortably be processed locally.

GCP was explored but is not required for the core V1 architecture.

---

### Why did we explore GCP?

To understand and test:

- Google Cloud project setup
- Google Cloud Storage
- authentication
- authorization
- IAM concepts
- Application Default Credentials
- Python Google Cloud SDK usage
- raw and processed cloud storage

---

### What is authentication?

Authentication answers:

`Who are you?`

Example:

Google verifies which identity is making a request.

---

### What is authorization?

Authorization answers:

`What are you allowed to do?`

In Google Cloud, IAM helps control authorization.

---

### What is IAM?

IAM stands for Identity and Access Management.

It connects:

- an identity
- a role
- a resource

Example:

A user or service account may be given permission to upload objects to a Cloud Storage bucket.

---

### What is ADC?

ADC stands for Application Default Credentials.

It provides a standard way for Google Cloud client libraries to discover available credentials.

During local development, ADC allowed Python to authenticate using the locally authenticated Google identity without storing service-account keys inside the repository.

---

### Did ADC upload the files automatically?

No.

ADC handled authentication.

The Python script performed the upload.

Conceptually:

Python  
→ ADC identifies the user  
→ IAM checks permissions  
→ Python uploads the file

---

### Why not keep a service-account JSON file inside the project?

A service-account key is a long-lived secret.

It would need to be:

- protected
- excluded from Git
- rotated if exposed

ADC allowed local development without storing such a key inside the repository.

---

### Why was GCP removed from the core V1 architecture?

Most ingestion and transformation already happened locally.

Uploading already-processed local files to cloud services did not currently solve a real:

- scale problem
- deployment problem
- collaboration problem
- availability requirement

Therefore, making GCS and BigQuery mandatory would add complexity without enough benefit.

---

### Was the GCP work wasted?

No.

The project successfully demonstrated:

- GCP project setup
- Cloud Storage
- CLI usage
- ADC
- Python Cloud Storage integration
- raw and processed cloud storage

This work can support a future cloud deployment.

---

### When would GCP become useful?

GCP would become more useful if the project later requires:

- hosted execution
- scheduled ingestion
- centralized storage
- multiple users
- larger datasets
- production deployment
- managed analytical infrastructure

A possible future architecture could be:

cBioPortal  
→ Cloud Run  
→ GCS  
→ BigQuery  
→ SQL analytics  
→ deployed application

---

## Data Source Questions

### Where does the data come from?

cBioPortal.

---

### How is the data accessed?

Using the cBioPortal REST API.

---

### What format is returned?

JSON.

---

### Did the API require an API key?

The public cBioPortal endpoints used in this project did not require an API key.

---

## Dataset Selection Questions

### How many studies were found?

Approximately 550 studies were returned from cBioPortal.

---

### Why did we not immediately choose breast cancer?

The dataset needed to be selected using actual data availability rather than choosing a cancer type arbitrarily.

---

### Why did we group cancer types?

Related cancer types can use different identifiers.

Example:

`brca → breast → tissue`

Grouping by hierarchy gave a more accurate view of available studies by cancer family.

---

### Why was sample size not enough to choose a dataset?

A large dataset may still be highly specialised.

Examples inspected included:

- Lung MSK — metastatic organotropism focus
- Pancreas MSK — KRAS-focused
- Breast TCGA PanCancer Atlas — broad clinical and molecular coverage

---

### Which dataset was selected?

`brca_tcga_pan_can_atlas_2018`

Breast Invasive Carcinoma — TCGA PanCancer Atlas.

---

### Why was it selected?

It contains broad:

- demographic data
- tumour stage
- subtype information
- survival data
- mutation data
- gene expression
- copy-number information
- methylation
- protein information
- structural variants

This makes it suitable for a general biomedical exploration platform.

---

## Clinical Data Questions

### How many patient-level clinical records were retrieved?

41,497 records.

---

### How many sample-level clinical records were retrieved?

19,348 records.

---

### How many unique patients are present?

1,084.

---

### How many unique samples are present?

1,084.

---

### Do patients have multiple samples?

No patient had more than one sample in the retrieved clinical dataset.

Observed relationship:

`1 patient → 1 sample`

---

### Why does that relationship matter?

It simplifies joins between:

- patient data
- sample data
- mutation data

However, the project still keeps both patient and sample identifiers because other biomedical datasets may not follow a one-to-one relationship.

---

### Were duplicate patient-attribute records found?

No.

There were:

- 0 duplicate patient-attribute pairs
- 0 duplicate sample-attribute pairs

---

### Is every clinical field complete?

No.

Patient-level fields have varying completeness.

Sample-level fields are generally more complete.

Missing values are preserved unless there is a justified reason to transform them.

---

### Why were missing values not automatically filled?

A missing biomedical value may have clinical or data-collection meaning.

Filling values without evidence could introduce false information.

---

### Why were unusual values not automatically removed?

An outlier is not automatically an error.

For example, very high mutation counts were also associated with very high TMB values.

Because the values were internally consistent, they were retained.

---

## Mutation Data Questions

### Which mutation profile was used?

`brca_tcga_pan_can_atlas_2018_mutations`

---

### Which sample list was used?

`brca_tcga_pan_can_atlas_2018_sequenced`

---

### Why was the POST mutation endpoint used?

The normal GET mutation endpoint required an `entrezGeneId`.

The project needed mutation records across the full sequenced cohort.

Therefore, the POST fetch endpoint was used.

---

### How many mutation records were retrieved?

84,226 mutation records.

---

### How many patients have at least one mutation record?

1,009 patients.

---

### How many samples have at least one mutation record?

1,009 samples.

---

### How many unique genes are represented?

16,488 genes.

---

### How many samples were listed as sequenced?

1,066 samples.

---

### Why do only 1,009 sequenced samples have mutation records?

A sample can be sequenced without having a returned mutation call.

Therefore:

`sequenced sample ≠ sample with a mutation`

There were:

- 1,066 sequenced samples
- 1,009 samples with mutation records
- 57 sequenced samples with no returned mutation record

---

### What is the most common mutation type in the dataset?

`Missense_Mutation`

There were 64,473 missense mutation records.

---

### Why count mutated genes by patient rather than by raw mutation rows?

One patient can have multiple mutation records for the same gene.

For a question such as:

"How many patients have a TP53 mutation?"

the correct measure should use unique:

`patientId + gene`

pairs.

---

### Which genes were most frequently mutated by patient?

Examples include:

- TP53 — 347 patients
- PIK3CA — 347 patients
- TTN — 187 patients
- CDH1 — 130 patients
- GATA3 — 127 patients

These counts describe the selected dataset only.

They should not automatically be interpreted as broader clinical conclusions.

---

## Transformation Questions

### Why was clinical data converted from long format to wide format?

The API returned records such as:

`patientId | clinicalAttributeId | value`

For analysis, it is easier to work with:

`patientId | AGE | SEX | SUBTYPE | OS_MONTHS | ...`

The wide structure is easier to inspect, query, and model.

---

### Why was mutation JSON flattened?

Mutation records contain nested gene information.

For example:

`gene.hugoGeneSymbol`

Flattening created normal tabular columns such as:

`gene`

This makes the data easier to load into an analytical database and query with SQL.

---

### Did flattening mutation data aggregate the mutations?

No.

One row in `mutation_analytics.csv` still represents one mutation record.

Aggregations such as gene frequency will be performed later using SQL.

---

### Was mutation transformation validated?

Yes.

Results:

- Raw mutation records: 84,226
- Processed rows: 84,226
- Missing `patientId`: 0
- Missing `sampleId`: 0
- Missing `gene`: 0
- Missing `mutationType`: 0

Row-count validation passed.

---

## Future User Questions

### Data Quality

BioData Copilot may answer questions such as:

- How many records are available?
- Which fields contain missing values?
- Are duplicates present?
- Which clinical fields are most complete?

---

### Clinical

Potential questions include:

- How are patients distributed by age?
- Which tumour stages are represented?
- Which breast-cancer subtypes are present?
- How is survival information distributed across groups?

---

### Genomic

Potential questions include:

- Which genes are most frequently mutated?
- How many patients have mutations in a given gene?
- What mutation types are most common?
- How do mutation patterns differ across clinical subtypes?

---

## Important Interpretation Boundary

The system should answer:

"What does the dataset show?"

It should not automatically answer:

"What treatment should this patient receive?"

"Does this mutation cause this outcome?"

"Which cancer is definitely the most dangerous?"

Those conclusions require additional scientific or clinical evidence beyond the current dataset.