#!/usr/bin/env python3
# =============================================================================
# File: session_log.py
# Purpose: Append entries to both daily rollup and unique per-session log files
# =============================================================================

import os
import sys
from datetime import datetime
from dda.config import load_config

cfg = load_config()
LOG_DIR = cfg["log_dir"]

SESSION_ID = datetime.now().strftime("%Y%m%d-%H%M%S")

def log_entry(message):
    os.makedirs(LOG_DIR, exist_ok=True)

    today = datetime.now().strftime("%Y-%m-%d")
    daily_file = os.path.join(LOG_DIR, f"session_{today}.txt")
    session_file = os.path.join(LOG_DIR, f"session_{SESSION_ID}.txt")

    timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    entry = f"{timestamp} [SESSION {SESSION_ID}] {message}"

    for target in [daily_file, session_file]:
        with open(target, "a") as f:
            f.write(entry + "\n")

    print(f"📄 Logged to {daily_file} and {session_file}: {entry}")

def main():
    if len(sys.argv) < 2:
        print("⚠️ Usage: session_log.py <message>")
        return
    message = sys.argv[1]
    log_entry(message)

if __name__ == "__main__":
    main()

# end of script