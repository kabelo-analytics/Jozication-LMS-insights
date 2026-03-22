from __future__ import annotations

import sqlite3
from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[1]
DB_PATH = BASE_DIR / "data" / "jozication_lms_analytics.db"
EXPORT_DIR = BASE_DIR / "exports"
SQL_DIR = BASE_DIR / "sql"
DOCS_DIR = BASE_DIR / "docs"


def read_sql_file(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def export_query(connection: sqlite3.Connection, sql_file: str, output_file: str) -> pd.DataFrame:
    query = read_sql_file(SQL_DIR / sql_file)
    frame = pd.read_sql_query(query, connection)
    frame.to_csv(EXPORT_DIR / output_file, index=False)
    return frame


def export_segment_views(connection: sqlite3.Connection) -> None:
    completion_by_region = pd.read_sql_query(
        """
        SELECT
            l.region,
            COUNT(*) AS enrollments,
            ROUND(AVG(e.completed_flag) * 100, 2) AS completion_rate_pct,
            ROUND(AVG(e.active_flag) * 100, 2) AS engagement_rate_pct
        FROM enrollments e
        JOIN learners l ON e.learner_id = l.learner_id
        GROUP BY l.region
        ORDER BY completion_rate_pct DESC;
        """,
        connection,
    )
    completion_by_region.to_csv(EXPORT_DIR / "completion_by_region.csv", index=False)

    completion_by_age_group = pd.read_sql_query(
        """
        SELECT
            l.age_group,
            COUNT(*) AS enrollments,
            ROUND(AVG(e.completed_flag) * 100, 2) AS completion_rate_pct,
            ROUND(AVG(e.active_flag) * 100, 2) AS engagement_rate_pct
        FROM enrollments e
        JOIN learners l ON e.learner_id = l.learner_id
        GROUP BY l.age_group
        ORDER BY completion_rate_pct DESC;
        """,
        connection,
    )
    completion_by_age_group.to_csv(EXPORT_DIR / "completion_by_age_group.csv", index=False)

    completion_by_device = pd.read_sql_query(
        """
        SELECT
            l.device_type,
            COUNT(*) AS enrollments,
            ROUND(AVG(e.completed_flag) * 100, 2) AS completion_rate_pct,
            ROUND(AVG(e.active_flag) * 100, 2) AS engagement_rate_pct,
            ROUND(AVG(e.satisfaction_score), 2) AS average_satisfaction
        FROM enrollments e
        JOIN learners l ON e.learner_id = l.learner_id
        GROUP BY l.device_type
        ORDER BY completion_rate_pct DESC;
        """,
        connection,
    )
    completion_by_device.to_csv(EXPORT_DIR / "completion_by_device_type.csv", index=False)


def export_additional_views(connection: sqlite3.Connection) -> None:
    sessions_distribution = pd.read_sql_query(
        """
        SELECT
            sessions_count,
            COUNT(*) AS enrollments
        FROM enrollments
        GROUP BY sessions_count
        ORDER BY sessions_count;
        """,
        connection,
    )
    sessions_distribution.to_csv(EXPORT_DIR / "sessions_distribution.csv", index=False)

    progress_distribution = pd.read_sql_query(
        """
        SELECT
            CASE
                WHEN progress_percent < 25 THEN '0-24%'
                WHEN progress_percent < 50 THEN '25-49%'
                WHEN progress_percent < 75 THEN '50-74%'
                ELSE '75-100%'
            END AS progress_band,
            COUNT(*) AS enrollments
        FROM enrollments
        GROUP BY progress_band
        ORDER BY CASE progress_band
            WHEN '0-24%' THEN 1
            WHEN '25-49%' THEN 2
            WHEN '50-74%' THEN 3
            ELSE 4
        END;
        """,
        connection,
    )
    progress_distribution.to_csv(EXPORT_DIR / "progress_distribution.csv", index=False)

    returning_trend = pd.read_sql_query(
        """
        SELECT
            activity_date,
            COUNT(DISTINCT CASE WHEN returned_flag = 1 THEN learner_id || '-' || course_id END) AS returning_enrollments
        FROM retention_events
        GROUP BY activity_date
        ORDER BY activity_date;
        """,
        connection,
    )
    returning_trend.to_csv(EXPORT_DIR / "returning_learner_trend.csv", index=False)

    dropout_by_course = pd.read_sql_query(
        """
        SELECT
            c.course_name,
            COUNT(*) AS enrollments,
            SUM(CASE WHEN e.completed_flag = 0 THEN 1 ELSE 0 END) AS non_completed_enrollments,
            ROUND(SUM(CASE WHEN e.completed_flag = 0 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS drop_off_rate_pct
        FROM enrollments e
        JOIN courses c ON e.course_id = c.course_id
        GROUP BY c.course_name
        ORDER BY drop_off_rate_pct DESC;
        """,
        connection,
    )
    dropout_by_course.to_csv(EXPORT_DIR / "dropout_by_course.csv", index=False)

    dropout_by_device = pd.read_sql_query(
        """
        SELECT
            l.device_type,
            COUNT(*) AS enrollments,
            SUM(CASE WHEN e.completed_flag = 0 THEN 1 ELSE 0 END) AS non_completed_enrollments,
            ROUND(SUM(CASE WHEN e.completed_flag = 0 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS drop_off_rate_pct
        FROM enrollments e
        JOIN learners l ON e.learner_id = l.learner_id
        GROUP BY l.device_type
        ORDER BY drop_off_rate_pct DESC;
        """,
        connection,
    )
    dropout_by_device.to_csv(EXPORT_DIR / "dropout_by_device_type.csv", index=False)

    dropout_by_age_group = pd.read_sql_query(
        """
        SELECT
            l.age_group,
            COUNT(*) AS enrollments,
            SUM(CASE WHEN e.completed_flag = 0 THEN 1 ELSE 0 END) AS non_completed_enrollments,
            ROUND(SUM(CASE WHEN e.completed_flag = 0 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS drop_off_rate_pct
        FROM enrollments e
        JOIN learners l ON e.learner_id = l.learner_id
        GROUP BY l.age_group
        ORDER BY drop_off_rate_pct DESC;
        """,
        connection,
    )
    dropout_by_age_group.to_csv(EXPORT_DIR / "dropout_by_age_group.csv", index=False)

    monthly_visitors = pd.read_sql_query(
        """
        WITH signup_visitors AS (
            SELECT
                strftime('%Y-%m', signup_date) AS month,
                COUNT(*) * 2.2 AS visitors
            FROM learners
            GROUP BY 1
        ),
        monthly_enrollments AS (
            SELECT
                strftime('%Y-%m', enrollment_date) AS month,
                COUNT(*) AS enrollments
            FROM enrollments
            GROUP BY 1
        )
        SELECT
            s.month,
            ROUND(s.visitors, 0) AS visitors,
            COALESCE(e.enrollments, 0) AS enrollments,
            ROUND(COALESCE(e.enrollments, 0) * 1.0 / s.visitors, 4) AS enrollment_rate
        FROM signup_visitors s
        LEFT JOIN monthly_enrollments e ON s.month = e.month
        ORDER BY s.month;
        """,
        connection,
    )
    monthly_visitors.to_csv(EXPORT_DIR / "monthly_visitors_enrollment_rate.csv", index=False)


def build_summary_markdown(
    kpi_df: pd.DataFrame,
    course_df: pd.DataFrame,
    retention_df: pd.DataFrame,
    segment_df: pd.DataFrame,
) -> None:
    kpi = kpi_df.iloc[0]
    top_course = course_df.iloc[0]
    low_course = course_df.sort_values("completion_rate_pct").iloc[0]
    eligible_segments = segment_df[segment_df["enrollments"] >= 40]
    best_segment = eligible_segments.iloc[0] if not eligible_segments.empty else segment_df.iloc[0]
    day_30 = retention_df.loc[retention_df["days_since_enrollment"] == 30, "retention_rate"].iloc[0]

    summary = f"""# Analysis Summary

## Executive Snapshot
- Total learners: {int(kpi["total_learners"]):,}
- Total courses: {int(kpi["total_courses"])}
- Total enrollments: {int(kpi["total_enrollments"]):,}
- Completion rate: {kpi["completion_rate"]:.2%}
- Drop-off rate: {kpi["drop_off_rate"]:.2%}
- Retention rate: {kpi["retention_rate"]:.2%}
- Average satisfaction: {kpi["average_satisfaction"]:.2f}

## Highlights
- The strongest course by completion rate is "{top_course["course_name"]}" at {top_course["completion_rate_pct"]:.2f}% completion.
- The weakest course by completion rate is "{low_course["course_name"]}" at {low_course["completion_rate_pct"]:.2f}% completion, reinforcing the synthetic difficulty penalty.
- Day 30 retention settles at {day_30:.2%}, showing a realistic decline from early return behaviour.
- The leading learner segment in the segmentation output is {best_segment["region"]} / {best_segment["age_group"]} / {best_segment["device_type"]}, with {best_segment["completion_rate_pct"]:.2f}% completion.

## Interpretation
- Activation is materially higher than completion, so the major product risk sits in sustaining momentum after first lesson.
- Desktop learners generally outperform mobile learners on completion and engagement, which suggests friction in the mobile learning experience.
- Advanced courses carry higher drop-off and lower satisfaction than beginner courses, which is the expected pattern for a realistic LMS journey.
"""
    (DOCS_DIR / "analysis_summary.md").write_text(summary, encoding="utf-8")


def main() -> None:
    EXPORT_DIR.mkdir(parents=True, exist_ok=True)
    DOCS_DIR.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(DB_PATH) as connection:
        kpi_df = export_query(connection, "02_kpi_summary.sql", "kpi_summary.csv")
        export_query(connection, "03_funnel_analysis.sql", "funnel_analysis.csv")
        export_query(connection, "04_enrollment_trends.sql", "monthly_enrollment_completion_trends.csv")
        export_query(connection, "05_engagement_analysis.sql", "engagement_analysis.csv")
        retention_df = export_query(connection, "06_retention_analysis.sql", "retention_rates.csv")
        export_query(connection, "07_cohort_retention.sql", "cohort_retention.csv")
        course_df = export_query(connection, "08_course_performance.sql", "course_performance.csv")
        segment_df = export_query(connection, "09_segmentation_analysis.sql", "segmentation_analysis.csv")
        export_query(connection, "10_satisfaction_analysis.sql", "satisfaction_analysis.csv")
        export_query(connection, "11_dropoff_analysis.sql", "dropoff_analysis.csv")

        export_segment_views(connection)
        export_additional_views(connection)
        build_summary_markdown(kpi_df, course_df, retention_df, segment_df)

    print(f"Analysis exports written to {EXPORT_DIR}")


if __name__ == "__main__":
    main()
