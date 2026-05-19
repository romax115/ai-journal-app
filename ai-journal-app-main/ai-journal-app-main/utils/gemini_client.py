import os
import streamlit as st
from google import genai
from dotenv import load_dotenv
import json

load_dotenv()

def get_secret(key):
    try:
        return st.secrets[key]
    except:
        return os.getenv(key)

client = genai.Client(api_key=get_secret("GEMINI_API_KEY"))

def analyze_journal_entry(content, mood_score):
    prompt = f"""
    You are a compassionate mental health journaling assistant.
    Analyze the following journal entry and return a JSON response only.
    
    Journal Entry: "{content}"
    User's self-rated mood: {mood_score}/10
    
    Return ONLY a valid JSON object with exactly these fields:
    {{
        "emotions": ["list", "of", "detected", "emotions"],
        "themes": ["list", "of", "key", "themes"],
        "ai_insight": "A warm, supportive 2-3 sentence insight about this entry. Be empathetic and non-clinical.",
        "risk_flag": false
    }}
    
    For emotions choose from: happy, sad, anxious, stressed, calm, angry, lonely, grateful, hopeful, overwhelmed, excited, confused
    For themes choose from: work, relationships, health, finances, family, sleep, study, self-esteem, social, future
    For risk_flag: set to true ONLY if the entry contains language suggesting self-harm or crisis
    
    Return only the JSON, no extra text.
    """

    try:
        response = client.models.generate_content(
            model="gemini-3.1-flash-lite-preview",
            contents=prompt
        )
        text = response.text.strip()
        text = text.replace("```json", "").replace("```", "").strip()
        result = json.loads(text)
        return result, None
    except Exception as e:
        return None, str(e)