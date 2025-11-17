import os
import tempfile
from pathlib import Path
from dda.modules.pdf_parser import parse_pdf
import fitz  # PyMuPDF

def create_temp_pdf(text="Hello World"):
    tmp_fd, tmp_path = tempfile.mkstemp(suffix=".pdf")
    os.close(tmp_fd)
    doc = fitz.open()
    page = doc.new_page()
    page.insert_text((72, 72), text)
    doc.save(tmp_path)
    doc.close()
    return Path(tmp_path)

def test_parse_valid_pdf():
    pdf_path = create_temp_pdf("Unit test content")
    path, content = parse_pdf(pdf_path)
    assert path == pdf_path
    assert "Unit test content" in content
    pdf_path.unlink()

def test_parse_invalid_pdf():
    tmp_fd, tmp_path = tempfile.mkstemp(suffix=".pdf")
    os.close(tmp_fd)
    with open(tmp_path, "w") as f:
        f.write("Not a real PDF")
    path, content = parse_pdf(tmp_path)
    assert path == tmp_path
    assert content.startswith("ERROR:")
    Path(tmp_path).unlink()
# end of script