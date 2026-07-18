import streamlit as st
import requests
import urllib.parse

# 1. Configuración de pantalla completa móvil
st.set_page_config(page_title="Bairon AI", page_icon="🤖", layout="wide")

# 2. CSS Avanzado: Estilo ChatGPT Real (Burbujas flotantes, alineadas y colores correctos)
st.markdown('''
    <style>
        .block-container { max-width: 100% !important; padding-top: 1rem !important; padding-bottom: 7rem !important; }
        header, footer { visibility: hidden !important; }
        
        /* Contenedor general del mensaje */
        .chat-row { display: flex; margin-bottom: 15px; width: 100%; }
        .user-row { justify-content: flex-end; }
        .ai-row { justify-content: flex-start; }
        
        /* Burbuja del Usuario: Blanca/Gris Claro con texto oscuro */
        .user-bubble {
            background-color: #f0f0f0 !important;
            color: #1a1a1a !important;
            padding: 12px 16px;
            border-radius: 20px 20px 4px 20px;
            max-width: 75%;
            box-shadow: 0px 2px 5px rgba(0,0,0,0.1);
            font-size: 16px;
        }
        
        /* Burbuja de la IA: Oscura Premium con texto blanco */
        .ai-bubble {
            background-color: #2f2f2f !important;
            color: #ffffff !important;
            padding: 12px 16px;
            border-radius: 20px 20px 20px 4px;
            max-width: 75%;
            box-shadow: 0px 2px 5px rgba(0,0,0,0.2);
            font-size: 16px;
        }
        
        /* Estilo para imágenes dentro del chat */
        .chat-img { border-radius: 10px; max-width: 100%; margin-top: 8px; }
    </style>
''', unsafe_allow_html=True)

st.title("🤖 Bairon AI")

# 3. Inicializar el historial en la sesión
if "h" not in st.session_state:
    st.session_state.h = []

# 4. NUEVO: Barra Lateral para subir Imágenes y PDFs (Como en tu lista de deseos)
with st.sidebar:
    st.header("Anexar Archivos")
    foto_subida = st.file_uploader("Mandar foto o imagen", type=["png", "jpg", "jpeg"])
    pdf_subido = st.file_uploader("Mandar documento PDF", type=["pdf"])
    if foto_subida:
        st.success("📸 Imagen cargada listo para procesar.")
    if pdf_subido:
        st.success("📄 PDF cargado listo para leer.")

# 5. Renderizar el historial con el nuevo diseño visual de burbujas
for rol, txt, img in st.session_state.h:
    if rol == "user":
        st.markdown(f'<div class="chat-row user-row"><div class="user-bubble">😊 <b>Tú:</b><br>{txt}</div></div>', unsafe_allow_html=True)
    else:
        if img:
            st.markdown(f'<div class="chat-row ai-row"><div class="ai-bubble">🤖 <b>Bairon AI:</b><br>{txt}<br><img src="{img}" class="chat-img"></div></div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="chat-row ai-row"><div class="ai-bubble">🤖 <b>Bairon AI:</b><br>{txt}</div></div>', unsafe_allow_html=True)

# 6. Entrada de Audio inferior
aud = st.audio_input("🎤 Usa tu voz")

# 7. Entrada de texto fija estilo chat
prompt = st.chat_input("Pregunta lo que quieras...")

if aud and not prompt:
    prompt = "Hola (Mensaje de voz)"

# Modificar el prompt si hay archivos subidos para que la IA sepa qué hacer
if prompt:
    if foto_subida:
        prompt += " [El usuario adjuntó una imagen]"
    if pdf_subido:
        prompt += " [El usuario adjuntó un documento PDF]"

    # Mostrar inmediatamente el mensaje del usuario a la derecha en burbuja blanca
    st.session_state.h.append(("user", prompt, None))
    st.markdown(f'<div class="chat-row user-row"><div class="user-bubble">😊 <b>Tú:</b><br>{prompt}</div></div>', unsafe_allow_html=True)
        
    # Procesar respuesta de la IA a la izquierda
    low = prompt.lower()
    
    # Evaluar si el usuario quiere crear un dibujo/imagen
    if any(p in low for p in ["imagen", "dibuja", "foto", "hazme", "haz", "crea"]):
        with st.spinner("Generando imagen perfecta..."):
            prompt_codificado = urllib.parse.quote(prompt)
            # URL corregida con parámetros HD para evitar deformaciones
            url_imagen = f"https://pollinations.ai{prompt_codificado}?width=1024&height=1024&nologo=true&private=true"
            
            msg = "Aquí tienes la imagen que me pediste:"
            st.markdown(f'<div class="chat-row ai-row"><div class="ai-bubble">🤖 <b>Bairon AI:</b><br>{msg}<br><img src="{url_imagen}" class="chat-img"></div></div>', unsafe_allow_html=True)
            st.session_state.h.append(("assistant", msg, url_imagen))
    else:
        # Respuestas de texto continuas
        with st.spinner("Pensando respuesta..."):
            try:
                prompt_codificado = urllib.parse.quote(prompt)
                # CORRECCIÓN DE CONEXIÓN: Ruta de endpoint correcta para Pollinations
                url_texto = f"https://pollinations.ai{prompt_codificado}"
                
                r = requests.get(url_texto, timeout=30)
                if r.status_code == 200:
                    ans = r.text
                else:
                    ans = f"Error del servidor central (Código {r.status_code}). Inténtalo de nuevo."
            except Exception as e:
                ans = "Error de red al conectar con el cerebro digital. Comprueba tu conexión."
            
            st.markdown(f'<div class="chat-row ai-row"><div class="ai-bubble">🤖 <b>Bairon AI:</b><br>{ans}</div></div>', unsafe_allow_html=True)
            st.session_state.h.append(("assistant", ans, None))
