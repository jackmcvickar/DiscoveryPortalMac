#!/usr/bin/env python3
# =============================================================================
# File: session_log.py
# Purpose: Append sign-on/sign-off entries into daily rollover log files
# =============================================================================

import os
import sys
from datetime import datetime

# Ensure logs directory exists
LOG_DIR = os.path.join(os.path.dirname(__file__), "logs")
os.makedirs(LOG_DIR, exist_ok=True)

def main():
    if len(sys.argv) < 2:
        print("Usage: session_log.py <message>")
        sys.exit(1)

    message = sys.argv[1]
    now = datetime.now()

    # Daily rollover filename
    log_filename = f"session_{now.strftime('%Y-%m-%d')}.txt"
    log_path = os.path.join(LOG_DIR, log_filename)

    # Format entry with timestamp
    entry = f"[{now.strftime('%Y-%m-%d %H:%M:%S')}] {message}\n"

    # Append to daily log file
    with open(log_path, "a") as f:
        f.write(entry)

    print(f"📄 Logged to {log_path}: {entry.strip()}")

if __name__ == "__main__":
    main()

# end of script