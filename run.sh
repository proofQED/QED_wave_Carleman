#!/usr/bin/env bash
# ============================================================
# run.sh — Search → Verify → Verdict loop
#
# Usage:  ./run.sh [max_iterations]
#
# Searches for a candidate (psi, s, alpha, lambda) that satisfies
# all conditions in problem.tex, using three Claude agents in a loop.
# ============================================================

set -euo pipefail

# ============================================================
# Activate conda environment
# ============================================================
eval "$($(dirname "$(which conda)" 2>/dev/null || echo "$HOME/miniconda3/bin")/conda shell.bash hook 2>/dev/null)" || eval "$($HOME/miniconda3/bin/conda shell.bash hook 2>/dev/null)"
conda activate wave

# ============================================================
# Configuration
# ============================================================
MAX_ITERATIONS=${1:-15}
PROJECT_ROOT="$(cd "$(dirname "$0")" && pwd)"
CANDIDATES_DIR="$PROJECT_ROOT/candidates"
PROMPTS_DIR="$PROJECT_ROOT/prompts"
LOG_FILE="$PROJECT_ROOT/candidates/orchestrate_log.txt"
FAILED_APPROACHES="$PROJECT_ROOT/candidates/failed_approaches.md"
BEST_SO_FAR="$PROJECT_ROOT/candidates/best_so_far.md"
STATUS_FILE="$PROJECT_ROOT/candidates/AUTO_RUN_STATUS.md"
PROBLEM_TEX="$PROJECT_ROOT/problem.tex"

CLAUDE_FLAGS="--dangerously-skip-permissions --verbose --output-format stream-json"

START_TIME=$(date '+%Y-%m-%d %H:%M:%S')

# ============================================================
# Ensure directories exist
# ============================================================
mkdir -p "$CANDIDATES_DIR"

# ============================================================
# Initialize accumulated state files
# ============================================================
if [ ! -f "$FAILED_APPROACHES" ]; then
    cat > "$FAILED_APPROACHES" << 'EOF'
# Failed Approaches Log

This file accumulates all previously tried candidates and why they failed.
The search agent should read this to avoid repeating dead ends.

---

EOF
fi

if [ ! -f "$BEST_SO_FAR" ]; then
    cat > "$BEST_SO_FAR" << 'EOF'
# Best Candidate So Far

No candidates tried yet.
EOF
fi

# ============================================================
# Logging helpers
# ============================================================
log() {
    local msg="[$(date '+%H:%M:%S')] $1"
    echo "$msg"
    echo "$msg" >> "$LOG_FILE"
}

update_status() {
    local iteration=$1
    local step=$2
    local state=$3
    local details=$4

    cat > "$STATUS_FILE" << EOF
# Wave PINN Candidate Search — Auto Status

| Field | Value |
|-------|-------|
| **Status** | $state |
| **Current Iteration** | $iteration / $MAX_ITERATIONS |
| **Current Step** | $step |
| **Started At** | $START_TIME |
| **Last Updated** | $(date '+%Y-%m-%d %H:%M:%S') |
| **PID** | $$ |

## Current Activity
$details
EOF
}

