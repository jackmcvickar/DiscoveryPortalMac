# dda/modules/document_loader.py

def load_document(file_path: str) -> bytes:
    """
    Load a document from disk.
    For now, just read raw bytes. Later you can expand to handle PDFs, images, etc.
    """
    with open(file_path, "rb") as f:
        return f.read()

# end of script