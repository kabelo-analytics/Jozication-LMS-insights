SELECT
    l.region,
    l.age_group,
    l.device_type,
    COUNT(*) AS enrollments,
    ROUND(AVG(e.completed_flag) * 100, 2) AS completion_rate_pct,
    ROUND(AVG(e.active_flag) * 100, 2) AS engagement_rate_pct,
    ROUND(AVG(e.satisfaction_score), 2) AS average_satisfaction,
    ROUND(AVG(e.sessions_count), 2) AS avg_sessions
FROM enrollments e
JOIN learners l
    ON e.learner_id = l.learner_id
GROUP BY l.region, l.age_group, l.device_type
ORDER BY completion_rate_pct DESC, average_satisfaction DESC;
