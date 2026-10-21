CREATE OR REPLACE VIEW subtype_gene_mutation_summary AS

SELECT
    SUBTYPE,
    gene,
    COUNT(*) AS mutated_patients

FROM patient_gene_mutations

GROUP BY
    SUBTYPE,
    gene;