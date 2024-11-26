CREATE TABLE series (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    accession TEXT NOT NULL,
    pubmed_id TEXT,
    summary TEXT NOT NULL,
    type TEXT NOT NULL
);
