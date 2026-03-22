SELECT
    COALESCE(dropout_stage, 'Completed') AS learner_journey_stage,
    COUNT(*) AS enrollments,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM enrollments), 2) AS share_of_enrollments_pct
FROM enrollments
GROUP BY COALESCE(dropout_stage, 'Completed')
ORDER BY enrollments DESC;
