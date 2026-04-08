# Jozication LMS Analytics

Jozication LMS Analytics is a synthetic learning analytics project built to show how a data analyst or product analyst might structure LMS reporting for an EdTech team. The repo focuses on the analytics layer: data generation, SQL analysis, exported reporting tables, and a static walkthrough.

## What the project covers

The project follows the learner journey from signup to completion and focuses on a few practical questions:

- where learners drop out of the course journey
- which course types underperform
- how device, region, and age group relate to completion
- how return behaviour changes from Day 1 to Day 30
- which metrics are useful for intervention planning

This is not a learner-facing product build. It is an analyst portfolio project built around reproducible reporting assets.

## Tech stack

- Python
- SQLite
- pandas
- NumPy
- SQL
- CSV exports for reporting or BI use

## Project structure

```text
Jozication/
|-- README.md
|-- requirements.txt
|-- data/
|   `-- jozication_lms_analytics.db
|-- docs/
|   |-- analysis_summary.md
|   `-- power_bi_dashboard_guide.md
|-- exports/
|   |-- cohort_retention.csv
|   |-- completion_by_age_group.csv
|   |-- completion_by_device_type.csv
|   |-- completion_by_region.csv
|   |-- course_performance.csv
|   |-- courses.csv
|   |-- dropout_analysis.csv
|   |-- dropout_by_age_group.csv
|   |-- dropout_by_course.csv
|   |-- dropout_by_device_type.csv
|   |-- engagement_analysis.csv
|   |-- enrollments.csv
|   |-- funnel_analysis.csv
|   |-- kpi_summary.csv
|   |-- learners.csv
|   |-- monthly_enrollment_completion_trends.csv
|   |-- monthly_visitors_enrollment_rate.csv
|   |-- progress_distribution.csv
|   |-- retention_events.csv
|   |-- retention_rates.csv
|   |-- returning_learner_trend.csv
|   |-- satisfaction_analysis.csv
|   |-- segmentation_analysis.csv
|   `-- sessions_distribution.csv
|-- notebooks/
|   `-- README.md
|-- scripts/
|   |-- generate_lms_data.py
|   `-- run_analysis.py
`-- sql/
    |-- 01_schema.sql
    |-- 02_kpi_summary.sql
    |-- 03_funnel_analysis.sql
    |-- 04_enrollment_trends.sql
    |-- 05_engagement_analysis.sql
    |-- 06_retention_analysis.sql
    |-- 07_cohort_retention.sql
    |-- 08_course_performance.sql
    |-- 09_segmentation_analysis.sql
    |-- 10_satisfaction_analysis.sql
    `-- 11_dropoff_analysis.sql
```

## Dataset

The core analytical model uses four tables:

1. `learners`
2. `courses`
3. `enrollments`
4. `retention_events`

The main analytical grain is learner-course enrollment. Retention is measured through return events captured at selected checkpoints.

## Synthetic data logic

The generator bakes in a few realistic LMS patterns on purpose:

- some learners sign up but never enroll
- some enroll but never start
- advanced courses are harder to complete than beginner courses
- more sessions and more time spent improve completion odds
- mobile learners carry a modest completion penalty relative to desktop
- return behaviour weakens from Day 1 to Day 30

That matters for interpretation. The strongest findings in this project are about KPI design and reporting structure, not unexpected discovery from messy real production data.

## Metric definitions

These are the key metrics used in the repo and walkthrough:

- `Activation rate`: started enrollments / total enrollments
- `Engagement rate`: active enrollments / total enrollments
- `Completion rate`: completed enrollments / total enrollments
- `Drop-off rate`: non-completed enrollments / total enrollments
- `Day 30 retention`: returning enrollments at Day 30 / eligible enrollments
- `Multi-checkpoint return rate`: distinct returning learner-course pairs across Days 1, 7, 14, and 30 / total enrollments
- `Average satisfaction`: average `satisfaction_score`

## About the visitor metric

There is no observed visitors table in the dataset.

To support a simple top-of-funnel view, the project defines a derived visitor baseline in SQL:

- `derived visitors = learners * 2.2`

This is a reporting assumption, not an observed acquisition metric. It is useful as a lightweight funnel scaffold, but it should not be treated as a hard business KPI in the same way as completion or Day 30 retention.

## Current supportable readout

From the current generated dataset:

- 4,200 learners
- 10 courses
- 6,800 enrollments
- 40.85% completion rate
- 59.15% non-completion rate
- 34.68% Day 30 retention
- 53.76% multi-checkpoint return rate
- 3.23 average satisfaction

The clearest pattern in the funnel is early loss between enrollment and course start. Once learners reach active learning, the remaining drop is much smaller.

## What the project supports well

- LMS funnel reporting
- course-level performance comparison
- device, region, and age-group cuts
- retention reporting by checkpoint
- exportable reporting tables for BI use

## What should be read more cautiously

- visitor-based funnel conversion, because the visitor baseline is derived
- highly granular segment rankings, because some cells are very small
- causal language about why learners drop or why a feature would improve outcomes

## Run instructions

```bash
pip install -r requirements.txt
python scripts/generate_lms_data.py
python scripts/run_analysis.py
```

After running:

- the SQLite database is created at `data/jozication_lms_analytics.db`
- base tables and analysis exports are written to `exports/`
- the narrative snapshot is written to `docs/analysis_summary.md`

## Portfolio value

This project is useful as a portfolio piece because it shows:

- SQL-based product analysis
- synthetic dataset design
- KPI definition and metric naming
- reporting-layer exports
- a clear line from data model to stakeholder-facing walkthrough
