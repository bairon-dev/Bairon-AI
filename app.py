

import streamlit as st
import urllib.parse
from groq import Groq

st.set_page_config(page_title="bairon IA", layout="centered")
st.markdown("<h1 style='text-align:center; color:white;'>bairon IA</h1>", unsafe_allow_html=True)

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        if "pollinations.ai" in m["content"]:
            st.image(m["content"])
        else:
            st.markdown(m["content"])

prompt = st.chat_input("Escribe /imagen para crear imagen")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        text = prompt.lower()
        if "/imagen" in text:
            q = text.replace("/imagen", "").strip()
            if q == "":
                q = "tesla en el cerro de la silla"
            url = "https://image.pollinations.ai/prompt/" + urllib.parse.quote(q) + "?width=1024&height=1024&nologo=true&enhance=true"
            st.write("Generando imagen: " + q)
            st.image(url)
            st.session_state.messages.append({"role": "assistant", "content": url})
        else:
            completion = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {"role": "system", "content": "Eres bairon IA, de Garcia NL."},
                    {"role": "user", "content": prompt}
                ]
            )
            ans = completion.choices[0].message.content
            st.markdown(ans)
            st.session_state.messages.append({"role": "assistant", "content": ans})