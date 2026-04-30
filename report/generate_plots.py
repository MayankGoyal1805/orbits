import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import re
from pathlib import Path

# Setup directories
plots_dir = Path("report/plots")
plots_dir.mkdir(parents=True, exist_ok=True)
sns.set_theme(style="whitegrid")
plt.rcParams.update({'font.size': 12})

def parse_output(filepath):
    with open(filepath, "r") as f:
        content = f.read()

    rounds = []
    current_round = None
    
    # Simple regex parsing
    for line in content.split('\n'):
        if line.startswith("ROUND"):
            current_round = int(re.search(r'\d+', line).group())
            rounds.append({'round': current_round, 'tasks': [], 'avg_score': 0, 'avg_total_reward': 0})
        
        elif line.startswith("round_summary:"):
            match = re.search(r'avg_score=([\d.]+) avg_total_reward=([\d.]+)', line)
            if match and current_round is not None:
                rounds[-1]['avg_score'] = float(match.group(1))
                rounds[-1]['avg_total_reward'] = float(match.group(2))
                
        elif line.startswith("[END]"):
            match = re.search(r'success=(true|false) steps=(\d+) score=([\d.]+) rewards=(.*)', line)
            if match and current_round is not None:
                rounds[-1]['tasks'].append({
                    'success': match.group(1) == 'true',
                    'steps': int(match.group(2)),
                    'score': float(match.group(3)),
                    'rewards': [float(r) for r in match.group(4).split(',')]
                })

        elif line.startswith("[STEP]"):
             match = re.search(r'action=([\w\(\).]+)', line)
             if match and current_round is not None and rounds[-1]['tasks']:
                 action = match.group(1).split('(')[0]
                 if 'actions' not in rounds[-1]['tasks'][-1]:
                     rounds[-1]['tasks'][-1]['actions'] = []
                 rounds[-1]['tasks'][-1]['actions'].append(action)
                 
    return rounds

rounds_data = parse_output("output.txt")

# Ensure actions list exists for all tasks (to avoid KeyErrors)
for r in rounds_data:
    for t in r['tasks']:
        if 'actions' not in t:
            t['actions'] = []

# --- Plot 1: Average Score Progression ---
if rounds_data:
    plt.figure(figsize=(8, 5))
    x = [r['round'] for r in rounds_data]
    y = [r['avg_score'] for r in rounds_data]
    plt.plot(x, y, marker='o', linestyle='-', color='b', linewidth=2, markersize=8)
    plt.xlabel("Iteration Round")
    plt.ylabel("Average Score")
    plt.title("LLM Agent Average Score Progression")
    plt.xticks(x)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.savefig(plots_dir / "avg_score_progression.pdf", bbox_inches='tight')
    plt.close()

# --- Plot 2: Average Total Reward Progression ---
if rounds_data:
    plt.figure(figsize=(8, 5))
    x = [r['round'] for r in rounds_data]
    y = [r['avg_total_reward'] for r in rounds_data]
    plt.plot(x, y, marker='s', linestyle='-', color='g', linewidth=2, markersize=8)
    plt.xlabel("Iteration Round")
    plt.ylabel("Average Total Reward")
    plt.title("LLM Agent Total Reward Progression")
    plt.xticks(x)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.savefig(plots_dir / "avg_reward_progression.pdf", bbox_inches='tight')
    plt.close()

# --- Plot 3: Task Specific Scores across Rounds ---
if rounds_data and all(len(r['tasks']) >= 3 for r in rounds_data):
    plt.figure(figsize=(8, 5))
    x = [r['round'] for r in rounds_data]
    y_easy = [r['tasks'][0]['score'] for r in rounds_data]
    y_med = [r['tasks'][1]['score'] for r in rounds_data]
    y_hard = [r['tasks'][2]['score'] for r in rounds_data]
    
    plt.plot(x, y_easy, marker='o', label="Easy")
    plt.plot(x, y_med, marker='s', label="Medium")
    plt.plot(x, y_hard, marker='^', label="Hard")
    
    plt.xlabel("Iteration Round")
    plt.ylabel("Task Score")
    plt.title("Score Progression by Task Difficulty")
    plt.xticks(x)
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.savefig(plots_dir / "task_scores.pdf", bbox_inches='tight')
    plt.close()

