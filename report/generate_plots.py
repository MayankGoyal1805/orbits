from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
REPORT_DIR = ROOT / "report"
FIG_DIR = REPORT_DIR / "figures"
RESULTS_PATH = ROOT / "iterative_inference_results.json"


def _set_style() -> None:
    plt.style.use("seaborn-v0_8-whitegrid")
    plt.rcParams.update(
        {
            "axes.titlesize": 11,
            "axes.labelsize": 9,
            "xtick.labelsize": 8,
            "ytick.labelsize": 8,
            "legend.fontsize": 8,
            "figure.titlesize": 12,
        }
    )


def _load_results() -> dict:
    return json.loads(RESULTS_PATH.read_text(encoding="utf-8"))


def _plot_round_score_reward(results: dict) -> None:
    rounds = results.get("rounds", [])
    x = [r["round"] for r in rounds]
    avg_score = [r["avg_score"] for r in rounds]
    avg_reward = [r["avg_total_reward"] for r in rounds]

    fig, ax1 = plt.subplots(figsize=(7.2, 3.6), dpi=170)
    ax2 = ax1.twinx()

    line1 = ax1.plot(x, avg_score, color="#1f77b4", marker="o", linewidth=2.3, label="Avg Score")
    line2 = ax2.plot(x, avg_reward, color="#d62728", marker="s", linewidth=2.3, label="Avg Total Reward")

    ax1.set_title("Round-Level Improvement: Score vs Reward")
    ax1.set_xlabel("Round")
    ax1.set_ylabel("Avg Score", color="#1f77b4")
    ax2.set_ylabel("Avg Total Reward", color="#d62728")
    ax1.tick_params(axis="y", colors="#1f77b4")
    ax2.tick_params(axis="y", colors="#d62728")
    ax1.set_xticks(x)
    ax1.grid(alpha=0.35, linestyle="--", linewidth=0.8)

    handles = line1 + line2
    labels = [h.get_label() for h in handles]
    ax1.legend(handles, labels, frameon=False, loc="upper left")
    fig.tight_layout()
    fig.savefig(FIG_DIR / "output_score_reward.png", bbox_inches="tight")
    plt.close(fig)


def _plot_task_total_reward(results: dict) -> None:
    rounds = results.get("rounds", [])
    task_ids = sorted({t["task_id"] for r in rounds for t in r.get("tasks", [])})
    x = [r["round"] for r in rounds]

    reward_by_task: dict[str, list[float]] = {task_id: [] for task_id in task_ids}

    for round_item in rounds:
        task_map = {t["task_id"]: t for t in round_item.get("tasks", [])}
        for task_id in task_ids:
            task = task_map[task_id]
            reward_by_task[task_id].append(float(task["total_reward"]))

    fig, ax = plt.subplots(figsize=(8.4, 3.6), dpi=170)
    colors = ["#1f77b4", "#2ca02c", "#ff7f0e"]
    for idx, task_id in enumerate(task_ids):
        label = task_id.replace("collision_avoidance_", "")
        color = colors[idx % len(colors)]
        ax.plot(x, reward_by_task[task_id], marker="o", linewidth=2.3, label=label, color=color)

    ax.set_title("Task Total Reward Across Rounds")
    ax.set_xlabel("Round")
    ax.set_ylabel("Total Reward")
    ax.set_xticks(x)
    ax.set_xlim(min(x) - 0.05, max(x) + 0.12)
    ax.grid(alpha=0.35, linestyle="--", linewidth=0.8)
    ax.legend(frameon=False, loc="center left", bbox_to_anchor=(1.01, 0.5), borderaxespad=0.0)
    fig.tight_layout(rect=[0.0, 0.0, 0.83, 1.0])
    fig.savefig(FIG_DIR / "output_task_reward.png", bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    _set_style()
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    results = _load_results()

    _plot_round_score_reward(results)
    _plot_task_total_reward(results)
    print(f"Wrote plots to {FIG_DIR}")


if __name__ == "__main__":
    main()
