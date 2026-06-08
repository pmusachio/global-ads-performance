"""Interactive Streamlit dashboard for the Marketing Budget Optimization project.

Lets a user explore the historical ad performance data and simulate the
optimal daily budget allocation across channels under configurable business
constraints (total budget, minimum ROAS, per-channel share bounds).

Run locally with:
    streamlit run src/dashboard.py
"""
import json
import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st

from src.optimizer import optimize_allocation
from src.transformers import saturation_curve

st.set_page_config(
    page_title="Marketing Budget Optimizer",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)

DRACULA = {
    "bg": "#282a36", "fg": "#f8f8f2", "cyan": "#8be9fd", "green": "#50fa7b",
    "orange": "#ffb86c", "pink": "#ff79c6", "purple": "#bd93f9", "red": "#ff5555",
    "yellow": "#f1fa8c", "comment": "#6272a4",
}
CHANNEL_COLORS = {
    "Google Ads": DRACULA["green"],
    "Meta Ads": DRACULA["cyan"],
    "TikTok Ads": DRACULA["pink"],
}
DATA_URL = "https://raw.githubusercontent.com/pmusachio/global-ads-performance/refs/heads/main/data/raw.csv"


@st.cache_data
def load_data():
    """Loads the historical dataset, falling back to the public GitHub copy."""
    try:
        path = "data/raw.csv" if os.path.exists("data/raw.csv") else DATA_URL
        df = pd.read_csv(path)
        df["date"] = pd.to_datetime(df["date"])
        return df
    except Exception:
        return None


@st.cache_data
def load_metrics():
    """Loads the saturation parameters (L, k) produced by the training run."""
    if not os.path.exists("models/metrics.json"):
        return None
    with open("models/metrics.json") as f:
        return json.load(f)


def color_for(channel: str) -> str:
    return CHANNEL_COLORS.get(channel, DRACULA["purple"])


def render_allocation_chart(channels, allocation, total_budget):
    fig, ax = plt.subplots(figsize=(6, 4))
    fig.patch.set_facecolor(DRACULA["bg"])
    ax.set_facecolor(DRACULA["bg"])

    y_pos = np.arange(len(channels))
    bars = ax.barh(y_pos, allocation, color=[color_for(c) for c in channels])
    ax.set_yticks(y_pos)
    ax.set_yticklabels(channels, color=DRACULA["fg"])
    ax.tick_params(colors=DRACULA["fg"])
    for spine in ["top", "right"]:
        ax.spines[spine].set_visible(False)
    for spine in ["bottom", "left"]:
        ax.spines[spine].set_color(DRACULA["fg"])
    for bar in bars:
        ax.text(
            bar.get_width() + total_budget * 0.01, bar.get_y() + bar.get_height() / 2,
            f"$ {bar.get_width():,.0f}", va="center", color=DRACULA["fg"], fontweight="bold",
        )
    ax.set_xlim([0, max(allocation) * 1.3])
    return fig


def render_saturation_curves(channels, allocation, channel_params, total_budget):
    fig, ax = plt.subplots(figsize=(8, 4.5))
    fig.patch.set_facecolor(DRACULA["bg"])
    ax.set_facecolor(DRACULA["bg"])

    x_spend = np.linspace(0, max(total_budget * 0.8, 20_000), 200)
    for i, channel in enumerate(channels):
        p = channel_params[channel]
        y_curve = saturation_curve(x_spend, p["L"], p["k"])
        color = color_for(channel)
        ax.plot(x_spend, y_curve, color=color, linewidth=2.5, alpha=0.6, label=channel)

        spend = allocation[i]
        revenue = saturation_curve(spend, p["L"], p["k"])
        ax.scatter([spend], [revenue], color=color, s=120, edgecolors=DRACULA["fg"], zorder=5)
        ax.vlines(spend, 0, revenue, color=color, linestyle=":", alpha=0.5)
        ax.hlines(revenue, 0, spend, color=color, linestyle=":", alpha=0.5)

    ax.tick_params(colors=DRACULA["fg"])
    for spine in ax.spines.values():
        spine.set_color(DRACULA["comment"])
    ax.set_xlabel("Daily Ad Spend ($)", color=DRACULA["fg"])
    ax.set_ylabel("Predicted Revenue ($)", color=DRACULA["fg"])
    ax.legend(facecolor=DRACULA["bg"], edgecolor=DRACULA["comment"], labelcolor=DRACULA["fg"])
    return fig


