# File: visuals.py
import math
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure
from typing import Dict, Optional, List


def generate_radar_chart(traits: Dict[str, float], title: str = "DISC Radar Chart") -> Figure:
    """
    Generate a radar chart for DISC trait values.

    Args:
        traits: Mapping of trait labels ('D','I','S','C') to numeric percentages.
        title: Optional title for the radar chart.

    Returns:
        A Matplotlib Figure object containing the radar chart.
    """
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
    """
    Project trait values onto a spiral radar, highlighting both traits and negated traits.

    Args:
        traits: Mapping of trait labels to numeric values (0–100).
        recursion_score: Scalar to stretch values along the spiral radius.
        negated_traits: Optional mapping of trait labels to negation values (0–100).
        title: Chart title.

    Returns:
        A Matplotlib Figure of the spiral projection.
    """
    labels = list(traits.keys())
    base_values = [traits[k] / 100 * recursion_score for k in labels]
    base_values += [base_values[0]]

    angles = np.linspace(0, 2 * np.pi, len(labels) + 1)

    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    ax.plot(angles, base_values, linewidth=2, label="Trait Spiral")
    ax.fill(angles, base_values, alpha=0.2)

    if negated_traits:
        neg_values = [negated_traits.get(k, 0) / 100 * recursion_score for k in labels]
        neg_values += [neg_values[0]]
        ax.plot(angles, neg_values, linestyle="dashed", color="red", label="Negated Traits")
        ax.fill(angles, neg_values, alpha=0.1, color="red")

    ax.set_title(title)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels)
    ax.set_yticklabels([])
    ax.legend(loc="upper right")

    return fig


def plot_circular_stage_map(
    current_index: int,
    next_index: int,
    labels: Optional[List[str]] = None,
    title: str = "Eriksonian Stage Progress Map"
) -> Figure:
    """
    Plot a circular map of stages, highlighting current and next stages.

    Args:
        current_index: Zero-based index of the current stage.
        next_index: Zero-based index of the next stage.
        labels: Optional list of stage labels; defaults to ['Stage 1',..., 'Stage 8'].
        title: Title for the plot.

    Returns:
        A Matplotlib Figure of the circular stage map.
    """
    if labels is None:
        labels = [f"Stage {i+1}" for i in range(8)]

    radius = 2.5
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.axis("off")

    for i, label in enumerate(labels):
        angle = 2 * np.pi * i / len(labels)
        x = radius * np.cos(angle)
        y = radius * np.sin(angle)
        color = "green" if i == current_index else "blue" if i == next_index else "gray"
        ax.text(x, y, label, ha="center", va="center", fontsize=10, color=color)

    ax.set_title(title)
    return fig
