from fastapi import FastAPI, Request, Response, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from app.models.character import CharacterType, Alignment, Tier
from app.services.database import DatabaseService
import os
import sys

app = FastAPI()
db = DatabaseService()

# Caminhos Absolutos para Vercel
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "app", "templates"))

# Montar estáticos se a pasta existir
static_dir = os.path.join(BASE_DIR, "app", "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return Response(status_code=204)

@app.get("/inventory", include_in_schema=False)
async def old_inventory():
    return RedirectResponse(url="/gallery", status_code=301)

@app.get("/")
async def read_root(request: Request):
    try:
        heroes = db.get_heroes() or []
        t3_count = len([c for c in heroes if c.get('current_tier') in ['T3', 'Transcended']])
        t4_count = len([c for c in heroes if c.get('current_tier') == 'T4'])
        
        return templates.TemplateResponse("dashboard.html", {
            "request": request, 
            "inventory": heroes,
            "t3_count": t3_count,
            "t4_count": t4_count
        })
    except Exception as e:
        print(f"Erro na Dashboard: {e}")
        return templates.TemplateResponse("dashboard.html", {"request": request, "inventory": [], "t3_count": 0, "t4_count": 0})

@app.get("/gallery")
async def gallery(request: Request):
    try:
        heroes = db.get_heroes() or []
        meta = db.get_meta()
        return templates.TemplateResponse("inventory.html", {"request": request, "inventory": heroes, "meta": meta})
    except Exception as e:
        print(f"Erro na Galeria: {e}")
        return templates.TemplateResponse("inventory.html", {"request": request, "inventory": [], "meta": {"types": [], "alignments": [], "genders": [], "tags": []}})

@app.post("/add-hero")
async def add_hero(
    name: str = Form(...), 
    base_type: str = Form(...), 
    base_alignment: str = Form(...), 
    gender: str = Form(...),
    tags: str = Form(""),
    tier: str = Form(...), 
    level: int = Form(...)
):
    tag_list = [t.strip() for t in tags.split(",") if t.strip()]
    db.add_hero(name, base_type, base_alignment, gender, tag_list, tier, level)
    return RedirectResponse(url="/gallery", status_code=303)

@app.get("/shadowland")
async def shadowland(request: Request):
    rooms = db.get_sl_rooms()
    heroes = db.get_heroes()
    meta = db.get_meta()
    return templates.TemplateResponse("shadowland.html", {
        "request": request, 
        "floors": rooms, 
        "inventory": heroes,
        "meta": meta
    })

@app.get("/settings")
async def settings(request: Request):
    meta = db.get_meta()
    return templates.TemplateResponse("settings.html", {"request": request, "meta": meta})

@app.post("/add-meta")
async def add_meta(category: str = Form(...), name: str = Form(...)):
    db.add_meta(category, name)
    return RedirectResponse(url="/settings", status_code=303)

@app.post("/delete-meta")
async def delete_meta(category: str = Form(...), item_id: int = Form(...)):
    db.delete_meta(category, item_id)
    return RedirectResponse(url="/settings", status_code=303)

@app.post("/add-room")
async def add_room(
    floor_number: int = Form(...), 
    room_name: str = Form(...), 
    req_type: str = Form(...), 
    req_alignment: str = Form(...),
    req_gender: str = Form(...),
    req_tags: str = Form("")
):
    tag_list = [t.strip() for t in req_tags.split(",") if t.strip()]
    db.add_room(floor_number, room_name, req_type, req_alignment, req_gender, tag_list)
    return RedirectResponse(url="/shadowland", status_code=303)

@app.post("/mark-used")
async def mark_used(inventory_id: int = Form(...), floor_number: int = Form(...)):
    db.mark_hero_used(inventory_id, floor_number)
    return RedirectResponse(url="/shadowland", status_code=303)

@app.post("/reset-week")
async def reset_week():
    db.reset_sl_week()
    return RedirectResponse(url="/shadowland", status_code=303)

app_vercel = app
