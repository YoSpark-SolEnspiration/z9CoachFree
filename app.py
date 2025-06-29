# File: z9CoachFree.py

import streamlit as st
import random
import pandas as pd
from typing import Dict, Any

from utils import load_json_file, save_json_file
from analyze_profile import analyze_profile
from z9_spiral_logic import map_disc_to_stage
from trait_summary import summarize_trait
from visuals import (
    generate_radar_chart,
    project_spiral,
    plot_circular_stage_map,
    plot_development_path,
    plot_harmonic_convergence,
    plot_negiton_damping,
    plot_triplet_state,
)
from pdf_export import generate_report
from convertkit_api import subscribe_user_to_convertkit

# ——— Helpers ——————————————————————————————————————————————————

def safe_load(path: str, default: Any) -> Any:
    try:
        return load_json_file(path)
    except FileNotFoundError:
        return default

def show_stage_insights(
    label: str,
    stage_key: str,
    simple: Dict[str, str],
    detailed: Dict[str, Dict[str, str]]
):
    st.subheader(f"{label}: {stage_key}")
    st.info(simple.get(stage_key, ""))
    if stage_key in detailed:
        d = detailed[stage_key]
        st.markdown(f"**Tip:** {d['tip']}  ")
        st.markdown(f"**Sol Spark:** _{d['sol_spark']}_  ")
        st.markdown(f"**Mindset Goal:** {d['mindset_goal']}")

def log_and_alert(profile: dict, final_stage: str, d: float, i: float, s: float, c: float):
    entry = {
        "timestamp": pd.Timestamp.now().isoformat(),
        "traits": profile["traits"],
        "trait_score": profile["trait_score"],
        "harmony_ratio": profile["harmony_ratio"],
        "stage": final_stage
    }
    log = safe_load("assessment_log.json", default=[])
    log.append(entry)
    save_json_file(log, "assessment_log.json")
    st.success("✅ Your profile has been saved to the log.")

# ——— Main App ——————————————————————————————————————————————————

