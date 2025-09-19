import os
from dotenv import load_dotenv
import google.generativeai as genai
import streamlit as st

# ------------------------
# Configuração da API
# ------------------------
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("❌ API Key do Gemini não encontrada no arquivo .env")
    st.stop()

genai.configure(api_key=api_key)

# Lista modelos disponíveis
available_models = [m for m in genai.list_models() if "generateContent" in m.supported_generation_methods]

if not available_models:
    st.error("❌ Nenhum modelo disponível para generateContent na sua conta.")
    st.stop()

# ------------------------
# Configuração da interface
# ------------------------
st.set_page_config(page_title="Chatbot Gemini", page_icon="🤖", layout="centered")
st.title("🤖 Chatbot com Gemini")

# Menu lateral para escolha do modelo
st.sidebar.header("⚙️ Configurações")
chosen_model = st.sidebar.selectbox(
    "Escolha o modelo:",
    options=[m.name for m in available_models],
    index=0,
)

st.sidebar.info(f"Modelo selecionado: `{chosen_model}`")

# Inicializa modelo e chat (reseta se mudar o modelo)
if "chosen_model" not in st.session_state or st.session_state.chosen_model != chosen_model:
    st.session_state.chosen_model = chosen_model
    st.session_state.model = genai.GenerativeModel(chosen_model)
    st.session_state.chat = st.session_state.model.start_chat(history=[])

# ------------------------
# Histórico e Chat
# ------------------------
# Exibe histórico de conversa
for msg in st.session_state.chat.history:
    role = "user" if msg.role == "user" else "assistant"
    with st.chat_message(role):
        st.markdown(msg.parts[0].text)

# Caixa de entrada
user_input = st.chat_input("Digite sua mensagem...")

if user_input:
    # Mostra mensagem do usuário
    with st.chat_message("user"):
        st.markdown(user_input)

    try:
        # Resposta do modelo
        response = st.session_state.chat.send_message(user_input)
        with st.chat_message("assistant"):
            st.markdown(response.text)
    except Exception as e:
        st.error(f"Erro: {e}")
