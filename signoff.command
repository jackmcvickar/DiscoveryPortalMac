#!/bin/bash
# =============================================================================
# File: signoff.command
# Purpose: Double-clickable macOS launcher for signoff.sh
# =============================================================================

# Open project root
cd ~/DiscoveryPortalMac || exit 1

# Source the signoff script so it runs in this shell
source signoff.sh

# Keep the terminal open after running
exec $SHELL

# end of script