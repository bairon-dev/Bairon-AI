import streamlit as st, requests, urllib.parse

st.set_page_config(page_title="Bairon AI", page_icon="🤖", layout="wide")
st.markdown("<style>.block-container{max-width:100%!important} header,footer{visibility:hidden}</style>", unsafe_allow_html=True)

st.markdown("<div style='text-align:center'><h1>🤖</h1><h2>BAIRON IA</h2><p>Tu asistente personal</p></div>", unsafe_allow_html=True)

if "chat" not in st.session_state:
    st.session_state.chat = []

with st.expander("📎 Mandar foto o PDF"):
    foto = st.file_uploader("Sube", type=["png","jpg","jpeg","pdf"])
    if foto and "pdf" not in foto.type:
        st.image(foto)

for rol, msg, img in st.session_state.chat:
    av = "😊" if rol=="user" else "🤖"
    with st.chat_message(rol, avatar=av):
        st.write(msg)
        if img:
            st.image(img)

prompt = st.chat_input("Escribe aqui... /imagen para imagen")

if prompt:
    st.session_state.chat.append(("user", prompt, None))
    with st.chat_message("user", avatar="😊"):
        st.write(prompt)
    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("Pensando..."):
            low = prompt.lower()
            if "quien te creo" in low:
                ans = "Me creo Bairon, soy Bairon IA."
                st.write(ans)
                st.session_state.chat.append(("assistant", ans, None))
            elif "/imagen" in low or "hazme una imagen" in low or "imagen de" in low or "dibuja" in low:
                clean = prompt.replace("/imagen","").replace("hazme una imagen de","").replace("hazme una imagen","").strip()
                if clean == "":
                    clean = "homero simpson"
                q = urllib.parse.quote(clean)
                url = f"https://image.pollinations.ai/prompt/{q}?nologo=true"
                st.write(f"Generando: {clean}")
                st.image(url)
                st.session_state.chat.append(("assistant", f"Generando: {clean}", url))
            else:
                q = urllib.parse.quote(f"Eres Bairon IA creado por Bairon. Pregunta: {prompt}")
                r = requests.get(f"https://text.pollinations.ai/{q}?model=openai", timeout=30)
                ans = r.text
                st.write(ans)
                st.session_state.chat.append(("assistant", ans, None))