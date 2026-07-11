
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



# Carga las variables de entorno desde el archivo .env
load_dotenv()

# Define las variables de entorno
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

    response = model.invoke(
        prompt_agente_envios
        + f"\nConsulta del usuario: {state['user_question']}"
    )

    return {
        "response": response.content,
        "messages": state["messages"] + [
            "Respondió agente envíos"
        ]
    }

def nodo_agente_garantias(state: AgentState):

    response = model.invoke(
        prompt_agente_garantias
        + f"\nConsulta del usuario: {state['user_question']}"
    )

    return {
        "response": response.content,
        "messages": state["messages"] + [
            "Respondió agente garantías"
        ]
    }

def nodo_agente_devoluciones(state: AgentState):

    response = model.invoke(
        prompt_agente_devoluciones
        + f"\nConsulta del usuario: {state['user_question']}"
    )

    return {
        "response": response.content,
        "messages": state["messages"] + [
            "Respondió agente devoluciones"
        ]
    }


def nodo_agente_pagos(state: AgentState):

    response = model.invoke(
        prompt_agente_pagos
        + f"\nConsulta del usuario: {state['user_question']}"
    )

    return {
        "response": response.content,
        "messages": state["messages"] + [
            "Respondió agente pagos"
        ]
    }


def nodo_agente_afiliados(state: AgentState):

    response = model.invoke(
        prompt_agente_afiliados
        + f"\nConsulta del usuario: {state['user_question']}"
    )

    return {
        "response": response.content,
        "messages": state["messages"] + [
            "Respondió agente afiliados"
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