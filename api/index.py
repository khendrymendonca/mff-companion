from fastapi import FastAPI, Request, Response
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from app.models.character import CharacterType, Alignment, Tier, UserCharacter
from app.models.floor import SLFloor
import os

app = FastAPI()

# Configuração de templates e estáticos
templates_path = os.path.join(os.path.dirname(__file__), "..", "app", "templates")
static_path = os.path.join(os.path.dirname(__file__), "..", "app", "static")

templates = Jinja2Templates(directory=templates_path)
app.mount("/static", StaticFiles(directory=static_path), name="static")

# Mock de dados para demonstração
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
    # Calculando estatísticas no Python para evitar erros no Jinja2
    t3_trans = len([c for c in MOCK_INVENTORY if c.current_tier in [Tier.T3, Tier.TRANSCENDED]])
    t4 = len([c for c in MOCK_INVENTORY if c.current_tier == Tier.T4])
    
    return templates.TemplateResponse("dashboard.html", {
        "request": request, 
        "inventory": MOCK_INVENTORY,
        "t3_count": t3_trans,
        "t4_count": t4
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
    # Convertendo personagens para dicionário para o JS do template
    inventory_dicts = [char.dict() for char in MOCK_INVENTORY]
    return templates.TemplateResponse("shadowland.html", {
        "request": request, 
        "floors": floors, 
        "inventory": inventory_dicts
    })

app_vercel = app
