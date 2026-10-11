cat > docs/questions_answered.md <<'EOF'
# BioData Copilot — Questions Answered

## Project Questions

### What are we building?
A biomedical data platform with grounded AI explanations.

### What should BigQuery do?
Store structured data and calculate deterministic analytical results.

### What should the LLM do?
Explain verified results.

### What should the LLM not do?
Invent:
- patient counts
- diagnoses
- clinical outcomes
- treatment recommendations
- unsupported biological conclusions

---

# Data Source Questions

### Where does the data come from?
cBioPortal.

### How is it accessed?
REST API.

### What format is returned?
JSON.

---

# Dataset Selection Questions

### How many studies were found?
Approximately 550.

### Why did we not immediately choose breast cancer?
We wanted a data-driven reason for selecting a disease area.

### Why group cancer types?
Because related cancer types can have different IDs.

Example:

`brca → breast`

### Why was dataset size not enough?
Some large datasets are highly specialised.

### Studies inspected closely
- Lung MSK metastatic study
- Pancreas MSK KRAS-focused study
- TCGA Breast PanCancer Atlas

### Final selected dataset
`brca_tcga_pan_can_atlas_2018`

### Why?
It combines broad clinical data with rich molecular information.

---

# Future User Questions

## Data Quality
- How many records are available?
- Which columns have missing values?
- Are duplicates present?
- Which clinical fields are most complete?

## Clinical
- How are patients distributed by age?
- What stages are represented?
- What subtypes are present?
- What survival information exists?

## Genomic
- What genes are most frequently mutated?
- How many mutations are recorded?
- How does mutation count vary across groups?

## Important boundary

The system should answer:

"What does the dataset show?"

It should not automatically answer:

"What treatment should this patient receive?"

or

"Which cancer is definitely the most dangerous?"
EOF