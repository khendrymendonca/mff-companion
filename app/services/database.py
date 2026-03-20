import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

class DatabaseService:
    def __init__(self):
        if not SUPABASE_URL or not SUPABASE_KEY:
            print("AVISO: SUPABASE_URL ou SUPABASE_KEY não configurados!")
        self.supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

    # HERÓIS (GALERIA)
    def get_heroes(self):
        try:
            response = self.supabase.table("user_inventory").select("*, characters(*)").execute()
            return response.data or []
        except Exception as e:
            print(f"Erro ao buscar heróis: {e}")
            return []

    def add_hero(self, name, b_type, b_alignment, gender, tags, tier, level):
        try:
            # Primeiro cria na tabela global de personagens se não existir
            char_res = self.supabase.table("characters").select("*").eq("name", name).execute()
            if not char_res.data:
                char_res = self.supabase.table("characters").insert({
                    "name": name, 
                    "base_type": b_type, 
                    "base_alignment": b_alignment,
                    "gender": gender,
                    "tags": tags if tags else []
                }).execute()
            
            char_id = char_res.data[0]['id']
            
            # Depois adiciona ao inventário do usuário
            return self.supabase.table("user_inventory").insert({
                "character_id": char_id,
                "current_tier": tier,
                "level": level,
                "is_used": False
            }).execute()
        except Exception as e:
            print(f"Erro ao adicionar herói: {e}")
            return None

    # SHADOWLAND (SALAS POR ANDAR)
    def get_sl_rooms(self):
        try:
            rooms = self.supabase.table("sl_rooms").select("*").order("floor_number").execute().data
            return rooms or []
        except Exception as e:
            print(f"Erro ao buscar salas: {e}")
            return []

    def add_room(self, floor_num, name, r_type, r_alignment, r_gender, r_tags=None, notes=""):
        try:
            return self.supabase.table("sl_rooms").insert({
                "floor_number": floor_num,
                "room_name": name,
                "req_type": r_type,
                "req_alignment": r_alignment,
                "req_gender": r_gender,
                "req_tags": r_tags if r_tags else [],
                "notes": notes
            }).execute()
        except Exception as e:
            print(f"Erro ao adicionar sala: {e}")
            return None

    def mark_hero_used(self, inventory_id, floor_number):
        try:
            # Marca como usado
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
        except Exception as e:
            print(f"Erro ao marcar como usado: {e}")
            return None

    def reset_sl_week(self):
        try:
            return self.supabase.table("user_inventory").update({"is_used": False}).neq("id", 0).execute()
        except Exception as e:
            print(f"Erro ao resetar semana: {e}")
            return None

    # METADADOS (CONFIGURAÇÕES)
    def get_meta(self):
        try:
            types = self.supabase.table("meta_types").select("*").execute().data or []
            alignments = self.supabase.table("meta_alignments").select("*").execute().data or []
            genders = self.supabase.table("meta_genders").select("*").execute().data or []
            tags = self.supabase.table("meta_tags").select("*").execute().data or []
            tiers = self.supabase.table("meta_tiers").select("*").order("priority").execute().data or []
            return {
                "types": types,
                "alignments": alignments,
                "genders": genders,
                "tags": tags,
                "tiers": tiers
            }
        except Exception as e:
            print(f"Erro ao buscar metadados: {e}")
            return {"types": [], "alignments": [], "genders": [], "tags": [], "tiers": []}

    def add_meta(self, category, name, priority=1):
        try:
            table_map = {
                "type": "meta_types",
                "alignment": "meta_alignments",
                "gender": "meta_genders",
                "tag": "meta_tags",
                "tier": "meta_tiers"
            }
            data = {"name": name}
            if category == "tier":
                data["priority"] = priority
            return self.supabase.table(table_map[category]).insert(data).execute()
        except Exception as e:
            print(f"Erro ao adicionar metadado: {e}")
            return None

    def update_hero(self, inventory_id, tier, level, b_type, b_alignment, gender, tags):
        try:
            # 1. Buscar o character_id associado
            inv = self.supabase.table("user_inventory").select("character_id").eq("id", inventory_id).single().execute()
            char_id = inv.data['character_id']

            # 2. Atualizar os dados de evolução no inventário
            self.supabase.table("user_inventory").update({
                "current_tier": tier,
                "level": level
            }).eq("id", inventory_id).execute()

            # 3. Atualizar os dados base (Uniformes mudam Tipo/Tags/Lado)
            self.supabase.table("characters").update({
                "base_type": b_type,
                "base_alignment": b_alignment,
                "gender": gender,
                "tags": tags if tags else []
            }).eq("id", char_id).execute()

            return True
        except Exception as e:
            print(f"Erro ao atualizar herói: {e}")
            return False
