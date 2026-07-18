 import streamlit as st
import requests
import urllib.parse

st.set_page_config(page_title='Bairon IA', layout='wide')
st.markdown('<style>.block-container{max-width:100%!important} header,footer,#MainMenu{visibility:hidden}</style>', unsafe_allow_html=True)

if 'c' not in st.session_state:
    st.session_state.c = []

with st.expander('Mandar foto, audio o PDF'):
    f = st.file_uploader('Foto', type=['png','jpg','jpeg'])
    a = st.audio_input('Grabar voz')
    if f:
        st.image(f)

for rol, msg, img in st.session_state.c:
    av = '😊' if rol == 'user' else '🤖'
    with st.chat_message(rol, avatar=av):
        st.write(msg)
        if img:
            st.image(img)

p = st.chat_input('Escribe /imagen para crear imagen')

if a and not p:
    p = 'Hola Bairon'

if p:
    st.session_state.c.append(('user', p, None))
    with st.chat_message('user', avatar='😊'):
        st.write(p)
    with st.chat_message('assistant', avatar='🤖'):
        with st.spinner('Pensando...'):
            low = p.lower()
            if 'quien te creo' in low or 'bairon-dev' in low or 'quien soy' in low or 'me conoces' in low:
                if 'bairon-dev' in low or 'quien soy' in low or 'me conoces' in low:
                    ans = 'Si, te reconozco, eres Bairon, bairon-dev, mi creador. Soy Bairon IA.'
                else:
                    ans = 'Me creo Bairon-dev, soy Bairon IA.'
                st.write(ans)
                st.session_state.c.append(('assistant', ans, None))
            elif '/imagen' in low or 'hazme una imagen' in low or 'imagen de' in low or 'dibuja' in low:
                clean = p.replace('/imagen','').replace('hazme una imagen de','').replace('hazme una imagen','').strip()
                if clean == '':
                    clean = 'los simpson'
                q = urllib.parse.quote(clean)
                url = f'https://image.pollinations.ai/prompt/{q}?nologo=true'
                st.write(f'Generando imagen: {clean}')
                st.image(url)
                st.session_state.c.append(('assistant', f'Generando imagen: {clean}', url))
            else:
                try:
                    qq = urllib.parse.quote(f'Eres Bairon IA creado por Bairon-dev. Pregunta: {p}')
                    r = requests.get(f'https://text.pollinations.ai/{qq}?model=openai', timeout=20)
                    ans = r.text if r.text else 'Soy Bairon IA, dime que necesitas.'
                except:
                    ans = 'Soy Bairon IA, dime que necesitas.'
                st.write(ans)
                st.session_state.c.append(('assistant', ans, None))