cat > docs/decisions.md <<'EOF'
# BioData Copilot — Decisions

## 1. Use `uv`

### Why
Provides:
- dependency management
- virtual environment
- `pyproject.toml`
- reproducible `uv.lock`

---

## 2. Build locally before GitHub

### Why
The project can be tested and cleaned before being published.

Git is still used locally for version control.

---

## 3. Keep Python simple first

### Why
The project is also being used to strengthen Python fundamentals.

Flow:

Simple code
→ Understand it
→ Find repetition
→ Refactor later

---

## 4. Use cBioPortal

### Why
It provides:
- public cancer studies
- REST APIs
- clinical data
- genomic data
- structured study metadata

---

## 5. Do not choose a cancer type randomly

### Why
The dataset choice should be justified through actual data availability.

---

## 6. Group studies by cancer family

### Problem
Related IDs appeared separately.

Example:

`brca`
and
`breast`

### Finding
`brca → parent breast`

### Decision
Group specific cancer types into broader families.

---

## 7. Do not select only by sample size

### Why
Large datasets can be highly specialised.

Example:
- Lung: metastatic organotropism
- Pancreas: KRAS-focused

---

## 8. Selected dataset

Study ID:

`brca_tcga_pan_can_atlas_2018`

### Why
It contains broad:
- demographics
- stage
- subtype
- survival data
- mutations
- expression
- copy-number data
- methylation
- protein information

This makes it suitable for a general biomedical data exploration project.

---

## 9. Limit V1 scope

Initially use:
1. Clinical data
2. Mutation data

Do not use every available molecular profile yet.

---

## 10. Separate facts from interpretation

Core rule:

BigQuery calculates facts.

The LLM explains verified facts.

Observed association does not automatically mean causation or clinical conclusion.
EOF