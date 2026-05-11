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
    comentarios = db["comentarios".find()]
    return comentarios

@app.post('/bares/{bar_id}/comentarios')
def post_eventpos(bar_id: int, datos: dict):
    datos['bar_id'] = bar_id
    datos['fecha']  = datetime.now().isoformat()
    # TODO: completar
    return {'mensaje': 'Comentario guardado'}

# TODO: implementar GET /bares/{bar_id}/eventos
# Debe retornar todos los eventos del bar desde la colección 'eventos'
@app.get('/bares/{bar_id}/eventos')
def get_eventos(bar_id: int):
    eventos = db["eventos".find()]
    return eventos

# TODO: implementar POST /bares/{bar_id}/eventos  
# Debe insertar el evento en la colección 'eventos'
# Recuerde agregar bar_id y fecha_creacion al documento antes de insertar
@app.post('/bares/{bar_id}/eventos')
def post_eventos(bar_id: int, datos: dict):
    datos['bar_id'] = bar_id
    datos['fecha']  = datetime.now().isoformat()
    # TODO: completar
    return {'mensaje': 'evento guardado'}

# Comentario: BAR_ID, E-MAIL, NOMBRE DE LA PERSONA QUE COMENTA, ID DEL COMENTARIO, FECHA, TEXTO, Clificacion
# Evento: lugar, fecha, hoR, tematica, id, limite de personas
 
