--How are patients distributed across subtypes?
SELECT
    COALESCE(SUBTYPE, 'Unknown') AS subtype,
    COUNT(*) AS patient_count,
    ROUND(
        100.0 * COUNT(*) / SUM(COUNT(*)) OVER (),
        2
    ) AS percentage
FROM patient_analytics
GROUP BY SUBTYPE
ORDER BY patient_count DESC;
