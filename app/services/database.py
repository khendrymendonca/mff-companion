import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL", "https://your-project.supabase.co")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "your-key")

class DatabaseService:
    def __init__(self):
        # Em um ambiente real, as chaves seriam validadas
        self.supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

    def get_characters(self):
        # Retorna a base de personagens global
        return self.supabase.table("characters").select("*").execute()

    def get_user_inventory(self, user_id: str):
        # Retorna o inventário do usuário logado
        return self.supabase.table("user_inventory").select("*, characters(*)").eq("user_id", user_id).execute()

    def update_character_usage(self, inventory_id: int, is_used: bool):
        return self.supabase.table("user_inventory").update({"is_used": is_used}).eq("id", inventory_id).execute()
