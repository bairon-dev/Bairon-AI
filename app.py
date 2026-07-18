import streamlit as st
import urllib.parse
import requests

st.set_page_config(page_title="Bairon-AI", layout="centered")

st.markdown("""
<style>
.stApp { background-color: #0e0e0e; }
h1 { color: white !important; text-align: center; font-family: sans-serif; }
.user-bubble { background-color: white; color: black; padding: 12px 18px; border-radius: 20px 20px 4px 20px; max-width: 80%; float: right; margin: 8px 0; clear: both; }
.bot-bubble { background-color: #2a2a2a; color: white; padding
