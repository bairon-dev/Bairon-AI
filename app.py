import streamlit as st
import requests

st.set_page_config(page_title="Bairon AI", page_icon="🤖", layout="wide")
st.title("Bairon AI")

if "msgs" not in st.session_state:
    st.session_state.msgs = []

# Mandar foto, audio o PDF (lo que tenias antes)
with st.expander("📎 Mandar foto, audio o PDF"):
    archivo = st.file_uploader("Sube archivo", type=["png","jpg","pdf","mp3","wav"])
    audio_input = st.audio_input("🎤 Grabar audio")
    if archivo:
        st.success(f"Archivo recibido: {archivo.name}")
    if audio_input:
        st.success("Audio recibido")

# Historial con avatar y burbujas
for rol, txt, img in st.session_state.msgs:
    avatar = "😊" if rol=="user" else "🤖"
    with st.chat_message(rol, avatar=avatar):
        st.write(txt)
        if img:
            st.image(img)

# Entrada
prompt = st.chat_input("Escribe /imagen para crear imagen")

if prompt:
    st.session_state.msgs.append(("user", prompt, None))
    with st.chat_message("user", avatar="😊"):
        st.write(prompt)

    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("Pensando..."):
            txt_low = prompt.lower()
            if "/imagen" in txt_low or "hazme una imagen" in txt_low or "simpson" in txt_low or "imagen" in txt_low:
                # Limpia el prompt para la imagen
                prompt_img = prompt.replace("/imagen","").replace("Hazme una imagen de","").strip()
                if prompt_img == "":
                    prompt_img = prompt
                st.write(f"Generando imagen: {prompt_img}")
                url = "https://image.pollinations.ai/prompt/" + prompt_img + "?width=1024&height=1024&nologo=true&model=turbo"
                st.image(url)
                st.session_state.msgs.append(("assistant", f"Generando imagen: {prompt_img}", url))
            else:
                r = requests.get("https://text.pollinations.ai/" + prompt + "?model=openai", timeout=60)
                ans = r.text
                st.write(ans)
                st.session_state.msgs.append(("assistant", ans, None))