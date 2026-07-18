import streamlit as st
import requests

st.set_page_config(page_title="Bairon AI", page_icon="🤖", layout="wide")

# 1. PANTALLA COMPLETA CELULAR + BURBUJAS BONITAS
st.markdown("""
<style>
.block-container {max-width:100% !important; padding: 1rem 0.5rem !important;}
header, footer {visibility: hidden;}
[data-testid="stChatMessage"] {
    border-radius: 20px !important;
    padding: 12px !important;
    margin: 8px 0 !important;
}
[data-testid="stChatMessage"][data-testid="user"] { background: #2b2b2b; }
</style>
""",