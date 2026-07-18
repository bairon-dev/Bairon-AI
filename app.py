import streamlit as st
import requests
import urllib.parse

st.set_page_config(page_title="Bairon AI", layout="wide")

if "c" not in st.session_state:
    st.session_state.c = []

with st.expander("Mandar foto, audio o PDF"):
    f = st.file_uploader("Foto", type=["png","jpg","jpeg"])
    a = st.audio_input("Grabar voz")

for r,m,i in st.session_state.c:
    with st.chat_message(r, avatar="😊" if r=="user" else "🤖"):
        st.write(m)
        if i:
            st.image(i)

p = st.chat_input("Escribe /imagen para imagen")

if a and not p:
    p = "Hola"

if p:
    st.session_state.c.append(("user", p, None))
    with st.chat_message("user", avatar="😊"):
        st.write(p)
    with st.chat_message("assistant", avatar="🤖"):
        low = p.lower()
        if "bairon-dev" in low or "quien soy" in low or "me conoces" in low:
            ans = "Si, eres Bairon, bairon-dev, mi creador."
        elif "quien te creo" in low:
            ans = "Me creo Bairon-dev."
        elif "/imagen" in low or "imagen de" in low or "dibuja" in low:
            clean = p.replace("/imagen","").strip() or "homero simpson"
            q = urllib.parse.quote(clean)
            url = f"https://image.pollinations.ai/prompt/{q}?nologo=true"
            st.image(url)
            st.session_state.c.append(("assistant", clean, url))
            ans = None
        else:
            qq = urllib.parse.quote(p)
            rr = requests.get(f"https://text.pollinations.ai/{qq}?model=openai", timeout=20)
            ans = rr.text
        if ans:
            st.write(ans)
            st.session_state.c.append(("assistant", ans, None))