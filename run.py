#!/usr/bin/env python3
# =============================================================================
# File: run.py
# Purpose: Single entry point for DiscoveryPortalMac workflow
# Features: Daily logs + automatic DB backup + forced Git commit + Git tag + Git push + Session IDs
# =============================================================================

import subprocess
import sys
import os
import shutil
import uuid
from datetime import datetime

ROOT = os.path.dirname(os.path.abspath(__file__))
PYTHON = sys.executable

# Ensure logs and backups folders exist
LOG_DIR = os.path.join(ROOT, "logs")
BACKUP_DIR = os.path.join(ROOT, "backups")
os.makedirs(LOG_DIR, exist_ok=True)
os.makedirs(BACKUP_DIR, exist_ok=True)

# Daily log file (one per day)
today = datetime.now().strftime("%Y%m%d")
LOG_FILE = os.path.join(LOG_DIR, f"session_{today}.log")

DB_PATH = os.path.join(ROOT, "Data", "dda.db")

# Generate a unique session ID (UUID shortened)
SESSION_ID = str(uuid.uuid4())[:8]

def run_and_log(label, script):
    """Run a Python module and append output to daily log file."""
    print(f"▶️ {label}...")
    with open(LOG_FILE, "a") as f:
        f.write(f"\n--- {label} ({datetime.now()}, ID: {SESSION_ID}) ---\n")
        subprocess.run([PYTHON, os.path.join(ROOT, script)], stdout=f, stderr=f)
    print(f"✅ {label} complete (logged).")

def migrate():
    run_and_log("Migration", "dda/modules/migrate.py")

def loader():
    run_and_log("Loader", "dda/modules/loader.py")

def extractor():
    run_and_log("Extractor", "dda/modules/extractor.py")

def retry():
    run_and_log("Retry", "dda/modules/retry.py")

def dashboard():
    run_and_log("Dashboard", "dda/modules/dashboard.py")

def signon():
    with open(LOG_FILE, "a") as f:
        f.write(f"\n=== Session started at {datetime.now()} (ID: {SESSION_ID}) ===\n")
    migrate()
    print(f"✅ Session started (log: {LOG_FILE}, ID: {SESSION_ID})")

def signoff():
    # Append closing marker to log
    with open(LOG_FILE, "a") as f:
        f.write(f"\n=== Session closed at {datetime.now()} (ID: {SESSION_ID}) ===\n")

    # Backup DB with daily snapshot
    backup_file = None
    if os.path.exists(DB_PATH):
        backup_file = os.path.join(BACKUP_DIR, f"db_{today}_{SESSION_ID}.db")
        shutil.copy2(DB_PATH, backup_file)
        print(f"📦 Database backup saved to {backup_file}")
    else:
        print("⚠️ No database found to back up.")

    # Git commit logs + backup (force add even if ignored)
    try:
        subprocess.run(["git", "add", "-f", LOG_FILE], check=True)
        if backup_file:
            subprocess.run(["git", "add", "-f", backup_file], check=True)
        commit_msg = f"Session snapshot {today} [ID: {SESSION_ID}]"
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)

        # Add Git tag for this session
        tag_name = f"session-{today}-{SESSION_ID}"
        subprocess.run(["git", "tag", "-f", tag_name], check=True)

        # Push commits and tags to remote
        subprocess.run(["git", "push", "origin", "main"], check=True)
        subprocess.run(["git", "push", "origin", "--tags"], check=True)

        print(f"📝 Git commit + tag pushed: {commit_msg} ({tag_name})")
    except Exception as e:
        print(f"⚠️ Git commit/tag/push failed: {e}")

    print(f"📊 Session closed. Snapshot saved to {LOG_FILE}")

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 run.py [signon|signoff|loader|extractor|retry|dashboard]")
        sys.exit(1)

    cmd = sys.argv[1].lower()
    if cmd == "signon":
        signon()
    elif cmd == "signoff":
        signoff()
    elif cmd == "loader":
        loader()
    elif cmd == "extractor":
        extractor()
    elif cmd == "retry":
        retry()
    elif cmd == "dashboard":
        dashboard()
    else:
        print(f"⚠️ Unknown command: {cmd}")

if __name__ == "__main__":
    main()

# end of script