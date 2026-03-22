# Jozication LMS Analytics

Portfolio project focused on the data and analytics layer of a learning management system. The project frames the analyst role as a data professional supporting product and business decisions across the learner journey: enrollment, activation, engagement, retention, completion, drop-off, satisfaction, course performance, and learner segmentation.

## Project Overview

Jozication LMS Analytics is a synthetic but realistic LMS product analytics project built for a data analyst or product analyst portfolio. It uses Python, SQLite, SQL, and Power BI-ready CSV outputs to model learner behaviour and answer practical product questions in an EdTech setting.

The project does not build learner-facing product features. It focuses on the analytics assets a data professional would create: structured data, KPI logic, SQL analysis, export tables, and dashboard planning.

## Business Problem

An LMS product team wants better visibility into learner performance across the product funnel:

Visitor -> Enrollment -> First Lesson / Activation -> Active Learning / Engagement -> Completion

The business needs to understand:
- How efficiently visitors become enrollments
- Where activation and drop-off happen
- Which learner segments perform differently
- Which courses underperform
- How retention changes over time
- How behaviour influences satisfaction

## Analyst Role Framing

This project positions the analyst as a cross-functional partner to product, growth, learner success, and leadership teams. The analyst is responsible for:
- Designing a reusable LMS-style dataset
- Defining KPI logic in a consistent way
- Building a relational data model
- Writing SQL queries for recurring product analysis
- Exporting Power BI-ready reporting tables
- Translating findings into business recommendations

## Tech Stack

- Python
- SQLite
- pandas
- NumPy
- SQL
- Power BI-ready CSV exports

## Project Structure

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

## Dataset Overview

The project uses exactly 4 analytical tables:

### 1. learners
- `learner_id`
- `age`
- `age_group`
- `gender`
- `region`
- `device_type`
- `signup_date`

### 2. courses
- `course_id`
- `course_name`
- `category`
- `difficulty_level`
- `duration_hours`

### 3. enrollments
- `enrollment_id`
- `learner_id`
- `course_id`
- `enrollment_date`
- `started_course_flag`
- `active_flag`
- `completed_flag`
- `completion_date`
- `progress_percent`
- `sessions_count`
- `hours_spent`
- `dropout_stage`
- `satisfaction_score`

### 4. retention_events
- `event_id`
- `learner_id`
- `course_id`
- `activity_date`
- `days_since_enrollment`
- `returned_flag`

## Synthetic Data Logic

The generator intentionally models realistic LMS behaviour:
- Some learners sign up but never enroll
- Some learners enroll but never start
- Some learners drop after the first lesson
- Some learners drop mid-course
- Some learners remain active without completing
- Some learners complete successfully
- Advanced courses have lower completion odds
- More sessions and more hours spent increase the probability of completion
- Higher progress tends to improve satisfaction
- Mobile learners face a modest completion and engagement penalty relative to desktop learners
- Retention decays from Day 1 to Day 30

## Relational Data Model

- `learners` is linked to `enrollments` by `learner_id`
- `courses` is linked to `enrollments` by `course_id`
- `retention_events` links back to the learner-course enrollment grain through `learner_id` and `course_id`

The analytical grain of the project is mostly learner-course enrollment, with retention measured at selected return intervals.

## Visitor Assumption

There is no physical visitors table by design. To support the required funnel KPI, the project defines a derived visitors metric in the analysis layer:

- `visitors = learners * 2.2`

This assumption represents anonymous site traffic that is directionally larger than registered learners. It keeps enrollment rate measurable without expanding the dataset beyond the requested LMS tables.

## KPI Definitions

These definitions are implemented exactly as required:

- Enrollment Rate = enrollments / visitors
- Activation Rate = started learners / enrolled learners
- Engagement Rate = active learners / enrolled learners
- Completion Rate = completed learners / enrolled learners
- Drop-off Rate = non-completed learners / enrolled learners
- Retention Rate = returning learners / enrolled learners
- Satisfaction Score = average satisfaction_score

## Analysis Questions Covered

1. Executive KPI summary
2. Learner funnel analysis
3. Enrollment trend analysis
4. Engagement analysis
5. Retention analysis
6. Cohort retention analysis
7. Course performance analysis
8. Learner segmentation analysis
9. Satisfaction analysis
10. Drop-off analysis

## SQL Assets

The `sql/` folder contains modular queries for:
- KPI summary
- Funnel analysis
- Enrollment and completion trends
- Engagement patterns
- Retention rates
- Cohort retention
- Course performance
- Segmentation analysis
- Satisfaction analysis
- Drop-off analysis

## Python Assets

### `scripts/generate_lms_data.py`
- Creates the synthetic LMS dataset
- Builds the SQLite database
- Exports base tables as CSV

### `scripts/run_analysis.py`
- Executes SQL analysis outputs
- Creates Power BI-ready reporting CSVs
- Produces `docs/analysis_summary.md`

## Summary of Findings

The generated data consistently shows a realistic LMS pattern:
- Enrollment volume is healthy, but completion is materially lower than activation
- Drop-off concentrates after early learning and mid-course stages
- Harder courses underperform beginner courses on completion and satisfaction
- More sessions and more hours spent strongly correlate with completion
- Mobile learners trail desktop learners on engagement and completion
- Day 30 retention is substantially lower than Day 1 retention, which is typical of course-based products

See `docs/analysis_summary.md` for the run-specific snapshot generated from the current dataset.

## Power BI Dashboard Plan

Recommended dashboard pages:
1. Executive Overview
2. Learner Funnel
3. Engagement Analysis
4. Retention Analysis
5. Course Performance
6. Learner Segmentation

Detailed visual guidance is provided in `docs/power_bi_dashboard_guide.md`.

## Portfolio Value

This project is built to demonstrate practical analyst capability for EdTech and digital product roles:
- SQL for business analysis
- Python-based data generation and analysis
- KPI design and metric governance
- Product funnel thinking
- Retention and cohort analysis
- Course and learner segmentation
- Power BI storytelling readiness

It is suitable as a GitHub portfolio project because it shows end-to-end thinking from raw data generation to reporting outputs and stakeholder-facing insights.

## Exported CSV Output Paths

Core tables:
- `exports/learners.csv`
- `exports/courses.csv`
- `exports/enrollments.csv`
- `exports/retention_events.csv`

Reporting tables:
- `exports/kpi_summary.csv`
- `exports/funnel_analysis.csv`
- `exports/monthly_enrollment_completion_trends.csv`
- `exports/monthly_visitors_enrollment_rate.csv`
- `exports/engagement_analysis.csv`
- `exports/retention_rates.csv`
- `exports/cohort_retention.csv`
- `exports/course_performance.csv`
- `exports/segmentation_analysis.csv`
- `exports/satisfaction_analysis.csv`
- `exports/dropoff_analysis.csv`
- `exports/completion_by_region.csv`
- `exports/completion_by_age_group.csv`
- `exports/completion_by_device_type.csv`
- `exports/sessions_distribution.csv`
- `exports/progress_distribution.csv`
- `exports/returning_learner_trend.csv`
- `exports/dropout_by_course.csv`
- `exports/dropout_by_device_type.csv`
- `exports/dropout_by_age_group.csv`

## Run Instructions

```bash
pip install -r requirements.txt
python scripts/generate_lms_data.py
python scripts/run_analysis.py
```

After running:
- SQLite database will be created at `data/jozication_lms_analytics.db`
- Base tables and analytics outputs will be created in `exports/`
- Narrative summary will be written to `docs/analysis_summary.md`
- Power BI planning notes will be available in `docs/power_bi_dashboard_guide.md`
