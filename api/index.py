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

@app.get("/")
async def read_root(request: Request):
    heroes = db.get_heroes()
    t3_count = len([c for c in heroes if c['current_tier'] in [Tier.T3.value, Tier.TRANSCENDED.value]])
    t4_count = len([c for c in heroes if c['current_tier'] == Tier.T4.value])
    
    return templates.TemplateResponse("dashboard.html", {
        "request": request, 
        "inventory": heroes,
        "t3_count": t3_count,
        "t4_count": t4_count
    })

@app.get("/gallery")
async def gallery(request: Request):
    heroes = db.get_heroes()
    return templates.TemplateResponse("inventory.html", {"request": request, "inventory": heroes})

@app.post("/add-hero")
async def add_hero(name: str = Form(...), base_type: str = Form(...), base_alignment: str = Form(...), tier: str = Form(...), level: int = Form(...)):
    db.add_hero(name, base_type, base_alignment, tier, level)
    return RedirectResponse(url="/gallery", status_code=303)

@app.get("/shadowland")
async def shadowland(request: Request):
    floors = db.get_sl_floors()
    heroes = db.get_heroes()
    return templates.TemplateResponse("shadowland.html", {
        "request": request, 
        "floors": floors, 
        "inventory": heroes
    })

@app.post("/add-floor")
async def add_floor(number: int = Form(...), name: str = Form(...), req_type: str = Form(...), req_alignment: str = Form(...)):
    db.add_floor(number, name, req_type, req_alignment)
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
