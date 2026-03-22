SELECT
    days_since_enrollment,
    COUNT(DISTINCT CASE WHEN returned_flag = 1 THEN learner_id || '-' || course_id END) AS returning_enrollments,
    COUNT(DISTINCT learner_id || '-' || course_id) AS eligible_enrollments,
    ROUND(
        COUNT(DISTINCT CASE WHEN returned_flag = 1 THEN learner_id || '-' || course_id END) * 1.0 /
        COUNT(DISTINCT learner_id || '-' || course_id),
        4
    ) AS retention_rate
FROM retention_events
WHERE days_since_enrollment IN (1, 7, 14, 30)
GROUP BY days_since_enrollment
ORDER BY days_since_enrollment;
