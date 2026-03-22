WITH monthly_enrollments AS (
    SELECT
        strftime('%Y-%m', enrollment_date) AS month,
        COUNT(*) AS enrollments
    FROM enrollments
    GROUP BY 1
),
monthly_completions AS (
    SELECT
        strftime('%Y-%m', completion_date) AS month,
        COUNT(*) AS completions
    FROM enrollments
    WHERE completed_flag = 1
    GROUP BY 1
)
SELECT
    e.month,
    e.enrollments,
    COALESCE(c.completions, 0) AS completions
FROM monthly_enrollments e
LEFT JOIN monthly_completions c
    ON e.month = c.month
ORDER BY e.month;
