from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from datetime import datetime
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

if os.environ.get("MONGO_URI"):
    client = MongoClient(os.environ["MONGO_URI"])
else:

    client = MongoClient("mongodb://ISIS2304D33202610:dZ0ce0y9R0HV@157.253.236.88:8087")

db = client["ISIS2304D33202610"]

@app.get("/")
def inicio():
    return {"estado": "API funcionando correctamente"}


@app.get('/bares/{bar_id}/comentarios')
def get_comentarios(bar_id: int):
    comentarios = []
    for doc in db["comentarios_bares"].find({"bar_id": bar_id}):
        doc["_id"] = str(doc["_id"])
        comentarios.append(doc)
    return comentarios


@app.post('/bares/{bar_id}/comentarios')
def post_comentario(bar_id: int, datos: dict):
    datos['bar_id'] = bar_id
    datos['fecha'] = datetime.now().isoformat()
    resultado = db["comentarios_bares"].insert_one(datos)
    return {"mensaje": "Comentario guardado", "id": str(resultado.inserted_id)}


@app.get('/bares/{bar_id}/eventos')
def get_eventos(bar_id: int):
    eventos = []
    for doc in db["eventos"].find({"bar_id": bar_id}):
        doc["_id"] = str(doc["_id"])
        eventos.append(doc)
    return eventos

@app.post('/bares/{bar_id}/eventos')
def post_evento(bar_id: int, datos: dict):
    datos["bar_id"] = bar_id
    datos["fecha_creacion"] = datetime.now().isoformat()
    resultado = db["eventos"].insert_one(datos)
    return {"mensaje": "Evento guardado", "id": str(resultado.inserted_id)}