def main():
    st.title("🎯 Intelligent Marketing Budget Optimization")
    st.markdown("Analytics dashboard powered by Saturation Regression models (Machine Learning).")

    metrics_data = load_metrics()
    df = load_data()

    if metrics_data is None:
        st.error(
            "🚨 `models/metrics.json` not found. Run `python -m src.train` "
            "(or the `dux_budget_optimization` notebook end to end) to train and save the models first."
        )
        return

    channel_params = {c: d["saturation_params"] for c, d in metrics_data["channels"].items()}
    channels = list(channel_params.keys())

    st.sidebar.title("⚙️ Optimization Controls")
    st.sidebar.markdown(
        "Set the financial constraints (business rules). The optimizer recalculates "
        "the ideal allocation in real time."
    )
    total_budget = st.sidebar.slider("💰 Total Daily Budget ($)", min_value=3000, max_value=50000, value=15000, step=500)
    min_roas = st.sidebar.slider("📈 Minimum Acceptable Global ROAS", min_value=1.0, max_value=6.0, value=2.0, step=0.1)

    st.sidebar.markdown("---")
    st.sidebar.markdown("**Per-channel share constraints:**")
    min_share = st.sidebar.slider("Minimum investment (% of total)", 0.05, 0.20, 0.10, 0.01)
    max_share = st.sidebar.slider("Maximum investment (% of total)", 0.30, 0.80, 0.50, 0.05)

    result = optimize_allocation(channel_params, total_budget, min_roas, min_share, max_share)

    tab_optimizer, tab_eda = st.tabs(["📊 Simulator & Optimizer", "📈 Historical Data"])

    with tab_optimizer:
        if not result["success"]:
            st.error(
                f"❌ **Infeasible**: the constraints are too strict. The model cannot guarantee a "
                f"ROAS of **{min_roas}x** with a budget of **$ {total_budget:,.2f}** while keeping each "
                f"channel between {min_share*100:.0f}% and {max_share*100:.0f}% of the total. "
                "Try relaxing the constraints in the sidebar."
            )
        else:
            allocation = np.array([result["allocation"][c] for c in channels])
            spend, revenue, roas = result["estimated_spend"], result["estimated_revenue"], result["estimated_roas"]

            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Suggested Investment", f"$ {spend:,.2f}")
            col2.metric("Estimated Revenue", f"$ {revenue:,.2f}")
            col3.metric("Projected ROAS", f"{roas:.2f}x")
            if spend < total_budget - 1:
                col4.metric(
                    "Budget Held Back", f"$ {total_budget - spend:,.2f}",
                    help="The model suggests withholding part of the budget to protect profitability.",
                )
            else:
                col4.metric("Budget Held Back", "$ 0.00")

            st.markdown("---")
            chart_col, curve_col = st.columns([1, 1.5])
            with chart_col:
                st.subheader("💳 Optimal Budget Distribution")
                st.pyplot(render_allocation_chart(channels, allocation, total_budget))
            with curve_col:
                st.subheader("📉 Saturation Curves")
                st.pyplot(render_saturation_curves(channels, allocation, channel_params, total_budget))

    with tab_eda:
        if df is not None:
            st.subheader("📚 Raw Dataset Sample")
            st.dataframe(df.sort_values("date", ascending=False).head(100), use_container_width=True)

            st.subheader("📈 Historical Macro View")
            daily = df.groupby("date")[["ad_spend", "revenue"]].sum().reset_index()
            st.line_chart(daily.set_index("date"), color=[DRACULA["red"], DRACULA["green"]])
        else:
            st.warning("Could not load `raw.csv`.")


if __name__ == "__main__":
    main()
