CREATE TABLE IF NOT EXISTS runs (
    run_id UUID PRIMARY KEY,
    task_id TEXT,
    status TEXT NOT NULL,
    request_json JSONB NOT NULL,
    result_json JSONB,
    error_message TEXT,
    prompt_version TEXT,
    correlation_id TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    started_at TIMESTAMPTZ,
    completed_at TIMESTAMPTZ
);

CREATE TABLE IF NOT EXISTS evidence (
    evidence_id BIGSERIAL PRIMARY KEY,
    run_id UUID NOT NULL REFERENCES runs(run_id),
    document_id TEXT NOT NULL,
    chunk_id TEXT NOT NULL,
    page_number INTEGER,
    clause_id TEXT,
    retrieved_query TEXT,
    retrieval_score DOUBLE PRECISION,
    passage_text TEXT,
    verification_status TEXT
);

CREATE TABLE IF NOT EXISTS agent_events (
    event_id BIGSERIAL PRIMARY KEY,
    run_id UUID NOT NULL REFERENCES runs(run_id),
    agent_name TEXT NOT NULL,
    step_name TEXT,
    event_type TEXT NOT NULL,
    tool_name TEXT,
    tool_input JSONB,
    tool_output_summary TEXT,
    duration_ms DOUBLE PRECISION,
    success BOOLEAN,
    error_type TEXT,
    prompt_version TEXT,
    input_tokens INTEGER,
    output_tokens INTEGER,
    estimated_cost DOUBLE PRECISION,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS feedback (
    feedback_id BIGSERIAL PRIMARY KEY,
    run_id UUID NOT NULL REFERENCES runs(run_id),
    satisfactory BOOLEAN NOT NULL,
    reason TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);