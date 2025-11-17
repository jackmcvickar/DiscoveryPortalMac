#!/bin/bash
# =============================================================================
# File: session.sh
# Purpose: Mark session start and end in logs
# =============================================================================

cd ~/DiscoveryPortalMac

if [ "$1" == "start" ]; then
    python session_log.py "SIGNON: Session started"
    echo "✅ Session start recorded."
elif [ "$1" == "end" ]; then
    python session_log.py "SIGNOFF: Session ended"
    echo "✅ Session end recorded."
else
    echo "Usage: ./session.sh start|end"
fi