# 🤖 BimBam Buy AI – Multiagente Inteligente con LangGraph y RAG

> **Asistente inteligente de atención al cliente desarrollado con Inteligencia Artificial Generativa, LangGraph, LangChain, FAISS y Google Gemini.**

---

## 📌 Descripción del proyecto

**BimBam Buy AI** es un asistente virtual basado en una arquitectura **Multiagente**, diseñado para responder consultas de clientes de una tienda de comercio electrónico.

El sistema utiliza un **agente orquestador** que analiza cada consulta y la deriva automáticamente al agente especializado correspondiente.

Cada agente consulta una **base documental independiente** mediante **RAG (Retrieval-Augmented Generation)** utilizando índices **FAISS**, permitiendo generar respuestas fundamentadas en documentación oficial.

---

## 🌍 Aplicabilidad

Si bien este proyecto fue desarrollado para un escenario de **comercio electrónico**, la arquitectura implementada puede adaptarse fácilmente a otros sectores que requieran automatizar la atención y gestión de consultas, como:

- 🏦 Banca y servicios financieros
- 🛡️ Seguros
- 🏥 Salud
- 🎓 Educación
- 🏢 Servicios corporativos
- 🛒 Retail

La combinación de **IA Generativa**, **RAG** y una arquitectura **Multiagente** permite construir asistentes especializados, escalables y basados en conocimiento documental.

---

## 🚀 Tecnologías utilizadas

* 🐍 Python
* 🧠 Google Gemini
* 🔗 LangChain
* 🕸️ LangGraph
* 📚 FAISS Vector Store
* 📄 PyPDFLoader
* ✂️ RecursiveCharacterTextSplitter
* 💬 Gradio
* 💾 SQLite (Checkpointer)
* 🌐 Git & GitHub

---

## 🏗️ Arquitectura del proyecto

```text
Usuario
    │
    ▼
Agente Orquestador
    │
    ├──────────────► Agente Envíos
    │
    ├──────────────► Agente Garantías
    │
    ├──────────────► Agente Devoluciones
    │
    ├──────────────► Agente Pagos
    │
    └──────────────► Agente Afiliados

Cada agente consulta su propio índice FAISS
construido a partir de documentación PDF.
```

---

## 🤖 Agentes especializados

### 📦 Agente de Envíos

Responde consultas relacionadas con:

* tiempos de entrega
* costos de envío
* modalidades de envío
* cobertura

---

### 🛡️ Agente de Garantías

Especializado en:

* garantías
* cobertura
* plazos
* procedimientos

---

### 💰 Agente de Reembolsos y Devoluciones

Gestiona consultas sobre:

* devoluciones
* reembolsos
* cambios
* condiciones

---

### 💳 Agente de Métodos de Pago

Responde consultas relacionadas con:

* medios de pago
* cuotas
* promociones
* validaciones

---

### ⭐ Agente de Afiliados

Especializado en:

* inscripción
* beneficios
* funcionamiento del programa
* requisitos

---

# 📚 Base documental (RAG)

El asistente consulta cinco documentos independientes:

* 📄 Guía de Tiempos y Costos de Envío
* 📄 Manual de Garantías
* 📄 Política de Reembolsos y Devoluciones
* 📄 Preguntas Frecuentes sobre Métodos de Pago
* 📄 Programa de Afiliados

Cada documento fue procesado mediante:

* carga del PDF
* división en *chunks*
* generación de *embeddings*
* almacenamiento en índices **FAISS**

---

# 🧠 Funcionamiento

1. El usuario realiza una consulta.
2. El Agente Orquestador identifica el tema.
3. Selecciona el agente especializado.
4. El agente consulta el índice FAISS correspondiente.
5. Se recupera el contexto más relevante.
6. Google Gemini genera una respuesta basada en la documentación.

---

# 🖥️ Interfaz

La aplicación utiliza **Gradio** para ofrecer una interfaz web simple e intuitiva.

---

## 📸 Capturas del proyecto

### Diagrama del grafo

> ![Diagrama del grafo](grafo.png)

---

### Interfaz del asistente

> ![Consulta de envíos](consulta-envios.png)

![Consulta de garantías](consulta-garantias.png)

![Consulta de pagos](consulta-pagos.png)

![Consulta de devoluciones](consulta-devoluciones.png)

![Consulta de afiliados](consulta-afiliados.png)

---

### ☁️ Proyecto desplegado

> **📌 Agregar aquí la captura del proyecto ejecutándose en la nube (OCI).**

---

## 📂 Estructura del proyecto

```text
.
├── app.py
├── backend.py
├── Multiagente.ipynb
├── requirements.txt
├── data/
│   └── pdfs/
├── faiss_envios/
├── faiss_garantias/
├── faiss_devoluciones/
├── faiss_pagos/
├── faiss_afiliados/
└── imágenes/
```

---

## ⚙️ Instalación

Clonar el repositorio:

```bash
git clone https://github.com/evs-11/ai-ecommerce-agent.git
```

Ingresar al proyecto:

```bash
cd ai-ecommerce-agent
```

Crear un entorno virtual:

```bash
python -m venv .venv
```

Activarlo:

### Windows

```bash
.venv\Scripts\activate
```

Instalar dependencias:

```bash
pip install -r requirements.txt
```

---

## ▶️ Ejecución

```bash
python app.py
```

La aplicación quedará disponible en:

```text
http://127.0.0.1:7860
```

---

## 💡 Características principales

* ✅ Arquitectura Multiagente
* ✅ LangGraph
* ✅ Orquestación inteligente
* ✅ RAG con documentación PDF
* ✅ Índices FAISS persistentes
* ✅ Recuperación de contexto
* ✅ Google Gemini
* ✅ Interfaz con Gradio
* ✅ Persistencia mediante SQLite
* ✅ Código modular

---

## 👩‍💻 Autor

**Elida Schultz**

---

## ⭐ Agradecimientos

A **Alura Latam** y a **Oracle Next Education (ONE)** por brindar la oportunidad de desarrollar este proyecto aplicando técnicas modernas de Inteligencia Artificial Generativa, recuperación aumentada (RAG) y arquitecturas Multiagente.

---

## 📌 Notas

El código y la documentación son parte del portfolio profesional de la autora.
