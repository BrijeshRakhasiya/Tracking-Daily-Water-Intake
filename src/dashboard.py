import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
from database import log_intake, get_intake_history
from agent import WaterIntakeAgent

# Page config
st.set_page_config(page_title="💧 AI Water Tracker", layout="wide")

# Session state
if "agent" not in st.session_state:
    st.session_state.agent = WaterIntakeAgent()

if "tracker_started" not in st.session_state:
    st.session_state.tracker_started = False

# 🎉 Welcome screen
if not st.session_state.tracker_started:
    st.markdown("<h1 style='text-align: center;'>💧 Welcome to AI Water Tracker</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Track your hydration with smart insights and beautiful visuals.</p>", unsafe_allow_html=True)
    if st.button("🚀 Start Tracking"):
        st.session_state.tracker_started = True
        st.rerun()

# 📋 Main dashboard
else:
    st.markdown("## 🧠 AI Water Tracker Dashboard")

    col1, col2 = st.columns([2, 1])
    with col1:
        username = st.text_input("👤 Enter your name:")
    with col2:
        intake = st.number_input("💦 Water intake (ml):", min_value=0, step=100)

    if st.button("✅ Log Intake"):
        if username and intake > 0:
            log_intake(username, intake)
            st.success(f"Logged {intake} ml for **{username}**")

            feedback = st.session_state.agent.analyze_intake(intake)
            st.info(f"🤖 AI Feedback: {feedback}")
        else:
            st.error("Please enter a valid name and intake amount.")

    if username:
        history = get_intake_history(username)

        if isinstance(history, pd.DataFrame):
            df = history
        elif isinstance(history, list) and len(history) > 0:
            df = pd.DataFrame(history, columns=["intake_ml", "date"])
        else:
            df = pd.DataFrame(columns=["date", "intake_ml"])

        if not df.empty:
            df["date"] = pd.to_datetime(df["date"])
            df = df.sort_values("date")

            st.markdown("### 📅 Your Intake History")
            st.dataframe(df.style.highlight_max(axis=0))

            # 📈 Chart: Line plot
            st.markdown("### 📊 Hydration Trend")
            fig, ax = plt.subplots(figsize=(10, 4))
            sns.lineplot(data=df, x="date", y="intake_ml", marker="o", ax=ax, color="teal")
            ax.set_title("Daily Water Intake", fontsize=14)
            ax.set_xlabel("Date")
            ax.set_ylabel("Intake (ml)")
            plt.xticks(rotation=45)
            st.pyplot(fig)

            # 🧠 AI Summary
            total_today = df[df["date"] == df["date"].max()]["intake_ml"].sum()
            summary = st.session_state.agent.analyze_intake(total_today)

            st.markdown("### 🧠 AI Summary")
            st.success(f"Today’s total: **{total_today} ml**\n\n🤖 {summary}")

            # 🌈 Hydration zone
            if total_today < 1500:
                st.warning("⚠️ You're in the **low hydration zone**. Drink more water!")
            elif total_today < 2500:
                st.info("✅ You're in the **healthy hydration zone**. Keep it up!")
            else:
                st.success("🏆 You're in the **excellent hydration zone**. Well done!")
