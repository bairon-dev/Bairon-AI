import streamlit as st
import requests
import urllib.parse

# 1. Configuración de página optimizada para celulares
st.set_page_config(page_title="Bairon AI", page_icon="🤖", layout="wide")

# 2. DISEÑO CHATGPT: CSS Avanzado para mover el usuario a la derecha y estilizar burbujas
st.markdown('''
    <style>
        /* Pantalla completa real en móviles */
        .block-container {
            max-width: 100% !important;
            padding-top: 1rem !important;
            padding-bottom: 6rem !important;
            padding-left: 0.5rem !important;
            padding-right: 0.5rem !important;
        }
        header, footer {visibility: hidden !important;}
        
        /* Forzar que el mensaje del usuario se vaya a la derecha como ChatGPT */
        .stChatMessage:has(img[alt="😊"]), .stChatMessage:has([data-testid="stChatMessageAvatar"]:-webkit-any-link) {
            flex-direction: row-reverse !important;
            text-align: right !important;
        }
        
        /* Ajustar el fondo de las burbujas para modo oscuro premium */
        div[data-testid="stChatMessage"] {
            background-color: #212121 !important;
            border-radius: 15px !important;
            padding: 10px !important;
            margin-bottom: 10px !important;
        }
    </style>
''', unsafe_allow_html=True)

st.title("🤖 Bairon AI")

# 3. Inicialización del historial de conversación
if "h" not in st.session_state:
    st.session_state.h = []

# 4. Renderizado del historial en tiempo real
for rol, txt, img in st.session_state.h:
    with st.chat_message(rol, avatar="😊" if rol == "user" else "🤖"):
        if txt:
            st.write(txt)
        if img:
            st.image(img)

# 5. Entrada de Audio integrada (ocupa toda la pantalla abajo)
aud = st.audio_input("🎤 Usa tu voz")

# 6. Barra de escritura fija abajo (Estilo ChatGPT)
prompt = st.chat_input("Pregunta lo que quieras...")

# Si usan el micrófono, activamos la respuesta
if aud and not prompt:
    prompt = "Hola (Mensaje de voz)"

# 7. Cerebro de la IA (Texto e Imágenes perfectas)
if prompt:
    # Registrar y mostrar mensaje del usuario a la derecha
    st.session_state.h.append(("user", prompt, None))
    with st.chat_message("user", avatar="😊"):
        st.write(prompt)
        
    # Respuesta del asistente a la izquierda
    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("Pensando..."):  # Indicador de carga
            low = prompt.lower()
            
            # Filtro inteligente para saber si pide una foto/dibujo
            if any(palabra in low for palabra in ["imagen", "dibuja", "foto", "hazme", "haz", "crea"]):
                prompt_codificado = urllib.parse.quote(prompt)
                # Forzamos calidad HD (1024x1024) y evitamos deformaciones en los rostros
                url_imagen = f"https://pollinations.ai{prompt_codificado}?width=1024&height=1024&nologo=true&private=true"
                
                st.image(url_imagen)
                mensaje_asistente = "Aquí tienes tu imagen 👆"
                st.write(mensaje_asistente)
                st.session_state.h.append(("assistant", mensaje_asistente, url_imagen))
                
            else:
                # Generación de respuestas de texto continuas
                try:
                    prompt_codificado = urllib.parse.quote(prompt)
                    url_texto = f"https://pollinations.ai{prompt_codificado}?model=openai"
                    
                    r = requests.get(url_texto, timeout=30)
                    ans = r.text if r.status_code == 200 else "Tuve un pequeño problema en mi servidor central."
                except Exception:
                    ans = "Error de conexión. Revisa tu internet."
                
                st.write(ans)
                st.session_state.h.append(("assistant", ans, None))
