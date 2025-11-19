#!/usr/bin/env python3
# =============================================================================
# File: indexer.py
# =============================================================================

import os, hashlib

def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

def ingest_directory(conn, folder, exclude_folders, exclude_exts, cfg):
    for root, dirs, files in os.walk(folder):
        if any(ex in root for ex in exclude_folders):
            continue
        for fname in files:
            ext = os.path.splitext(fname)[1].lower()
            if ext in exclude_exts:
                continue
            fpath = os.path.join(root, fname)
            file_hash = sha256_file(fpath)

            existing = conn.execute("SELECT id FROM documents WHERE hash=?", (file_hash,)).fetchone()
            if existing:
                # Insert a second row marked duplicate
                conn.execute(
                    "INSERT INTO documents (filepath, filename, is_duplicate, status, category) VALUES (?, ?, 1, 'indexed', 'Uncategorized')",
                    (fpath, fname),
                )
            else:
                conn.execute(
                    "INSERT INTO documents (filepath, filename, hash, is_duplicate, status, category) VALUES (?, ?, ?, 0, 'indexed', 'Uncategorized')",
                    (fpath, fname, file_hash),
                )
    conn.commit()

# end of script