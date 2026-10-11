# Dataset Selection

## Selected Study

**Study ID:** `brca_tcga_pan_can_atlas_2018`

**Study:** Breast Invasive Carcinoma — TCGA PanCancer Atlas

## Selection Process

The cBioPortal API returned 550 public studies.

Studies were grouped into broader cancer families using the cancer-type hierarchy. Several high-coverage families were identified, including lung, breast, bowel, prostate, and pancreatic cancers.

Representative studies were then compared based on:

- sample size
- clinical attribute availability
- molecular profile availability
- clarity of study scope
- suitability for a general biomedical data exploration project

## Studies Inspected

### Lung
`luad_mskcc_2023_met_organotropism`

Rich clinical and metastatic information, but the study is focused specifically on metastatic organotropism.

### Pancreas
`pdac_msk_2024`

Contains useful clinical and genomic information, but many attributes are centred on KRAS-specific analysis.

### Breast
`brca_tcga_pan_can_atlas_2018`

Provides broad clinical information including stage, subtype, survival, demographics, and genomic summary variables.

It also exposes multiple molecular profiles including mutations, copy-number alterations, mRNA expression, protein expression, methylation, and structural variants.

## Decision

The TCGA Breast Cancer PanCancer Atlas study was selected because it provides a broad combination of clinical and molecular information without restricting the project to one narrow biological research question.

## V1 Data Scope

For the first version of BioData Copilot, the project will initially use:

1. Clinical data
2. Mutation data

Additional molecular profiles may be added later if required.