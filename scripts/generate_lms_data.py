from __future__ import annotations

import math
import random
import sqlite3
from pathlib import Path

import numpy as np
import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
EXPORT_DIR = BASE_DIR / "exports"
SQL_DIR = BASE_DIR / "sql"
DB_PATH = DATA_DIR / "jozication_lms_analytics.db"
SEED = 20260310


def sigmoid(value: float) -> float:
    return 1 / (1 + math.exp(-value))


def get_age_group(age: int) -> str:
    if age < 25:
        return "18-24"
    if age < 35:
        return "25-34"
    if age < 45:
        return "35-44"
    return "45+"


def build_learners(rng: random.Random, count: int = 4200) -> pd.DataFrame:
    regions = {
        "Gauteng": 0.34,
        "Western Cape": 0.18,
        "KwaZulu-Natal": 0.17,
        "Eastern Cape": 0.09,
        "Limpopo": 0.08,
        "Mpumalanga": 0.06,
        "Free State": 0.04,
        "North West": 0.03,
        "Northern Cape": 0.01,
    }
    genders = ["Female", "Male", "Non-binary"]
    gender_weights = [0.51, 0.46, 0.03]
    devices = ["Mobile", "Desktop", "Tablet"]
    device_weights = [0.56, 0.36, 0.08]
    signup_dates = pd.date_range("2024-01-01", "2025-12-31", freq="D")

    learner_rows = []
    signup_options = list(signup_dates)
    region_names = list(regions.keys())
    region_weights = list(regions.values())

    for learner_number in range(1, count + 1):
        age = int(np.clip(rng.gauss(29, 8), 18, 58))
        learner_rows.append(
            {
                "learner_id": f"L{learner_number:05d}",
                "age": age,
                "age_group": get_age_group(age),
                "gender": rng.choices(genders, weights=gender_weights, k=1)[0],
                "region": rng.choices(region_names, weights=region_weights, k=1)[0],
                "device_type": rng.choices(devices, weights=device_weights, k=1)[0],
                "signup_date": pd.Timestamp(rng.choice(signup_options)).date().isoformat(),
            }
        )

    return pd.DataFrame(learner_rows)


def build_courses() -> pd.DataFrame:
    course_rows = [
        ("C001", "Data Literacy for Teams", "Analytics Foundations", "Beginner", 8),
        ("C002", "Excel for Operations", "Productivity", "Beginner", 10),
        ("C003", "SQL for Product Metrics", "Data Analysis", "Intermediate", 18),
        ("C004", "Power BI Storytelling", "Business Intelligence", "Intermediate", 16),
        ("C005", "Product Analytics Fundamentals", "Product Analytics", "Intermediate", 14),
        ("C006", "Python for Reporting Automation", "Data Analysis", "Advanced", 22),
        ("C007", "Cohort Analysis in Practice", "Product Analytics", "Advanced", 20),
        ("C008", "Customer Research for EdTech", "Product Strategy", "Intermediate", 12),
        ("C009", "Experimentation and A/B Testing", "Product Analytics", "Advanced", 24),
        ("C010", "Dashboard Design for Execs", "Business Intelligence", "Beginner", 9),
    ]
    return pd.DataFrame(
        course_rows,
        columns=["course_id", "course_name", "category", "difficulty_level", "duration_hours"],
    )


