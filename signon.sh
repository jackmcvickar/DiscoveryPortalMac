#!/bin/zsh
# =============================================================================
# File: signon.sh
# Purpose: Start session, activate venv, run migration, log session start
# =============================================================================

cd ~/DiscoveryPortalMac
source dda/venv/bin/activate

# Create logs folder if missing
mkdir -p logs

# Timestamp for log file
timestamp=$(date +"%Y%m%d_%H%M%S")
logfile="logs/session_${timestamp}.log"

echo "🔧 Running migration..." | tee -a "$logfile"
python3 dda/modules/migrate.py | tee -a "$logfile"

echo "✅ Session started at $(date)" | tee -a "$logfile"
echo "📊 Log file: $logfile"
# end of script