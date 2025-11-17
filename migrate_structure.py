#!/usr/bin/env python3
# =============================================================================
# File: migrate_structure.py
# Purpose: Flatten dda/dda structure into dda/, move Docs/logs, update shell scripts
# =============================================================================

import os
import shutil

ROOT = os.path.expanduser("~/DiscoveryPortalMac")
DDA_ROOT = os.path.join(ROOT, "dda")
NESTED = os.path.join(DDA_ROOT, "dda")

def move_scripts():
    if os.path.exists(NESTED):
        for fname in ["report.py", "extractor.py", "retry.py", "session_log.py", "config.py"]:
            src = os.path.join(NESTED, fname)
            dst = os.path.join(DDA_ROOT, fname)
            if os.path.exists(src):
                print(f"📂 Moving {src} → {dst}")
                shutil.move(src, dst)

def move_folders():
    for folder in ["Docs", "logs"]:
        nested = os.path.join(NESTED, folder)
        dst = os.path.join(DDA_ROOT, folder)
        root_dup = os.path.join(ROOT, folder)

        if os.path.exists(nested):
            print(f"📂 Moving {nested} → {dst}")
            shutil.move(nested, dst)

        if os.path.exists(root_dup):
            print(f"🗑️ Removing duplicate {root_dup}")
            shutil.rmtree(root_dup)

def update_shell_scripts():
    for fname in ["signon.sh", "signoff.sh"]:
        path = os.path.join(ROOT, fname)
        if os.path.exists(path):
            with open(path, "r") as f:
                content = f.read()
            # Replace nested cd path
            content = content.replace("cd ~/DiscoveryPortalMac/dda/dda", "cd ~/DiscoveryPortalMac/dda")
            # Replace ../session_log.py style with ./session_log.py
            content = content.replace("../session_log.py", "session_log.py")
            content = content.replace("../report.py", "report.py")
            with open(path, "w") as f:
                f.write(content)
            print(f"✏️ Updated {fname}")

def cleanup():
    if os.path.exists(NESTED):
        print(f"🗑️ Removing empty nested folder {NESTED}")
        shutil.rmtree(NESTED)

def main():
    move_scripts()
    move_folders()
    update_shell_scripts()
    cleanup()
    print("✅ Migration complete. Project flattened and cleaned.")

if __name__ == "__main__":
    main()

# end of script