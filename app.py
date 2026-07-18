import streamlit as st
import requests

st.title("Bairon AI")

if "m" not in st.session_state:
    st.session_state.m = []

for x in st.session_state.m:
    with st.chat_message(x[0]):
        st.write(x[1])

if p := st.chat_input("Pregunta..."):
    st.session_state.m.append(["user", p])
    with st.chat_message("user"):
        st.write(p)
    with st.chat_message("assistant"):
        with st.spinner("Pensando..."):
            r = requests.get("https://text.pollinations.ai/" + p)
            a = r.text
            st.write(a)
    st.session_state.m.append(["assistant", a])