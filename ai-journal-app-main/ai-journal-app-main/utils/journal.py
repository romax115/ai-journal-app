from utils.supabase_client import supabase
from datetime import datetime

def save_entry(user_id, content, mood_score, emotions, themes, ai_insight):
    try:
        response = supabase.table("journal_entries").insert({
            "user_id": user_id,
            "content": content,
            "mood_score": mood_score,
            "emotions": emotions,
            "themes": themes,
            "ai_insight": ai_insight,
            "created_at": datetime.now().isoformat()
        }).execute()
        return response.data, None
    except Exception as e:
        return None, str(e)

def get_entries(user_id, limit=10):
    try:
        response = supabase.table("journal_entries")\
            .select("*")\
            .eq("user_id", user_id)\
            .order("created_at", desc=True)\
            .limit(limit)\
            .execute()
        return response.data, None
    except Exception as e:
        return None, str(e)

def get_all_entries(user_id):
    try:
        response = supabase.table("journal_entries")\
            .select("*")\
            .eq("user_id", user_id)\
            .order("created_at", desc=True)\
            .execute()
        return response.data, None
    except Exception as e:
        return None, str(e)

def delete_entry(entry_id):
    try:
        response = supabase.table("journal_entries")\
            .delete()\
            .eq("id", entry_id)\
            .execute()
        return True, None
    except Exception as e:
        return False, str(e)