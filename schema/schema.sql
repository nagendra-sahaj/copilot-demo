CREATE TABLE IF NOT EXISTS clients (
    client_id VARCHAR PRIMARY KEY,
    client_name VARCHAR NOT NULL,
    industry VARCHAR NOT NULL,
    region VARCHAR NOT NULL,
    tier VARCHAR NOT NULL,
    annual_revenue_usd BIGINT NOT NULL
);

CREATE TABLE IF NOT EXISTS issues (
    issue_id VARCHAR PRIMARY KEY,
    client_id VARCHAR NOT NULL REFERENCES clients(client_id),
    title VARCHAR NOT NULL,
    description VARCHAR NOT NULL,
    category VARCHAR NOT NULL,
    severity VARCHAR NOT NULL,
    status VARCHAR NOT NULL,
    created_date DATE NOT NULL,
    resolved_date DATE,
    revenue_impact_usd BIGINT NOT NULL DEFAULT 0,
    business_impact_description VARCHAR NOT NULL,
    business_scenario VARCHAR,
    resolution_notes VARCHAR
);

CREATE TABLE IF NOT EXISTS features (
    feature_id VARCHAR PRIMARY KEY,
    title VARCHAR NOT NULL,
    description VARCHAR NOT NULL,
    category VARCHAR NOT NULL,
    status VARCHAR NOT NULL,
    requested_by_clients INTEGER NOT NULL DEFAULT 0,
    revenue_generation_usd BIGINT NOT NULL DEFAULT 0,
    complexity VARCHAR NOT NULL,
    priority_score FLOAT NOT NULL DEFAULT 0.0,
    target_quarter VARCHAR,
    release_date DATE
);

CREATE TABLE IF NOT EXISTS feedback (
    feedback_id VARCHAR PRIMARY KEY,
    client_id VARCHAR NOT NULL REFERENCES clients(client_id),
    feature_id VARCHAR REFERENCES features(feature_id),
    feedback_type VARCHAR NOT NULL,
    sentiment VARCHAR NOT NULL,
    submitted_date DATE NOT NULL,
    revenue_opportunity_usd BIGINT NOT NULL DEFAULT 0,
    description VARCHAR NOT NULL
);