append_failed_approach() {
    local round_num=$1
    local candidate_file=$2
    local report_file=$3

    cat >> "$FAILED_APPROACHES" << EOF

## Round $round_num

### Candidate
\`\`\`python
$(cat "$candidate_file" 2>/dev/null || echo "File not found")
\`\`\`

### Why it failed
$(grep -A 50 "## Failure Analysis" "$report_file" 2>/dev/null || echo "No failure analysis available")

---

EOF
}

# ============================================================
# Claude invocation helpers (matching lean project pattern)
#
# Each call saves the full raw JSON stream to a per-step file
# in the round directory, AND extracts a human-readable summary
# (tool calls, tool outputs, assistant text, result) to the
# main log + terminal.
# ============================================================

# run_claude: stream output, save raw JSON, log tool use + results
#   $1 = prompt
#   $2 = raw JSON output path (optional; defaults to /dev/null)
run_claude() {
    local prompt="$1"
    local raw_log="${2:-/dev/null}"

    claude $CLAUDE_FLAGS -p "$prompt" 2>&1 | tee "$raw_log" | while IFS= read -r line; do
        local type
        type=$(echo "$line" | jq -r '.type // empty' 2>/dev/null) || true
        case "$type" in
            assistant)
                # Log tool calls with name + input summary
                echo "$line" | jq -r '
                    .message.content[]? |
                    if .type == "tool_use" then
                        ">>> Tool: \(.name)" +
                        (if .name == "Bash" then
                            "\n    command: " + (.input.command // "" | .[0:300])
                        elif .name == "Write" or .name == "Edit" then
                            "\n    file: " + (.input.file_path // "")
                        elif .name == "Read" then
                            "\n    file: " + (.input.file_path // "")
                        else "" end)
                    elif .type == "text" then
                        .text
                    else empty end
                ' 2>/dev/null || true
                ;;
            tool)
                # Log tool results (truncated to 500 chars)
                echo "$line" | jq -r '
                    "<<< Tool result (" + (.name // "unknown") + "):\n" +
                    (.result // "" | .[0:500]) +
                    (if ((.result // "") | length) > 500 then "\n    ... (truncated)" else "" end)
                ' 2>/dev/null || true
                ;;
            result)
                local result
                result=$(echo "$line" | jq -r '.result // empty') || true
                local cost
                cost=$(echo "$line" | jq -r '.total_cost_usd // "N/A"') || true
                local duration_ms
                duration_ms=$(echo "$line" | jq -r '.duration_ms // 0') || true
                local duration_s=$(( duration_ms / 1000 ))
                echo "$result"
                echo "--- Cost: \$$cost | Duration: ${duration_s}s ---"
                ;;
        esac
    done | tee -a "$LOG_FILE"
}

# run_claude_capture: silent run, save raw JSON, return only final result
#   $1 = prompt
#   $2 = raw JSON output path (optional; defaults to temp file)
run_claude_capture() {
    local prompt="$1"
    local raw_log="${2:-}"
    local tmpfile
    tmpfile=$(mktemp)

    claude $CLAUDE_FLAGS -p "$prompt" > "$tmpfile" 2>&1

    # Save raw JSON if path provided
    if [ -n "$raw_log" ]; then
        cp "$tmpfile" "$raw_log"
    fi

    # Log human-readable summary to stderr + LOG_FILE
    cat "$tmpfile" | while IFS= read -r line; do
        local type
        type=$(echo "$line" | jq -r '.type // empty' 2>/dev/null) || true
        case "$type" in
            assistant)
                echo "$line" | jq -r '
                    .message.content[]? |
                    if .type == "tool_use" then
                        ">>> Tool: \(.name)"
                    elif .type == "text" then
                        .text
                    else empty end
                ' 2>/dev/null || true
                ;;
            result)
                local result
                result=$(echo "$line" | jq -r '.result // empty') || true
                echo "$result"
                ;;
        esac
    done | tee -a "$LOG_FILE" >&2

    # Extract and return the result
    local result
    result=$(grep '"type":"result"' "$tmpfile" 2>/dev/null | tail -1 | jq -r '.result // empty') || true
    rm -f "$tmpfile"
    echo "$result"
}

# ============================================================
# Render prompts with Jinja2 (no sed, no placeholder collisions)
# ============================================================
render_prompts() {
    local round_num=$1
    python3 "$PROJECT_ROOT/render_prompts.py" "$round_num" "$PROJECT_ROOT" "$MAX_ITERATIONS"
}

# ============================================================
# Main loop
# ============================================================
log "=========================================="
log "Starting candidate search loop"
log "Max iterations: $MAX_ITERATIONS"
log "Project root: $PROJECT_ROOT"
log "=========================================="

for i in $(seq 1 "$MAX_ITERATIONS"); do
    ROUND_DIR="$CANDIDATES_DIR/round_$i"
    mkdir -p "$ROUND_DIR"

    log ""
    log "============ ROUND $i / $MAX_ITERATIONS ============"

    # ----------------------------------------------------------
    # Step 0: Render prompts with Jinja2 for this round
    # ----------------------------------------------------------
    RENDERED_DIR=$(render_prompts "$i")
    log "Rendered prompts to $RENDERED_DIR"

    # ----------------------------------------------------------
    # Step 1: Search Agent — propose a candidate
    # ----------------------------------------------------------
    update_status "$i" "1/3 Search" "RUNNING" "Search agent proposing candidate..."
    log "Step 1: Running search agent..."

    run_claude "Load task from $RENDERED_DIR/prompt_search.md. This is round $i of $MAX_ITERATIONS. Follow all instructions in that file." \
        "$ROUND_DIR/AUTO_LOG_SEARCH.jsonl"

    if [ ! -f "$ROUND_DIR/candidate.py" ]; then
        log "ERROR: Search agent did not produce $ROUND_DIR/candidate.py"
        update_status "$i" "1/3 Search" "ERROR" "No candidate file produced"
        continue
    fi
    log "Search agent produced candidate."

    # ----------------------------------------------------------
    # Step 2: Verify Agent — run verification
    # ----------------------------------------------------------
    update_status "$i" "2/3 Verify" "RUNNING" "Verify agent running checks..."
    log "Step 2: Running verify agent..."

    run_claude "Load task from $RENDERED_DIR/prompt_verify.md. This is round $i. Follow all instructions in that file." \
        "$ROUND_DIR/AUTO_LOG_VERIFY.jsonl"

    if [ ! -f "$ROUND_DIR/verification_report.md" ]; then
        log "ERROR: Verify agent did not produce verification report"
        update_status "$i" "2/3 Verify" "ERROR" "No report produced"
        # Still append to failed approaches
        append_failed_approach "$i" "$ROUND_DIR/candidate.py" "/dev/null"
        continue
    fi
    log "Verify agent produced report."

    # ----------------------------------------------------------
    # Step 3: Verdict Agent — DONE or CONTINUE
    # ----------------------------------------------------------
    update_status "$i" "3/3 Verdict" "RUNNING" "Verdict agent deciding..."
    log "Step 3: Running verdict agent..."

    VERDICT_OUTPUT=$(run_claude_capture "Load task from $RENDERED_DIR/prompt_verdict.md. Follow all instructions in that file. Reply with exactly one word: DONE or CONTINUE." \
        "$ROUND_DIR/AUTO_LOG_VERDICT.jsonl")
    DECISION=$(echo "$VERDICT_OUTPUT" | tail -1)

    log "Iteration $i: Decision is '$DECISION'"

    if [[ "$DECISION" == *"DONE"* ]]; then
        log ""
        log "=========================================="
        log "SUCCESS! Candidate found in round $i."
        log "Candidate: $ROUND_DIR/candidate.py"
        log "Report: $ROUND_DIR/verification_report.md"
        log "=========================================="

        update_status "$i" "COMPLETE" "DONE" "Candidate found! See round_$i/"

        # Copy winning candidate to top level
        cp "$ROUND_DIR/candidate.py" "$CANDIDATES_DIR/winning_candidate.py"
        cp "$ROUND_DIR/verification_report.md" "$CANDIDATES_DIR/winning_report.md"

        echo ""
        echo "=========================================="
        echo "SUCCESS — all conditions satisfied."
        echo "Winning candidate: $CANDIDATES_DIR/winning_candidate.py"
        echo "=========================================="
        exit 0
    fi

    # CONTINUE — record failure and move on
    log "Verdict: CONTINUE — recording failed approach."
    append_failed_approach "$i" "$ROUND_DIR/candidate.py" "$ROUND_DIR/verification_report.md"

    # Update best-so-far tracking
    PASS_COUNT=$(grep -c "True" "$ROUND_DIR/verification_report.md" 2>/dev/null || echo "0")
    cat >> "$BEST_SO_FAR" << EOF

## Round $i
- Conditions passing: ~$PASS_COUNT mentions of True
- Candidate: $ROUND_DIR/candidate.py
- Report: $ROUND_DIR/verification_report.md
EOF

    update_status "$i" "COMPLETE" "CONTINUE" "Round $i done. Moving to round $((i+1))."

    # Brief pause between rounds
    sleep 2
done

# Max iterations reached without success
log ""
log "=========================================="
log "FAILED: Max iterations ($MAX_ITERATIONS) reached without finding a valid candidate."
log "See $FAILED_APPROACHES for all attempts."
log "See $BEST_SO_FAR for the best candidate found."
log "=========================================="

update_status "$MAX_ITERATIONS" "COMPLETE" "FAILED" "Max iterations reached. No valid candidate found."
exit 1
