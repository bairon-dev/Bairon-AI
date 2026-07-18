         import streamlit as st
from groq import Groq
import urllib.parse, base64, io
from PIL import Image
import PyPDF2

st.set_page_config(page_title="bairon IA", page_icon="b", layout="centered")

st.markdown("""
<style>
#MainMenu, footer, header {visibility: hidden;}
.stApp {background:#0a0a0a;}
h1 {text-align:center; font-weight:200; letter-spacing:6px; font-size:32px!important; margin-top:10px; color:white;}
.stChatMessage {background:#171717; border-radius:18px; border:1px solid #222;}
</style>
""", unsafe_allow_html=True)

st.markdown("<h1>bairon IA</h1>", unsafe_allow_html=True)

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- MOSTRAR CHAT ---
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        if "pollinations.ai" in m["content"]:
            st.image(m["content"])
        else:
            st.markdown(m["content"])

# --- BARRA PARA SUBIR ARCHIVOS ARRIBA DEL CHAT ---
with st.expander("📎 Mandar foto, audio o PDF"):
    col1, col2, col3 = st.columns(3)
    with col1:
        foto = st.file_uploader("Foto", type=["jpg","jpeg","png"], label_visibility="collapsed", key="foto")
        if foto: st.image(foto, width=150)
    with col2:
        audio = st.file_uploader("Audio", type=["mp3","wav","m4a","mp4"], label_visibility="collapsed", key="audio")
    with col3:
        pdf = st.file_uploader("PDF", type=["pdf"], label_visibility="collapsed", key="pdf")
        if pdf: st.caption(f"PDF: {pdf.name}")

def es_imagen(t): return any(x in t.lower() for x in ["imagen","dibujame","dibújame","/imagen","foto de"])

# --- INPUT PRINCIPAL ---
if prompt := st.chat_input("Escribe algo, o pide una imagen..."):

    # 1. SI HAY PDF
    contexto = ""
    if pdf:
        reader = PyPDF2.PdfReader(pdf)
        texto_pdf = "".join([(p.extract_text() or "") for p in reader.pages[:10]])
        contexto += f"\n[El usuario subió este PDF: {texto_pdf[:7000]}]\n"

    # 2. SI HAY AUDIO
    if audio:
        with st.spinner("Escuchando audio..."):
            try:
                tr = client.audio.transcriptions.create(
                    file=(audio.name, audio.read()),
                    model="whisper-large-v3",
                    language="es",
                    response_format="json"
                )
                contexto += f"\n[El usuario dijo en audio: {tr.text}]\n"
                prompt = f"{prompt} (dijo en audio: {tr.text})"
            except Exception as e:
                st.error(f"Error audio: {e}")

    st.session_state.messages.append({"role":"user","content":prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # A) GENERAR IMAGEN
        if es_imagen(prompt):
            limpio = prompt.lower()
            for k in ["hazme una imagen de","crea una imagen de","genera una imagen de","hazme una imagen","crea una imagen","imagen de","/imagen","dibujame","dibújame"]:
                limpio = limpio.replace(k,"")
            limpio = limpio.strip() or "a cool photo"
            with st.spinner("Creando..."):
                url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(limpio)}?width=1024&height=1024&nologo=true&enhance=true"
                st.image(url, caption=limpio)
                st.session_state.messages.append({"role":"assistant","content":url})

        # B) ANALIZAR FOTO
        elif foto:
            with st.spinner("Viendo foto..."):
                img = Image.open(foto)
                buff = io.BytesIO()
                img.save(buff, format="JPEG")
                b64 = base64.b64encode(buff.getvalue()).decode()
                resp = client.chat.completions.create(
                    model="llama-3.2-11b-vision-preview",
                    messages=[{"role":"user","content":[
                        {"type":"text","text": f"{contexto}\n{prompt}"},
                        {"type":"image_url","image_url":{"url": f"data:image/jpeg;base64,{b64}"}}
                    ]}]
                )
                ans = resp.choices[0].message.content
                st.markdown(ans)
                st.session_state.messages.append({"role":"assistant","content":ans})

        # C) CHAT NORMAL + PDF
        else:
            resp = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[{"role":"system","content": f"Eres bairon IA, asistente de Garcia NL, chido y útil. Respondes corto.{contexto}"}] +
                         [{"role":m["role"],"content":m["content"]} for m in st.session_state.messages if "pollinations" not in m["content"]][-12:]
            )
            ans = resp.choices[0].message.content
            st.markdown(ans)
            st.session_state.messages.append({"role":"assistant","content":ans})