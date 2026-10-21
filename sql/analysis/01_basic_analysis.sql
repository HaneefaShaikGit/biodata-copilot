-- 1. Total patients

SELECT
    COUNT(*) AS total_patients
FROM patient_analytics;


-- 2. Patient distribution by subtype

SELECT
    SUBTYPE,
    COUNT(*) AS patient_count
FROM patient_analytics
GROUP BY SUBTYPE
ORDER BY patient_count DESC;


-- 3. Average age by subtype

SELECT
    SUBTYPE,
    COUNT(*) AS patient_count,
    ROUND(AVG(AGE), 2) AS average_age
FROM patient_analytics
WHERE SUBTYPE IS NOT NULL
GROUP BY SUBTYPE
ORDER BY patient_count DESC;


-- 4. Most frequently mutated genes by patient

SELECT
    gene,
    COUNT(DISTINCT patientId) AS mutated_patients
FROM mutation_analytics
GROUP BY gene
ORDER BY mutated_patients DESC
LIMIT 20;


-- 5. Mutation types

SELECT
    mutationType,
    COUNT(*) AS mutation_count
FROM mutation_analytics
GROUP BY mutationType
ORDER BY mutation_count DESC;