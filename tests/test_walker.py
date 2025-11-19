import os
import tempfile
from dda.fs import walker

def test_sha256_file_and_collect_files(tmp_path):
    # Create a dummy file
    fpath = tmp_path / "sample.txt"
    fpath.write_text("hello world")

    # Hash should be reproducible
    h1 = walker.sha256_file(str(fpath))
    h2 = walker.sha256_file(str(fpath))
    assert h1 == h2

    # Collect files should find it
    files = walker.collect_files(str(tmp_path), exclude_folders=[], exclude_exts=[])
    assert str(fpath) in files

# end of script