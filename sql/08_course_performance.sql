SELECT
    c.course_id,
    c.course_name,
    c.category,
    c.difficulty_level,
    c.duration_hours,
    COUNT(e.enrollment_id) AS enrollments,
    ROUND(AVG(e.completed_flag) * 100, 2) AS completion_rate_pct,
    ROUND(AVG(e.active_flag) * 100, 2) AS engagement_rate_pct,
    ROUND(AVG(e.satisfaction_score), 2) AS average_satisfaction,
    SUM(CASE WHEN e.completed_flag = 0 THEN 1 ELSE 0 END) AS non_completed_enrollments
FROM courses c
LEFT JOIN enrollments e
    ON c.course_id = e.course_id
GROUP BY c.course_id, c.course_name, c.category, c.difficulty_level, c.duration_hours
ORDER BY completion_rate_pct DESC, average_satisfaction DESC;
