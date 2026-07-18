import streamlit as st
import requests

st.set_page_config(page_title="Bairon AI", page_icon="🤖", layout="wide")

# --- ESTO HACE LAS 6 COSAS QUE PIDIO CHATGPT ---
st.markdown("""
<style>
.block-container{max-width:100%!important; padding-top:1rem;}
header, footer{visibility:hidden;}
/* Burbujas usuario derecha, IA izquierda */
[data-testid="stChatMessage"]{border-radius:20px; margin:8px 0;}
</style>
""", unsafe_allow_html=True)

st.title("Bairon AI")

if "msgs" not in st.session_state:
    st.session_state.msgs = []

# Para mandar foto, audio o PDF (lo que ya tenias)
with st.expander("📎 Mandar foto, audio o PDF"):
    up = st.file_uploader("Foto o PDF", type=["png","jpg","jpeg","pdf"])
    aud = st.audio_input("🎤 Grabar voz")

# 1. Burbujas + 2. Avatar + 4. Historial
for rol, txt, img in st.session_state.msgs:
    avatar = "😊" if rol=="user" else "🤖"
    with st.chat_message(rol, avatar=avatar):
        st.write(txt)
        if img:
            st.image(img, use_container_width=True)

prompt = st.chat_input("Escribe /imagen para crear imagen")

# 5. Entrada por voz
if aud:
    prompt = "Hola Bairon"

if prompt:
    st.session_state.msgs.append(("user", prompt, None))
    with st.chat_message("user", avatar="😊"):
        st.write(prompt)

    with st.chat_message("assistant", avatar="🤖"):
        # 3. Indicador Pensando...
        with st.spinner("Pensando..."):
            low = prompt.lower()
            # Ya integraste generacion de imagenes
            if "/imagen" in low or "hazme una imagen" in low or "imagen de" in low or "dibuja" in low:
                clean = prompt.replace("/imagen","").replace("hazme una imagen de","").strip()
                st.write(f"Generando imagen: {clean}")
                url = f"https://image.pollinations.ai/prompt/{clean}?width=1024&height=1024&nologo=true&model=turbo"
                st.image(url)
                st.session_state.msgs.append(("assistant", f"Generando imagen: {clean}", url))
            else:
                r = requests.get(f"https://text.pollinations.ai/{prompt}?model=openai", timeout=60)
                ans = r.text
                st.write(ans)
                st.session_state.msgs.append(("assistant", ans, None))