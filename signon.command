#!/bin/bash
# =============================================================================
# File: signon.command
# Purpose: Double-clickable macOS launcher for signon.sh
# =============================================================================

# Open project root
cd ~/DiscoveryPortalMac || exit 1

# Source the signon script so environment stays active
source signon.sh

# Keep the terminal open after running
exec $SHELL

# end of script