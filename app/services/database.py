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
# HERÓIS (GALERIA)
def add_hero(self, name, b_type, b_alignment, gender, tags, tier, level):
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
    return self.supabase.table("user_inventory").insert({
        "character_id": char_id,
        "current_tier": tier,
        "level": level,
        "is_used": False
    }).execute()

# SHADOWLAND (SALAS POR ANDAR)
def get_sl_rooms(self):
    # Agrupa salas por andar para o front
    rooms = self.supabase.table("sl_rooms").select("*").order("floor_number").execute().data
    return rooms

def add_room(self, floor_num, name, r_type, r_alignment, r_gender, r_tags=None, notes=""):
    return self.supabase.table("sl_rooms").insert({
        "floor_number": floor_num,
        "room_name": name,
        "req_type": r_type,
        "req_alignment": r_alignment,
        "req_gender": r_gender,
        "req_tags": r_tags if r_tags else [],
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

    # METADADOS (CONFIGURAÇÕES)
    def get_meta(self):
        try:
            types = self.supabase.table("meta_types").select("*").execute().data or []
            alignments = self.supabase.table("meta_alignments").select("*").execute().data or []
            genders = self.supabase.table("meta_genders").select("*").execute().data or []
            tags = self.supabase.table("meta_tags").select("*").execute().data or []
            return {
                "types": types,
                "alignments": alignments,
                "genders": genders,
                "tags": tags
            }
        except Exception as e:
            print(f"Erro ao buscar metadados: {e}")
            return {"types": [], "alignments": [], "genders": [], "tags": []}

    def add_meta(self, category, name):
        table_map = {
            "type": "meta_types",
            "alignment": "meta_alignments",
            "gender": "meta_genders",
            "tag": "meta_tags"
        }
        return self.supabase.table(table_map[category]).insert({"name": name}).execute()

    def delete_meta(self, category, item_id):
        table_map = {
            "type": "meta_types",
            "alignment": "meta_alignments",
            "gender": "meta_genders",
            "tag": "meta_tags"
        }
        return self.supabase.table(table_map[category]).delete().eq("id", item_id).execute()
