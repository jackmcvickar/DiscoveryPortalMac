#!/usr/bin/env python3
# =============================================================================
# File: pipeline.py
# =============================================================================

import os
from dda.modules import pdf_parser, classifier, status_logger, db_utils

def process_document(file_path: str, db_conn) -> None:
    try:
        status_logger.log_status_message(f"Loaded document: {file_path}")
        path, content = pdf_parser.parse_pdf(file_path)
        status_logger.log_status_message(f"Parsed document: {path}")

        status, category, account_id = classifier.classify_document(file_path)
        status_logger.log_status_message(f"Classified document: {category} ({status})")

        filename = os.path.basename(file_path)
        records = [(file_path, category, status, filename)]
        db_utils.insert_document(records, db_conn)
        status_logger.log_status_message(f"Inserted document into DB: {filename}")

    except Exception as e:
        filename = os.path.basename(file_path)
        records = [(file_path, "Error Report", "error", filename)]
        try:
            db_utils.insert_document(records, db_conn)
        except Exception:
            pass
        status_logger.log_status_message(f"Error processing {file_path}: {e}")

# end of script