def main():
    st.set_page_config(page_title="Z9 Insight Engine", layout="centered")
    st.title("🧠 Z9 Insight Engine — Z9 Coach Free © 2025"
             
             "⚡A New Dawn of DISC Profiles")

    # Load all JSON sources safely up-front
    DEFAULT_SIMPLE = {f"Stage {i}": "" for i in range(1,9)}
    stage_summaries = safe_load("stage_summaries.json", DEFAULT_SIMPLE)
    ee_narratives   = safe_load("results_ee_stage_summaries.json", {})
    path_map        = safe_load("stage_path_map.json", {})

    # Sidebar
    st.sidebar.subheader("🔖 Quick E.Erikson Stage Tips")
    for lbl, tip in stage_summaries.items():
        st.sidebar.markdown(f"**{lbl}**: {tip}")
    st.sidebar.markdown("---")

    # DISC quiz + perceived stage form
    questions = load_json_file("master_disc_questions.json")
    sampled   = random.sample(questions, 16)

    with st.form("quiz"):
        st.subheader("📋 Quiz Questions"
                      "🤔Answer each question according to how you currently feel.")
        responses = {}
        for idx, q in enumerate(sampled):
            responses[idx] = st.radio(q["question"], q["options"], key=f"q_{idx}")

        st.subheader("🧭 Your Perceived EE Stage")
        perceived = st.selectbox(
            "Select the stage that resonates with you:",
            list(stage_summaries.keys())
        )

        submit = st.form_submit_button("📊 Generate My Profile")

    if not submit:
        return

    # Score mapping
    score_map = {"Strongly Disagree":1, "Disagree":2, "Agree":4, "Strongly Agree":5}
    d = i = s = c = 0.0
    for idx, q in enumerate(sampled):
        val = score_map.get(responses[idx], 0)
        if q["trait"] == "D": d += val
        if q["trait"] == "I": i += val
        if q["trait"] == "S": s += val
        if q["trait"] == "C": c += val

    # Analyze + map
    profile    = analyze_profile(d, i, s, c, stage_label=perceived)
    auto_stage = map_disc_to_stage(d, i, s, c)

    # Indices for visuals
    perc_idx = int(perceived.split()[1]) - 1
    auto_idx = int(auto_stage.split()[1]) - 1

    # — Stage Insights ————————————————————————————————
    st.markdown("---")
    st.header("🔍 Stage Insights")
    show_stage_insights("Perceived Stage", perceived,    stage_summaries, ee_narratives)
    show_stage_insights("Auto-Mapped Stage", auto_stage, stage_summaries, ee_narratives)
    gap = abs(perc_idx - auto_idx)
    st.metric("Alignment Gap", f"{gap}", delta_color="normal" if gap<=1 else "inverse")

      # Determine dominant trait once
    dominant = max(profile["traits"], key=profile["traits"].get)

    # — Charts & Summaries —————————————————————————————
    st.markdown("---")
    st.header("📊 Your Charts & Metrics")
    st.success(f"Composite Trait Score: **{profile['trait_score']}**")

    # 🔵 DISC Radar Chart
    st.subheader("🔵 DISC Radar Chart")
    st.pyplot(generate_radar_chart(profile["traits"]))
    st.markdown(
        "“Your footprint across Dominance, Influence, Steadiness, and Conscientiousness”  \n"
        "This spider-web plot shows at a glance where you naturally shine and where you might pull back. "
        "High spikes indicate strengths you lean on—today and always—while lower points reveal growth edges. "
        f"For your dominant trait (**{dominant}**), notice how your peak fuels your daily drive, and use that "
        "energy to shore up any softer quadrants in small, actionable steps."
    )

    # 🌀 Z9 Spiral Projection
    st.subheader("🌀 Z9 Spiral Projection")
    st.pyplot(project_spiral(profile["traits"], recursion_score=3.0, negated_traits=profile["negated"]))
    st.markdown(
        "“Visualizing your trait harmony and recursive growth”  \n"
        "By mapping your trait percentages onto a spiral, this chart reflects how balanced (or lopsided) "
        "your self-expression is over repeated cycles. A smooth, rounded spiral means your styles feed one another; "
        "dips and jagged edges pinpoint where you may over- or under-invest. For your dominant style, see how deeply "
        f"it loops at each recursion—lean into its momentum consciously, so it lifts rather than overshadows your other qualities."
    )
    
    st.subheader("🧩 Your Trait Summary")
    st.markdown(summarize_trait(profile["traits"]))
    st.metric("Stable Recursion Score", profile["recursion_result"]["stable_score"])

    st.subheader("⚖️ Balance & Negation Metrics")
    col1, col2 = st.columns(2)
    col1.metric("Harmony Ratio", f"{profile['harmony_ratio']}%")
    neg_rate = round(sum(profile["negated"].values()) / max(len(profile["negated"]),1) * 100)
    col2.metric("Avg Negation Rate", f"{neg_rate}%")
    if profile["negated"]:
        df_neg = pd.DataFrame(profile["negated"], index=["Negation %"]).T
        st.bar_chart(df_neg)
    st.markdown("Your harmony ratio shows overall balance; negation highlights development areas.")

    # — Remedies & Coaching ————————————————————————————
    st.markdown("---")
    st.header("🌿 Your Comprehensive Remedies & Coaching")
    remedies = profile.get("remedies", {})
    if remedies:
        for trait, data in remedies.items():
            st.subheader(f"{trait} Remedies")
            st.markdown(f"**Action:** {data['action']}")
            st.markdown(f"*Rationale:* {data['rationale']}")
            st.markdown(f"*Sol Enspiration Advice:* _{data['mister_anu_advice']}_")
            st.markdown(f"*Stage Tip:* {data['stage_tip']}")
            for idx, url in enumerate(data.get("products", []), 1):
                st.markdown(f"- [Product {idx}]({url})")
            st.markdown("---")
    else:
        st.info("No coaching remedies available.")

