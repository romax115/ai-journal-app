import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from utils.dashboard import get_mood_data, get_emotion_counts, get_theme_counts

def show_dashboard_page(user):
    st.title("📊 Mood Dashboard")

    df, error = get_mood_data(user.id)

    if error:
        st.error(f"Could not load data: {error}")
        return

    if df is None or df.empty:
        st.info("No journal entries yet. Start journaling to see your dashboard! 📝")
        return

    # ── Summary Stats ──
    st.subheader("📈 Overview")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Entries", len(df))
    with col2:
        avg_mood = round(df["mood_score"].mean(), 1)
        st.metric("Average Mood", f"{avg_mood}/10")
    with col3:
        best_mood = df["mood_score"].max()
        st.metric("Best Mood", f"{best_mood}/10")
    with col4:
        lowest_mood = df["mood_score"].min()
        st.metric("Lowest Mood", f"{lowest_mood}/10")

    st.divider()

    # ── Mood Over Time Chart ──
    st.subheader("📉 Mood Over Time")
    fig_mood = px.line(
        df,
        x="created_at",
        y="mood_score",
        title="Your Mood Journey",
        labels={"created_at": "Date", "mood_score": "Mood Score"},
        markers=True,
        color_discrete_sequence=["#7C3AED"]
    )
    fig_mood.update_layout(
        yaxis_range=[0, 10],
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
    )
    st.plotly_chart(fig_mood, use_container_width=True)

    st.divider()

    # ── Emotions & Themes Charts ──
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("💭 Top Emotions")
        emotion_counts = get_emotion_counts(df)
        if emotion_counts:
            emotion_df = pd.DataFrame(
                list(emotion_counts.items()),
                columns=["Emotion", "Count"]
            ).sort_values("Count", ascending=False)
            fig_emotions = px.bar(
                emotion_df,
                x="Count",
                y="Emotion",
                orientation="h",
                color_discrete_sequence=["#7C3AED"]
            )
            fig_emotions.update_layout(
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
            )
            st.plotly_chart(fig_emotions, use_container_width=True)
        else:
            st.info("No emotion data yet")

    with col2:
        st.subheader("🏷️ Top Themes")
        theme_counts = get_theme_counts(df)
        if theme_counts:
            theme_df = pd.DataFrame(
                list(theme_counts.items()),
                columns=["Theme", "Count"]
            ).sort_values("Count", ascending=False)
            fig_themes = px.pie(
                theme_df,
                values="Count",
                names="Theme",
                color_discrete_sequence=px.colors.sequential.Purples_r
            )
            fig_themes.update_layout(
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
            )
            st.plotly_chart(fig_themes, use_container_width=True)
        else:
            st.info("No theme data yet")

    st.divider()

    # ── Mood Distribution ──
    st.subheader("🎯 Mood Distribution")
    fig_hist = px.histogram(
        df,
        x="mood_score",
        nbins=10,
        title="How often you felt each mood level",
        labels={"mood_score": "Mood Score", "count": "Number of Entries"},
        color_discrete_sequence=["#7C3AED"]
    )
    fig_hist.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
    )
    st.plotly_chart(fig_hist, use_container_width=True)