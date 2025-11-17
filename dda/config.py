#!/usr/bin/env python3
# =============================================================================
# File: config.py
# Purpose: Central configuration loader for DDA scripts
# =============================================================================

import os
import configparser

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config.ini")

def load_config():
    parser = configparser.ConfigParser()
    parser.read(CONFIG_PATH)

    return {
        "db_path": parser.get("paths", "db_path", fallback="./Data/dda.db"),
        "docs_dir": parser.get("paths", "docs_dir", fallback="./Docs"),
        "log_dir": parser.get("paths", "log_dir", fallback="./logs"),
        "default_status": parser.get("settings", "default_status", fallback="PENDING"),
    }

# end of script