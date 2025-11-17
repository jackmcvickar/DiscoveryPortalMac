import fitz  # PyMuPDF

def parse_pdf(path):
    """
    Parse a PDF file and return (path, text).
    If parsing fails, return (path, 'ERROR: ...').
    """
    try:
        doc = fitz.open(str(path))
        text = "".join([page.get_text() for page in doc])
        return path, text
    except Exception as e:
        return path, f"ERROR: {e}"
# end of script