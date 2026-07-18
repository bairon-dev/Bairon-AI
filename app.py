import streamlit as st, requests, urllib.parse
st.set_page_config(layout="centered")

if "m" not in st.session_state:
    st.session_state.m = []

with st.expander("📎 Mandar foto, audio o PDF"):
    st.file_uploader("", label_visibility="collapsed")

for a,b,c in st.session_state.m:
    with st.chat_message(a):
        st.write(b)
        if c: st.image(c)

q = st.chat_input("Escribe /imagen para crear imagen")
if q:
    st.session_state.m.append(("user", q, None))
    with st.chat_message("user"): st.write(q)
    with st.chat_message("assistant"):
        l = q.lower()
        if "bairon-dev" in l or "quien soy" in l:
            t = "Eres Bairon, bairon-dev, mi creador"
            st.write(t)
            st.session_state.m.append(("assistant", t, None))
        elif "imagen" in l or "simpson" in l:
            clean = l.replace("hazme una imagen de","").replace("imagen","").strip() or "los simpson"
            url = "https://image.pollinations.ai/prompt/" + urllib.parse.quote(clean) + "?nologo=true"
            st.write("Generando imagen: " + clean)
            st.image(url)
            st.session_state.m.append(("assistant", "Generando imagen: " + clean, url))
        else:
            r = requests.get("https://text.pollinations.ai/" + urllib.parse.quote(q), timeout=20).text
            st.write(r)
            st.session_state.m.append(("assistant", r, None))