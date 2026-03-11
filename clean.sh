#!/usr/bin/env bash
# ============================================================
# clean.sh — Remove all generated files, restore repo to
#             its initial state (before any run.sh execution).
#
# Usage:  ./clean.sh
# ============================================================

set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "$0")" && pwd)"
CANDIDATES_DIR="$PROJECT_ROOT/candidates"

echo "Cleaning generated files in $PROJECT_ROOT ..."

# Round directories (round_1, round_2, …)
rm -rf "$CANDIDATES_DIR"/round_*/

# State files created by run.sh
rm -f "$CANDIDATES_DIR/failed_approaches.md"
rm -f "$CANDIDATES_DIR/best_so_far.md"
rm -f "$CANDIDATES_DIR/orchestrate_log.txt"
rm -f "$CANDIDATES_DIR/AUTO_RUN_STATUS.md"

# Winning output (copied on success)
rm -f "$CANDIDATES_DIR/winning_candidate.py"
rm -f "$CANDIDATES_DIR/winning_report.md"

# Python bytecode caches
find "$PROJECT_ROOT" -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true

echo "Done. Repository is back to its initial state."
