import streamlit as st
from utils.journal import save_entry, get_entries, delete_entry
from utils.gemini_client import analyze_journal_entry
from datetime import datetime

def show_journal_page(user):
    st.title("📝 My Journal")

    # New entry section
    st.subheader("Write a new entry")

    content = st.text_area(
        "How are you feeling today?",
        placeholder="Write freely about your day, thoughts, feelings...",
        height=200
    )

    mood_score = st.slider(
        "Rate your mood today",
        min_value=1,
        max_value=10,
        value=5,
        help="1 = Very low, 10 = Excellent"
    )

    mood_emojis = {
        1: "😭", 2: "😢", 3: "😔", 4: "😕", 5: "😐",
        6: "🙂", 7: "😊", 8: "😄", 9: "😁", 10: "🤩"
    }
    st.write(f"Mood: {mood_emojis[mood_score]}")

    if st.button("Save Entry ✅", use_container_width=True):
        if content.strip():
            with st.spinner("Analyzing your entry with AI... 🤖"):
                # Analyze with Gemini
                analysis, error = analyze_journal_entry(content, mood_score)

                if analysis:
                    emotions = analysis.get("emotions", [])
                    themes = analysis.get("themes", [])
                    ai_insight = analysis.get("ai_insight", "")
                    risk_flag = analysis.get("risk_flag", False)

                    # Save to database
                    data, save_error = save_entry(
                        user_id=user.id,
                        content=content,
                        mood_score=mood_score,
                        emotions=emotions,
                        themes=themes,
                        ai_insight=ai_insight
                    )

                    if data:
                        st.success("Entry saved successfully! ✅")

                        # Show AI analysis
                        st.subheader("🤖 AI Analysis")
                        col1, col2 = st.columns(2)
                        with col1:
                            st.write("**Emotions detected:**")
                            for emotion in emotions:
                                st.write(f"• {emotion}")
                        with col2:
                            st.write("**Themes detected:**")
                            for theme in themes:
                                st.write(f"• {theme}")

                        st.info(f"💬 {ai_insight}")

                        # Show crisis resources if risk flagged
                        if risk_flag:
                            st.error("💙 We noticed you might be going through something difficult.")
                            st.warning("""
                                **You are not alone. Please reach out:**
                                - 🆘 **Samaritans (UK):** Call 116 123 (free, 24/7)
                                - 💬 **Crisis Text Line:** Text SHOUT to 85258
                                - 🏥 **NHS Mental Health:** 111 (option 2)
                            """)
                        st.rerun()
                    else:
                        st.error(f"Failed to save: {save_error}")
                else:
                    st.error(f"AI analysis failed: {error}")
        else:
            st.warning("Please write something before saving!")

    # Past entries section
    st.divider()
    st.subheader("📖 Past Entries")

    entries, error = get_entries(user.id)

    if error:
        st.error(f"Could not load entries: {error}")
    elif not entries:
        st.info("No entries yet. Write your first one above! 👆")
    else:
        for entry in entries:
            date = datetime.fromisoformat(entry["created_at"]).strftime("%B %d, %Y %I:%M %p")
            mood = entry["mood_score"]
            emoji = mood_emojis.get(mood, "😐")

            with st.expander(f"{emoji} {date} — Mood: {mood}/10"):
                st.write(entry["content"])

                if entry.get("emotions"):
                    st.write(f"**Emotions:** {', '.join(entry['emotions'])}")
                if entry.get("themes"):
                    st.write(f"**Themes:** {', '.join(entry['themes'])}")
                if entry.get("ai_insight"):
                    st.info(f"🤖 {entry['ai_insight']}")

                if st.button("Delete Entry 🗑️", key=f"delete_{entry['id']}"):
                    success, err = delete_entry(entry["id"])
                    if success:
                        st.success("Entry deleted!")
                        st.rerun()
                    else:
                        st.error(f"Could not delete: {err}")