import streamlit as st
import time

st.set_page_config(page_title="Bairon AI", page_icon="🤖", layout="centered")

# --- CSS PARA QUE SE VEA COMO APP, NO COMO WEB ---
st.markdown("""
<style>
    .block-container { padding-top: 1rem; padding-bottom: 6rem; max-width: 750px; }
    header { visibility: hidden; }
    [data-testid="stChatMessage"] { border-radius: 20px; padding: 10px; }
    /* Usuario a la derecha */
    [data-testid="stChatMessage"]:has(div[data-testid="stChatMessageAvatarUser"]) {
        flex-direction: row-reverse; background: #2b2d31;
    }
</style>
""", unsafe_allow_html=True)

st.title("Bairon AI 🤖")

# --- MEMORIA ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hola, soy Bairon AI. ¿En qué te ayudo hoy?"}
    ]

# --- MOSTRAR HISTORIAL ---
for m in st.session_state.messages:
    avatar = "🧑" if m["role"] == "user" else "🤖"
    with st.chat_message(m["role"], avatar=avatar):
        st.markdown(m["content"])
        if "image" in m:
            st.image(m["image"])

# --- ENTRADA POR VOZ + TEXTO ---
col1, col2 = st.columns([4, 1])
with col2:
    audio =