#!/bin/bash
# =============================================================================
# File: cleanup_dbs.sh
# Purpose: Enforce canonical DB path ./Data/dda.db and remove redundant DBs
# =============================================================================

cd ~/DiscoveryPortalMac || exit 1

CANONICAL="./Data/dda.db"

# Check canonical DB exists
if [ ! -f "$CANONICAL" ]; then
  echo "❌ Canonical DB not found at $CANONICAL"
  exit 1
fi

# Remove redundant DBs
for REDUNDANT in "./Data/dda.db" "./Data/dda.db"; do
  if [ -f "$REDUNDANT" ]; then
    rm "$REDUNDANT"
    echo "🗑️ Removed redundant DB: $REDUNDANT"
  fi
done

echo "✅ Canonical DB enforced at $CANONICAL"

# end of script
