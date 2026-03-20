from fastapi import FastAPI, Request, Response
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from app.models.character import CharacterType, Alignment, Tier, UserCharacter
from app.models.floor import SLFloor
import os
import sys

# Garante que o diretório raiz esteja no PATH para imports
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

app = FastAPI()

# Caminhos Absolutos para Vercel
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "app", "templates"))

# Montar estáticos se a pasta existir
static_dir = os.path.join(BASE_DIR, "app", "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Mock de dados
MOCK_INVENTORY = [
    UserCharacter(name="Capitão América", base_type=CharacterType.COMBAT, base_alignment=Alignment.HERO, current_tier=Tier.T3),
    UserCharacter(name="Homem de Ferro", base_type=CharacterType.BLAST, base_alignment=Alignment.HERO, current_tier=Tier.T3),
    UserCharacter(name="Viúva Negra", base_type=CharacterType.SPEED, base_alignment=Alignment.HERO, current_tier=Tier.T2),
    UserCharacter(name="Thanos", base_type=CharacterType.UNIVERSAL, base_alignment=Alignment.VILLAIN, current_tier=Tier.T4),
    UserCharacter(name="Duende Verde", base_type=CharacterType.SPEED, base_alignment=Alignment.VILLAIN, current_tier=Tier.T2),
]

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return Response(status_code=204)

@app.get("/")
async def read_root(request: Request):
    t3_count = len([c for c in MOCK_INVENTORY if c.current_tier in [Tier.T3, Tier.TRANSCENDED]])
    t4_count = len([c for c in MOCK_INVENTORY if c.current_tier == Tier.T4])
    
    return templates.TemplateResponse("dashboard.html", {
        "request": request, 
        "inventory": MOCK_INVENTORY,
        "t3_count": t3_count,
        "t4_count": t4_count
    })

@app.get("/inventory")
async def inventory(request: Request):
    return templates.TemplateResponse("inventory.html", {"request": request, "inventory": MOCK_INVENTORY})

@app.get("/shadowland")
async def shadowland(request: Request):
    floors = [
        SLFloor(number=1, name="Sala de Vilões", requirements={"alignment": Alignment.VILLAIN}),
        SLFloor(number=2, name="Sala de Combate", requirements={"type": CharacterType.COMBAT}),
        SLFloor(number=3, name="Velocidade / Herói", requirements={"type": CharacterType.SPEED, "alignment": Alignment.HERO})
    ]
    # Garantir que os enums sejam serializáveis para JSON
    inventory_dicts = []
    for char in MOCK_INVENTORY:
        d = char.dict()
        d['base_type'] = str(d['base_type'].value)
        d['base_alignment'] = str(d['base_alignment'].value)
        d['current_tier'] = str(d['current_tier'].value)
        inventory_dicts.append(d)

    return templates.TemplateResponse("shadowland.html", {
        "request": request, 
        "floors": floors, 
        "inventory": inventory_dicts
    })

app_vercel = app
