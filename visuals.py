import math
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure
from typing import Dict, Optional, List
from statistics import harmonic_mean


def generate_radar_chart(
    traits: Dict[str, float],
    title: str = "DISC Radar Chart"
) -> Figure:
    labels = list(traits.keys())
    values = list(traits.values())
    values += [values[0]]  # close the loop
    angles = [n / float(len(labels)) * 2 * math.pi for n in range(len(labels))]
    angles += [angles[0]]
    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    ax.plot(angles, values, linewidth=2)
    ax.fill(angles, values, alpha=0.25)
    ax.set_title(title)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels)
    ax.set_yticklabels([])
    return fig


def project_spiral(
    traits: Dict[str, float],
    recursion_score: float = 3.0,
    negated_traits: Optional[Dict[str, float]] = None,
    title: str = "Z9 Spiral Projection"
) -> Figure:
    labels = list(traits.keys())
    base = [traits[t] / 100 * recursion_score for t in labels]
    base += [base[0]]
    angles = np.linspace(0, 2 * math.pi, len(labels) + 1)
    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    ax.plot(angles, base, linewidth=2, label="Traits")
    ax.fill(angles, base, alpha=0.2)
    if negated_traits:
        neg = [negated_traits.get(t, 0) / 100 * recursion_score for t in labels]
        neg += [neg[0]]
        ax.plot(angles, neg, linestyle='--', color='red', label="Negation")
        ax.fill(angles, neg, alpha=0.1, color='red')
    ax.set_title(title)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels)
    ax.set_yticklabels([])
    ax.legend(loc='upper right')
    return fig


def plot_circular_stage_map(
    current_index: int,
    next_index: int,
    labels: Optional[List[str]] = None,
    title: str = "Eriksonian Stage Progress Map"
) -> Figure:
    if labels is None:
        labels = [f"Stage {i+1}" for i in range(8)]
    radius = 3.0
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.axis('off')
    for i, lbl in enumerate(labels):
        angle = 2 * math.pi * i / len(labels)
        x, y = radius * math.cos(angle), radius * math.sin(angle)
        color = 'green' if i == current_index else 'blue' if i == next_index else 'gray'
        ax.text(x, y, lbl, ha='center', va='center', fontsize=12, color=color)
    ax.set_title(title)
    return fig


def plot_development_path(
    perceived_idx: int,
    auto_idx: int,
    ee_summaries: Dict[str, Dict],
    path_map: Dict[str, Dict],
    dominant_trait: str
) -> Figure:
    step = 1 if auto_idx >= perceived_idx else -1
    indices = list(range(perceived_idx, auto_idx + step, step))
    stages = [f"Stage {i+1}" for i in indices]
    obstacles = [path_map.get(s, {}).get("obstacle", "-") for s in stages]
    actions = [path_map.get(s, {}).get("remedies", {}).get(dominant_trait, {}).get("action", "-") for s in stages]
    summaries = [ee_summaries.get(s, {}).get("summary", "") for s in stages]
    fig, ax = plt.subplots(figsize=(8, len(stages) * 1.2))
    ax.axis('off')
    y_pos = list(range(len(stages)))[::-1]
    for idx, (stg, obs, act, summ, y) in enumerate(zip(stages, obstacles, actions, summaries, y_pos)):
        ax.text(0.02, y, f"{stg}", fontsize=12, fontweight='bold')
        ax.text(0.20, y, f"Obstacle: {obs}", fontsize=10)
        ax.text(0.20, y - 0.3, f"Action: {act}", fontsize=10)
        ax.text(0.20, y - 0.6, f"Context: {summ}", fontsize=9, style='italic')
        if idx < len(stages) - 1:
            ax.plot([0.05, 0.05], [y - 0.1, y_pos[idx+1] + 0.1], color='black')
    ax.set_ylim(-1, len(stages))
    ax.set_title("Your Development Journey", pad=20)
    return fig


def plot_harmonic_convergence(
    traits: Dict[str, float]
) -> Figure:
    """
    Plot the Harmonic Convergence Index based on trait percentages.
    """
    values = list(traits.values())
    hm = harmonic_mean([v for v in values if v > 0]) if any(v > 0 for v in values) else 0
    fig, ax = plt.subplots()
    ax.barh(["Harmonic Convergence"], [hm])
    ax.set_xlim(0, 100)
    ax.set_title(f"Harmonic Convergence Index: {hm:.2f}")
    return fig


def plot_negiton_damping(
    traits: Dict[str, float]
) -> Figure:
    """
    Plot a damping curve for negation levels.
    """
    neg = [100 - v for v in traits.values()]
    damping = [100 * (1 - n/100)**2 for n in neg]
    fig, ax = plt.subplots()
    ax.plot(list(traits.keys()), damping, marker='o')
    ax.set_ylabel("Damping Level")
    ax.set_title("Negiton Rest-Phase Damping")
    return fig


def plot_triplet_state(
    traits: Dict[str, float]
) -> Figure:
    """
    Plot a pie chart of the top three trait states.
    """
    top3 = sorted(traits.items(), key=lambda x: x[1], reverse=True)[:3]
    labels, values = zip(*top3) if top3 else ([], [])
    fig, ax = plt.subplots()
    ax.pie(values, labels=labels, autopct='%1.1f%%')
    ax.set_title("Triplet State Distribution")
    return fig
