CREATE TABLE miniml_file (
    id SERIAL PRIMARY KEY,
    path TEXT NOT NULL UNIQUE
);

CREATE TABLE series (
    id SERIAL PRIMARY KEY,
    miniml_file_id INTEGER NOT NULL REFERENCES miniml_file (id),
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
    description TEXT NULL,
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
    local_path TEXT,
    attempt_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    success BOOLEAN NOT NULL DEFAULT FALSE,
    error_message TEXT
);

CREATE TABLE extraction_failure (
    id SERIAL PRIMARY KEY,
    miniml_file_id INTEGER NOT NULL REFERENCES miniml_file (id),
    error_message TEXT NOT NULL,
    attempt_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
