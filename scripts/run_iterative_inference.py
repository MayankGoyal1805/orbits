from __future__ import annotations

import argparse
import io
from contextlib import redirect_stdout
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


def _reflection_notes(
    round_results: list[dict],
    round_index: int,
    previous_summary: dict | None,
) -> list[str]:
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

    if previous_summary is not None:
        current_avg_score = float(mean(result["score"] for result in round_results)) if round_results else 0.0
        current_avg_reward = float(mean(result["total_reward"] for result in round_results)) if round_results else 0.0
        current_success_rate = (
            sum(1 for result in round_results if result["success"]) / len(round_results)
            if round_results
            else 0.0
        )

        stagnated = (
            round(current_avg_score, 4) == round(float(previous_summary.get("avg_score", 0.0)), 4)
            and round(current_avg_reward, 4) == round(float(previous_summary.get("avg_total_reward", 0.0)), 4)
            and round(current_success_rate, 4) == round(float(previous_summary.get("success_rate", 0.0)), 4)
        )
        if stagnated:
            notes.append(
                f"Exploration note for round {round_index + 1}: do not repeat the same first-step action for all tasks; prefer a maneuver action when highest_collision_probability > 0.24."
            )

            first_actions = {
                str(result.get("first_action", "")) for result in round_results if str(result.get("first_action", ""))
            }
            if len(first_actions) == 1 and "request_tracking_update" in first_actions:
                notes.append(
                    "Exploration note: avoid request_tracking_update as the first move this round; choose one of radial_maneuver, along_track_maneuver, or normal_maneuver with magnitude 0.45 to 0.60."
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


def _cross_round_memory_notes(previous_rounds: list[dict]) -> list[str]:
    notes: list[str] = []
    for summary in previous_rounds:
        round_idx = int(summary.get("round", 0))
        notes.append(
            "Previous round summary "
            f"(round {round_idx}): avg_score={float(summary.get('avg_score', 0.0)):.4f}, "
            f"avg_total_reward={float(summary.get('avg_total_reward', 0.0)):.4f}, "
            f"success_rate={float(summary.get('success_rate', 0.0)):.2f}."
        )

        task_snippets: list[str] = []
        for task in summary.get("tasks", []):
            task_snippets.append(
                f"{task.get('task_id', 'unknown')}:"
                f"success={task.get('success', False)},"
                f"score={float(task.get('score', 0.0)):.4f},"
                f"total_reward={float(task.get('total_reward', 0.0)):.4f},"
                f"first_action={task.get('first_action', '') or 'n/a'}"
            )
        if task_snippets:
            notes.append(
                f"Previous round {round_idx} task outcomes: " + " | ".join(task_snippets)
            )
    return notes


def _write_text_report(
    path: Path,
    round_reports: list[dict],
    best_round: dict | None,
    requested_rounds: int,
    executed_rounds: int,
    client_mode: str,
) -> None:
    lines: list[str] = []
    lines.append("Iterative Inference Detailed Report")
    lines.append("=" * 34)
    lines.append(f"requested_rounds: {requested_rounds}")
    lines.append(f"executed_rounds: {executed_rounds}")
    lines.append(f"client_mode: {client_mode}")
    lines.append("")

    for report in round_reports:
        summary = report["summary"]
        lines.append(f"ROUND {summary['round']}")
        lines.append("-" * 10)
        lines.append(f"strategy_notes_count: {len(report['strategy_notes'])}")
        for note in report["strategy_notes"]:
            lines.append(f"  - {note}")
        lines.append("")
        lines.append("task step logs:")
        for block in report["task_logs"]:
            lines.append(block.rstrip())
        lines.append("")
        lines.append(
            f"round_summary: avg_score={summary['avg_score']:.4f} "
            f"avg_total_reward={summary['avg_total_reward']:.4f} "
            f"success_rate={summary['success_rate']:.2f}"
        )
        task_successes = sum(1 for result in summary["tasks"] if result["success"])
        lines.append(f"success_count: {task_successes}/{len(summary['tasks'])}")
        lines.append("")

    if best_round is not None:
        lines.append("BEST ROUND")
        lines.append("-" * 10)
        lines.append(
            f"round={best_round['round']} avg_score={best_round['avg_score']:.4f} "
            f"success_rate={best_round['success_rate']:.2f}"
        )
        lines.append("")

    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Run iterative self-improvement inference rounds.")
    parser.add_argument("--rounds", type=int, default=3, help="Number of iterative rounds to run.")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("outputs/evals/iterative_inference_results.json"),
        help="Output JSON for per-round summaries.",
    )
    parser.add_argument(
        "--text-output",
        type=Path,
        default=Path("output.txt"),
        help="Detailed human-readable run log and summary output.",
    )
    args = parser.parse_args()

    if args.rounds < 1:
        raise ValueError("--rounds must be >= 1")

    print(
        f"[CONFIG] requested_rounds={args.rounds} model={inference.MODEL_NAME} max_steps={inference.MAX_STEPS}",
        flush=True,
    )
    if args.rounds == 1:
        print(
            "[INFO] Running a single round. If this is unexpected, check ITERATIVE_ROUNDS/ITERABLE_ROUNDS overrides.",
            flush=True,
        )
    if args.rounds > 1 and inference.MAX_STEPS <= 1:
        print(
            "[WARN] MAX_STEPS is 1. Multi-round adaptation is heavily constrained and rounds may look identical.",
            flush=True,
        )

    client = OpenAI(base_url=inference.API_BASE_URL, api_key=inference.API_KEY) if inference.API_KEY else None
    client_mode = "llm" if client is not None else "fallback-heuristic"
    print(f"[MODE] client_mode={client_mode}", flush=True)

    if client is None and not inference.ALLOW_HEURISTIC_FALLBACK:
        raise RuntimeError(
            "LLM client is unavailable and fallback is disabled. "
            "Set one of (HF_TOKEN, OPENAI_API_KEY, GROQ_API_KEY, API_KEY) plus API_BASE_URL and MODEL_NAME, "
            "or explicitly set ALLOW_HEURISTIC_FALLBACK=1."
        )

    if client is not None:
        inference._validate_model_availability(client)

    if client is None:
        print(
            "[WARN] HF_TOKEN/API credentials were not loaded; iterative rounds will use deterministic fallback policy.",
            flush=True,
        )

    strategy_memory = _load_dataset_strategy_notes()
    all_rounds: list[dict] = []
    round_reports: list[dict] = []

    for round_idx in range(1, args.rounds + 1):
        print(f"[ROUND] index={round_idx} strategy_notes={len(strategy_memory)}", flush=True)
        round_results: list[dict] = []
        round_task_logs: list[str] = []

        for task_id in inference.TASK_IDS:
            log_buffer = io.StringIO()
            with redirect_stdout(log_buffer):
                result = inference.run_task(
                    task_id=task_id,
                    client=client,
                    strategy_memory=strategy_memory,
                    emit_logs=True,
                )

            task_log = log_buffer.getvalue()
            if task_log:
                print(task_log, end="", flush=True)
                round_task_logs.append(task_log)
            round_results.append(result)

        summary = _summarize_round(round_idx, round_results)
        all_rounds.append(summary)
        round_reports.append(
            {
                "summary": summary,
                "strategy_notes": list(strategy_memory),
                "task_logs": round_task_logs,
            }
        )
        print(
            f"[ROUND-END] index={round_idx} avg_score={summary['avg_score']:.4f} "
            f"success_rate={summary['success_rate']:.2f}",
            flush=True,
        )

        # Keep dataset priors as base context, include all previous round data/rewards,
        # and append latest adaptive reflection notes.
        previous_summary = all_rounds[-2] if len(all_rounds) >= 2 else None
        prior_round_data_notes = _cross_round_memory_notes(all_rounds)
        reflection_notes = _reflection_notes(
            round_results,
            round_idx,
            previous_summary,
        )
        strategy_memory = _load_dataset_strategy_notes() + prior_round_data_notes + reflection_notes

    best_round = (
        max(all_rounds, key=lambda item: (item["success_rate"], item["avg_score"]))
        if all_rounds
        else None
    )
    payload = {
        "requested_rounds": args.rounds,
        "executed_rounds": len(all_rounds),
        "client_mode": client_mode,
        "rounds": all_rounds,
        "best_round": best_round,
    }

    if len(all_rounds) >= 2:
        first = all_rounds[0]
        all_same = all(
            round_item["avg_score"] == first["avg_score"]
            and round_item["avg_total_reward"] == first["avg_total_reward"]
            and round_item["success_rate"] == first["success_rate"]
            for round_item in all_rounds[1:]
        )
        if all_same:
            print(
                "[WARN] All rounds produced identical summary metrics. "
                "This is expected in fallback-heuristic mode and may also happen when prompts do not change behavior.",
                flush=True,
            )

    write_path = args.output
    text_write_path = args.text_output
    try:
        write_path.parent.mkdir(parents=True, exist_ok=True)
        write_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
        text_write_path.parent.mkdir(parents=True, exist_ok=True)
        _write_text_report(
            text_write_path,
            round_reports,
            best_round,
            requested_rounds=args.rounds,
            executed_rounds=len(all_rounds),
            client_mode=client_mode,
        )
    except PermissionError:
        write_path = Path("iterative_inference_results.json")
        write_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
        text_write_path = Path("output.txt")
        _write_text_report(
            text_write_path,
            round_reports,
            best_round,
            requested_rounds=args.rounds,
            executed_rounds=len(all_rounds),
            client_mode=client_mode,
        )
        print(
            f"[WARN] Could not write to requested output path(s); "
            f"wrote JSON to {write_path} and text report to {text_write_path} instead.",
            flush=True,
        )

    if best_round is not None:
        print(
            f"[BEST] round={best_round['round']} avg_score={best_round['avg_score']:.4f} "
            f"success_rate={best_round['success_rate']:.2f} json_output={write_path} text_output={text_write_path}",
            flush=True,
        )


if __name__ == "__main__":
    main()
