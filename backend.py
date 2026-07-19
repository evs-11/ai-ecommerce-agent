
# backend.py

import os
import re
import sqlite3
from dotenv import load_dotenv
from typing import TypedDict, List
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.sqlite import SqliteSaver
import warnings
warnings.filterwarnings("ignore", message=".*TqdmWarning.*")


from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS

import streamlit as st


# Carga las variables de entorno desde el archivo .env, si no utilizamos Streamlit, se ejecutaria ésto.
#load_dotenv()

# Define las variables de entorno
#GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")



# Como utilizamos Streamlit usamos esto:
load_dotenv()

try:
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
except Exception:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")



# Define el estado del agente (AgentState)

class AgentState(TypedDict):
    user_question: str
    category: str
    agent_selected: str
    response: str
    messages: List[str]

# Inicializa la base de datos para checkpoints
conn = sqlite3.connect("checkpoints.db", check_same_thread=False)
memory = SqliteSaver(conn)


# Inicializa el modelo de lenguaje
model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0
)


embeddings = GoogleGenerativeAIEmbeddings(
    model="models/gemini-embedding-001",
    google_api_key=GEMINI_API_KEY
)


# funciones


def cargar_pdf_envios():

    loader = PyPDFLoader(
        "data/pdfs/Guias de Tiempos y Costos de Envío de BimBay Buy.pdf"
    )

    documentos = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    chunks = splitter.split_documents(documentos)

    return chunks



def cargar_pdf_garantias():

    loader = PyPDFLoader(
        "data/pdfs/Manual de Garantía de Productos de BimBam Buy.pdf"
    )

    documentos = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    chunks = splitter.split_documents(documentos)

    return chunks



def cargar_pdf_devoluciones():

    loader = PyPDFLoader(
        "data/pdfs/Políticas de Reembolsos y Devoluciones de BimBAm Buy.pdf"
    )

    documentos = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    chunks = splitter.split_documents(documentos)

    return chunks        



def cargar_pdf_pagos():

    loader = PyPDFLoader(
        "data/pdfs/Preguntas Frecuentes sobre Métodos de Pago de BimBam Buy.pdf"
    )

    documentos = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    chunks = splitter.split_documents(documentos)

    return chunks


def cargar_pdf_afiliados():

    loader = PyPDFLoader(
        "data/pdfs/Programa de Afiliados de BimBam Buy.pdf"
    )

    documentos = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    chunks = splitter.split_documents(documentos)

    return chunks    



# Indices


chunks_envios = cargar_pdf_envios()

if os.path.exists("faiss_envios"):

    vector_envios = FAISS.load_local(
        "faiss_envios",
        embeddings,
        allow_dangerous_deserialization=True
    )

    print("FAISS de envíos cargado correctamente")

else:

    vector_envios = FAISS.from_documents(
        chunks_envios,
        embeddings
    )

    vector_envios.save_local("faiss_envios")

    print("FAISS de envíos creado correctamente")



chunks_garantias = cargar_pdf_garantias()

if os.path.exists("faiss_garantias"):

    vector_garantias = FAISS.load_local(
        "faiss_garantias",
        embeddings,
        allow_dangerous_deserialization=True
    )

    print("FAISS de garantías cargado correctamente")

else:

    vector_garantias = FAISS.from_documents(
        chunks_garantias,
        embeddings
    )

    vector_garantias.save_local("faiss_garantias")

    print("FAISS de garantías creado correctamente")



chunks_devoluciones = cargar_pdf_devoluciones()

if os.path.exists("faiss_devoluciones"):

    vector_devoluciones = FAISS.load_local(
        "faiss_devoluciones",
        embeddings,
        allow_dangerous_deserialization=True
    )

    print("FAISS de devoluciones cargado correctamente")

else:

    vector_devoluciones = FAISS.from_documents(
        chunks_devoluciones,
        embeddings
    )

    vector_devoluciones.save_local("faiss_devoluciones")

    print("FAISS de devoluciones creado correctamente")



chunks_pagos = cargar_pdf_pagos()

if os.path.exists("faiss_pagos"):

    vector_pagos = FAISS.load_local(
        "faiss_pagos",
        embeddings,
        allow_dangerous_deserialization=True
    )

    print("FAISS de pagos cargado correctamente")

else:

    vector_pagos = FAISS.from_documents(
        chunks_pagos,
        embeddings
    )

    vector_pagos.save_local("faiss_pagos")

    print("FAISS de pagos creado correctamente")



chunks_afiliados = cargar_pdf_afiliados() 

if os.path.exists("faiss_afiliados"): 

    vector_afiliados = FAISS.load_local(
         "faiss_afiliados",
         embeddings, 
         allow_dangerous_deserialization=True 
    ) 
    
    print("FAISS de afiliados cargado correctamente") 
    
else: 

    vector_afiliados = FAISS.from_documents( 
        chunks_afiliados,
        embeddings 
    ) 
    
    vector_afiliados.save_local("faiss_afiliados") 
    
    print("FAISS de afiliados creado correctamente")

      


# Prompts
triage_prompt = """
Eres un agente orquestador de atención al cliente.

Tu función es analizar la consulta del usuario y decidir qué agente especializado debe atenderla.

No debes responder directamente la consulta.
Solo debes identificar el agente correspondiente.

Agentes disponibles:

- agente_envios
- agente_garantias
- agente_devoluciones
- agente_pagos
- agente_afiliados

Devuelve únicamente uno de estos valores:

agente_envios
agente_garantias
agente_devoluciones
agente_pagos
agente_afiliados

No agregues explicaciones, puntuación ni texto adicional.
"""


