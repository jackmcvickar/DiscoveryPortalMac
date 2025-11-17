import os
from dda.modules import walker

def test_walk_documents_filters(tmp_path):
    docs_dir = tmp_path / "docs"
    docs_dir.mkdir()
    (docs_dir / "file.pdf").write_text("dummy")
    (docs_dir / ".DS_Store").write_text("junk")
    (docs_dir / "script.py").write_text("junk")

    records = walker.walk_documents(str(docs_dir))
    assert any("file.pdf" in r[0] for r in records)
    assert all(".DS_Store" not in r[0] and ".py" not in r[0] for r in records)
# end of script