import streamlit as st, requests, urllib.parse
st.set_page_config(page_title="bairon IA", layout="centered")
st.markdown('<h1 style="text-align:center; letter-spacing:8px; font-size:45px">bairon IA</h1>', unsafe_allow_html=True)

if "c" not in st.session_state:
    st.session_state.c=[]

with st.expander("📎 Mandar foto, audio o PDF"):
    up = st.file_uploader("sube archivo", type=["png","jpg","jpeg","pdf","mp3","wav"], label_visibility="collapsed")

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
        if "bairon" in low or "quien soy" in low or "me conoces" in low:
            ans = "Si, eres Bairon, bairon-dev, mi creador"
            st.write(ans)
            st.session_state.c.append(("assistant", ans, None))
        elif "quien te creo" in low:
            ans = "Me creo bairon-dev"
            st.write(ans)
            st.session_state.c.append(("assistant", ans, None))
        elif "imagen" in low:
            clean = p.replace("/imagen","").replace("Hazme una imagen de","").replace("Haz una imagen de","").replace("imagen de","").strip()
            if clean == "":
                clean = "un perro"
            q = urllib.parse.quote(clean)
            url = "https://image.pollinations.ai/prompt/" + q + "?nologo=true"
            st.write("Generando imagen: " + clean)
            st.image(url, use_container_width=True)
            st.session_state.c.append(("assistant", "Generando imagen: " + clean, url))
        else:
            q = urllib.parse.quote(p)
            r = requests.get("https://text.pollinations.ai/" + q + "?model=openai", timeout=20)
            ans = r.text
            st.write(ans)
            st.session_state.c.append(("assistant", ans, None))