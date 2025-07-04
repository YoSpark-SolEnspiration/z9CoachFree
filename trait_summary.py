# File: trait_summary.py
from typing import Dict


def summarize_trait(traits: dict, stage: str, mood: int) -> str:
    """
    Identify the dominant DISC trait and return a rich summary message including
    growth path and caution flag.

    Args:
        traits: Mapping of DISC trait labels ('D','I','S','C') to numeric values.

    Returns:
        A formatted markdown string summarizing the trait, growth path, and development flag.
    """
    # Ensure we use a key function that returns a non-optional float
    top_trait = max(traits.keys(), key=lambda k: traits[k])

    summaries: Dict[str, Dict[str, str]] = {
        "D": {
            "summary": "Direct, driven, and goal-focused.",
            "growth_path": "Develop trust by integrating patience and collaboration.",
            "development_flag": "Overdominance can suppress cooperation and empathy."
        },
        "I": {
            "summary": "Expressive, social, and inspiring.",
            "growth_path": "Grow by anchoring ideas in stability and routines.",
            "development_flag": "Overexpression can blur boundaries and decrease follow-through."
        },
        "S": {
            "summary": "Stable, supportive, and cooperative.",
            "growth_path": "Expand your comfort by embracing bold ideas and decisive leadership.",
            "development_flag": "Overreliance on routine can cause passivity or resistance to change."
        },
        "C": {
            "summary": "Precise, principled, and analytical.",
            "growth_path": "Build trust in self-expression and relational fluidity.",
            "development_flag": "Overstructure can cause perfectionism and emotional disconnect."
        }
    }

    data = summaries.get(top_trait)
    if not data:
        return "You have a balanced personality."

    # Construct a markdown-formatted multi-line summary
    return (
        f"**{data['summary']}**  \n"
        f"**Growth Path:** {data['growth_path']}  \n"
        f"**Flag:** {data['development_flag']}"
    )
