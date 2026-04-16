from __future__ import annotations

import os
import subprocess


def test_inference_fallback_logs_required_lines() -> None:
    env = os.environ.copy()
    env["ALLOW_HEURISTIC_FALLBACK"] = "1"
    env["ORBITS_DISABLE_DOTENV"] = "1"

    completed = subprocess.run(
        ["python", "inference.py"],
        check=True,
        capture_output=True,
        text=True,
        env=env,
    )
    lines = [line for line in completed.stdout.splitlines() if line.strip()]

    assert any(line.startswith("[START]") for line in lines)
    assert any(line.startswith("[STEP]") for line in lines)
    assert any(line.startswith("[END]") for line in lines)
    assert all(
        line.startswith("[START]") or line.startswith("[STEP]") or line.startswith("[END]")
        for line in lines
    )
