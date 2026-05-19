import streamlit as st
from utils.weekly_summary import generate_weekly_summary, save_weekly_summary

def show_weekly_summary_page(user):
    st.title("💬 Weekly AI Summary")
    st.write("Get a personalized AI summary of your emotional journey this week.")

    if st.button("✨ Generate My Weekly Summary", use_container_width=True):
        with st.spinner("AI is analyzing your week... 🤖"):
            summary, error = generate_weekly_summary(user.id)

            if error:
                if error == "No entries this week":
                    st.info("You have no journal entries this week. Start journaling to get your weekly summary! 📝")
                else:
                    st.error(f"Could not generate summary: {error}")
            else:
                # Save to database
                save_weekly_summary(user.id, summary)

                # Display summary
                st.subheader("📋 Your Week in Review")
                st.info(f"💬 {summary['summary']}")

                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Entries This Week", summary["entry_count"])
                with col2:
                    st.metric("Average Mood", f"{summary['average_mood']}/10")

                # Highlights
                st.subheader("✨ Highlights")
                for highlight in summary.get("highlights", []):
                    st.success(f"• {highlight}")

                # Suggestions
                st.subheader("💡 Self-Care Suggestions")
                for suggestion in summary.get("suggestions", []):
                    st.warning(f"• {suggestion}")

                # Mental health resources if needed
                if summary.get("needs_support"):
                    st.divider()
                    st.error("💙 It looks like this was a tough week. You are not alone.")
                    st.subheader("🆘 Mental Health Resources")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown("""
                        **Immediate Support:**
                        - 🆘 **Samaritans:** 116 123 (free, 24/7)
                        - 💬 **Crisis Text Line:** Text SHOUT to 85258
                        - 🏥 **NHS Urgent Mental Health:** 111 (option 2)
                        """)
                    with col2:
                        st.markdown("""
                        **Online Resources:**
                        - 🌐 [Mind UK](https://www.mind.org.uk)
                        - 🌐 [NHS Mental Health](https://www.nhs.uk/mental-health)
                        - 🌐 [Student Minds](https://www.studentminds.org.uk)
                        """)