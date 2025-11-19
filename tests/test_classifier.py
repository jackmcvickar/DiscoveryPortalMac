#!/usr/bin/env python3
# =============================================================================
# File: test_classifier.py
# Purpose: Validate classifier stub outputs
# =============================================================================

from dda.modules import classifier

def test_classify_document_credit_card():
    filepath = "/root/No. 17 - Credit Cards/USAA/2022/file.pdf"
    status, category, account_id = classifier.classify_document(filepath)
    assert status == "indexed"
    assert category == "Credit Cards"

def test_classify_document_error_file():
    filepath = "/root/error_report.pdf"
    status, category, account_id = classifier.classify_document(filepath)
    assert status == "error"
    assert category == "Error Report"

# end of script