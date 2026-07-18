import streamlit as st
import requests, time

st.set_page_config(page_title="Bairon AI", page_icon="🤖", layout="centered")

# --- ESTO HACE QUE OCUPE TODA LA PANTALLA ---
st.markdown("""
<style>
.block-container { max-width: 100% !important; padding: 0 10px !important; }
header {visibility: hidden;}
footer {visibility: hidden;}
[data-testid="stChatMessage"] { border-radius: 18px; margin-bottom: 10px; }
</style>
""", unsafe_allow_html=True)

st.title("Bairon AI 🤖")

# 1. GUARDA HISTORIAL
if "messages" not in st.session_state:
    st.session_state.messages = [{"role":"assistant","content":"Hola, soy Bairon AI 👋