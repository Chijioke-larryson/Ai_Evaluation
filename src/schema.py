"""SQLite schema for the evaluation lab."""

SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS tools (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    provider TEXT NOT NULL DEFAULT '',
    category TEXT NOT NULL DEFAULT '',
    version TEXT NOT NULL DEFAULT '',
    description TEXT NOT NULL DEFAULT '',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    is_demo INTEGER NOT NULL DEFAULT 0 CHECK (is_demo IN (0, 1)),
    UNIQUE(name, provider)
);

CREATE TABLE IF NOT EXISTS experiments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    task_description TEXT NOT NULL DEFAULT '',
    programming_language TEXT NOT NULL DEFAULT 'Python',
    category TEXT NOT NULL,
    difficulty TEXT NOT NULL DEFAULT 'Beginner',
    tool_id INTEGER NOT NULL,
    prompt_text TEXT NOT NULL DEFAULT '',
    generated_response TEXT NOT NULL DEFAULT '',
    expected_behavior TEXT NOT NULL DEFAULT '',
    status TEXT NOT NULL DEFAULT 'Draft',
    execution_time_ms REAL,
    tests_passed INTEGER NOT NULL DEFAULT 0,
    tests_failed INTEGER NOT NULL DEFAULT 0,
    pass_rate REAL,
    reviewer_correctness_score INTEGER,
    reviewer_readability_score INTEGER,
    reviewer_maintainability_score INTEGER,
    reviewer_usefulness_score INTEGER,
    reviewer_documentation_score INTEGER,
    failure_analysis TEXT NOT NULL DEFAULT '',
    limitations TEXT NOT NULL DEFAULT '',
    business_application TEXT NOT NULL DEFAULT '',
    notes TEXT NOT NULL DEFAULT '',
    evaluation_source TEXT NOT NULL DEFAULT '',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    is_demo INTEGER NOT NULL DEFAULT 0 CHECK (is_demo IN (0, 1)),
    FOREIGN KEY (tool_id) REFERENCES tools(id) ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS test_cases (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    experiment_id INTEGER NOT NULL,
    test_name TEXT NOT NULL,
    input_data TEXT NOT NULL DEFAULT '',
    expected_output TEXT NOT NULL DEFAULT '',
    actual_output TEXT NOT NULL DEFAULT '',
    status TEXT NOT NULL DEFAULT 'Not run',
    error_message TEXT NOT NULL DEFAULT '',
    execution_time_ms REAL,
    FOREIGN KEY (experiment_id) REFERENCES experiments(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS research_notes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tool_id INTEGER,
    title TEXT NOT NULL,
    observation TEXT NOT NULL DEFAULT '',
    strengths TEXT NOT NULL DEFAULT '',
    limitations TEXT NOT NULL DEFAULT '',
    potential_use_cases TEXT NOT NULL DEFAULT '',
    source_url TEXT NOT NULL DEFAULT '',
    source_type TEXT NOT NULL DEFAULT 'Personal observation',
    research_date TEXT NOT NULL DEFAULT CURRENT_DATE,
    capabilities TEXT NOT NULL DEFAULT '',
    pricing_notes TEXT NOT NULL DEFAULT '',
    privacy_security_observations TEXT NOT NULL DEFAULT '',
    personal_evaluation_notes TEXT NOT NULL DEFAULT '',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    is_demo INTEGER NOT NULL DEFAULT 0 CHECK (is_demo IN (0, 1)),
    FOREIGN KEY (tool_id) REFERENCES tools(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS business_use_cases (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    business_problem TEXT NOT NULL DEFAULT '',
    proposed_ai_solution TEXT NOT NULL DEFAULT '',
    target_users TEXT NOT NULL DEFAULT '',
    expected_benefit TEXT NOT NULL DEFAULT '',
    risks TEXT NOT NULL DEFAULT '',
    implementation_effort TEXT NOT NULL DEFAULT 'Medium',
    priority TEXT NOT NULL DEFAULT 'Medium',
    validation_status TEXT NOT NULL DEFAULT 'Hypothesis',
    required_human_review TEXT NOT NULL DEFAULT '',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    is_demo INTEGER NOT NULL DEFAULT 0 CHECK (is_demo IN (0, 1))
);

CREATE INDEX IF NOT EXISTS idx_experiments_tool_id ON experiments(tool_id);
CREATE INDEX IF NOT EXISTS idx_experiments_status ON experiments(status);
CREATE INDEX IF NOT EXISTS idx_experiments_category ON experiments(category);
CREATE INDEX IF NOT EXISTS idx_test_cases_experiment_id ON test_cases(experiment_id);
CREATE INDEX IF NOT EXISTS idx_research_notes_tool_id ON research_notes(tool_id);
CREATE INDEX IF NOT EXISTS idx_business_use_cases_priority ON business_use_cases(priority);
"""

