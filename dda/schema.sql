-- =============================================================================
-- File: schema.sql
-- Purpose: Define canonical schema for ./Data/dda.db
-- =============================================================================

-- Documents table: tracks every file and its extraction status
CREATE TABLE IF NOT EXISTS documents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    filepath TEXT UNIQUE NOT NULL,
    status TEXT CHECK(status IN ('pending','complete','error')) NOT NULL DEFAULT 'pending'
);

-- Checkpoints table: records batch progress for resumable/continuous extraction
CREATE TABLE IF NOT EXISTS checkpoints (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    last_doc_id INTEGER,
    batch_num INTEGER,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Optional: index for faster lookups by status
CREATE INDEX IF NOT EXISTS idx_documents_status ON documents(status);

-- Optional: index for faster lookups by filepath
CREATE INDEX IF NOT EXISTS idx_documents_filepath ON documents(filepath);

-- end of file