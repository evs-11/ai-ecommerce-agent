import streamlit as st
import uuid

from backend import graph


def responder_consulta(pregunta):

    try:

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

    except Exception as e:

        return f"❌ Error: {e}"


st.set_page_config(
    page_title="BimBam Buy AI",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 BimBam Buy AI")

st.write(
    """
Asistente inteligente de atención al cliente.

Puedes consultar sobre:

- 📦 Envíos
- 🛡️ Garantías
- 💰 Devoluciones
- 💳 Métodos de pago
- ⭐ Programa de afiliados
"""
)

pregunta = st.text_area(
    "Escribe tu consulta",
    placeholder="Ej.: ¿Cuánto demora un envío a Córdoba?"
)

if st.button("Consultar"):

    if pregunta.strip():

        with st.spinner("Consultando..."):

            respuesta = responder_consulta(pregunta)

        st.success("Respuesta")

        st.write(respuesta)