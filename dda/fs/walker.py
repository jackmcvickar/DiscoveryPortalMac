import os
import hashlib

def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

def collect_files(root_dir, exclude_folders, exclude_exts):
    files = []
    for dirpath, _, fnames in os.walk(root_dir):
        if any(excl in dirpath for excl in exclude_folders):
            continue
        for fname in fnames:
            ext = os.path.splitext(fname)[1].lower()
            if ext in exclude_exts or fname.startswith(".") or fname.endswith("dda.db"):
                continue
            files.append(os.path.join(dirpath, fname))
    return files

# end of script