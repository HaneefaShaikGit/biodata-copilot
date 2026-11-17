# BioData Copilot — Dataset Selection

## Selected Study

**Study ID:** `brca_tcga_pan_can_atlas_2018`

**Study:** Breast Invasive Carcinoma — TCGA PanCancer Atlas

---

## Why Dataset Selection Was Treated as a Separate Step

The project did not start by assuming that breast cancer was the correct dataset.

The cBioPortal API currently returns more than 550 public studies.

Rather than selecting a study based only on familiarity or sample size, the available studies were explored programmatically.

The selection considered:

- study coverage,
- cancer family,
- sample size,
- clinical attributes,
- molecular profiles,
- study specialization,
- suitability for a general biomedical analytics project.

---

## Cancer-Family Grouping

An early issue was that related cancer types can appear under different cBioPortal identifiers.

For example:

`brca → breast → tissue`

Therefore, the cancer-type hierarchy was followed to group specific cancer types into broader cancer families.

This provided a better view of the available study landscape than relying only on raw cancer-type IDs.

Recent exploration identified high-coverage families including:

- Lung
- Breast
- CNS / Brain
- Prostate
- Lymphoid
- Bowel
- Soft Tissue
- Skin
- Kidney
- Pancreas

---

## Candidate Comparison

The broader shortlist included studies from:

- Breast
- Lung
- Bowel
- Prostate
- Pancreas

The most informative detailed comparison focused on three representative studies.

---

### Lung

**Study ID:** `luad_mskcc_2023_met_organotropism`

Current metadata includes:

- 91 clinical attributes,
- 3 molecular profiles.

The study contains detailed:

- clinical information,
- survival information,
- treatment data,
- mutation information,
- metastatic-site information.

### Limitation

The study is specifically designed around metastatic organotropism.

This makes it scientifically useful but comparatively specialized for a general-purpose V1 biomedical analytics platform.

---

### Pancreas

**Study ID:** `pdac_msk_2024`

Current metadata includes:

- 52 clinical attributes,
- 3 molecular profiles.

The study contains:

- clinical information,
- survival data,
- treatment information,
- mutation data,
- TMB and MSI information,
- extensive KRAS-related variables.

### Limitation

The dataset is strongly centered on KRAS biology.

It is therefore better suited to a focused pancreatic-cancer/KRAS analysis than a broader first version of BioData Copilot.

---

### Breast

**Study ID:** `brca_tcga_pan_can_atlas_2018`

Current cBioPortal metadata includes:

- 60 clinical attributes,
- 17 molecular profiles.

Available information includes:

- demographics,
- tumour stage,
- molecular subtype,
- survival,
- radiation therapy,
- mutations,
- copy-number alterations,
- mRNA expression,
- methylation,
- protein measurements,
- structural variants.

### Limitation

The study contains more molecular data than V1 needs.

Using every available profile would unnecessarily increase the project scope.

The V1 scope was therefore restricted to:

1. clinical data,
2. mutation data.

---

## Final Candidate Comparison

| Criterion | Lung MSK | Pancreas MSK | Breast TCGA PanCancer |
|---|---|---|---|
| Study ID | `luad_mskcc_2023_met_organotropism` | `pdac_msk_2024` | `brca_tcga_pan_can_atlas_2018` |
| Approx. samples | 2,653 | 2,336 | 1,084 |
| Clinical attributes | 91 | 52 | 60 |
| Molecular profiles | 3 | 3 | 17 |
| Survival data | Yes | Yes | Yes |
| Mutation data | Yes | Yes | Yes |
| Copy-number data | Yes | Yes | Yes |
| Structural variants | Yes | Yes | Yes |
| mRNA expression observed | No | No | Yes |
| Protein data observed | No | No | Yes |
| Methylation observed | No | No | Yes |
| Main focus | Metastatic organotropism | KRAS biology | Broad clinical and molecular characterization |
| V1 limitation | Too specialized | Too KRAS-focused | Broad but more complex |
| Decision | Not selected | Not selected | **Selected** |

---

## Final Decision

The TCGA Breast Cancer PanCancer Atlas cohort was selected because it provides a broad combination of:

- clinical information,
- demographic information,
- tumour stage,
- breast-cancer subtype,
- survival,
- mutation data,
- and additional molecular profiles.

The choice was not based on having the largest number of samples.

Instead, the study offered the strongest balance between:

- breadth,
- interpretability,
- analytical flexibility,
- and future extensibility.

---

## V1 Data Scope

BioData Copilot V1 uses:

### Clinical Data

Examples include:

- age,
- sex,
- race,
- ethnicity,
- tumour stage,
- subtype,
- survival,
- radiation therapy.

### Mutation Data

Examples include:

- gene,
- mutation type,
- protein change,
- genomic position,
- allele information,
- tumour and normal read counts.

---

## Deferred Molecular Data

The selected study also contains additional profiles that are not part of V1:

- mRNA expression,
- methylation,
- protein expression,
- phosphoprotein data,
- copy-number alterations,
- structural variants.

These remain possible future extensions if they support a clear analytical or research question.

They were intentionally excluded from V1 to prevent unnecessary scope expansion.

---

## Selection Process Summary

```text
550+ public cBioPortal studies
        ↓
Group studies by cancer family
        ↓
Compare coverage and study size
        ↓
Shortlist candidate studies
        ↓
Compare clinical attributes
        ↓
Compare molecular profiles
        ↓
Inspect actual study scope
        ↓
Evaluate specialization
        ↓
Select TCGA Breast PanCancer Atlas
```

The final selection therefore reflects a data-driven study-selection process rather than an arbitrary choice of disease area.