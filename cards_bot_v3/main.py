from fastapi import FastAPI, Request, WebSocket
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from pydantic import BaseModel

app = FastAPI()
templates = Jinja2Templates(directory="site")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

duels_tournoi: List[dict] = []

class Duel(BaseModel):
    joueur1: str
    joueur2: str
    etat: str

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "duels": duels_tournoi})

@app.post("/add_duel")
async def add_duel(duel: Duel):
    duels_tournoi.append(duel.dict())
    return {"status": "ok", "message": "Duel ajouté"}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        await websocket.send_json(duels_tournoi)