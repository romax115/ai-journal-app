from utils.supabase_client import supabase

def sign_up(email, password, full_name):
    try:
        response = supabase.auth.sign_up({
            "email": email,
            "password": password,
        })
        user = response.user
        if user:
            # Create a profile for the user
            supabase.table("profiles").insert({
                "id": user.id,
                "email": email,
                "full_name": full_name,
            }).execute()
        return user, None
    except Exception as e:
        return None, str(e)

def sign_in(email, password):
    try:
        response = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password,
        })
        return response.user, None
    except Exception as e:
        return None, str(e)

def sign_out():
    supabase.auth.sign_out()