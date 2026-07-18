import streamlit as st, requests, urllib.parse

st.set_page_config(page_title="bairon IA", layout="centered")
st.markdown("""
<style>
header, footer, #MainMenu {visibility:hidden}
.block-container{max-width:700px!important; padding-top:10px}
h1{font-family:monospace; text-align:center; font-size:48px; letter-spacing:8px; font-weight:900; margin:20px 0}
div[data-testid='stExpander']{background:#111111!important; border:1px solid #2a2a2a!important; border-radius:12px!important}
div[data-testid='stChatMessage']{background:transparent!important; border:none!important; padding:5px 0!important}
/* burbuja usuario blanca */
div[data-testid='stChatMessage']:has(div[data-testid='stChatMessageAvatarUser']){justify-content:flex-end}
div[data-testid='stChatMessage']:has(div[data-testid='stChatMessageAvatarUser']) div[data-testid='stMarkdownContainer']{background:white!important; color:black!important; border-radius