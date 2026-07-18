import streamlit as st

st.set_page_config(page_title="Bairon AI", page_icon="🤖", layout="centered")

# Estilo tipo chat
st.markdown("""
<style>
    .stApp { background: #0e1117; }
    .block-container { padding-top: 2rem; max-width: 700px; }
</style>
""", unsafe_allow_html=True)

st.title("Bairon AI 🤖")

# Historial
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar historial con burbujas
for msg in st.session_state.messages:
    with st.chat_message(msg["role"], avatar="🧑" if msg["role"]=="user" else "🤖"):
        st.markdown(msg["content"])

# Input
if prompt := st.chat_input("Pregunta lo que quieras..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="🧑"):
        st.markdown(prompt)
    
    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("Pensando..."):
            # AQUÍ VA TU CÓDIGO DE IA
            response = f"Respuesta a: {prompt}" # cambia esto por tu función
        
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})