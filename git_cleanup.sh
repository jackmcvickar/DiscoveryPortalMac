#!/bin/bash
# =============================================================================
# File: git_cleanup.sh
# Purpose: Automate Git cleanup and tag commit (Selective Tracking)
# =============================================================================

cd ~/DiscoveryPortalMac || exit 1

SESSION_ID=$(date +"%Y%m%d-%H%M%S")

# Step 1: Ensure canonical DB is tracked
if [ -f Data/dda.db ]; then
  git add Data/dda.db
  echo "✅ Canonical DB ./Data/dda.db staged"
fi

# Step 2: Stage modifications and deletions of tracked files
git add -u
echo "✅ Modified and deleted tracked files staged"

# Step 3: Stage important untracked files (selective)
git add Docs/ dda/modules/ requirements.txt || true
echo "✅ Important untracked files staged (Docs/, dda/modules/, requirements.txt)"

# Commit everything
git commit -m "Git cleanup: session $SESSION_ID"

# Tag the cleanup commit
git tag "cleanup-$SESSION_ID"

echo "📄 Git cleanup complete. Commit + tag created for session $SESSION_ID"

# end of script