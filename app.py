import streamlit as st
import requests
import urllib.parse

st.set_page_config(page_title="bairon IA", layout="centered")

if "chat" not in st.session_state:
    st.session_state.chat = []

with st.expander("Mandar foto, audio o PDF"):
    st.file_uploader("archivo", type=["png","jpg","jpeg","pdf"], label_visibility="collapsed")

for rol, txt, img in st.session_state.chat:
    with st.chat_message(rol):
        st.write(txt)
        if img:
            st.image(img, use_container_width=True)

p = st.chat_input("Escribe /imagen para crear imagen")

if p:
    st.session_state.chat.append(("user", p, None))
    with st.chat_message("user"):
        st.write(p)

    with st.chat_message("assistant"):
        low = p.lower()
        clean = low.replace("hazme una imagen de","").replace("haz una imagen de","").replace("/imagen","").replace("imagen de","").strip()
        if clean == "":
            clean = "los simpson"
        if "imagen" in low or "simpson" in low or "homero" in low:
            q = urllib.parse.quote(clean)
            url = "https://image.pollinations.ai/prompt/" + q + "?nologo=true"
            st.write("Generando imagen: " + clean)
            st.image(url, use_container_width=True)
            st.session_state.chat.append(("assistant", "Generando imagen: " + clean, url))
        else:
            qq = urllib.parse.quote(p)
            rr = requests.get("https://text.pollinations.ai/" + qq + "?model=openai", timeout=20)
            ans = rr.text
            st.write(ans)
            st.session_state.chat.append(("assistant", ans, None))