# Power BI Dashboard Guide

## 1. Executive Overview
- KPI cards: total learners, total enrollments, active learners, completion rate, drop-off rate, retention rate, average satisfaction.
- Line chart: `monthly_enrollment_completion_trends.csv` using `month`, `enrollments`, and `completions`.
- Column chart: `monthly_visitors_enrollment_rate.csv` for visitors vs enrollments.
- Funnel visual: `funnel_analysis.csv` using `stage` and `stage_volume`.

Notes:
- Treat visitor-based enrollment rate as a derived reporting assumption, not a core observed KPI.
- Keep Day 30 retention separate from the broader multi-checkpoint return rate.

## 2. Learner Funnel
- Funnel visual: `funnel_analysis.csv`.
- Table or clustered bar chart: `funnel_analysis.csv` for conversion and drop-off between stages.
- Supporting bar chart: `dropoff_analysis.csv` by learner journey stage.

## 3. Engagement Analysis
- Histogram or column chart: `sessions_distribution.csv`.
- Bar chart: `engagement_analysis.csv` by `sessions_band` vs `completion_rate_pct`.
- Column chart: `progress_distribution.csv`.
- Scatter plot: use `enrollments.csv` with `sessions_count`, `hours_spent`, and `completed_flag`.

## 4. Retention Analysis
- KPI cards: Day 1, Day 7, Day 14, Day 30 retention from `retention_rates.csv`.
- Line chart: `returning_learner_trend.csv`.
- Matrix heatmap: `cohort_retention.csv` with `cohort_month` on rows, `days_since_enrollment` on columns, and `retention_rate` as values.

## 5. Course Performance
- Bar chart: `course_performance.csv` for enrollments by course.
- Sorted bar chart: `course_performance.csv` for completion rate by course.
- Dot plot or column chart: `course_performance.csv` for satisfaction by course.
- Bar chart: `dropout_by_course.csv` for course-level drop-off.

## 6. Learner Segmentation
- Bar charts: `completion_by_age_group.csv`, `completion_by_region.csv`, `completion_by_device_type.csv`.
- Matrix or heatmap: `segmentation_analysis.csv` by region, age group, and device type.
- Column chart: `completion_by_device_type.csv` for satisfaction by device.

Notes:
- Apply a minimum-volume filter before ranking highly specific segments.

## Recommended Slicers
- Course
- Category
- Difficulty level
- Region
- Device type
- Age group
- Enrollment month

## Modeling Notes
- Keep `learners.csv`, `courses.csv`, `enrollments.csv`, and `retention_events.csv` as the core tables in Power BI.
- Use the exported summary CSVs as reporting-layer tables for quick visuals.
- Link `learners` to `enrollments` on `learner_id`, `courses` to `enrollments` on `course_id`, and `enrollments` to `retention_events` using `learner_id` plus `course_id`.
