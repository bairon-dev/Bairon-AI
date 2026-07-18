

import streamlit as st
import urllib.parse
from groq import Groq

st.set_page_config(page_title="bairon IA", layout="centered")

# DISEÑO BONITO COMO LA FOTO
st.markdown("""
<style>
#MainMenu, footer, header {visibility:hidden;}
.stApp {background:#0a0a0a;}
h1 {text-align:center; font-weight:800; letter-spacing:5px; font-size:50px!important; color:white; margin-top:10px;}

.user-bubble {
    background:white; color:black; padding:14px 18px; border-radius:20px 20px 0 20px;
    max-width:80%; margin:10px 0 10px auto; text-align:left; font-size:16px;
}
.bot-bubble {
    background:#1e1e1e; color:white; padding:14px 18px; border-radius:20px 20px 20px 0;
    max-width:80%; margin:10px auto 10px 0; text-align:left; font-size:16px;
}
</style>
""", unsafe_allow_html=True)

st.markdown("<h1>bairon IA</h1>", unsafe_allow_html=True)

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar historial bonito
for m in st.session_state.messages:
    if m["role"] == "user":
        st.markdown(f'<div class="user-bubble">{m["content"]}</div>', unsafe_allow_html=True)
    else:
        if "pollinations.ai" in m["content"]:
            st.markdown(f'<div class="bot-bubble">Generando imagen: {m.get("prompt","")}</div>', unsafe_allow_html=True)
            st.image(m["content"])
        else:
            st.markdown(f'<div class="bot-bubble">{m["content"]}</div>', unsafe_allow_html=True)

# Si no hay mensajes, saludo inicial
if len(st.session_state.messages) == 0:
    st.markdown('<div class="bot-bubble">Hola, ¿en qué puedo ayudarte?<br><br>Usa <b>/imagen</b> para crear imagenes</div>', unsafe_allow_html=True)

prompt = st.chat_input("Escribe /imagen para crear imagen")

if prompt:
    st.session_state.messages.append({"role":"user","content":prompt})
    st.markdown(f'<div class="user-bubble">{prompt}</div>', unsafe_allow_html=True)

    if "/imagen" in prompt.lower():
        q = prompt.lower().replace("/imagen","").strip()
        if q == "": q = "tesla en el cerro de la silla"
        st.markdown(f'<div class="bot-bubble">Generando imagen: {q}</div>', unsafe_allow_html=True)
        url = "https://image.pollinations.ai/prompt/" + urllib.parse.quote(q) + "?width=1024&height=1024&nologo=true&enhance=true"
        st.image(url)
        st.session_state.messages.append({"role":"assistant","content":url, "prompt":q})
    else:
        resp = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role":"system","content":"Eres bairon IA"}, {"role":"user","content":prompt}]
        )
        ans = resp.choices[0].message.content
        st.markdown(f'<div class="bot-bubble">{ans}</div>', unsafe_allow_html=True)
        st.session_state.messages.append({"role":"assistant","content":ans})