def build_enrollments(
    learners_df: pd.DataFrame,
    courses_df: pd.DataFrame,
    rng: random.Random,
    target_count: int = 6800,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    difficulty_effect = {"Beginner": 0.45, "Intermediate": 0.0, "Advanced": -0.55}
    device_effect = {"Desktop": 0.18, "Tablet": 0.02, "Mobile": -0.18}
    age_effect = {"18-24": -0.08, "25-34": 0.06, "35-44": 0.12, "45+": 0.03}
    region_effect = {
        "Gauteng": 0.06,
        "Western Cape": 0.04,
        "KwaZulu-Natal": 0.01,
        "Eastern Cape": -0.03,
        "Limpopo": -0.05,
        "Mpumalanga": -0.03,
        "Free State": -0.01,
        "North West": -0.02,
        "Northern Cape": -0.04,
    }
    category_preference = {
        "18-24": ["Product Analytics", "Data Analysis", "Business Intelligence"],
        "25-34": ["Data Analysis", "Product Analytics", "Business Intelligence"],
        "35-44": ["Business Intelligence", "Product Strategy", "Productivity"],
        "45+": ["Productivity", "Business Intelligence", "Analytics Foundations"],
    }

    learners_index = learners_df.set_index("learner_id")
    learner_ids = learners_df["learner_id"].tolist()
    course_lookup = courses_df.to_dict("records")
    analysis_days = [1, 7, 14, 30]

    enrollment_rows: list[dict[str, object]] = []
    retention_rows: list[dict[str, object]] = []
    used_pairs: set[tuple[str, str]] = set()

    while len(enrollment_rows) < target_count:
        learner_id = rng.choice(learner_ids)
        learner = learners_index.loc[learner_id]
        preferred_categories = category_preference[learner["age_group"]]

        weighted_courses = []
        for course in course_lookup:
            weight = 1.0
            if course["category"] == preferred_categories[0]:
                weight = 1.45
            elif course["category"] == preferred_categories[1]:
                weight = 1.2
            elif course["category"] == preferred_categories[2]:
                weight = 1.1
            weighted_courses.append(weight)

        course = rng.choices(course_lookup, weights=weighted_courses, k=1)[0]
        pair = (learner_id, course["course_id"])
        if pair in used_pairs:
            continue
        used_pairs.add(pair)

        signup_ts = pd.Timestamp(learner["signup_date"])
        enrollment_offset = rng.randint(0, 90)
        enrollment_date = signup_ts + pd.Timedelta(days=enrollment_offset)
        if enrollment_date > pd.Timestamp("2025-12-31"):
            enrollment_date = pd.Timestamp("2025-12-31") - pd.Timedelta(days=rng.randint(0, 10))

        start_score = (
            0.55
            + difficulty_effect[course["difficulty_level"]] * 0.3
            + device_effect[learner["device_type"]] * 0.25
            + region_effect[learner["region"]] * 0.15
        )
        started = 1 if rng.random() < min(max(start_score, 0.42), 0.95) else 0

        if started == 0:
            sessions = 0
            hours_spent = 0.0
            progress = 0.0
            active = 0
            completed = 0
            completion_date = None
            dropout_stage = "Enrolled not started"
        else:
            sessions = max(1, int(round(rng.gauss(4.6, 2.4))))
            if learner["device_type"] == "Mobile":
                sessions = max(1, sessions - rng.choice([0, 1]))
            if course["difficulty_level"] == "Advanced":
                sessions = max(1, sessions - rng.choice([0, 1]))

            hours_cap = course["duration_hours"] * rng.uniform(0.35, 1.28)
            hours_spent = round(min(max(rng.gauss(sessions * 1.45, 2.8), 0.8), hours_cap), 1)
            progress_seed = (
                12
                + sessions * 10.5
                + hours_spent * 1.35
                + difficulty_effect[course["difficulty_level"]] * 18
                + device_effect[learner["device_type"]] * 12
                + age_effect[learner["age_group"]] * 9
            )
            progress = round(float(np.clip(progress_seed + rng.gauss(0, 10), 4, 100)), 1)
            active = 1 if sessions >= 3 and progress >= 20 else 0

            completion_score = (
                -2.25
                + progress / 23
                + sessions * 0.18
                + hours_spent / max(course["duration_hours"], 1) * 1.5
                + difficulty_effect[course["difficulty_level"]]
                + device_effect[learner["device_type"]] * 0.9
                + age_effect[learner["age_group"]] * 0.5
            )
            completed = 1 if rng.random() < sigmoid(completion_score) else 0

            if completed:
                progress = round(float(np.clip(max(progress, rng.uniform(86, 100)), 86, 100)), 1)
                active = 1
                sessions = max(sessions, rng.randint(6, 14))
                min_hours = course["duration_hours"] * 0.75
                max_hours = course["duration_hours"] * 1.2
                hours_spent = round(max(hours_spent, rng.uniform(min_hours, max_hours)), 1)
                completion_gap = rng.randint(8, 80)
                completion_date = (enrollment_date + pd.Timedelta(days=completion_gap)).date().isoformat()
                dropout_stage = None
            else:
                completion_date = None
                if progress < 10:
                    dropout_stage = "Dropped after enrollment"
                elif progress < 25:
                    dropout_stage = "Dropped after first lesson"
                elif progress < 60:
                    dropout_stage = "Dropped mid-course"
                else:
                    dropout_stage = "Active no completion" if active == 1 else "Dropped late-course"

        if started == 0:
            satisfaction = round(rng.uniform(1.0, 2.6), 1)
        else:
            satisfaction_base = (
                1.6
                + progress / 35
                + completed * 0.7
                + active * 0.2
                + sessions * 0.03
                + device_effect[learner["device_type"]] * 0.3
                + difficulty_effect[course["difficulty_level"]] * 0.18
            )
            satisfaction = round(float(np.clip(satisfaction_base + rng.gauss(0, 0.35), 1, 5)), 1)

        enrollment_rows.append(
            {
                "enrollment_id": f"E{len(enrollment_rows) + 1:05d}",
                "learner_id": learner_id,
                "course_id": course["course_id"],
                "enrollment_date": enrollment_date.date().isoformat(),
                "started_course_flag": started,
                "active_flag": active,
                "completed_flag": completed,
                "completion_date": completion_date,
                "progress_percent": progress,
                "sessions_count": sessions,
                "hours_spent": hours_spent,
                "dropout_stage": dropout_stage,
                "satisfaction_score": satisfaction,
            }
        )

        retention_anchor = (
            0.68
            + completed * 0.18
            + active * 0.12
            + min(sessions, 10) * 0.012
            + device_effect[learner["device_type"]] * 0.18
            + difficulty_effect[course["difficulty_level"]] * 0.1
        )
        day_decay = {1: 0.0, 7: -0.14, 14: -0.24, 30: -0.37}
        for day in analysis_days:
            returned = 1 if started == 1 and rng.random() < min(max(retention_anchor + day_decay[day], 0.06), 0.95) else 0
            retention_rows.append(
                {
                    "event_id": f"R{len(retention_rows) + 1:06d}",
                    "learner_id": learner_id,
                    "course_id": course["course_id"],
                    "activity_date": (enrollment_date + pd.Timedelta(days=day)).date().isoformat(),
                    "days_since_enrollment": day,
                    "returned_flag": returned,
                }
            )

    return pd.DataFrame(enrollment_rows), pd.DataFrame(retention_rows)


def write_sqlite(
    learners_df: pd.DataFrame,
    courses_df: pd.DataFrame,
    enrollments_df: pd.DataFrame,
    retention_df: pd.DataFrame,
) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    schema_sql = (SQL_DIR / "01_schema.sql").read_text(encoding="utf-8")
    with sqlite3.connect(DB_PATH) as connection:
        connection.executescript(schema_sql)
        learners_df.to_sql("learners", connection, if_exists="append", index=False)
        courses_df.to_sql("courses", connection, if_exists="append", index=False)
        enrollments_df.to_sql("enrollments", connection, if_exists="append", index=False)
        retention_df.to_sql("retention_events", connection, if_exists="append", index=False)


def export_base_csvs(
    learners_df: pd.DataFrame,
    courses_df: pd.DataFrame,
    enrollments_df: pd.DataFrame,
    retention_df: pd.DataFrame,
) -> None:
    EXPORT_DIR.mkdir(parents=True, exist_ok=True)
    learners_df.to_csv(EXPORT_DIR / "learners.csv", index=False)
    courses_df.to_csv(EXPORT_DIR / "courses.csv", index=False)
    enrollments_df.to_csv(EXPORT_DIR / "enrollments.csv", index=False)
    retention_df.to_csv(EXPORT_DIR / "retention_events.csv", index=False)


def main() -> None:
    random.seed(SEED)
    np.random.seed(SEED)
    rng = random.Random(SEED)

    learners_df = build_learners(rng)
    courses_df = build_courses()
    enrollments_df, retention_df = build_enrollments(learners_df, courses_df, rng)

    write_sqlite(learners_df, courses_df, enrollments_df, retention_df)
    export_base_csvs(learners_df, courses_df, enrollments_df, retention_df)

    print(f"Created database at {DB_PATH}")
    print(f"Learners: {len(learners_df)}")
    print(f"Courses: {len(courses_df)}")
    print(f"Enrollments: {len(enrollments_df)}")
    print(f"Retention events: {len(retention_df)}")


if __name__ == "__main__":
    main()
