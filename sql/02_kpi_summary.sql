WITH visitors AS (
    SELECT COUNT(*) * 2.2 AS total_visitors
    FROM learners
),
enrollment_base AS (
    SELECT
        COUNT(*) AS total_enrollments,
        COUNT(DISTINCT learner_id) AS enrolled_learners,
        SUM(started_course_flag) AS started_learners,
        SUM(active_flag) AS active_learners,
        SUM(completed_flag) AS completed_learners,
        AVG(satisfaction_score) AS average_satisfaction
    FROM enrollments
),
retention_base AS (
    SELECT
        COUNT(DISTINCT CASE WHEN returned_flag = 1 THEN learner_id || '-' || course_id END) AS returning_pairs
    FROM retention_events
    WHERE days_since_enrollment IN (1, 7, 14, 30)
)
SELECT
    (SELECT COUNT(*) FROM learners) AS total_learners,
    (SELECT COUNT(*) FROM courses) AS total_courses,
    total_enrollments,
    active_learners,
    completed_learners,
    ROUND(average_satisfaction, 2) AS average_satisfaction,
    ROUND(total_enrollments * 1.0 / total_visitors, 4) AS derived_enrollment_rate,
    ROUND(started_learners * 1.0 / total_enrollments, 4) AS activation_rate,
    ROUND(active_learners * 1.0 / total_enrollments, 4) AS engagement_rate,
    ROUND(completed_learners * 1.0 / total_enrollments, 4) AS completion_rate,
    ROUND((total_enrollments - completed_learners) * 1.0 / total_enrollments, 4) AS drop_off_rate,
    ROUND(returning_pairs * 1.0 / total_enrollments, 4) AS multi_checkpoint_return_rate
FROM enrollment_base, visitors, retention_base;
