-- Drop old table if it exists
DROP TABLE IF EXISTS documents;

-- Create documents table with richer schema
CREATE TABLE documents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category TEXT,
    account_id TEXT,
    owner TEXT,
    period TEXT,
    confidence REAL,
    filepath TEXT,
    filesize INTEGER,
    hash TEXT,
    last_modified TEXT,
    account_number_last4 TEXT,
    year TEXT,
    status TEXT,
    filename TEXT
);

-- Helpful indexes for faster lookups
CREATE INDEX idx_documents_status ON documents(status);
CREATE INDEX idx_documents_filepath ON documents(filepath);