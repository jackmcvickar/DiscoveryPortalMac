#!/bin/bash
# Entry point for DiscoveryPortalMac pipeline

# Activate virtual environment
source "$(dirname "$0")/dda/venv/bin/activate"

# Run the document loader, which now reads paths from config.ini
python -m dda.modules.document_loader "$@"
# end of script