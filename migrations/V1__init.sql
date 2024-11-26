CREATE TABLE series (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    accession TEXT NOT NULL UNIQUE,
    pubmed_id TEXT,
    summary TEXT NOT NULL,
    type TEXT NOT NULL,
    submission_date DATE NOT NULL,
    release_date DATE NOT NULL,
    last_update_date DATE NOT NULL,
    additional_metadata JSONB
);

CREATE TABLE platform (
    id SERIAL PRIMARY KEY,
    series_id INTEGER NOT NULL REFERENCES series (id),
    title TEXT NOT NULL,
    accession TEXT NOT NULL UNIQUE,
    technology TEXT NOT NULL,
    distribution TEXT NOT NULL,
    organism TEXT NOT NULL,
    description TEXT NOT NULL,
    submission_date DATE NOT NULL,
    release_date DATE NOT NULL,
    last_update_date DATE NOT NULL,
    additional_metadata JSONB
);

CREATE TABLE sample (
    id SERIAL PRIMARY KEY,
    series_id INTEGER NOT NULL REFERENCES series (id),
    title TEXT NOT NULL,
    accession TEXT NOT NULL UNIQUE,
    type TEXT NOT NULL,
    description TEXT NOT NULL,
    submission_date DATE NOT NULL,
    release_date DATE NOT NULL,
    last_update_date DATE NOT NULL,
    additional_metadata JSONB
);

CREATE TABLE download_attempt (
    id SERIAL PRIMARY KEY,
    gse_id TEXT NOT NULL,
    url TEXT NOT NULL,
    attempt_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    success BOOLEAN NOT NULL DEFAULT FALSE,
    error_message TEXT
);