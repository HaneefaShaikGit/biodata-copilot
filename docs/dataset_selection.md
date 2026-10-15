# BioData Copilot — Dataset Selection

## Selected Study

**Study ID:** `brca_tcga_pan_can_atlas_2018`

**Study:** Breast Invasive Carcinoma — TCGA PanCancer Atlas

---

## Selection Process

The cBioPortal API returned approximately 550 public studies.

Rather than choosing a cancer type arbitrarily, the studies were grouped into broader cancer families using the cBioPortal cancer-type hierarchy.

Several high-coverage cancer families were identified, including:

- Lung
- Breast
- Bowel
- Prostate
- Pancreas

Representative studies were then compared based on:

- sample size
- clinical attribute availability
- molecular profile availability
- survival information
- study scope
- degree of specialisation
- suitability for a general biomedical data exploration project

---

## Cancer-Family Grouping

An important issue discovered during exploration was that related cancer types could appear under different identifiers.

For example:

`brca → breast → tissue`

Therefore, studies were grouped using the cancer-type parent hierarchy rather than relying only on raw cancer-type IDs.

This provided a more meaningful comparison of study availability across broader disease families.

---

# Candidate Studies Inspected

## Lung

**Study ID:** `luad_mskcc_2023_met_organotropism`

### Strengths

The study contains rich clinical information including:

- age
- sex
- race
- stage
- survival
- treatment
- mutation data
- TMB
- MSI
- metastatic-site information

### Limitation

The study is specifically focused on metastatic organotropism.

Although it contains extensive clinical data, the specialised research focus makes it less suitable for a general-purpose biomedical exploration platform.

---

## Pancreas

**Study ID:** `pdac_msk_2024`

### Strengths

The study contains useful:

- clinical information
- survival information
- treatment information
- mutation data
- TMB
- MSI

It also contains extensive KRAS-related variables.

### Limitation

Many of the available variables are centred around KRAS biology.

This makes the dataset valuable for a focused pancreatic-cancer/KRAS analysis, but less suitable for a broader V1 platform.

---

## Breast

**Study ID:** `brca_tcga_pan_can_atlas_2018`

### Strengths

The study provides broad clinical information including:

- age
- sex
- race
- ethnicity
- tumour stage
- molecular subtype
- survival outcomes
- radiation therapy
- mutation count
- genomic summary variables

It also provides multiple molecular profiles, including:

- mutation data
- copy-number alterations
- mRNA expression
- protein information
- methylation
- structural variants

### Limitation

The study contains many molecular data types, which could make the project unnecessarily complex if all profiles were included at once.

This was handled by limiting V1 to clinical and mutation data.

---

# Final Candidate Comparison

| Criterion | Lung MSK 2023 | Pancreas MSK 2024 | Breast TCGA PanCancer |
|---|---|---|---|
| Study ID | `luad_mskcc_2023_met_organotropism` | `pdac_msk_2024` | `brca_tcga_pan_can_atlas_2018` |
| Approx. sample size | 2,653 | 2,336 | 1,084 |
| Clinical attributes | 91 | 52 | Broad clinical set |
| Survival data | Yes | Yes | Yes |
| Stage data | Yes | Yes | Yes |
| Treatment data | Very detailed | Good | Available |
| Metastasis data | Very detailed | Limited | General |
| Mutation data | Yes | Yes | Yes |
| Copy-number data | Yes | Yes | Yes |
| Structural variants | Yes | Yes | Yes |
| mRNA expression | Not observed during inspection | Not observed during inspection | Yes |
| Protein data | Not observed during inspection | Not observed during inspection | Yes |
| Methylation data | Not observed during inspection | Not observed during inspection | Yes |
| Main study focus | Metastatic organotropism | KRAS biology | Broad breast-cancer molecular and clinical analysis |
| Main limitation for V1 | Too specialised | Too KRAS-focused | Broader and more complex |
| Decision | Not selected | Not selected | **Selected** |

---

# Decision

The TCGA Breast Cancer PanCancer Atlas study was selected.

Study ID:

`brca_tcga_pan_can_atlas_2018`

The main reason was not simply sample size.

The selected study provides a broad combination of:

- clinical information
- survival data
- stage
- subtype
- demographic information
- mutation data
- additional molecular profiles

This makes it more suitable for a general biomedical data exploration platform than the more specialised lung and pancreatic studies.

---

# V1 Data Scope

Although the selected study contains many molecular profiles, BioData Copilot V1 will initially use only:

1. Clinical data
2. Mutation data

The project will not initially include:

- mRNA expression analysis
- methylation analysis
- protein analysis
- copy-number analysis
- structural-variant analysis

These may be added later if they support a clear analytical requirement.

---

# Final Reasoning

The study-selection process followed this logic:

```text
~550 cBioPortal studies
        ↓
Group studies by cancer family
        ↓
Compare study coverage
        ↓
Shortlist representative studies
        ↓
Compare clinical attributes
        ↓
Compare molecular profiles
        ↓
Inspect actual fields
        ↓
Evaluate study specialisation
        ↓
Select TCGA Breast PanCancer Atlas
```
The lung and pancreatic studies contained strong clinical and genomic data, but both were built around more specialised research questions.
The Breast TCGA PanCancer Atlas cohort was selected because it offers broader clinical and molecular coverage and supports multiple future analytical directions.
The V1 scope is intentionally limited to clinical and mutation data so the project remains manageable while preserving the possibility of expanding into additional molecular profiles later.