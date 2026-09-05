# Wave Carleman — Automated Weight Function Search

The project's former internal name was `wave_PINN`, which still appears in the archived records and Python files.

**Model used:** This archived run mainly used Claude Opus 4.6 (`claude-opus-4-6`).

This repository is an instance of an early development version of **QED**, specialized to searching for a weight function for a Carleman estimate. For the current system, see the [QED repository](https://github.com/proofQED/QED). The associated paper is [QED: An Open-Source Multi-Agent System for Generating Mathematical Proofs on Open Problems](https://openreview.net/forum?id=EPCNlZRUc3).

> The early development run archived here used **7 rounds**. With a more advanced version of QED and a more capable model, the same problem is expected to require only 1 round.

Automated search for a weight function for a Carleman estimate using a three-agent loop: **Search**, **Verify**, **Verdict**.

Given the wave operator `□u = u_tt − c² u_xx`, the pipeline finds `ψ(x,t)`, `s`, `α`, `λ` such that a set of necessary and sufficient conditions hold on `[0,∞) × [0,T]`. The full problem is defined in `problem.tex`.

## Prerequisites

```bash
conda activate wave
```

The `wave` conda environment must contain: `python 3.12+`, `numpy`, `sympy`, `jinja2`.

To create it:
```bash
conda create -y -n wave python=3.12 numpy sympy jinja2
```

Additionally, the following CLI tools must be on `$PATH`:
- `claude` — [Claude Code CLI](https://github.com/anthropics/claude-code)
- `jq` — JSON processor

## Quick Start

```bash
cd /path/to/wave_Carleman  # replace with your checkout location
./run.sh          # default 15 iterations
./run.sh 30       # custom max iterations
```

## Pipeline Overview

```
┌──────────────────────────────────────────────────────────┐
│                     run.sh (orchestrator)                 │
│                                                          │
│  for round in 1..max_iterations:                         │
│                                                          │
│    ┌─────────────────────────────────────────────────┐   │
│    │ Step 0: Render prompts (Jinja2)                 │   │
│    │   render_prompts.py round_N project_root max    │   │
│    │   → candidates/round_N/prompt_search.md         │   │
│    │   → candidates/round_N/prompt_verify.md         │   │
│    │   → candidates/round_N/prompt_verdict.md        │   │
│    └─────────────────────────────────────────────────┘   │
│                          │                               │
│    ┌─────────────────────▼───────────────────────────┐   │
│    │ Step 1: Search Agent (Claude)                   │   │
│    │   reads: problem.tex, failed_approaches.md,     │   │
│    │          prev round's verification_report.md    │   │
│    │   writes: candidates/round_N/candidate.py       │   │
│    │           candidates/round_N/candidate_log.md   │   │
│    └─────────────────────────────────────────────────┘   │
│                          │                               │
│    ┌─────────────────────▼───────────────────────────┐   │
│    │ Step 2: Verify Agent (Claude)                   │   │
│    │   runs: python3 verify_engine.py candidate.py   │   │
│    │   writes: candidates/round_N/                   │   │
│    │           verification_report.md                │   │
│    └─────────────────────────────────────────────────┘   │
│                          │                               │
│    ┌─────────────────────▼───────────────────────────┐   │
│    │ Step 3: Verdict Agent (Claude)                  │   │
│    │   reads: verification_report.md                 │   │
│    │   outputs: DONE or CONTINUE                     │   │
│    └─────────────────────────────────────────────────┘   │
│                          │                               │
│         DONE ──► exit 0 (copy winning candidate)         │
│         CONTINUE ──► append to failed_approaches.md      │
│                       └──► next round                    │
└──────────────────────────────────────────────────────────┘
```

### Agent Details

**Search Agent** — Proposes a candidate `ψ(x,t)` and parameters `(s, α, λ)`. It reads the problem definition, all previously failed approaches, and the previous round's verification report to avoid repeating mistakes and to fix specific failing conditions.

**Verify Agent** — Runs `verify_engine.py` on the candidate (both human-readable and JSON modes), reads the output, and writes a structured verification report with per-condition status (True / False / unknown), symbolic expressions, numerical sampling results, and a failure analysis section diagnosing what went wrong.

**Verdict Agent** — Reads the verification report and outputs exactly one word: `DONE` (all 4 conditions = True) or `CONTINUE` (any condition is False or unknown).

## File Structure

The checked-in `candidates/` files preserve the original seven-round search, including its reasoning, verification reports, and execution logs. The root-level `tmp_*.py` files contain exploratory mathematical analyses and are retained as research records. Historical prompts and logs contain paths from the original machine; `run.sh` renders new prompts for the current checkout before each round. `clean.sh` deletes the archived rounds and winning outputs, so use it only when intentionally resetting the search.

```
wave_Carleman/
│
│  # ── Problem definition ──
├── problem.tex               # LaTeX: full problem statement with operator definitions
│
│  # ── Verification engine ──
├── verify_engine.py          # Symbolic + numerical verification of candidates
│                             #   CLI: python3 verify_engine.py <candidate.py> [--json]
│                             #   Checks all 4 conditions, returns structured results
├── verify.py                 # Original standalone verifier (kept for reference)
│
│  # ── Prompt templates (Jinja2) ──
├── prompts/
│   ├── search.md             # Search agent template — {{ problem_tex }}, {{ candidate_file }}, etc.
│   ├── verify.md             # Verify agent template — {{ project_root }}, {{ candidate_file }}, etc.
│   └── verdict.md            # Verdict agent template — {{ verification_report }}
│
│  # ── Orchestration ──
├── render_prompts.py         # Jinja2 renderer: fills templates with real paths per round
├── run.sh                    # Main loop: render → search → verify → verdict
│
│  # ── Candidates (archived run and runtime outputs) ──
└── candidates/
    ├── example_candidate.py  # Example candidate (for testing the engine)
    │
    │  # ── Created by run.sh per round ──
    ├── round_1/
    │   ├── prompt_search.md          # Rendered search prompt (all paths filled in)
    │   ├── prompt_verify.md          # Rendered verify prompt
    │   ├── prompt_verdict.md         # Rendered verdict prompt
    │   ├── candidate.py              # Written by search agent
    │   ├── candidate_log.md          # Written by search agent (reasoning)
    │   └── verification_report.md    # Written by verify agent
    ├── round_2/
    │   └── ...
    ├── round_N/
    │   └── ...
    │
    │  # ── Accumulated state ──
    ├── failed_approaches.md          # All failed candidates + why they failed
    ├── best_so_far.md                # Tracks best candidate across rounds
    ├── orchestrate_log.txt           # Full execution log
    ├── AUTO_RUN_STATUS.md            # Live status (current round, step, PID)
    │
    │  # ── Final output (on success) ──
    ├── winning_candidate.py          # Copy of the passing candidate
    └── winning_report.md             # Copy of the passing verification report
```

## Input / Output Reference

### Inputs (static, created before running)

| File | Description |
|------|-------------|
| `problem.tex` | Full problem definition: operators □, ˜□, L, L₁, L₂, conditions, notation |
| `prompts/search.md` | Jinja2 template for the search agent |
| `prompts/verify.md` | Jinja2 template for the verify agent |
| `prompts/verdict.md` | Jinja2 template for the verdict agent |
| `verify_engine.py` | Verification engine (deterministic, not modified at runtime) |

### Outputs (generated at runtime)

| File | Created by | Description |
|------|-----------|-------------|
| `candidates/round_N/candidate.py` | Search agent | Defines `psi` and `subs_dict` |
| `candidates/round_N/candidate_log.md` | Search agent | Mathematical reasoning for the candidate |
| `candidates/round_N/verification_report.md` | Verify agent | Structured report with all condition statuses |
| `candidates/round_N/prompt_*.md` | `render_prompts.py` | Rendered prompts with real paths |
| `candidates/failed_approaches.md` | `run.sh` | Accumulates all failed candidates and failure analyses |
| `candidates/best_so_far.md` | `run.sh` | Tracks the best candidate found so far |
| `candidates/orchestrate_log.txt` | `run.sh` | Full timestamped execution log |
| `candidates/AUTO_RUN_STATUS.md` | `run.sh` | Live status for monitoring |
| `candidates/winning_candidate.py` | `run.sh` | Final passing candidate (on success) |
| `candidates/winning_report.md` | `run.sh` | Final passing verification report (on success) |

## Candidate File Format

Each candidate is a Python file defining two variables. Symbols (`x`, `t`, `c`, `x0`, `alpha`, `s`, `lam`, `sp`) are injected by `verify_engine.py` at load time — do not import anything.

```python
# Description: quadratic in x with shifted center
psi = t - (x + x0)**2

subs_dict = {
    alpha : 2,
    x0    : c / 2,
    s     : -2,       # must be negative
    lam   : -c**2,
}
```

- `psi` — SymPy expression in `x`, `t`, and optionally auxiliary symbols like `x0`
- `subs_dict` — maps `alpha`, `s`, `lam` (and any auxiliary symbols) to values that may depend on `c`

## Verification Conditions

The engine checks four conditions (all must hold on `[0,∞) × [0,T]`):

| # | Condition | Type |
|---|-----------|------|
| 1 | `L₁ψ ≤ Lψ ≤ −L₁ψ` | Necessary |
| 2 | `lim(x→+∞) λψ = +∞` | Necessary |
| 3 | `L₂ψ ≥ 0` | Necessary |
| 4 | `(L₁ψ)² − (Lψ)² ≥ c²(∂²ₓₜφ)²` | Sufficient |

Each condition is checked symbolically (SymPy). If SymPy returns `unknown`, numerical sampling on a grid of `(x, t, c)` values is used as a fallback.

## Running verify_engine.py Standalone

```bash
conda activate wave

# Human-readable output
python3 verify_engine.py candidates/example_candidate.py

# JSON output
python3 verify_engine.py candidates/example_candidate.py --json
```

## Termination

- **Success** (`exit 0`): All 4 conditions return `True`. The winning candidate is copied to `candidates/winning_candidate.py`.
- **Failure** (`exit 1`): Max iterations reached without finding a valid candidate. See `candidates/failed_approaches.md` for all attempts and `candidates/best_so_far.md` for the closest candidate.

## Monitoring a Running Search

While `run.sh` is running:

```bash
# Live status
cat candidates/AUTO_RUN_STATUS.md

# Follow the log
tail -f candidates/orchestrate_log.txt

# Check a specific round's result
cat candidates/round_3/verification_report.md
```

## Citation

If you find this early development instance useful, please cite the QED paper:

Chenyang An, Qihao Ye, Minghao Pan, and Jiayun Zhang. (2026). [QED: An Open-Source Multi-Agent System for Generating Mathematical Proofs on Open Problems](https://openreview.net/forum?id=EPCNlZRUc3).

```bibtex
@inproceedings{
    an2026qed,
    title={{QED}: An Open-Source Multi-Agent System for Generating Mathematical Proofs on Open Problems},
    author={Chenyang An and Qihao Ye and Minghao Pan and Jiayun Zhang},
    booktitle={3rd AI for Math Workshop: Toward Self-Evolving Scientific Agents},
    year={2026},
    url={https://openreview.net/forum?id=EPCNlZRUc3}
}
```
