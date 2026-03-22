#!/usr/bin/env python3
"""
Evaluation harness for autobluebird.
Runs Bluebird (with --calibrate) against NestJS projects listed in manifest.json
and computes a false-positive-weighted objective score.

Usage: uv run autobluebird/evaluate.py
"""

import json
import subprocess
import sys
import time
from pathlib import Path

MANIFEST_FILE = Path(__file__).parent / "manifest.json"


def load_manifest() -> dict:
    return json.loads(MANIFEST_FILE.read_text())


def run_bluebird(project_path: str, bluebird_bin: str, options: dict) -> dict | None:
    """Run bluebird --format json --calibrate on a project and return parsed JSON."""
    cmd = [bluebird_bin, "--format", "json", "--calibrate"]

    if options.get("includeHeuristic"):
        cmd.append("--include-heuristic")
    if options.get("verbose"):
        cmd.append("--verbose")

    cmd.extend(["-p", project_path])

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=600,
        )
    except FileNotFoundError:
        print(f"[ERROR] bluebird binary not found: {bluebird_bin}", file=sys.stderr)
        return None
    except subprocess.TimeoutExpired:
        print(f"[ERROR] bluebird timed out on {project_path}", file=sys.stderr)
        return None

    stdout = result.stdout.strip()
    if not stdout:
        print(f"[ERROR] bluebird produced no output for {project_path}", file=sys.stderr)
        if result.stderr:
            print(f"  stderr: {result.stderr[:500]}", file=sys.stderr)
        return None

    try:
        return json.loads(stdout)
    except json.JSONDecodeError as e:
        print(f"[ERROR] Failed to parse bluebird JSON: {e}", file=sys.stderr)
        return None


def compute_objective(results: list[dict], alpha: float) -> dict:
    """Aggregate per-project results into a single objective metric."""
    if not results:
        return {
            "objective": 0.0,
            "raw_score_avg": 0.0,
            "calibrated_score_avg": 0.0,
            "estimated_fp_rate": 1.0,
            "projects_evaluated": 0,
        }

    raw_scores = []
    calibrated_scores = []
    fp_rates = []

    for r in results:
        raw_scores.append(r.get("score", 0))
        calibration = r.get("calibration")
        if calibration:
            calibrated_scores.append(calibration["calibratedScore"]["score"])
            total = (
                calibration["confirmedCount"]
                + calibration["uncertainCount"]
                + calibration["likelyFalsePositiveCount"]
            )
            fp_rate = calibration["likelyFalsePositiveCount"] / total if total > 0 else 0.0
            fp_rates.append(fp_rate)
        else:
            calibrated_scores.append(r.get("score", 0))
            fp_rates.append(0.0)

    raw_avg = sum(raw_scores) / len(raw_scores)
    cal_avg = sum(calibrated_scores) / len(calibrated_scores)
    fp_avg = sum(fp_rates) / len(fp_rates)

    objective = cal_avg - alpha * (fp_avg * 100)

    return {
        "objective": round(objective, 3),
        "raw_score_avg": round(raw_avg, 3),
        "calibrated_score_avg": round(cal_avg, 3),
        "estimated_fp_rate": round(fp_avg, 4),
        "projects_evaluated": len(results),
    }


def main():
    manifest = load_manifest()
    projects = manifest.get("projects", [])
    bluebird_bin = manifest.get("bluebird_bin", "bluebird")
    alpha = manifest.get("alpha", 0.5)

    if not projects:
        print("[ERROR] No projects defined in manifest.json", file=sys.stderr)
        sys.exit(1)

    valid_projects = [p for p in projects if p.get("path")]
    if not valid_projects:
        print("[ERROR] No projects with valid 'path' in manifest.json", file=sys.stderr)
        print("Set the 'path' field to an absolute path to your NestJS project", file=sys.stderr)
        sys.exit(1)

    print(f"Evaluating {len(valid_projects)} project(s)...\n")

    results = []
    times = []

    for proj in valid_projects:
        name = proj.get("name", proj["path"])
        options = proj.get("options", {})
        start = time.time()

        print(f"  Scanning: {name} ...", end=" ", flush=True)
        output = run_bluebird(proj["path"], bluebird_bin, options)
        elapsed = time.time() - start
        times.append(elapsed)

        if output is None:
            print(f"FAIL ({elapsed:.1f}s)")
            continue

        results.append(output)
        score = output.get("score", "?")
        diag_count = output.get("diagnosticCount", "?")
        cal = output.get("calibration", {})
        fp_count = cal.get("likelyFalsePositiveCount", 0) if cal else 0
        print(f"score={score} diags={diag_count} fp={fp_count} ({elapsed:.1f}s)")

    metrics = compute_objective(results, alpha)

    print("\n---")
    print(f"objective:              {metrics['objective']:.3f}")
    print(f"raw_score_avg:          {metrics['raw_score_avg']:.3f}")
    print(f"calibrated_score_avg:   {metrics['calibrated_score_avg']:.3f}")
    print(f"estimated_fp_rate:      {metrics['estimated_fp_rate']:.4f}")
    print(f"projects_evaluated:     {metrics['projects_evaluated']}")
    print(f"avg_time_sec:           {sum(times) / len(times):.1f}" if times else "avg_time_sec:           0.0")


if __name__ == "__main__":
    main()
