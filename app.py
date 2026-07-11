
import gradio as gr
from backend import graph
import uuid

def consultar_asistente(pregunta: str):

    thread_id = str(uuid.uuid4())

    thread_config = {
        "configurable": {
            "thread_id": thread_id
        }
    }

    initial_state = {
        "user_question": pregunta,
        "category": "",
        "agent_selected": "",
        "response": "",
        "messages": []
    }

    respuesta = ""

    for s in graph.stream(initial_state, thread_config):

        step = list(s.values())[0]

        if "response" in step:
            respuesta = step["response"]

    return respuesta

