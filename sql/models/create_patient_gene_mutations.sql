CREATE OR REPLACE VIEW patient_gene_mutations AS

SELECT DISTINCT
    p.patientId,
    p.SUBTYPE,
    m.gene

FROM patient_analytics AS p

INNER JOIN mutation_analytics AS m
    ON p.patientId = m.patientId

WHERE p.SUBTYPE IS NOT NULL;