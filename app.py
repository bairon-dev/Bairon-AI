import streamlit as st
import urllib.parse, base64, io
from groq import Groq
from PIL import Image
import PyPDF2

st.set_page_config(page_title="bairon IA", layout="centered")
st.markdown("""
<style>
#MainMenu, footer, header {visibility:hidden;}
.stApp {background:#0a0a0a;}
h1 {text-align:center; font-weight:800; letter-spacing:5px; font-size:45px!important; color:white;}
.user-bubble {background:white; color:black; padding:12px 16px; border-radius:18px 18px 0 18px; max-width:85%; margin:8px 0 8px auto;}
.bot-bubble {background:#1e1e1e; color:white; padding:12px 16px; border-radius:18px 18px 18px 0; max-width:85%; margin:8px auto 8px 0;}
</style>
""", unsafe_allow_html=True)
st.markdown("<h1>bairon IA</h1>", unsafe_allow_html=True)
client = Groq(api_key=st.secrets["GROQ_API_KEY"])
if "messages" not in st.session_state: st.session_state.messages = []

for m in st.session_state.messages:
    if m["role"] == "user": st.markdown(f'<div class="user-bubble">{m["content"]}</div>', unsafe_allow_html=True)
    else:
        if "pollinations.ai" in m["content"]: st.image(m["content"])
        else: st.markdown(f'<div class="bot-bubble">{m["content"]}</div>', unsafe_allow_html=True)

with st.expander("📎 Mandar foto, audio o PDF"):
    foto = st.file_uploader("Foto", type=["jpg","jpeg","png"], key="f")
    audio = st.file_uploader("Audio", type=["mp3","wav","m4a"], key="a")
    pdf = st.file_uploader("PDF", type=["pdf"], key="p")

prompt = st.chat_input("Escribe /imagen para crear imagen")

if prompt:
    st.session_state.messages.append({"role":"user","content":prompt})
    st.markdown(f'<div class="user-bubble">{prompt}</div>', unsafe_allow_html=True)
    contexto = ""; b64_img = None
    if pdf:
        try:
            reader = PyPDF2.PdfReader(pdf)
            txt = "".join([ (p.extract_text() or "") for p in reader.pages[:8]])[:6000]
            contexto += f" PDF: {txt} "
        except: pass
    if audio:
        try:
            tr = client.audio.transcriptions.create(file=(audio.name, audio.getvalue()), model="whisper-large-v3", response_format="json")
            contexto += f" Audio: {tr.text} "
        except: pass
    if foto:
        try:
            img = Image.open(foto); buff = io.BytesIO(); img.save(buff, format="JPEG")
            b64_img = base64.b64encode(buff.getvalue()).decode()
        except: pass

    low = prompt.lower()
    triggers = ["/imagen", "hazme una imagen", "creame una imagen", "crea una imagen", "genera una imagen", "generame una imagen", "haz una imagen", "dibujame", "imagen de"]
    es_imagen = any(t in low for t in triggers)

    if es_imagen:
        q = prompt.lower()
        for t in triggers: q = q.replace(t, "")
        q = q.strip().lstrip("de").strip()
        if not q: q = "un perro"
        st.markdown(f'<div class="bot-bubble">Generando imagen: {q}</div>', unsafe_allow_html=True)
        url = "https://image.pollinations.ai/prompt/" + urllib.parse.quote(q) + "?width=1024&height=1024&nologo=true&enhance=true"
        st.image(url)
        st.session_state.messages.append({"role":"assistant","content":url})
    elif b64_img:
        resp = client.chat.completions.create(model="meta-llama/llama-4-scout-17b-16e-instruct", messages=[{"role":"user","content":[{"type":"text","text":f"Eres bairon IA creado por Bairon de Garcia NL. Nunca digas Meta. Contexto:{contexto} Pregunta:{prompt}"},{"type":"image_url","image_url":{"url":f"data:image/jpeg;base64,{b64_img}"}}]}])
        ans = resp.choices[0].message.content
        st.markdown(f'<div class="bot-bubble">{ans}</div>', unsafe_allow_html=True)
        st.session_state.messages.append({"role":"assistant","content":ans})
    else:
        resp = client.chat.completions.create(model="llama-3.1-8b-instant", messages=[{"role":"system","content":f"Eres bairon IA creado por Bairon en Garcia NL. Nunca digas que eres de Meta. {contexto}"},{"role":"user","content":prompt}])
        ans = resp.choices[0].message.content
        st.markdown(f'<div class="bot-bubble">{ans}</div>', unsafe_allow_html=True)
        st.session_state.messages.append({"role":"assistant","content":ans})
