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
h1 {text-align:center; font-weight:800; letter-spacing:5px; font-size:45px!important; color:white; margin-top:10px;}
.user-bubble {background:white; color:black; padding:12px 16px; border-radius:18px 18px 0 18px; max-width:85%; margin:8px 0 8px auto;}
.bot-bubble {background:#1e1e1e; color:white; padding:12px 16px; border-radius:18px 18px 18px 0; max-width:85%; margin:8px auto 8px 0;}
[data-testid="stExpander"] {background:#1e1e1e; border-radius:12px;}
</style>
""", unsafe_allow_html=True)

st.markdown("<h1>bairon IA</h1>", unsafe_allow_html=True)

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

if "messages" not in st.session_state:
    st.session_state.messages = []

# Historial bonito
for m in st.session_state.messages:
    if m["role"] == "user":
        st.markdown(f'<div class="user-bubble">{m["content"]}</div>', unsafe_allow_html=True)
    else:
        if "pollinations.ai" in m["content"]:
            st.image(m["content"])
        else:
            st.markdown(f'<div class="bot-bubble">{m["content"]}</div>', unsafe_allow_html=True)

if len(st.session_state.messages) == 0:
    st.markdown('<div class="bot-bubble">Soy bairon IA de Garcia NL 😎<br><br>📸 Manda foto<br>🎤 Manda audio<br>📄 Manda PDF<br>🎨 Escribe <b>/imagen</b> para crear fotos</div>', unsafe_allow_html=True)

# ARCHIVOS
with st.expander("📎 Mandar foto, audio o PDF"):
    foto = st.file_uploader("Foto", type=["jpg","jpeg","png"], key="f")
    audio = st.file_uploader("Audio", type=["mp3","wav","m4a"], key="a")
    pdf = st.file_uploader("PDF", type=["pdf"], key="p")

prompt = st.chat_input("Escribe /imagen para crear imagen")

if prompt:
    st.session_state.messages.append({"role":"user","content":prompt})
    st.markdown(f'<div class="user-bubble">{prompt}</div>', unsafe_allow_html=True)

    contexto = ""
    b64_img = None

    # Leer PDF
    if pdf:
        try:
            reader = PyPDF2.PdfReader(pdf)
            txt = "".join([ (p.extract_text() or "") for p in reader.pages[:8]])[:6000]
            contexto += f" El usuario mando un PDF que dice: {txt} "
        except: pass

    # Leer Audio
    if audio:
        try:
            tr = client.audio.transcriptions.create(
                file=(audio.name, audio.getvalue()),
                model="whisper-large-v3",
                response_format="json"
            )
            contexto += f" Audio transcrito: {tr.text} "
            if prompt.strip() == "":
                prompt = tr.text
        except Exception as e:
            st.markdown(f'<div class="bot-bubble">Error audio: {e}</div>', unsafe_allow_html=True)

    # Leer Foto
    if foto:
        try:
            img = Image.open(foto)
            buff = io.BytesIO()
            img.save(buff, format="JPEG")
            b64_img = base64.b64encode(buff.getvalue()).decode()
        except: pass

    low = prompt.lower()

    if "/imagen" in low or "genera una imagen de" in low or "hazme una imagen" in low:
        q = low.replace("/imagen","").replace("hazme una imagen de","").replace("hazme una imagen","").replace("genera una imagen de","").strip()
        if q == "": q = "tesla en el cerro de la silla"
        st.markdown(f'<div class="bot-bubble">Generando imagen: {q}</div>', unsafe_allow_html=True)
        url = "https://image.pollinations.ai/prompt/" + urllib.parse.quote(q) + "?width=1024&height=1024&nologo=true&enhance=true"
        st.image(url)
        st.session_state.messages.append({"role":"assistant","content":url})

    elif b64_img:
        # Si hay foto, usa vision
        resp = client.chat.completions.create(
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            messages=[{
                "role":"user",
                "content":[
                    {"type":"text","text":f"Eres bairon IA creado por Bairon de Garcia NL. Nunca digas Meta. Contexto: {contexto} Pregunta: {prompt}"},
                    {"type":"image_url","image_url":{"url":f"data:image/jpeg;base64,{b64_img}"}}
                ]
            }]
        )
        ans = resp.choices[0].message.content
        st.markdown(f'<div class="bot-bubble">{ans}</div>', unsafe_allow_html=True)
        st.session_state.messages.append({"role":"assistant","content":ans})

    else:
        system = "Eres bairon IA, creado por Bairon en Garcia, Nuevo León, Mexico. NUNCA digas que eres de Meta AI, Llama o Meta. Si preguntan quien te hizo di: Me creó Bairon. Eres chido, corto, hablas español."
        resp = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role":"system","content":system + " " + contexto},
                {"role":"user","content":prompt}
            ]
        )
        ans = resp.choices[0].message.content
        st.markdown(f'<div class="bot-bubble">{ans}</div>', unsafe_allow_html=True)
        st.session_state.messages.append({"role":"assistant","content":ans})