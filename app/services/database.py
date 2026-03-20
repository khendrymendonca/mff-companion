import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

class DatabaseService:
    def __init__(self):
        self.supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

    # HERÓIS (GALERIA)
    def get_heroes(self):
        # Busca da tabela user_inventory e faz join com characters
        response = self.supabase.table("user_inventory").select("*, characters(*)").execute()
        return response.data

    def add_hero(self, name, b_type, b_alignment, tier, level):
        # Primeiro cria na tabela global de personagens se não existir
        char_res = self.supabase.table("characters").select("*").eq("name", name).execute()
        if not char_res.data:
            char_res = self.supabase.table("characters").insert({
                "name": name, 
                "base_type": b_type, 
                "base_alignment": b_alignment
            }).execute()
        
        char_id = char_res.data[0]['id']
        
        # Depois adiciona ao inventário do usuário
        return self.supabase.table("user_inventory").insert({
            "character_id": char_id,
            "current_tier": tier,
            "level": level,
            "is_used": False
        }).execute()

    # SHADOWLAND (ANDARE E HISTÓRICO)
    def get_sl_floors(self):
        return self.supabase.table("sl_floors").select("*").order("floor_number").execute().data

    def add_floor(self, number, name, req_type, req_alignment, notes=""):
        return self.supabase.table("sl_floors").insert({
            "floor_number": number,
            "room_name": name,
            "req_type": req_type,
            "req_alignment": req_alignment,
            "notes": notes
        }).execute()

    def mark_hero_used(self, inventory_id, floor_number):
        # Marca como usado e salva o histórico
        self.supabase.table("user_inventory").update({
            "is_used": True, 
            "last_floor_used": floor_number
        }).eq("id", inventory_id).execute()
        
        # Buscar character_id para o histórico
        inv = self.supabase.table("user_inventory").select("character_id").eq("id", inventory_id).single().execute()
        
        return self.supabase.table("sl_history").insert({
            "floor_number": floor_number,
            "character_id": inv.data['character_id']
        }).execute()

    def reset_sl_week(self):
        # Limpa o status de 'is_used' de todos os heróis para a nova semana
        return self.supabase.table("user_inventory").update({"is_used": False}).neq("id", 0).execute()
