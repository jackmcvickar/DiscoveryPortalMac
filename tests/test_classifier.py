import pytest
from dda.modules import classifier

def test_classify_document_credit_card():
    filepath = "/root/No. 17 - Credit Cards/USAA/2022/file.pdf"
    status, category, account_id = classifier.classify_document(filepath)
    assert status == "Processed"
    assert category == "Credit Cards"
    assert account_id == "USAA"

def test_classify_document_error_file():
    filepath = "/root/error_report.pdf"
    status, category, account_id = classifier.classify_document(filepath)
    assert status == "Error"
# end of script