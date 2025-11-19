-- =============================================================================
-- File: schema.sql
-- Purpose: Define canonical schema for ./Data/dda.db with rich metadata
-- =============================================================================

-- Documents table: tracks every file and its extraction status + metadata
CREATE TABLE IF NOT EXISTS documents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category TEXT,                -- folder name (e.g. "2025 Court Prep")
    filepath TEXT UNIQUE NOT NULL,-- absolute path to file
    filename TEXT,                -- base filename
    status TEXT CHECK(status IN ('pending','indexed','complete','error'))
           NOT NULL DEFAULT 'pending',
    confidence REAL,              -- optional confidence score
    last_modified TEXT,           -- ISO timestamp of last modification
    year INTEGER,                 -- optional year extracted
    owner TEXT,                   -- optional owner tag
    account_id TEXT,              -- optional account identifier
    period TEXT,                  -- optional reporting period
    hash TEXT UNIQUE,             -- SHA-256 hash for deduplication
    tags TEXT                     -- derived tags from filename/content
);

-- Checkpoints table: records batch progress for resumable/continuous extraction
CREATE TABLE IF NOT EXISTS checkpoints (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    last_doc_id INTEGER,
    batch_num INTEGER,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for faster lookups
CREATE INDEX IF NOT EXISTS idx_documents_status ON documents(status);
CREATE INDEX IF NOT EXISTS idx_documents_filepath ON documents(filepath);
CREATE INDEX IF NOT EXISTS idx_documents_hash ON documents(hash);
CREATE INDEX IF NOT EXISTS idx_documents_tags ON documents(tags);

-- end of file