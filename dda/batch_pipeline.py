#!/usr/bin/env python3
# =============================================================================
# File: batch_pipeline.py
# Purpose: Batch processing of a folder of documents
# =============================================================================

import os
from dda.pipeline import process_document
from dda.modules import status_logger

def process_folder(folder_path: str, db_conn) -> None:
    """
    Process all documents in a folder.
    """
    try:
        for root, dirs, files in os.walk(folder_path):
            for fname in files:
                file_path = os.path.join(root, fname)
                status_logger.log_status_message(f"Starting batch process for: {file_path}")
                process_document(file_path, db_conn)
        # Log summary at the end
        status_logger.log_status_summary(db_conn)
    except Exception as e:
        status_logger.log_status_message(f"Error in batch process: {e}")

# end of script