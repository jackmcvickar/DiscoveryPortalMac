#!/bin/bash
# =============================================================================
# run_test.sh
# Purpose: Automate full pipeline test (reset DB, extract, analyze, dashboard, commit)
#          Adds daily log file + session ID banner for traceability
# =============================================================================

set -e  # stop on first error

# --- Config ---
DB_PATH="Data/dda.db"
START_PERIOD="2024-04"
END_PERIOD="2025-11"
LOG_DIR="logs"
SESSION_ID=$(uuidgen | cut -c1-8)
LOG_FILE="$LOG_DIR/test_$(date +%Y-%m-%d)_$SESSION_ID.txt"

mkdir -p "$LOG_DIR"

# Redirect all output to both console and log file
exec > >(tee -a "$LOG_FILE") 2>&1

echo "🚀 Starting full test run at $(date)"
echo "🆔 Session ID: $SESSION_ID"
echo "📅 Gap Analysis Window: $START_PERIOD -> $END_PERIOD"
echo "📝 Log file: $LOG_FILE"

# --- Reset DB ---
if [ -f "$DB_PATH" ]; then
  rm "$DB_PATH"
  echo "🗑️ Removed old DB at $DB_PATH"
fi

# --- Run extractor ---
echo "📂 Running extractor..."
python3 -m dda.modules.extractor

# --- Verify DB count ---
COUNT=$(sqlite3 "$DB_PATH" "SELECT COUNT(*) FROM documents;")
echo "📊 DB now contains $COUNT documents"

# --- Run gap analysis ---
echo "🔎 Running gap analysis..."
python3 -m dda.modules.gap_analysis --start "$START_PERIOD" --end "$END_PERIOD"

# --- Run dashboard ---
echo "📊 Running dashboard..."
python3 -m dda.reports.dashboard_gap --start "$START_PERIOD" --end "$END_PERIOD"

# --- Stage files for commit ---
echo "📄 Staging CSV snapshot + modified Python files..."
git add reports/gap_analysis_summary_${START_PERIOD}_to_${END_PERIOD}.csv
git add DDA/modules/*.py DDA/reports/*.py run_test.sh || true

# --- Commit + Tag ---
git commit -m "Gap analysis snapshot $SESSION_ID ($START_PERIOD->$END_PERIOD)" || echo "⚠️ Commit skipped (no changes)"
git tag "snapshot-$SESSION_ID"
echo "📌 Git commit + tag created: snapshot-$SESSION_ID"

echo "✅ Test run complete at $(date)"
echo "📝 Log saved to $LOG_FILE"
# end of script