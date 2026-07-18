import streamlit as st
import requests
import urllib.parse

st.set_page_config(page_title="Bairon AI", page_icon="🤖", layout="wide")
st.markdown("""
<style>
.block-container{max-width:900px!important; padding-top:20px}
header, footer, #MainMenu{visibility:hidden}
div[data-testid='stChatMessage']{border-radius:20px; padding:15px; margin-bottom:10px; border:1px solid #333}
</style>
""", unsafe_allow_html=True)

st.markdown("<h2 style='text-align:center'>🤖 Bairon AI</h2>", unsafe_allow_html=True)

if "chat" not in st.session_state:
    st.session_state.chat = []

with st.expander("📎 Mandar foto, audio o PDF"):
    foto = st.file_uploader("Foto", type=["png","jpg","jpeg"], label_visibility="collapsed")
    audio = st.audio_input("Graba voz")
    pdf = st.file_uploader("PDF", type=["pdf"], label_visibility="collapsed")
    if foto:
        st.image(foto, width=200)

for rol, texto, img in st.session_state.chat: