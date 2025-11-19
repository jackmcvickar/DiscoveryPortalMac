

# Copilot Status – 2025-11-18

## Database
- `documents` table now includes:
  - `tags` TEXT
  - `text_source` TEXT (added via migration)
- Migration script cleans excluded categories from config.ini.
- Verified top categories are meaningful and junk folders removed.

## Ingestion
- Canonical entrypoint: `dda/indexer.py`
- Metadata layers:
  - Category = top-level folder
  - Tags = filename heuristics + content extraction
  - Text extraction methods:
    - PyPDF2 (quiet wrapper)
    - pdfplumber fallback
    - python-docx
    - OCR (if enabled)
- Logging hook reports extraction method per file.
- `text_source` persisted in DB for auditability.

## Outstanding Tasks
- Extend migration to ensure `text_source` column exists in all environments.
- Normalize tags into separate `document_tags` table (future).
- Dashboard queries to show counts by `text_source`.
- Audit ingestion coverage with sample queries.

## Extraction Coverage

To audit which text extraction methods were used during ingestion, run:

```sql
-- Count documents by extraction method
SELECT text_source, COUNT(*) AS doc_count
FROM documents
GROUP BY text_source
ORDER BY doc_count DESC;

-- Example: show top 20 docs where OCR was used
SELECT filename, category, tags
FROM documents
WHERE text_source = 'OCR'
LIMIT 20;

## Dashboard Queries – Extraction Coverage

-- Count documents by extraction method
SELECT text_source, COUNT(*) AS doc_count
FROM documents
GROUP BY text_source
ORDER BY doc_count DESC;

-- Count documents by category × extraction method
SELECT category, text_source, COUNT(*) AS doc_count
FROM documents
GROUP BY category, text_source
ORDER BY category, doc_count DESC;

-- Show top 10 categories with highest OCR usage
SELECT category, COUNT(*) AS ocr_count
FROM documents
WHERE text_source = 'OCR'
GROUP BY category
ORDER BY ocr_count DESC
LIMIT 10;

-- Show sample docs where pdfplumber was used
SELECT filename, category, tags
FROM documents
WHERE text_source = 'pdfplumber'
LIMIT 20;

# end of document

# Copilot Catch-Up Document

## Date: 2025-11-17

---

## Current DB
- Path: /Users/jackmcvickar/DiscoveryPortalMac/Data/dda.db
- Schema: `documents` table defined in `dda/schema.sql`
- Deduplication: enforced via `UNIQUE(hash)` with `ON CONFLICT DO UPDATE`

---

## Active Ingestion
- Entry point: `dda/indexer.py`
- Config source: `config.ini` ([paths], [settings])
- Progress: `dda/progress.py` (clean progress bar)
- Category tagging: folder name used as `category`
- Status field: defaults to `Indexed`

---

## Swift App Integration
- `DBManager.swift` points to same `dda.db`
- `DocumentRepository.swift` queries `documents` table
- `FileIndexer.swift` handles file rows for UI

---

## Reporting & Outputs
- Reports generated in `/reports` (CSV, PNG, XLSX)
- Run logs in `/Outputs` and `/logs`
- Unresolved documents tracked in `unresolved_documents_chunk*.csv`

---

## Architectural Breakout

### Root
- `ingest.py` (debug script, to be retired)
- `pipeline.py` (wrapper/orchestrator)
- `run.py`, `run_dda.sh`, `run_test.sh` (execution scripts)
- `config.ini` (canonical paths/settings)
- `schema.sql` (DB schema definition)
- `reports/` (analytics outputs)
- `Outputs/` (pipeline run logs)
- `logs/` (session logs, loader logs)

### `dda/` package
- `indexer.py` (canonical ingestion loader)
- `pipeline.py`, `batch_pipeline.py` (orchestration)
- `config.py` (config parsing)
- `progress.py` (progress indicator)
- `schema.sql` (canonical schema)
- `document_api.py`, `dashboard_api.py`, `dashboard_queries.py` (APIs)
- `db_schema_inspector.py`, `list_tables.py` (schema introspection)

### Swift App (`DiscoveryPortalMac/`)
- `DBManager.swift` (SQLite integration)
- `DocumentRepository.swift` (queries documents)
- `FileIndexer.swift`, `IndexedFilesView.swift` (UI for indexed files)
- `Models.swift`, `Item.swift`, `Document.swift` (data models)
- `DiscoveryPortalMacApp.swift` (app entrypoint)

### Data
- `dda.db` (canonical DB)
- Subfolders: `2025 Court Prep`, `2025OctAllFilesJack`, `2025OctAllFilesTammy`, `McVickar - Respondent's Discovery Production`

---

## Outstanding Tasks
- Confirm ingestion fully wired into `dda/indexer.py` (retire `ingest.py`)
- Ensure schema bootstrap uses `dda/schema.sql`
- Verify unresolved CSV reconciliation pipeline
- Add batch commit logic using `batch_size` from config.ini

---

## Notes
- Repo hygiene confirmed (no oversized files in Git history)
- `config.ini` is canonical source of paths/settings
- Daily checkpoint doc (`copilot_status.md`) updated here