# 🗺️ Your Development Journey
    st.subheader("🗺️ Your Development Journey")
    fig = plot_development_path(
        perc_idx,
        auto_idx,
        ee_narratives,
        path_map,
        dominant
    )
    st.pyplot(fig)
    st.markdown(
        "“A step-by-step path from where you feel to where you’re guided”  \n"
        "This linear flow walks you through each Erikson stage between your Perceived and Auto-Mapped stages, "
        "annotating emotional obstacles and your tailored action tip. It transforms abstract theory into a clear roadmap: "
        "at every rung, you’ll know which inner hurdle to address and which D/I/S/C exercise to activate for real traction."
    )

    # 🎶 Harmonic Convergence Index
    st.subheader("🎶 Harmonic Convergence Index")
    st.pyplot(plot_harmonic_convergence(profile["traits"]))
    st.markdown(
        "“Measuring the resonance of your four styles”  \n"
        "Borrowing from Z9’s mathematical core, this index scores how well your traits blend into a coherent whole. "
        "Higher convergence means your behaviors are singing in tune; lower suggests internal dissonance. "
        f"Your dominant trait (**{dominant}**)'s presence here shows how its frequency either supports or drowns out the ensemble—"
        "use awareness of this “song” to fine-tune your daily interactions."
    )

    # ⏳ Negiton Rest-Phase Damping
    st.subheader("⏳ Negiton Rest-Phase Damping")
    st.pyplot(plot_negiton_damping(profile["traits"]))
    st.markdown(
        "“Spotlighting the shadows of your primary trait”  \n"
        "Negiton damping reflects how your lesser traits pull back when your dominant style takes over. Think of it as the echo "
        "chamber of the qualities you habitually suppress. For your top style, see which secondary trait is most muted—and experiment "
        "with a brief “negiton reset” exercise (like a 2-minute stretch or journaling prompt) to bring that voice back into harmony."
    )

    # 🔄 Triplet State Function
    st.subheader("🔄 Triplet State Function")
    st.pyplot(plot_triplet_state(profile["traits"]))
    st.markdown(
        "“Capturing your three-trait interplay in dynamic form”  \n"
        "This tri-node graph models how any three of your trait percentages interact in real time—like a mini ecosystem of you. "
        "Notice the vertex that’s furthest from center: it’s the combination driving your current mindset. Leaning into that triplet "
        "can turbocharge creativity or productivity; gently pull it back if you sense burnout or tunnel vision."
    )

    # — Download / Subscribe / Log —————————————————————
    st.markdown("---")
    st.subheader("📥 Download Your Full Insight Report")
    pdf_bytes = generate_report({
        "traits": profile["traits"],
        "trait_score": profile["trait_score"],
        "harmony_ratio": profile["harmony_ratio"],
        "stage": auto_stage
    })
    st.download_button("Download PDF", pdf_bytes, "Z9_Insight_Report.pdf", "application/pdf")

    st.subheader("📬 Get Follow-Up Coaching Tips")
    email = st.text_input("Your email:")
    if st.button("Subscribe"):
        ok = subscribe_user_to_convertkit(
            email,
            st.secrets["convertkit_api_key"],
            st.secrets["convertkit_form_id"]
        )
        st.success("✅ Subscribed!") if ok else st.error("⚠️ Subscription failed.")

    log_and_alert(profile, auto_stage, d, i, s, c)

    st.markdown("""
© 2025 **KYLE DUSAN HENSON JR LC** + **YO SPARK: SOL ENSPIRATION LC**  
Licensed under **Enterprise4Eternity, LC**.  
Contact: [solenspirationin@gmail.com](mailto:solenspirationin@gmail.com)
""")

if __name__ == "__main__":
    main()
