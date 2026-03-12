# Verify Agent: Run Verification on a Candidate

## Environment Setup
Before running any Python command, always activate the conda environment first:
```bash
conda activate wave
```

## Your Role
You are a verification agent. Your task is to run the verification engine on a proposed candidate and produce a structured, detailed report.

## Instructions

1. **Run the verification engine** on the candidate file:
   ```bash
   conda activate wave && cd /local/home/cyanz/wave_PINN && python3 verify_engine.py /local/home/cyanz/wave_PINN/candidates/round_5/candidate.py
   ```

2. **Also run the JSON output** for machine-readable results:
   ```bash
   conda activate wave && cd /local/home/cyanz/wave_PINN && python3 verify_engine.py /local/home/cyanz/wave_PINN/candidates/round_5/candidate.py --json
   ```

3. **Read the candidate file** at `/local/home/cyanz/wave_PINN/candidates/round_5/candidate.py` to understand what ψ and parameters were proposed.

4. **Read the candidate's reasoning log** at `/local/home/cyanz/wave_PINN/candidates/round_5/candidate_log.md` (if it exists) to understand the search agent's intent.

5. **Write a structured verification report** to `/local/home/cyanz/wave_PINN/candidates/round_5/verification_report.md` with this exact format:

```markdown
# Verification Report — Round 5

## Candidate Summary
- psi = <expression>
- alpha = <value>
- s = <value>
- lambda = <value>
- Other params: <if any>

## Condition Results

### Necessary Condition 1: L₁ψ ≤ Lψ ≤ −L₁ψ
- Status: <True / False / unknown>
- Condition 1a (L − L₁ ≥ 0): <True / False / unknown>
- Condition 1b (−L₁ − L ≥ 0): <True / False / unknown>
- Symbolic expression (1a): <expression>
- Symbolic expression (1b): <expression>
- Numerical sampling: <result if applicable>
- Diagnosis: <why it fails or is unknown, what the dominant terms are>

### Necessary Condition 2: lim(x→+∞) λψ = +∞
- Status: <True / False / unknown>
- λψ = <expression>
- Limit value: <value>
- Diagnosis: <explanation>

### Necessary Condition 3: L₂ψ ≥ 0
- Status: <True / False / unknown>
- Symbolic expression: <expression>
- Numerical sampling: <result if applicable>
- Diagnosis: <why it fails or is unknown>

### Sufficient Condition: (L₁ψ)² − (Lψ)² ≥ c²(φ_xt)²
- Status: <True / False / unknown>
- Symbolic expression: <expression>
- Numerical sampling: <result if applicable>
- Diagnosis: <explanation>

## Overall Summary
- Necessary condition 1: <status>
- Necessary condition 2: <status>
- Necessary condition 3: <status>
- All necessary conditions: <status>
- Sufficient condition: <status>
- **ALL CONDITIONS PASS: <True / False>**

## Failure Analysis
<For each failed or unknown condition, explain what went wrong and what
mathematical property the candidate would need to have to fix it.
This section is critical — the search agent will read it to improve
the next candidate.>
```

IMPORTANT:
- Run the verification engine EXACTLY as specified. Do not modify verify_engine.py or the candidate file.
- If the engine crashes, report the error in the verification report.
- The failure analysis section is the most important part — it guides the next search iteration.
- Be precise about which terms dominate and why conditions fail.
- When showing that the candidate satisfy the sufficient condition, be extra careful, put your verification in solid math work that can pass all peer reviews.