import streamlit as st
from groq import Groq
import urllib.parse, base64, io
from PIL import Image
import PyPDF2

st.set_page_config(page_title="bairon IA", page_icon="b", layout="centered")

st.markdown("""
<style>
#MainMenu, footer, header {visibility: hidden;}
.stApp {background:#000000;}
h1 {text-align:center; font-weight:300; letter-spacing:7px; color:white; font-size:30px; margin:20px 0 10px 0;}

/* TU BURBUJA BLANCA - como en tu foto */
div[data-testid="stChatMessage"]:has(div[data-testid="stChatMessageAvatarUser"]) {
    background:white!important; 
    color:black!important; 
    border-radius:18px 18px 0 18px!important; 
    margin-left:15%!important;
    border:none!important;
}
div[data-testid="stChatMessage"]:has(div[data-testid="stChatMessageAvatarAssistant"]) {
    background:#222222!important; 
    color:white!important; 
    border-radius:18px 18px 18px 0!important; 
    margin-right:15%!important;
    border:none!important;
}
div[data-testid="stChatMessage"] p, div[data-testid="stChatMessage"] span {color:inherit!important;}
.stChatInput {background:#1a1a1a!important;}
</style>
""", unsafe_allow_html=True)

st.markdown("<h1>bairon IA</h1>", unsafe_allow_html=True)

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role":"assistant","content":"Soy Bairon AI: Hazme una imagen de una tesla en el cerro de la silla. ¿Quieres que te genere una imagen? Usa /imagen + lo que quieras."}
   