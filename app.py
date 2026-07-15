
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



# ==========================================
# app.py
# Interfaz gráfica con Gradio
# ==========================================

import gradio as gr
import uuid

# Importa el grafo construido en backend.py
from backend import graph


# ==========================================
# Función que ejecuta el multiagente
# ==========================================

def responder_consulta(pregunta):

    try:

        # Crea un identificador único para cada conversación
        thread_id = str(uuid.uuid4())

        thread_config = {
            "configurable": {
                "thread_id": thread_id
            }
        }

        # Estado inicial del grafo
        initial_state = {
            "user_question": pregunta,
            "category": "",
            "agent_selected": "",
            "response": "",
            "messages": []
        }

        respuesta = ""

        # Ejecuta el grafo paso a paso
        for s in graph.stream(initial_state, thread_config):

            step = list(s.values())[0]

            # Obtiene la respuesta del agente
            if "response" in step:
                respuesta = step["response"]

        return respuesta

    except Exception as e:

        # Muestra el error completo en la terminal
        print(f"Error: {e}")

        # Devuelve un mensaje amigable en Gradio
        return (
            "❌ Ocurrió un error al procesar la consulta.\n\n"
            f"Detalle técnico: {e}"
        )


# ==========================================
# Construcción de la interfaz gráfica
# ==========================================

with gr.Blocks(
    theme=gr.themes.Soft(
        primary_hue="blue",
        secondary_hue="slate",
        neutral_hue="slate",
        spacing_size="sm",
        text_size="sm"
    ),
    title="BimBam Buy AI"
) as demo:

    # Título
    gr.Markdown("""
# 🤖 BimBam Buy AI

### Asistente Inteligente de Atención al Cliente
""")

    # Descripción
    gr.Markdown("""
Bienvenido al asistente inteligente de **BimBam Buy**.

Puedes realizar consultas sobre:

📦 Envíos

🛡️ Garantías

💰 Reembolsos y devoluciones

💳 Métodos de pago

⭐ Programa de afiliados
""")

    gr.Markdown("---")

    with gr.Row():

        # Caja donde escribe el usuario
        pregunta = gr.Textbox(
            label="Escribe tu consulta",
            placeholder="Ej.: ¿Cuánto demora un envío a Córdoba?",
            lines=2,
            autofocus=True
        )

        # Botón
        boton = gr.Button(
            "💬 Consultar",
            variant="primary",
            size="lg"
        )

    # Información sobre el asistente
    gr.Markdown(
        "📚 **Las respuestas se generan utilizando Inteligencia Artificial y la documentación oficial de BimBam Buy almacenada en la base de conocimiento.**"
    )


    # Caja donde aparece la respuesta
    respuesta = gr.Textbox(
        label="Respuesta del asistente",
        lines=12,
)   

    # Asociación del botón con la función
    boton.click(
        fn=responder_consulta,
        inputs=pregunta,
        outputs=respuesta
    )


# ==========================================
# Ejecutar la aplicación
# ==========================================

if __name__ == "__main__":
    demo.launch(share=False, prevent_thread_lock=True)