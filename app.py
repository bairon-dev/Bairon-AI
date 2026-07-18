import streamlit as st, requests, urllib.parse

st.set_page_config(page_title="Bairon AI", page_icon="🤖", layout="wide")
st.markdown("<style>.block-container{max-width:100%!important} header,footer{visibility:hidden}</style>", unsafe_allow_html=True)

st.markdown("<div style='text-align:center'><h1>🤖</h1><h2>BAIRON IA</h2><p>Tu asistente personal</p></div>", unsafe_allow_html=True)

if "chat" not in st.session_state:
    st.session_state.chat = []

with st.expander("📎 Mandar foto, audio o PDF"):
    foto = st.file_uploader("Foto o PDF", type=["png","jpg","jpeg","pdf"])
    if foto and "pdf" not in foto.type:
        st.image(foto)

voz = st.audio_input("🎤 Grabar voz")

for rol, msg, img in st.session_state.chat:
    av = "😊" if rol=="user" else "🤖"
    with st.chat_message(rol, avatar=av):
        st.write(msg)
        if img:
            st.image(img)

prompt = st