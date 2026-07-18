
import streamlit as st
from groq import Groq
import urllib.parse

st.set_page_config(page_title="bairon IA", page_icon="b", layout="centered")

st.markdown("""
<style>
#MainMenu, footer, header {visibility: hidden;}
.stApp {background:#000000;}
h1 {text-align:center; font-weight:300; letter-spacing:6px; color:white; font-size:28px; margin-top:15px;}
</style>
""", unsafe_allow_html=True)

st.markdown("<h1>bairon IA</h1>", unsafe_allow_html=True)

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({
        "role": "assistant",
        "content": "Soy Bairon AI: Hazme una imagen de una tesla en el cerro de la silla. ¿Quieres que te genere una imagen? Usa /imagen + lo que quieras."
    })

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        if "pollinations.ai" in m["content"]:
            st.image(m["content"])
        else:
            st.markdown(m["content"])

if prompt := st.chat_input("Escribe /imagen para crear imagen"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        low = prompt.lower()
        if "/imagen" in low or "imagen de" in low or "hazme una imagen" in low:
            q = low.replace("/imagen","").replace("hazme una imagen de","").replace("hazme una imagen","").replace("imagen de","").strip()
            if q == "":
                q = "una tesla en el cerro de la silla"
            msg_gen = f"Generando imagen: {q}"
            st.markdown(msg_gen)
            st.session_state.messages.append({"role": "assistant", "content": msg_gen})
            url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(q)}?width=1024&height=1024&nologo=true&enhance=true"
            st.image(url)
            st.session_state.messages.append({"role": "assistant", "content": url})
        else:
            historial = []
            for x in st.session_state.messages[-8:]:
                if "pollinations.ai" not in x["content"]:
                    historial.append({"role": x["role"], "content": x["content"]})
            resp = client.chat.completions.create(
                model="llama-