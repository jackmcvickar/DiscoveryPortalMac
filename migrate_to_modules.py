#!/usr/bin/env python3
# =============================================================================
# File: migrate_to_modules.py
# Purpose: Restructure dda project into package style with modules subfolder
# =============================================================================

import os
import shutil

ROOT = os.path.expanduser("~/DiscoveryPortalMac")
DDA_ROOT = os.path.join(ROOT, "dda")
MODULES = os.path.join(DDA_ROOT, "modules")

def ensure_modules_folder():
    os.makedirs(MODULES, exist_ok=True)
    init_file = os.path.join(MODULES, "__init__.py")
    if not os.path.exists(init_file):
        open(init_file, "w").close()
        print(f"✅ Created {init_file}")

def move_scripts():
    scripts = ["report.py", "session_log.py", "extractor.py", "retry.py"]
    for fname in scripts:
        src = os.path.join(DDA_ROOT, fname)
        dst = os.path.join(MODULES, fname)
        if os.path.exists(src):
            print(f"📂 Moving {src} → {dst}")
            shutil.move(src, dst)

def update_imports():
    for fname in os.listdir(MODULES):
        if fname.endswith(".py"):
            path = os.path.join(MODULES, fname)
            with open(path, "r") as f:
                content = f.read()
            # Replace old import style
            content = content.replace("from config import load_config",
                                      "from dda.config import load_config")
            with open(path, "w") as f:
                f.write(content)
            print(f"✏️ Updated imports in {fname}")

def main():
    ensure_modules_folder()
    move_scripts()
    update_imports()
    print("✅ Migration complete. Scripts moved into dda/modules and imports updated.")

if __name__ == "__main__":
    main()

# end of script