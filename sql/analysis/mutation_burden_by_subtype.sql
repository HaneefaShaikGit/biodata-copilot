SELECT
    p.SUBTYPE,

    COUNT(*) AS total_patients,

    COUNT(s.TMB_NONSYNONYMOUS) AS patients_with_tmb,

    ROUND(AVG(s.TMB_NONSYNONYMOUS), 2) AS average_tmb,
    ROUND(MEDIAN(s.TMB_NONSYNONYMOUS), 2) AS median_tmb,

    ROUND(AVG(s.MUTATION_COUNT), 2) AS average_mutation_count,
    ROUND(MEDIAN(s.MUTATION_COUNT), 2) AS median_mutation_count

FROM patient_analytics AS p

INNER JOIN sample_analytics AS s
    ON p.patientId = s.patientId

WHERE p.SUBTYPE IS NOT NULL

GROUP BY p.SUBTYPE

ORDER BY p.SUBTYPE;