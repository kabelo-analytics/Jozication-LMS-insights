SELECT
    CASE
        WHEN sessions_count <= 2 THEN '1-2 sessions'
        WHEN sessions_count <= 5 THEN '3-5 sessions'
        WHEN sessions_count <= 8 THEN '6-8 sessions'
        ELSE '9+ sessions'
    END AS sessions_band,
    COUNT(*) AS enrollments,
    ROUND(AVG(hours_spent), 2) AS avg_hours_spent,
    ROUND(AVG(progress_percent), 2) AS avg_progress_percent,
    ROUND(AVG(completed_flag) * 100, 2) AS completion_rate_pct
FROM enrollments
GROUP BY 1
ORDER BY
    CASE sessions_band
        WHEN '1-2 sessions' THEN 1
        WHEN '3-5 sessions' THEN 2
        WHEN '6-8 sessions' THEN 3
        ELSE 4
    END;
