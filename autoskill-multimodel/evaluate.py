#!/usr/bin/env python3
"""
Multi-model evaluation harness for autoskill.
Uses counselors CLI to get parallel judgments from multiple AI models.
"""

import json
import os
import re
import subprocess
import tempfile
import time
from pathlib import Path

SKILL_FILE = Path(__file__).parent / "skill.md"
BENCHMARKS_DIR = Path(__file__).parent / "benchmarks"

# Models to use for judging (from counselors ls)
JUDGE_TOOLS = os.environ.get("JUDGE_TOOLS", "claude-opus,codex-5.3-high")


def load_skill() -> str:
    return SKILL_FILE.read_text()


def load_benchmarks() -> list[dict]:
    benchmarks = []
    for path in sorted(BENCHMARKS_DIR.glob("*.md")):
        content = path.read_text()
        benchmarks.append({
            "name": path.stem,
            "content": content,
            "input_code": extract_section(content, "Input Code"),
            "expected": extract_section(content, "Expected Behaviors"),
            "scoring": extract_section(content, "Scoring"),
        })
    return benchmarks


def extract_section(content: str, header: str) -> str:
    pattern = rf"## {header}\s*\n(.*?)(?=\n## |\Z)"
    match = re.search(pattern, content, re.DOTALL)
    return match.group(1).strip() if match else ""


def run_claude(prompt: str) -> str:
    """Run a prompt through Claude CLI (for skill execution)."""
    result = subprocess.run(
        ["claude", "-p", prompt],
        capture_output=True,
        text=True,
        timeout=120,
    )
    if result.returncode != 0:
        raise RuntimeError(f"Claude CLI failed: {result.stderr}")
    return result.stdout.strip()


def run_counselors_judge(prompt: str, tools: str) -> dict[str, float]:
    """
    Run judgment through counselors to get multiple model opinions.
    Returns dict of {model_id: score}.
    """
    # Create temp file for the prompt
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
        f.write(prompt)
        prompt_file = f.name

    try:
        # Use counselors mkdir to set up output directory
        mkdir_result = subprocess.run(
            ["counselors", "mkdir", "--json"],
            input=prompt,
            capture_output=True,
            text=True,
            timeout=30,
        )

        if mkdir_result.returncode != 0:
            raise RuntimeError(f"counselors mkdir failed: {mkdir_result.stderr}")

        mkdir_json = json.loads(mkdir_result.stdout)
        prompt_path = mkdir_json.get("promptFilePath")

        # Run counselors with the prompt
        result = subprocess.run(
            ["counselors", "run", "-f", prompt_path, "--tools", tools, "--json"],
            capture_output=True,
            text=True,
            timeout=300,  # 5 min timeout for multi-model
        )

        if result.returncode != 0:
            raise RuntimeError(f"counselors run failed: {result.stderr}")

        # Parse JSON output to get results
        # Find the JSON in output (may have progress text before it)
        stdout = result.stdout
        json_start = stdout.find('{')
        if json_start == -1:
            raise RuntimeError("No JSON found in counselors output")
        manifest = json.loads(stdout[json_start:])
        scores = {}

        for tool_result in manifest.get("tools", []):
            tool_id = tool_result.get("toolId", "unknown")
            output_file = tool_result.get("outputFile")

            if output_file and Path(output_file).exists():
                output_text = Path(output_file).read_text()
                # Extract score from each model's judgment
                score_match = re.search(r'"score"\s*:\s*([\d.]+)', output_text)
                if score_match:
                    scores[tool_id] = float(score_match.group(1))
                else:
                    # Try to infer from text
                    if "1.0" in output_text or "full score" in output_text.lower():
                        scores[tool_id] = 1.0
                    elif "0.5" in output_text or "partial" in output_text.lower():
                        scores[tool_id] = 0.5
                    else:
                        scores[tool_id] = 0.0

        return scores

    finally:
        os.unlink(prompt_file)


def aggregate_scores(scores: dict[str, float]) -> float:
    """Aggregate multiple model scores into a single score."""
    if not scores:
        return 0.0
    # Use median to be robust to outliers
    sorted_scores = sorted(scores.values())
    n = len(sorted_scores)
    if n % 2 == 0:
        return (sorted_scores[n//2 - 1] + sorted_scores[n//2]) / 2
    return sorted_scores[n//2]


def run_skill(skill: str, code: str) -> str:
    """Run the skill against input code."""
    prompt = f"""You are following these skill instructions:

{skill}

Now apply this skill to the following code:

{code}

Provide your explanation following the skill's output format."""

    return run_claude(prompt)


def judge_output_multimodel(output: str, expected: str, scoring: str, tools: str) -> tuple[float, dict]:
    """Judge the skill output using multiple models via counselors."""
    prompt = f"""You are a strict evaluator. Score the following explanation.

## Expected Behaviors
{expected}

## Scoring Rubric
{scoring}

## Actual Output
{output}

---

Evaluate the output against EACH expected behavior. Be strict but fair.

Respond with ONLY a JSON object:
{{"score": <0.0 or 0.5 or 1.0>, "reasoning": "<brief explanation>"}}"""

    try:
        scores = run_counselors_judge(prompt, tools)
        aggregated = aggregate_scores(scores)
        return aggregated, scores
    except Exception as e:
        print(f"    [counselors failed: {e}, falling back to single model]")
        # Fallback to single Claude call
        text = run_claude(prompt)
        match = re.search(r'"score"\s*:\s*([\d.]+)', text)
        score = float(match.group(1)) if match else 0.0
        return score, {"claude-fallback": score}


def main():
    skill = load_skill()
    benchmarks = load_benchmarks()
    tools = JUDGE_TOOLS

    print(f"Multi-model evaluation using: {tools}")
    print(f"Running {len(benchmarks)} benchmarks...\n")

    total_score = 0.0
    max_score = len(benchmarks)
    times = []
    all_model_scores = []

    for bench in benchmarks:
        start = time.time()

        try:
            # Run skill (single model)
            output = run_skill(skill, bench["input_code"])

            # Judge with multiple models
            score, model_scores = judge_output_multimodel(
                output,
                bench["expected"],
                bench["scoring"],
                tools
            )
            all_model_scores.append(model_scores)

        except Exception as e:
            print(f"[ERROR] {bench['name']}: {e}")
            score = 0.0
            model_scores = {}

        elapsed = time.time() - start
        times.append(elapsed)
        total_score += score

        if score > 0.9:
            status = "PASS"
        elif score > 0.4:
            status = "PARTIAL"
        else:
            status = "FAIL"

        model_str = ", ".join(f"{k}={v}" for k, v in model_scores.items())
        print(f"[{status}] {bench['name']}: {score:.2f} ({elapsed:.1f}s) [{model_str}]")

    pass_rate = total_score / max_score if max_score > 0 else 0.0
    avg_time = sum(times) / len(times) if times else 0.0

    # Calculate per-model agreement
    print("\n---")
    print(f"pass_rate:     {pass_rate:.3f}")
    print(f"total_score:   {total_score:.1f}")
    print(f"max_score:     {max_score:.1f}")
    print(f"benchmarks:    {len(benchmarks)}")
    print(f"avg_time_sec:  {avg_time:.1f}")
    print(f"judge_tools:   {tools}")


if __name__ == "__main__":
    main()
