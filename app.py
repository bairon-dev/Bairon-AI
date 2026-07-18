import streamlit as st
import urllib.parse
from groq import Groq

st.set_page_config(page_title="Bairon-AI", layout="centered")

st.markdown("""
<style>
.stApp { background-color: #0e0e0e; }
h1 { color: white!important; font-size: 26px!important; }
.user-bubble { background-color: white; color: black; padding: 12px 18px; border-radius: 20px; max-width: 85%; float: right; margin: 8px 0; }
.bot-bubble { background-color: #2a2a2a; color: white; padding: 14px 18px; border-radius: 20px; max-width: 90%; margin: 8px 0; }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1>Bairon-AI - Garcia NL</h1>", unsafe_allow_html=True)

# CONECTA CEREBRO
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

if "chat" not in st.session_state:
    st.session_state.chat = []

for msg in st.session_state.chat:
    if msg["role"] == "user":
        st.markdown(f'<div style="display:flex; justify-content:flex-end;"><div class="user-bubble">{msg["content"]}</div></div>', unsafe_allow_html=True)
    else:
        if msg["type"] == "text":
            st.markdown(f'<div class="bot-bubble">{msg["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="bot-bubble">Generando imagen: {msg["prompt"]}</div>', unsafe_allow_html=True)
            st.image(msg["content"], use_container_width=True)

prompt = st.chat_input("Escribe algo o /imagen...")

if prompt:
    st.session_state.chat.append({"role": "user", "type": "text", "content": prompt})

    if prompt.lower().startswith("/imagen"):
        texto = prompt.replace("/imagen", "").strip() or "tesla en el cerro de la silla"
        encoded = urllib.parse.quote(texto)
        img_url = f"https://image.pollinations.ai/prompt/{encoded}?width=1024&height=1024&nologo=true"
        st.session_state.chat.append({"role": "bot", "type": "image", "content": img_url, "prompt": texto})
    else:
        # CEREBRO AQUÍ
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "Eres Bairon-AI, creada por Bairon en Garcia, NL. Eres inteligente, hablas español mexicano, regio, breve. Si piden frase, haz una frase chida."},
                *[{"role": m["role"], "content": m["content"]} for m in st.session_state.chat if m["type"]=="text"][-8:]
            ]
        )
        respuesta = completion.choices[0].message.content
        st.session_state.chat.append({"role": "bot", "type": "text", "content": respuesta})

    st.rerun()