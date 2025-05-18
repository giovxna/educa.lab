import os
import textwrap
import warnings
import streamlit as st
from datetime import date
from google import genai
from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

# Configurar a API
st.set_page_config(page_title="EducaLab", layout="centered")
st.title("🧠 EducaLab - Aprenda do seu jeito")

GOOGLE_API_KEY = st.secrets.get("GOOGLE_API_KEY") or st.text_input("🔑 Insira sua GOOGLE_API_KEY:", type="password")
if GOOGLE_API_KEY:
    os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY
    client = genai.Client()
    MODEL_ID = "gemini-2.0-flash"

    def to_markdown(text):
        text = text.replace('•', '  *')
        return textwrap.indent(text, '> ', predicate=lambda _: True)

    def call_agent(agent: Agent, message_text: str) -> str:
        session_service = InMemorySessionService()
        runner = Runner(agent=agent, app_name=agent.name, session_service=session_service)
        content = types.Content(role="user", parts=[types.Part(text=message_text)])
        final_response = ""
        for event in runner.run(user_id="user1", session_id="session1", new_message=content):
            if event.is_final_response():
                for part in event.content.parts:
                    if part.text is not None:
                        final_response += part.text + "\n"
        return final_response

    def criar_agente_explicador(modo_usuario):
        instrucoes = {
            "infantil": "Explique como se o usuário tivesse 5 anos...",
            "ensino_medio": "Explique como para um estudante do ensino médio...",
            "adulto": "Explique de forma clara e técnica...",
            "fofoca": "Explique como se fosse uma fofoca...",
            "memes": "Explique com tom de meme e linguagem da internet..."
        }
        return Agent(
            name="agente_explicador",
            model=MODEL_ID,
            instruction=instrucoes.get(modo_usuario, "Explique de forma clara."),
            description="Agente que explica conceitos com estilo personalizado."
        )

    def agente_quiz(assunto):
        agent = Agent(name="quiz", model=MODEL_ID, instruction="Crie um quiz simples.", description="Quiz")
        return call_agent(agent, f"Crie uma pergunta sobre: {assunto}")

    def agente_link_alura(assunto):
        agent = Agent(name="link_alura", model=MODEL_ID, instruction="Sugira um curso da Alura.", description="Cursos")
        return call_agent(agent, f"Sugira um curso para: {assunto}")

    def agente_plano_estudo(assunto):
        agent = Agent(
            name="plano_estudo",
            model=MODEL_ID,
            instruction="Crie um plano de estudo básico sobre esse tema.",
            description="Plano de estudo"
        )
        return call_agent(agent, f"Plano de estudos sobre: {assunto}")

    with st.form("formulario"):
        assunto = st.text_input("📚 O que você quer aprender?")
        tempo = st.selectbox("⏱️ Tempo disponível:", ["2", "5", "10", "15"])
        estilo = st.selectbox("🧠 Estilo de explicação:", {
            "👶 Como se eu tivesse 5 anos": "infantil",
            "🧑 Ensino médio": "ensino_medio",
            "👨‍🎓 Adulto curioso": "adulto",
            "🤪 Fofoca divertida": "fofoca",
            "😂 Em memes": "memes",
            "🎲 Aleatório": "aleatorio"
        }.keys())
        submitted = st.form_submit_button("📖 Aprender agora!")

    if submitted and assunto:
        if estilo == "🎲 Aleatório":
            import random
            estilo_escolhido = random.choice(["infantil", "ensino_medio", "adulto", "fofoca", "memes"])
            st.info(f"🎲 Estilo sorteado: {estilo_escolhido}")
        else:
            estilo_escolhido = {
                "👶 Como se eu tivesse 5 anos": "infantil",
                "🧑 Ensino médio": "ensino_medio",
                "👨‍🎓 Adulto curioso": "adulto",
                "🤪 Fofoca divertida": "fofoca",
                "😂 Em memes": "memes"
            }[estilo]

        explicador = criar_agente_explicador(estilo_escolhido)
        prompt = f"Explique o conceito de '{assunto}' em no máximo {tempo} minutos."
        explicacao = call_agent(explicador, prompt)
        quiz = agente_quiz(assunto)
        link = agente_link_alura(assunto)
        plano = agente_plano_estudo(assunto)

        st.subheader("📚 Explicação:")
        st.markdown(to_markdown(explicacao))

        st.subheader("❓ Quiz:")
        st.markdown(to_markdown(quiz))

        st.subheader("📎 Curso sugerido:")
        st.markdown(to_markdown(link))

        st.subheader("🗂️ Plano de Estudos:")
        st.markdown(to_markdown(plano))

else:
    st.warning("⚠️ Insira sua chave da API Google para começar.")
