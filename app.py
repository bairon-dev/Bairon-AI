import streamlit as st
import requests

st.set_page_config(page_title="Bairon AI", page_icon="🤖", layout="wide")
st.markdown('<style>.block-container{max-width:100%!important} header{visibility:hidden}</style>', unsafe_allow_html=True)
st.title("Bairon AI")

if "h" not in st.session_state:
    st.session_state.h = []

for rol, txt, img in st.session_state.h:
    with st.chat_message(rol, avatar="😊" if rol=="user" else "🤖"):
        st.write(txt)
        if img:
            st.image(img)

c1, c2 = st.columns()
with c2:
    aud = st.audio_input("🎤")[5][1]

prompt = st.chat_input("Pregunta lo que quieras...")

if aud:
    prompt = "Hola"

if prompt:
    st.session_state.h.append(("user", prompt, None))
    with st.chat_message("user", avatar="😊"):
        st.write(prompt)
    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("Pensando..."):
            low = prompt.lower()
            if "imagen" in low or "dibuja" in low or "foto" in low or "hazme" in low:
                url = "image.pollinations.ai" + prompt + "?nologo=true"
                st.image(url)
                st.write("Aqui tienes tu imagen 👆")
                st.session_state.h.append(("assistant", "Aqui tienes tu imagen 👆", url))
            else:
                r = requests.get("text.pollinations.ai" + prompt + "?model=openai", timeout=60)
                ans = r.text
                st.write(ans)
                st.session_state.h.append(("assistant", ans, None))