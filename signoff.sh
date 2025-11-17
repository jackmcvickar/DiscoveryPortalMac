#!/bin/zsh
# =============================================================================
# File: signoff.sh
# Purpose: End session, snapshot logs
# =============================================================================

cd ~/DiscoveryPortalMac
source dda/venv/bin/activate

# Use latest log file
latest_log=$(ls -t logs/session_*.log | head -n 1)

echo "📊 Session closed at $(date)" | tee -a "$latest_log"
echo "✅ Snapshot saved to $latest_log"
# end of script