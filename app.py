import streamlit as st
import requests

st.set_page_config(page_title="Bairon AI", page_icon="🤖")

# Pantalla completa celular
st.markdown("<style>.block-container{padding-top:1rem; max-width:100%} header{visibility:hidden}</style>", unsafe_allow_html=True)

st.title("Bairon AI")

# Guarda historial
if "messages" not in st.session_state:
    st.session_state.messages = []

# Burbujas + avatar
for m in st.session_state.messages:
    avatar = "🧑" if m["role"]=="user" else "🤖"
    with st.chat_message(m["role"], avatar