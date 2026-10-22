--Which genes are most frequently mutated within each subtype?
WITH patient_gene AS (
    SELECT DISTINCT
        p.patientId,
        p.SUBTYPE,
        m.gene
    FROM patient_analytics AS p
    INNER JOIN mutation_analytics AS m
        ON p.patientId = m.patientId
    WHERE p.SUBTYPE IS NOT NULL
),

subtype_totals AS (
    SELECT
        SUBTYPE,
        COUNT(*) AS subtype_patients
    FROM patient_analytics
    WHERE SUBTYPE IS NOT NULL
    GROUP BY SUBTYPE
),

gene_counts AS (
    SELECT
        SUBTYPE,
        gene,
        COUNT(*) AS mutated_patients
    FROM patient_gene
    GROUP BY SUBTYPE, gene
),

ranked AS (
    SELECT
        g.SUBTYPE,
        g.gene,
        g.mutated_patients,
        s.subtype_patients,

        ROUND(
            100.0 * g.mutated_patients / s.subtype_patients,
            2
        ) AS mutation_percentage,

        ROW_NUMBER() OVER (
            PARTITION BY g.SUBTYPE
            ORDER BY g.mutated_patients DESC, g.gene
        ) AS gene_rank

    FROM gene_counts AS g

    INNER JOIN subtype_totals AS s
        ON g.SUBTYPE = s.SUBTYPE
)

SELECT
    SUBTYPE,
    gene,
    mutated_patients,
    subtype_patients,
    mutation_percentage
FROM ranked
WHERE gene_rank <= 10
ORDER BY SUBTYPE, gene_rank;