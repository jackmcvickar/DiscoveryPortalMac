#!/usr/bin/env python3
# =============================================================================
# File: pdf_parser.py
# Purpose: Parse PDF files into text
# =============================================================================

from PyPDF2 import PdfReader

def parse_pdf(path):
    """Return (path, text) for a PDF file. On error, return 'ERROR:' message."""
    try:
        reader = PdfReader(path)
        text = "".join(page.extract_text() or "" for page in reader.pages)
        return path, text
    except Exception:
        return path, "ERROR: unable to parse PDF"

# end of script