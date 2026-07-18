import streamlit as st
import requests

st.set_page_config(page_title="Bairon AI")

if "msgs" not in st.session_state:
    st.session_state.msgs = []

st.title("Bairon AI")

for rol, txt, img in st.session_state.msgs:
    with st.chat_message(rol):
        st.write(txt)
        if img:
            st.image(img)

if prompt := st.chat_input("Pregunta..."):

    st.session_state.msgs.append(("user", prompt, None))
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Pensando..."):
            low = prompt.lower()
            if "imagen" in low or "dibuja" in low or "foto" in low:
                url = "https://image.pollinations.ai/prompt/" + prompt + "?nologo=true"
                st.image(url)
                st.write("Imagen generada")
                st.session_state.msgs.append(("assistant", "Imagen generada", url))
            else:
                r = requests.get("https://text.pollinations.ai/" + prompt + "?model=openai", timeout=60)
                ans = r.text
                st.write(ans)
                st.session_state.msgs.append(("assistant", ans, None))