prompt_agente_envios = """
Eres un especialista en tiempos, costos y modalidades de envío.

Responde únicamente preguntas relacionadas con envíos.

Si la consulta no pertenece a este tema, indica que debe ser atendida por otro agente.
"""

prompt_agente_garantias = """
Eres un especialista en garantías de productos.

Responde consultas sobre cobertura, plazos, condiciones y procedimientos de garantía.
"""

prompt_agente_devoluciones = """
Eres un especialista en políticas de reembolsos y devoluciones.

Explica claramente los requisitos, plazos y procedimientos.
"""

prompt_agente_pagos = """
Eres un especialista en métodos de pago.

Responde preguntas sobre medios de pago aceptados, cuotas, promociones y validaciones.
"""

prompt_agente_afiliados = """
Eres un especialista en el programa de afiliados.

Explica beneficios, requisitos de inscripción y funcionamiento del programa.
"""



# Nodos

def nodo_orquestador(state: AgentState):

    response = model.invoke(
        triage_prompt
        + f"\nConsulta del usuario: {state['user_question']}"
    )

    agente = response.content.strip()

    return {
        "agent_selected": agente,
        "messages": state["messages"] + [
            "El orquestador seleccionó: " + agente
        ]
    }


def nodo_agente_envios(state: AgentState):

    documentos = vector_envios.similarity_search(
        state["user_question"],
        k=3
    )

    contexto = "\n\n".join(
        documento.page_content
        for documento in documentos
    )

    response = model.invoke(
        prompt_agente_envios
        + "\n\nUsa esta información del documento:\n"
        + contexto
        + f"\n\nConsulta del usuario: {state['user_question']}"
    )

    return {
        "response": response.content,
        "messages": state["messages"] + [
            "Respondió agente envíos usando PDF"
        ]
    }


def nodo_agente_garantias(state: AgentState):

    documentos = vector_garantias.similarity_search(
        state["user_question"],
        k=3
    )

    contexto = "\n\n".join(
        documento.page_content
        for documento in documentos
    )

    response = model.invoke(
        prompt_agente_garantias
        + "\n\nInformación del documento:\n"
        + contexto
        + f"\n\nConsulta del usuario: {state['user_question']}"
    )

    return {
        "response": response.content,
        "messages": state["messages"] + [
            "Respondió agente garantías usando PDF"
        ]
    }



def nodo_agente_devoluciones(state: AgentState):

    documentos = vector_devoluciones.similarity_search(
        state["user_question"],
        k=3
    )

    contexto = "\n\n".join(
        documento.page_content
        for documento in documentos
    )

    response = model.invoke(
        prompt_agente_devoluciones
        + "\n\nInformación del documento:\n"
        + contexto
        + f"\n\nConsulta del usuario: {state['user_question']}"
    )

    return {
        "response": response.content,
        "messages": state["messages"] + [
            "Respondió agente devoluciones usando PDF"
        ]
    }



def nodo_agente_pagos(state: AgentState):

    documentos = vector_pagos.similarity_search(
        state["user_question"],
        k=3
    )

    contexto = "\n\n".join(
        documento.page_content
        for documento in documentos
    )

    response = model.invoke(
        prompt_agente_pagos
        + "\n\nInformación del documento:\n"
        + contexto
        + f"\n\nConsulta del usuario: {state['user_question']}"
    )

    return {
        "response": response.content,
        "messages": state["messages"] + [
            "Respondió agente pagos usando PDF"
        ]
    }


def nodo_agente_afiliados(state: AgentState):

    documentos = vector_afiliados.similarity_search(
        state["user_question"],
        k=3
    )

    contexto = "\n\n".join(
        documento.page_content
        for documento in documentos
    )

    response = model.invoke(
        prompt_agente_afiliados
        + "\n\nInformación del documento:\n"
        + contexto
        + f"\n\nConsulta del usuario: {state['user_question']}"
    )

    return {
        "response": response.content,
        "messages": state["messages"] + [
            "Respondió agente afiliados usando PDF"
        ]
    }


def seleccionar_agente(state: AgentState):
    """
    Devuelve el nombre del agente seleccionado por el orquestador.
    LangGraph utiliza este valor para decidir qué rama del grafo seguir.
    """
    return state["agent_selected"]



# Construcción del grafo
builder = StateGraph(AgentState)

builder.add_node("orquestador", nodo_orquestador)

builder.add_node("agente_envios", nodo_agente_envios)
builder.add_node("agente_garantias", nodo_agente_garantias)
builder.add_node("agente_devoluciones", nodo_agente_devoluciones)
builder.add_node("agente_pagos", nodo_agente_pagos)
builder.add_node("agente_afiliados", nodo_agente_afiliados)

builder.set_entry_point("orquestador")


# Arista Condicional
builder.add_conditional_edges(
    "orquestador",
    seleccionar_agente,
    {
        "agente_envios": "agente_envios",
        "agente_garantias": "agente_garantias",
        "agente_devoluciones": "agente_devoluciones",
        "agente_pagos": "agente_pagos",
        "agente_afiliados": "agente_afiliados",
    },
)


# Arista Secuencial
builder.add_edge("agente_envios", END)
builder.add_edge("agente_garantias", END)
builder.add_edge("agente_devoluciones", END)
builder.add_edge("agente_pagos", END)
builder.add_edge("agente_afiliados", END)

graph = builder.compile(checkpointer=memory)