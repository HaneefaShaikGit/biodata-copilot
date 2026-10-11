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

## Final Candidate Comparison

| Criterion | Lung MSK 2023 | Pancreas MSK 2024 | Breast TCGA PanCancer |
|---|---|---|---|
| Study ID | `luad_mskcc_2023_met_organotropism` | `pdac_msk_2024` | `brca_tcga_pan_can_atlas_2018` |
| Sample size | 2,653 | 2,336 | ~1,084 |
| Clinical attributes | 91 | 52 | Broad clinical set |
| Survival data | Yes | Yes | Yes |
| Stage data | Yes | Yes | Yes |
| Treatment data | Very detailed | Good | Available |
| Metastasis data | Very detailed | Limited | General |
| Mutation data | Yes | Yes | Yes |
| Copy-number data | Yes | Yes | Yes |
| Structural variants | Yes | Yes | Yes |
| mRNA expression | Not observed | Not observed | Yes |
| Protein data | Not observed | Not observed | Yes |
| Methylation data | Not observed | Not observed | Yes |
| Main study focus | Metastatic organotropism | KRAS biology | Broad breast-cancer molecular/clinical analysis |
| Main limitation for V1 | Too specialised | Too KRAS-focused | More complex, but broad |
| Decision | Not selected | Not selected | **Selected** |

### Final Reasoning

The lung and pancreatic studies contain strong clinical and genomic data, but both are designed around relatively specialised research questions.

The TCGA Breast PanCancer Atlas cohort was selected because it provides a broader combination of clinical, survival, subtype, mutation and additional molecular information. This makes it more suitable for a general-purpose biomedical data exploration platform.

The V1 project will still limit itself to clinical and mutation data to keep the scope manageable.