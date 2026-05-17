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

#os.environ para despliegue. Descomente cuando ya probó todo local.
client = MongoClient(os.environ["MONGO_URI"])
# TODO: conectarse al cluster Admonsis  
# client = MongoClient("mongodb://<usuario>:<contraseña>@157.253.236.88:8087")

# client = MongoClient("mongodb://ISIS2304D33202610:dZ0ce0y9R0HV@157.253.236.88:808")
# TODO: conectarse a la base de datos Admonsis  
# db = client["ISIS2304D33202610"]
db = client["parranderos"]


@app.get("/")
def inicio():
    return {"estado": "API funcionando correctamente"}


@app.get('/bares/{bar_id}/comentarios')
def get_comentarios(bar_id: int):
    # Buscar en la colección "comentarios_bares"
    resultados = db["comentarios_bares"].find({"bar_id": bar_id})
    
    # Convertir los resultados a una lista que Python pueda enviar
    comentarios = []
    for documento in resultados:
        documento["_id"] = str(documento["_id"])  # MongoDB usa _id especial, lo convertimos a texto
        comentarios.append(documento)
    
    return comentarios  # Si no hay comentarios, devuelve una lista vacía []


@app.post('/bares/{bar_id}/comentarios')
def post_comentario(bar_id: int, datos: dict):
    # Agregar el bar_id y la fecha al documento (el PDF dice que ya están agregados ANTES del TODO)
    datos['bar_id'] = bar_id
    datos['fecha'] = datetime.now().isoformat()
    
    # Insertar en MongoDB
    resultado = db["comentarios_bares"].insert_one(datos)
    
    return {"mensaje": "Comentario guardado", "id": str(resultado.inserted_id)}


@app.get('/bares/{bar_id}/eventos')
def get_eventos(bar_id: int):
    # Buscar en la colección "eventos"
    resultados = db["eventos"].find({"bar_id": bar_id})
    
    # Convertir a lista
    eventos = []
    for documento in resultados:
        documento["_id"] = str(documento["_id"])
        eventos.append(documento)
    
    return eventos

@app.post('/bares/{bar_id}/eventos')
def post_evento(bar_id: int, datos: dict):
    # Agregar bar_id y fecha_creacion
    datos["bar_id"] = bar_id
    datos["fecha_creacion"] = datetime.now().isoformat()
    
    # Insertar en MongoDB
    resultado = db["eventos"].insert_one(datos)
    
    return {"mensaje": "Evento guardado", "id": str(resultado.inserted_id)}