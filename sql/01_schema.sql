DROP TABLE IF EXISTS retention_events;
DROP TABLE IF EXISTS enrollments;
DROP TABLE IF EXISTS courses;
DROP TABLE IF EXISTS learners;

CREATE TABLE learners (
    learner_id TEXT PRIMARY KEY,
    age INTEGER NOT NULL,
    age_group TEXT NOT NULL,
    gender TEXT NOT NULL,
    region TEXT NOT NULL,
    device_type TEXT NOT NULL,
    signup_date TEXT NOT NULL
);

CREATE TABLE courses (
    course_id TEXT PRIMARY KEY,
    course_name TEXT NOT NULL,
    category TEXT NOT NULL,
    difficulty_level TEXT NOT NULL,
    duration_hours REAL NOT NULL
);

CREATE TABLE enrollments (
    enrollment_id TEXT PRIMARY KEY,
    learner_id TEXT NOT NULL,
    course_id TEXT NOT NULL,
    enrollment_date TEXT NOT NULL,
    started_course_flag INTEGER NOT NULL,
    active_flag INTEGER NOT NULL,
    completed_flag INTEGER NOT NULL,
    completion_date TEXT,
    progress_percent REAL NOT NULL,
    sessions_count INTEGER NOT NULL,
    hours_spent REAL NOT NULL,
    dropout_stage TEXT,
    satisfaction_score REAL,
    FOREIGN KEY (learner_id) REFERENCES learners (learner_id),
    FOREIGN KEY (course_id) REFERENCES courses (course_id)
);

CREATE TABLE retention_events (
    event_id TEXT PRIMARY KEY,
    learner_id TEXT NOT NULL,
    course_id TEXT NOT NULL,
    activity_date TEXT NOT NULL,
    days_since_enrollment INTEGER NOT NULL,
    returned_flag INTEGER NOT NULL,
    FOREIGN KEY (learner_id) REFERENCES learners (learner_id),
    FOREIGN KEY (course_id) REFERENCES courses (course_id)
);
