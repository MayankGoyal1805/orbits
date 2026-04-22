from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
REPORT_DIR = ROOT / "report"
FIG_DIR = REPORT_DIR / "figures"
RESULTS_PATH = ROOT / "iterative_inference_results.json"


def _load_results() -> dict:
    return json.loads(RESULTS_PATH.read_text(encoding="utf-8"))


def _task_thresholds(results: dict) -> dict[str, float]:
    # Pull task thresholds from current runtime config so plotted thresholds
    # reflect the same config used by the simulator.
    import sys

    src_dir = ROOT / "src"
    if str(src_dir) not in sys.path:
        sys.path.insert(0, str(src_dir))

    from orbits_env.tasks.catalog import get_task

    task_ids: set[str] = set()
    for round_item in results.get("rounds", []):
        for task in round_item.get("tasks", []):
            task_ids.add(task["task_id"])

    thresholds: dict[str, float] = {}
    for task_id in sorted(task_ids):
        thresholds[task_id] = float(get_task(task_id).success_probability_threshold)
    return thresholds


def _plot_round_trends(results: dict) -> None:
    rounds = results.get("rounds", [])
    x = [r["round"] for r in rounds]
    avg_score = [r["avg_score"] for r in rounds]
    avg_reward = [r["avg_total_reward"] for r in rounds]
    success_rate = [r["success_rate"] for r in rounds]

    fig, ax = plt.subplots(figsize=(7.0, 3.4), dpi=160)
    ax.plot(x, avg_score, marker="o", linewidth=2, label="Avg Score")
    ax.plot(x, avg_reward, marker="s", linewidth=2, label="Avg Total Reward")
    ax.plot(x, success_rate, marker="^", linewidth=2, label="Success Rate")

    ax.set_title("Round-Level Trends")
    ax.set_xlabel("Round")
    ax.set_ylabel("Metric Value")
    ax.set_xticks(x)
    ax.grid(alpha=0.3, linestyle="--", linewidth=0.8)
    ax.legend(frameon=False)
    fig.tight_layout()
    fig.savefig(FIG_DIR / "round_trends.png", bbox_inches="tight")
    plt.close(fig)


def _plot_task_progression(results: dict) -> None:
    rounds = results.get("rounds", [])
    task_ids = sorted({t["task_id"] for r in rounds for t in r.get("tasks", [])})
    x = [r["round"] for r in rounds]

    scores_by_task: dict[str, list[float]] = {task_id: [] for task_id in task_ids}
    rewards_by_task: dict[str, list[float]] = {task_id: [] for task_id in task_ids}

    for round_item in rounds:
        task_map = {t["task_id"]: t for t in round_item.get("tasks", [])}
        for task_id in task_ids:
            task = task_map[task_id]
            scores_by_task[task_id].append(float(task["score"]))
            rewards_by_task[task_id].append(float(task["total_reward"]))

    fig, axes = plt.subplots(1, 2, figsize=(10.2, 3.4), dpi=160)

    for task_id in task_ids:
        axes[0].plot(x, scores_by_task[task_id], marker="o", linewidth=2, label=task_id.replace("collision_avoidance_", ""))
    axes[0].set_title("Task Score by Round")
    axes[0].set_xlabel("Round")
    axes[0].set_ylabel("Score")
    axes[0].set_xticks(x)
    axes[0].grid(alpha=0.3, linestyle="--", linewidth=0.8)

    for task_id in task_ids:
        axes[1].plot(x, rewards_by_task[task_id], marker="s", linewidth=2, label=task_id.replace("collision_avoidance_", ""))
    axes[1].set_title("Task Total Reward by Round")
    axes[1].set_xlabel("Round")
    axes[1].set_ylabel("Total Reward")
    axes[1].set_xticks(x)
    axes[1].grid(alpha=0.3, linestyle="--", linewidth=0.8)

    handles, labels = axes[1].get_legend_handles_labels()
    fig.legend(handles, labels, loc="upper center", ncol=3, frameon=False, bbox_to_anchor=(0.5, 1.06))
    fig.tight_layout(rect=[0, 0, 1, 0.95])
    fig.savefig(FIG_DIR / "task_progression.png", bbox_inches="tight")
    plt.close(fig)


def _plot_final_risk_vs_threshold(results: dict) -> None:
    rounds = results.get("rounds", [])
    if not rounds:
        return

    best_round = results.get("best_round") or rounds[-1]
    tasks = best_round.get("tasks", [])
    thresholds = _task_thresholds(results)

    task_labels = [t["task_id"].replace("collision_avoidance_", "") for t in tasks]
    observed = [float(t["highest_collision_probability"]) for t in tasks]
    target = [float(thresholds[t["task_id"]]) for t in tasks]

    x = range(len(tasks))
    width = 0.36

    fig, ax = plt.subplots(figsize=(7.2, 3.4), dpi=160)
    ax.bar([i - width / 2 for i in x], observed, width=width, label="Observed Final Highest Risk")
    ax.bar([i + width / 2 for i in x], target, width=width, label="Success Threshold")

    ax.set_title("Final Risk vs Success Threshold (Best Round)")
    ax.set_xlabel("Task")
    ax.set_ylabel("Collision Probability")
    ax.set_xticks(list(x))
    ax.set_xticklabels(task_labels)
    ax.grid(axis="y", alpha=0.3, linestyle="--", linewidth=0.8)
    ax.legend(frameon=False)
    fig.tight_layout()
    fig.savefig(FIG_DIR / "risk_vs_threshold.png", bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    results = _load_results()
    _plot_round_trends(results)
    _plot_task_progression(results)
    _plot_final_risk_vs_threshold(results)
    print(f"Wrote plots to {FIG_DIR}")


if __name__ == "__main__":
    main()
