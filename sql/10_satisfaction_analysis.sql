SELECT
    CASE
        WHEN progress_percent < 25 THEN '0-24%'
        WHEN progress_percent < 50 THEN '25-49%'
        WHEN progress_percent < 75 THEN '50-74%'
        ELSE '75-100%'
    END AS progress_band,
    completed_flag,
    COUNT(*) AS enrollments,
    ROUND(AVG(satisfaction_score), 2) AS average_satisfaction
FROM enrollments
GROUP BY progress_band, completed_flag
ORDER BY
    CASE progress_band
        WHEN '0-24%' THEN 1
        WHEN '25-49%' THEN 2
        WHEN '50-74%' THEN 3
        ELSE 4
    END,
    completed_flag;
