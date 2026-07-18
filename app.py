import streamlit as st
import urllib.parse

st.set_page_config(page_title="Bairon-AI", page_icon="🤖")
st.title("🤖 Bairon-AI")
st.subheader("Hecha en Garcia NL - 100% en Android")
st.caption("Por @bairon-dev")

if "chat" not in st.session_state:
    st.session_state.chat = []

for msg in st.session_state.chat:
    with st.chat_message(msg["role"]):
        if msg["type"] == "text":
            st.write(msg["content"])
        else:
            st.image(msg["content"])

prompt = st.chat_input("Escribe /imagen para crear ima...")

if prompt:
    st.session_state.chat.append({"role": "user", "type": "text", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        if prompt.lower().startswith("/imagen"):
            texto = prompt.replace("/imagen", "").strip()
            if not texto:
                texto = "una tesla en el cerro de la silla"
            st.write(f"Generando imagen: {texto}")
            # API gratis para generar imagen
            encoded = urllib.parse.quote(texto)
            img_url = f"https://image.pollinations.ai/prompt/{encoded}?width=800&height=800&nologo=true"
            st.image(img_url)
            st.session_state.chat.append({"role": "assistant", "type": "text", "content": f"Generando imagen: {texto}"})
            st.session_state.chat.append({"role": "assistant", "type": "image", "content": img_url})
        else:
            respuesta = f"Soy Bairon AI: {prompt}. ¿Quieres que te genere una imagen? Usa /imagen + lo que quieras."
            st.write(respuesta)
            st.session_state.chat.append({"role": "assistant", "type": "text", "content": respuesta})