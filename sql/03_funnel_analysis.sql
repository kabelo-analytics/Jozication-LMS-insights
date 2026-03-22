WITH visitors AS (
    SELECT CAST(COUNT(*) * 2.2 AS INTEGER) AS visitors
    FROM learners
),
funnel AS (
    SELECT 'Visitors' AS stage, visitors AS stage_volume FROM visitors
    UNION ALL
    SELECT 'Enrollments', COUNT(*) FROM enrollments
    UNION ALL
    SELECT 'Started', SUM(started_course_flag) FROM enrollments
    UNION ALL
    SELECT 'Active', SUM(active_flag) FROM enrollments
    UNION ALL
    SELECT 'Completed', SUM(completed_flag) FROM enrollments
),
ordered AS (
    SELECT
        stage,
        stage_volume,
        ROW_NUMBER() OVER (
            ORDER BY CASE stage
                WHEN 'Visitors' THEN 1
                WHEN 'Enrollments' THEN 2
                WHEN 'Started' THEN 3
                WHEN 'Active' THEN 4
                WHEN 'Completed' THEN 5
            END
        ) AS stage_order
    FROM funnel
)
SELECT
    stage,
    stage_volume,
    LAG(stage_volume) OVER (ORDER BY stage_order) AS previous_stage_volume,
    ROUND(
        stage_volume * 1.0 / NULLIF(LAG(stage_volume) OVER (ORDER BY stage_order), 0),
        4
    ) AS conversion_rate_from_previous_stage,
    (LAG(stage_volume) OVER (ORDER BY stage_order) - stage_volume) AS drop_off_volume,
    ROUND(
        (LAG(stage_volume) OVER (ORDER BY stage_order) - stage_volume) * 1.0 /
        NULLIF(LAG(stage_volume) OVER (ORDER BY stage_order), 0),
        4
    ) AS drop_off_pct_from_previous_stage
FROM ordered
ORDER BY stage_order;
