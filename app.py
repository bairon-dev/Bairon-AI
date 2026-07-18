import streamlit as st
import time

st.set_page_config(page_title="Bairon AI", page_icon="🤖")

st.markdown("""
<style>
.block-container{max-width:700px; padding-top:20px}
</style>
""", unsafe_allow_html=True)

st.title("Bairon AI 🤖")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    avatar = "🧑" if msg["role"] == "user" else "🤖"
    with st.chat_message(msg["role"], avatar=avatar):
        st.write(msg["content"])

if prompt := st.chat_input("Pregunta lo que quieras..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="🧑"):
        st.write(prompt)

    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("Pensando..."):
            time.sleep(0.8)
            # AQUÍ VA TU IA REAL
            respuesta = f"Respuesta de Bairon a: {prompt}"
            st.write(respuesta)
    
    st.session_state.messages.append({"role": "assistant", "content": respuesta})
