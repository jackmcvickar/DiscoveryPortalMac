import tempfile
from dda.extract import text

def test_extract_text_from_pdf(tmp_path):
    # Create a dummy PDF with PyPDF2
    from reportlab.pdfgen import canvas
    pdf_path = tmp_path / "test.pdf"
    c = canvas.Canvas(str(pdf_path))
    c.drawString(100, 750, "Hello PDF")
    c.save()

    cfg = {"enable_ocr": False}
    extracted, method = text.extract_text_from_file(str(pdf_path), ".pdf", cfg)
    assert "Hello PDF" in extracted
    assert method in ("PyPDF2", "pdfplumber")

def test_extract_text_from_docx(tmp_path):
    from docx import Document
    doc_path = tmp_path / "test.docx"
    doc = Document()
    doc.add_paragraph("Hello DOCX")
    doc.save(str(doc_path))

    cfg = {}
    extracted, method = text.extract_text_from_file(str(doc_path), ".docx", cfg)
    assert "Hello DOCX" in extracted
    assert method == "python-docx"

# end of script