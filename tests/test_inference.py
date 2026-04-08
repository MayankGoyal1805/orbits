from __future__ import annotations

import subprocess


def test_inference_fallback_logs_required_lines() -> None:
    completed = subprocess.run(
        ["python", "inference.py"],
        check=True,
        capture_output=True,
        text=True,
    )
    lines = [line for line in completed.stdout.splitlines() if line.strip()]

    assert any(line.startswith("[START]") for line in lines)
    assert any(line.startswith("[STEP]") for line in lines)
    assert any(line.startswith("[END]") for line in lines)
    assert all(
        line.startswith("[START]") or line.startswith("[STEP]") or line.startswith("[END]")
        for line in lines
    )
