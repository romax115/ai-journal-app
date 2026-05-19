from utils.supabase_client import supabase
from utils.gemini_client import client
from datetime import datetime, timedelta
import pandas as pd

def get_weekly_entries(user_id):
    try:
        week_ago = (datetime.now() - timedelta(days=7)).isoformat()
        response = supabase.table("journal_entries")\
            .select("*")\
            .eq("user_id", user_id)\
            .gte("created_at", week_ago)\
            .order("created_at", desc=False)\
            .execute()
        return response.data, None
    except Exception as e:
        return None, str(e)

def generate_weekly_summary(user_id):
    entries, error = get_weekly_entries(user_id)

    if error:
        return None, error

    if not entries or len(entries) < 1:
        return None, "No entries this week"

    # Build summary context
    entries_text = ""
    mood_scores = []
    all_emotions = []
    all_themes = []

    for entry in entries:
        date = datetime.fromisoformat(entry["created_at"]).strftime("%B %d")
        entries_text += f"\n- {date} (Mood: {entry['mood_score']}/10): {entry['content'][:150]}..."
        mood_scores.append(entry["mood_score"])
        if entry.get("emotions"):
            all_emotions.extend(entry["emotions"])
        if entry.get("themes"):
            all_themes.extend(entry["themes"])

    avg_mood = round(sum(mood_scores) / len(mood_scores), 1)

    prompt = f"""
    You are a compassionate mental health journaling assistant.
    Based on this person's journal entries from the past week, generate a warm weekly summary.
    
    Entries this week:
    {entries_text}
    
    Average mood: {avg_mood}/10
    Most common emotions: {list(set(all_emotions))}
    Most common themes: {list(set(all_themes))}
    
    Return ONLY a valid JSON object with exactly these fields:
    {{
        "summary": "A warm, empathetic 3-4 sentence summary of their week emotionally. Be supportive and non-clinical.",
        "highlights": ["2-3 positive observations from their week"],
        "suggestions": ["2-3 gentle, actionable self-care suggestions based on their entries"],
        "needs_support": false
    }}
    
    For needs_support: set to true if the overall week shows consistently very low mood (below 3) or concerning patterns.
    Return only the JSON, no extra text.
    """

    try:
        from google import genai
        response = client.models.generate_content(
            model="gemini-3.1-flash-lite-preview",
            contents=prompt
        )
        text = response.text.strip()
        text = text.replace("```json", "").replace("```", "").strip()
        import json
        result = json.loads(text)
        result["average_mood"] = avg_mood
        result["entry_count"] = len(entries)
        return result, None
    except Exception as e:
        return None, str(e)

def save_weekly_summary(user_id, summary_data):
    try:
        week_start = (datetime.now() - timedelta(days=7)).date().isoformat()
        week_end = datetime.now().date().isoformat()
        response = supabase.table("weekly_summaries").insert({
            "user_id": user_id,
            "summary": summary_data["summary"],
            "average_mood": summary_data["average_mood"],
            "week_start": week_start,
            "week_end": week_end,
        }).execute()
        return response.data, None
    except Exception as e:
        return None, str(e)