import streamlit as st, requests, urllib.parse
st.set_page_config(page_title="bairon IA", layout="centered")

if "c" not in st.session_state:
    st.session_state.c=[]

with st.expander("Mandar foto, audio o PDF"):
    up = st.file_uploader(" ", type=["png","jpg","jpeg","pdf","mp3"], label_visibility="collapsed")

for rol, txt, img in st.session_state.c:
    with st.chat_message(rol):
        st.write(txt)
        if img:
            st.image(img, use_container_width=True)

p = st.chat_input("Escribe /imagen para crear imagen")

if p:
    st.session_state.c.append(("user", p, None))
    with st.chat_message("user"):
        st.write(p)

    with st.chat_message("assistant"):
        low = p.lower()
        clean = p.lower().replace("hazme una imagen de","").replace("haz una imagen de","").replace("hazme una imagen","").replace("/imagen","").strip()
        if clean == "":
            clean = "los simpson"
        if "imagen" in low or "simpson" in low or "homero" in low:
            q = urllib.parse.quote(clean)
            url = "https://image.pollinations.ai/prompt/" + q + "?nologo=true"
            st.write("Generando imagen: " + clean)
            st.image(url, use_container_width=True)
            st.session_state.c.append(("assistant", "Generando imagen: " + clean, url))
        else:
            if "bairon" in low or "quien soy" in low:
                ans = "Si, eres bairon-dev, mi creador"
            else:
                qq = urllib.parse.quote(p)
                r