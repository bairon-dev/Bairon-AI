import streamlit as st

st.set_page_config(page_title="Bairon-AI", page_icon="🤖")
st.title("🤖 Bairon-AI")
st.subheader("Hecha en Garcia NL - 100% en Android")
st.write("Por @bairon-dev")

prompt = st.chat_input("Escribe algo...")

if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.write(m["content"])

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)
    respuesta = f"Soy Bairon-AI, creada por Bairon en Garcia NL. Me dijiste: '{prompt}'. ¡Estoy viva! 🔥"
    with st.chat_message("assistant"):
        st.write(respuesta)
    st.session_state.messages.append({"role": "assistant", "content": respuesta})
