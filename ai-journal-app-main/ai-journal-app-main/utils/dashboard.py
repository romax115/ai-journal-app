import pandas as pd
from utils.supabase_client import supabase

def get_mood_data(user_id):
    try:
        response = supabase.table("journal_entries")\
            .select("mood_score, emotions, themes, created_at")\
            .eq("user_id", user_id)\
            .order("created_at", desc=False)\
            .execute()
        
        if not response.data:
            return None, None
        
        df = pd.DataFrame(response.data)
        df["created_at"] = pd.to_datetime(df["created_at"])
        df["date"] = df["created_at"].dt.date
        return df, None
    except Exception as e:
        return None, str(e)

def get_emotion_counts(df):
    emotion_counts = {}
    for emotions in df["emotions"]:
        if emotions:
            for emotion in emotions:
                emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
    return emotion_counts

def get_theme_counts(df):
    theme_counts = {}
    for themes in df["themes"]:
        if themes:
            for theme in themes:
                theme_counts[theme] = theme_counts.get(theme, 0) + 1
    return theme_counts