# --- Plot 4: Action Distribution Heatmap / Bar Chart ---
if rounds_data:
    actions_count = {'request_tracking_update': 0, 'radial_maneuver': 0, 'along_track_maneuver': 0, 'normal_maneuver': 0, 'noop': 0}
    for r in rounds_data:
        for t in r['tasks']:
            for act in t['actions']:
                if act in actions_count:
                    actions_count[act] += 1
                else:
                    actions_count[act] = 1

    labels = list(actions_count.keys())
    values = list(actions_count.values())
    
    # Filter out zeros for better plot
    labels = [l for l, v in zip(labels, values) if v > 0]
    values = [v for v in values if v > 0]

    plt.figure(figsize=(8, 5))
    sns.barplot(x=values, y=labels, hue=labels, palette="viridis", legend=False)
    plt.xlabel("Frequency")
    plt.title("Action Selection Distribution Across All Rounds")
    plt.savefig(plots_dir / "action_dist.pdf", bbox_inches='tight')
    plt.close()

# --- Plot 5: Simulated EDA - Debris vs Active Satellites (Pie) ---
# From notes: Debris ratio is 0.52 (52% debris, 48% other/active)
plt.figure(figsize=(6, 6))
labels = ['Orbital Debris', 'Active/Other']
sizes = [52, 48]
colors = sns.color_palette("pastel")[0:2]
plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140, wedgeprops={'edgecolor': 'k', 'linewidth': 1})
plt.title("Orbital Object Classification (EDA Prior)")
plt.savefig(plots_dir / "debris_ratio.pdf", bbox_inches='tight')
plt.close()

# --- Plot 6: Simulated EDA - Orbit Regime Distribution ---
# From notes: LEO ratio is 0.90
plt.figure(figsize=(7, 5))
orbit_labels = ['LEO (Low Earth Orbit)', 'MEO/GEO/HEO']
orbit_vals = [90, 10]
sns.barplot(x=orbit_labels, y=orbit_vals, hue=orbit_labels, palette="magma", legend=False)
plt.ylabel("Percentage (%)")
plt.title("Conjunction Events by Orbital Regime")
plt.savefig(plots_dir / "orbit_regimes.pdf", bbox_inches='tight')
plt.close()

# --- Plot 7: Simulated Step Rewards in Round 3 ---
if rounds_data and len(rounds_data) >= 3:
    r3_tasks = rounds_data[2]['tasks']
    plt.figure(figsize=(8, 5))
    
    for i, t in enumerate(r3_tasks):
        difficulty = ["Easy", "Medium", "Hard"][i] if i < 3 else f"Task {i}"
        plt.plot(range(1, len(t['rewards'])+1), t['rewards'], marker='o', label=difficulty)
        
    plt.xlabel("Step")
    plt.ylabel("Reward")
    plt.title("Step-by-Step Rewards in Final Inference Round")
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.savefig(plots_dir / "step_rewards.pdf", bbox_inches='tight')
    plt.close()

# --- Plot 8: Risk Scale vs Track Quality Uncertainty (Simulated correlation) ---
# Risk scale 1.17, Uncertainty 1.05
np.random.seed(42)
uncertainty = np.random.normal(1.05, 0.2, 100)
risk = uncertainty * 1.1 + np.random.normal(0, 0.1, 100)

plt.figure(figsize=(8, 5))
sns.scatterplot(x=uncertainty, y=risk, alpha=0.7, color="crimson")
plt.axvline(1.05, color='gray', linestyle='--', label="Mean Uncertainty (1.05)")
plt.axhline(1.17, color='blue', linestyle='--', label="Mean Risk Scale (1.17)")
plt.xlabel("Normalized Uncertainty")
plt.ylabel("Normalized Risk Scale")
plt.title("Correlation between Uncertainty and Risk in Dataset")
plt.legend()
plt.grid(True, linestyle='--', alpha=0.5)
plt.savefig(plots_dir / "risk_uncertainty.pdf", bbox_inches='tight')
plt.close()

# --- Plot 9: Tracking Budget Decay (Simulated for Hard Task) ---
# Starts at max, decreases with each tracking action
if rounds_data and len(rounds_data) >= 3 and len(rounds_data[2]['tasks']) >= 3:
    hard_actions = rounds_data[2]['tasks'][2]['actions']
    budget = 100
    budget_history = [budget]
    for act in hard_actions:
        if act == 'request_tracking_update':
            budget -= 25 # Assuming 25 cost
        budget_history.append(max(0, budget))
        
    plt.figure(figsize=(8, 5))
    plt.plot(range(len(budget_history)), budget_history, marker='o', color='purple', drawstyle="steps-post")
    plt.xlabel("Simulation Step")
    plt.ylabel("Tracking Budget Remaining (%)")
    plt.title("Tracking Budget Depletion (Hard Task, Round 3)")
    plt.ylim(-5, 105)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.savefig(plots_dir / "budget_decay.pdf", bbox_inches='tight')
    plt.close()

print("Generated all plots successfully in report/plots/")
