
--How complete are important clinical fields?

SELECT
    'AGE' AS field,
    COUNT(AGE) AS available,
    COUNT(*) - COUNT(AGE) AS missing,
    ROUND(100.0 * COUNT(AGE) / COUNT(*), 2) AS completeness_percentage
FROM patient_analytics

UNION ALL

SELECT
    'RACE',
    COUNT(RACE),
    COUNT(*) - COUNT(RACE),
    ROUND(100.0 * COUNT(RACE) / COUNT(*), 2)
FROM patient_analytics

UNION ALL

SELECT
    'ETHNICITY',
    COUNT(ETHNICITY),
    COUNT(*) - COUNT(ETHNICITY),
    ROUND(100.0 * COUNT(ETHNICITY) / COUNT(*), 2)
FROM patient_analytics

UNION ALL

SELECT
    'TUMOR_STAGE',
    COUNT(AJCC_PATHOLOGIC_TUMOR_STAGE),
    COUNT(*) - COUNT(AJCC_PATHOLOGIC_TUMOR_STAGE),
    ROUND(
        100.0 * COUNT(AJCC_PATHOLOGIC_TUMOR_STAGE) / COUNT(*),
        2
    )
FROM patient_analytics

UNION ALL

SELECT
    'SUBTYPE',
    COUNT(SUBTYPE),
    COUNT(*) - COUNT(SUBTYPE),
    ROUND(100.0 * COUNT(SUBTYPE) / COUNT(*), 2)
FROM patient_analytics

UNION ALL

SELECT
    'OS_MONTHS',
    COUNT(OS_MONTHS),
    COUNT(*) - COUNT(OS_MONTHS),
    ROUND(100.0 * COUNT(OS_MONTHS) / COUNT(*), 2)
FROM patient_analytics

ORDER BY completeness_percentage DESC;