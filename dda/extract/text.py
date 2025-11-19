import re
import contextlib
import io
import warnings
from PyPDF2.errors import PdfReadWarning
from PyPDF2 import PdfReader
import pdfplumber
from docx import Document
from PIL import Image
import pytesseract

warnings.filterwarnings("ignore", category=PdfReadWarning)

def quiet_pypdf2_extract(fpath):
    text = ""
    with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
        reader = PdfReader(fpath)
        for page in reader.pages[:3]:
            text += page.extract_text() or ""
    return text

def extract_text_from_file(fpath, ext, cfg):
    text = ""
    method_used = None
    try:
        if ext == ".pdf":
            try:
                text = quiet_pypdf2_extract(fpath)
                if text.strip():
                    method_used = "PyPDF2"
            except Exception:
                pass
            if not text.strip():
                try:
                    with pdfplumber.open(fpath) as pdf:
                        for page in pdf.pages[:3]:
                            text += page.extract_text() or ""
                    if text.strip():
                        method_used = "pdfplumber"
                except Exception:
                    pass
        elif ext == ".docx":
            doc = Document(fpath)
            for para in doc.paragraphs[:50]:
                text += para.text + " "
            method_used = "python-docx"
        elif ext in [".jpg", ".jpeg", ".png", ".tif", ".tiff", ".bmp"]:
            if cfg.get("enable_ocr", False):
                img = Image.open(fpath)
                text = pytesseract.image_to_string(img, lang=cfg.get("ocr_lang", "eng"))
                if text.strip():
                    method_used = "OCR"
    except Exception:
        pass
    return text, method_used

# end of script