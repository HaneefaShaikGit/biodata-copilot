--Which genes are most frequently mutated?
WITH sequenced AS (
    SELECT COUNT(*) AS sequenced_patients
    FROM sample_analytics
    WHERE MUTATION_COUNT IS NOT NULL
)

SELECT
    gene,
    COUNT(DISTINCT patientId) AS mutated_patients,
    (SELECT sequenced_patients FROM sequenced) AS sequenced_patients,
    ROUND(
        100.0 * COUNT(DISTINCT patientId)
        / (SELECT sequenced_patients FROM sequenced),
        2
    ) AS patient_percentage

FROM mutation_analytics

GROUP BY gene

ORDER BY mutated_patients DESC

LIMIT 20;