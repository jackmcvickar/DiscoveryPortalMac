#!/usr/bin/env python3
# =============================================================================
# File: progress.py
# Purpose: Central progress utilities for DDA scripts
# =============================================================================

from tqdm import tqdm

def wrap(iterable, desc="Progress"):
    """
    Wrap an iterable with a tqdm progress bar.
    Example:
        for item in wrap(items, desc="Indexing"):
            ...
    """
    return tqdm(iterable, desc=desc)

# end of script