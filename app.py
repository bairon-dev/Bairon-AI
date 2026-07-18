import streamlit as st
from groq import Groq
import PyPDF2
from PIL import Image
import urllib.parse, base64

st.set_page_config(page_title="Bairon-AI PRO", page_icon="🔥", layout="wide")
st.title("Bairon-AI PRO MAX 🔥 - Garcia NL")

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# --- FUNCIONES ---
def generar_imagen(prompt):
    url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(prompt)}?width=1024&height=1024&nologo=true&enhance=true"
    return url

def detectar_imagen(texto):
    triggers = ["hazme una imagen", "crea una imagen", "genera una imagen", "imagen de", "dibujame", "dibújame", "hasme una imagen"]
    return any(t in texto.lower() for t in triggers)

# --- SIDEBAR - TODO LO MULTIMODAL ---
with st.sidebar:
    st.header("📎 Herramientas PRO")

    st.subheader("🖼️ Analizar Foto")
    foto = st.file_uploader("Sube una foto", type=["jpg","png","jpeg"])
    if foto:
        st.image(foto, width=200)
        if st.button("¿Qué hay en la foto?"):
            with st.spinner("Analizando..."):
                # Convertir a base64 para vision
                img = Image.open(foto)
                # Groq Vision
                try:
                    # Guardar temporal
                    import io
                    buffered = io.BytesIO()
                    img.save(buffered, format="JPEG")
                    img_b64 = base64.b64encode(buffered.getvalue()).decode()

                    resp = client.chat.completions.create(
                        model="llama-3.2-11b-vision-preview",
                        messages=[{"role":"user","content":[
                            {"type":"text","text":"Describe esta imagen detalladamente en español, estilo regio."},
                            {"type":"image_url","image_url":{"url": f"data:image/jpeg;base64,{img_b64}"}}
                        ]}]
                    )
                    st.success(resp.choices[0].message.content)
                except Exception as e:
                    st.error(f"Error vision: {e} - Prueba con modelo texto")

    st.subheader("🎙️ Transcribir Audio")
    audio = st.file_uploader("Sube audio", type=["mp3","wav","m4a","mp4"])
    if audio and st.button("Transcribir audio"):
        with st.spinner("Escuchando..."):
            try:
                trans = client.audio.transcriptions.create(
                    file=(audio.name, audio.read()),
                    model="whisper-large-v3",
                    response_format="json",
                    language="es"
                )
                st.write("**Dijo:**", trans.text)
                st.session_state['audio_text'] = trans.text
            except Exception as e:
                st.error(f"Error audio: {e}")

    st.subheader("📄 Leer PDF / Tarea")
    pdf = st.file_uploader("Sube PDF", type=["pdf"])
    if pdf:
        reader = PyPDF2.PdfReader(pdf)
        texto = ""
        for page in reader.pages[:10]: # primeras 10 paginas
            texto += page.extract_text()
        st.success(f"PDF leído: {len(texto)} letras")
        if st.button("Resumir PDF"):
            with st.spinner("Leyendo..."):
                resp = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[{"role":"user","content": f"Resume esto en español, estilo corto y chido: {texto[:8000]}"}]
                )
                st.write(resp.choices[0].message.content)

st.divider()

# --- CHAT PRINCIPAL ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        if "https://image.pollinations" in m["content"]:
            st.image(m["content"])
        else:
            st.markdown(m["content"])

if prompt := st.chat_input("Pregúntame lo que sea, manda foto en el panel de la izquierda..."):
    st.session_state.messages.append({"role":"user","content":prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Si hay texto de audio, lo anexamos
    if 'audio_text' in st.session_state:
        prompt = f"El usuario dijo en audio: {st.session_state['audio_text']} \n Pregunta: {prompt}"
        del st.session_state['audio_text']

    with st.chat_message("assistant"):
        if detectar_imagen(prompt):
            # Extraer prompt limpio
            for t in ["hazme una imagen de","crea una imagen de","genera una imagen de","imagen de","hazme una imagen","crea una imagen"]:
                prompt = prompt.lower().replace(t,"")
            prompt = prompt.strip()
            with st.spinner("Creando imagen PRO..."):
                url = generar_imagen(prompt)
                st.image(url, caption=prompt)
                st.session_state.messages.append({"role":"assistant","content":url})
        else:
            try:
                resp = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[{"role":"system","content":"Eres Bairon-AI PRO, asistente todo terreno de Garcia NL. Hablas regio, eres chido, ayudas con tarea, código, consejos. Si te mandan foto, audio o pdf usa el contexto."}] +
                             [{"role":m["role"],"content":m["content"]} for m in st.session_state.messages if "pollinations" not in m["content"]][-12:],
                )
                ans = resp.choices[0].message.content
                st.markdown(ans)
                st.session_state.messages.append({"role":"assistant","content":ans})
            except Exception as e:
                st.error(str(e))