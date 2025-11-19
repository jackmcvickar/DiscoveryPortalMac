#!/usr/bin/env python3
# =============================================================================
# File: config.py
# Purpose: Central configuration loader for DDA scripts
# =============================================================================

import os
import configparser

# Point to config.ini at the project root (one level up from dda/)
CONFIG_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config.ini")

def load_config():
    parser = configparser.ConfigParser()
    parser.read(CONFIG_PATH)

    return {
        "db_path": parser.get("paths", "db_path", fallback="./Data/dda.db"),
        "docs_path": parser.get("paths", "docs_path", fallback="./Docs"),
        "outputs_path": parser.get("paths", "outputs_path", fallback="./Outputs"),
        "logs_path": parser.get("paths", "logs_path", fallback="./logs"),
        "tmp_path": parser.get("paths", "tmp_path", fallback="./tmp"),
        "default_status": parser.get("settings", "default_status", fallback="PENDING"),
    }

def load():
    """Alias for load_config(), for backwards compatibility."""
    return load_config()

# end of script