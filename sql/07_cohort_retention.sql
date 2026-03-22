WITH cohort_base AS (
    SELECT
        e.learner_id,
        e.course_id,
        strftime('%Y-%m', e.enrollment_date) AS cohort_month,
        r.days_since_enrollment,
        r.returned_flag
    FROM enrollments e
    JOIN retention_events r
        ON e.learner_id = r.learner_id
       AND e.course_id = r.course_id
)
SELECT
    cohort_month,
    days_since_enrollment,
    COUNT(DISTINCT learner_id || '-' || course_id) AS cohort_size,
    COUNT(DISTINCT CASE WHEN returned_flag = 1 THEN learner_id || '-' || course_id END) AS retained_enrollments,
    ROUND(
        COUNT(DISTINCT CASE WHEN returned_flag = 1 THEN learner_id || '-' || course_id END) * 1.0 /
        COUNT(DISTINCT learner_id || '-' || course_id),
        4
    ) AS retention_rate
FROM cohort_base
WHERE days_since_enrollment IN (1, 7, 14, 30)
GROUP BY cohort_month, days_since_enrollment
ORDER BY cohort_month, days_since_enrollment;
