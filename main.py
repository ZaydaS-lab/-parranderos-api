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
    comentarios =  db["bares"].finde_one({"Comentarios escritos": bar_id}, {"_id": 0})

    # TODO: completar
    return comentarios or {}

@app.post('/bares/{bar_id}/comentarios')
def post_comentario(bar_id: int, datos: dict):


    #Son campos que existen pero no se deben pedir al usuario

    datos['bar_id'] = bar_id
    datos['fecha']  = datetime.now().isoformat()
    # TODO: completar
    db["comentarios"].insert_one[datos]

    return {'mensaje': 'Comentario guardado'}

# TODO: implementar GET /bares/{bar_id}/eventos
# Debe retornar todos los eventos del bar desde la colección 'eventos'

@app.get('/bares/{bar_id}/eventos')
def get_eventos(bar_id: int):
    eventos = list(db.eventos.find({"bar_id": bar_id},{"_id": 0}))

    # TODO: completar
    return eventos or {}


# TODO: implementar POST /bares/{bar_id}/eventos  
# Debe insertar el evento en la colección 'eventos'
# Recuerde agregar bar_id y fecha_creacion al documento antes de insertar
@app.post('/bares/{bar_id}/eventos')
def post_evento(bar_id: int, datos: dict):

    datos["bar_id"] = bar_id
    datos["fecha_creacion"] = datetime.now()
    #Son campos que existen pero no se deben pedir al usuario
    # TODO: completar
    resultado = db.db["evento"].insert_one[datos]

 
