from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from statistics import mean

from openai import OpenAI

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import inference


def _load_dataset_strategy_notes() -> list[str]:
    priors_path = Path("src/orbits_env/tasks/task_priors.json")
    if not priors_path.exists():
        return []
    try:
        payload = json.loads(priors_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return []

    stats = payload.get("dataset_stats", {})
    debris_ratio = float(stats.get("debris_ratio", 0.5))
    leo_ratio = float(stats.get("leo_ratio", 0.5))
    risk_scale = float(stats.get("risk_scale", 1.0))
    uncertainty_scale = float(stats.get("uncertainty_scale", 1.0))

    notes = [
        f"Dataset prior: debris ratio is {debris_ratio:.2f}; prioritize early risk reduction.",
        f"Dataset prior: LEO ratio is {leo_ratio:.2f}; expect dense conjunction pressure.",
        f"Dataset prior: risk scale is {risk_scale:.2f}; avoid passive noop under moderate/high risk.",
        f"Dataset prior: uncertainty scale is {uncertainty_scale:.2f}; spend tracking budget early when uncertainty remains high.",
    ]
    return notes


def _reflection_notes(round_results: list[dict]) -> list[str]:
    notes: list[str] = []
    failed = [result for result in round_results if not result["success"]]

    if failed:
        notes.append(
            "Adaptive note: if highest_collision_probability exceeds 0.22, avoid noop and use moderate maneuver magnitude (0.45 to 0.6)."
        )

    if any(result["tracking_updates_used"] == 0 and result["highest_collision_probability"] > 0.2 for result in round_results):
        notes.append(
            "Adaptive note: use request_tracking_update early when uncertainty is elevated and tracking budget is available."
        )

    if any(result["total_offset_km"] > 1.45 for result in round_results):
        notes.append(
            "Adaptive note: cap aggressive maneuvering once total_offset_km exceeds 1.4 unless immediate collision risk is high."
        )

    if any(result["termination_reason"] == "horizon_reached" for result in round_results):
        notes.append(
            "Adaptive note: prioritize the top-risk event and reduce it below threshold before broad balancing maneuvers."
        )

    return notes


def _summarize_round(round_index: int, results: list[dict]) -> dict:
    avg_score = float(mean(result["score"] for result in results)) if results else 0.0
    avg_reward = float(mean(result["total_reward"] for result in results)) if results else 0.0
    success_rate = (sum(1 for result in results if result["success"]) / len(results)) if results else 0.0

    summary = {
        "round": round_index,
        "avg_score": round(avg_score, 4),
        "avg_total_reward": round(avg_reward, 4),
        "success_rate": round(success_rate, 4),
        "tasks": results,
    }
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description="Run iterative self-improvement inference rounds.")
    parser.add_argument("--rounds", type=int, default=3, help="Number of iterative rounds to run.")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("outputs/evals/iterative_inference_results.json"),
        help="Output JSON for per-round summaries.",
    )
    args = parser.parse_args()

    client = OpenAI(base_url=inference.API_BASE_URL, api_key=inference.API_KEY) if inference.API_KEY else None
    strategy_memory = _load_dataset_strategy_notes()
    all_rounds: list[dict] = []

    for round_idx in range(1, args.rounds + 1):
        print(f"[ROUND] index={round_idx} strategy_notes={len(strategy_memory)}", flush=True)
        round_results: list[dict] = []

        for task_id in inference.TASK_IDS:
            result = inference.run_task(
                task_id=task_id,
                client=client,
                strategy_memory=strategy_memory,
                emit_logs=True,
            )
            round_results.append(result)

        summary = _summarize_round(round_idx, round_results)
        all_rounds.append(summary)
        print(
            f"[ROUND-END] index={round_idx} avg_score={summary['avg_score']:.4f} "
            f"success_rate={summary['success_rate']:.2f}",
            flush=True,
        )

        # Keep dataset priors as base context and append latest adaptive reflection notes.
        strategy_memory = _load_dataset_strategy_notes() + _reflection_notes(round_results)

    best_round = (
        max(all_rounds, key=lambda item: (item["success_rate"], item["avg_score"]))
        if all_rounds
        else None
    )
    payload = {
        "rounds": all_rounds,
        "best_round": best_round,
    }

    write_path = args.output
    try:
        write_path.parent.mkdir(parents=True, exist_ok=True)
        write_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    except PermissionError:
        write_path = Path("iterative_inference_results.json")
        write_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
        print(f"[WARN] Could not write to {args.output}; wrote to {write_path} instead.", flush=True)

    if best_round is not None:
        print(
            f"[BEST] round={best_round['round']} avg_score={best_round['avg_score']:.4f} "
            f"success_rate={best_round['success_rate']:.2f} output={write_path}",
            flush=True,
        )


if __name__ == "__main__":
    main()
