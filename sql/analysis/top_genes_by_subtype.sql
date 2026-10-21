WITH subtype_totals AS (

    SELECT
        SUBTYPE,
        COUNT(*) AS subtype_patients

    FROM patient_analytics

    WHERE SUBTYPE IS NOT NULL

    GROUP BY SUBTYPE
),

gene_prevalence AS (

    SELECT
        g.SUBTYPE,
        g.gene,
        g.mutated_patients,
        s.subtype_patients,

        ROUND(
            100.0 * g.mutated_patients / s.subtype_patients,
            2
        ) AS mutation_percentage

    FROM subtype_gene_mutation_summary AS g

    INNER JOIN subtype_totals AS s
        ON g.SUBTYPE = s.SUBTYPE
),

ranked_genes AS (

    SELECT
        *,
        ROW_NUMBER() OVER (
            PARTITION BY SUBTYPE
            ORDER BY mutation_percentage DESC, gene
        ) AS gene_rank

    FROM gene_prevalence
)

SELECT
    SUBTYPE,
    gene,
    mutated_patients,
    subtype_patients,
    mutation_percentage,
    gene_rank

FROM ranked_genes

WHERE gene_rank <= 10

ORDER BY
    SUBTYPE,
    gene_rank;