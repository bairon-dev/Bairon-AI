import streamlit as st, requests, urllib.parse

st.set_page_config(page_title="Bairon IA", layout="wide")
st.markdown("<style>.block-container{max-width:100%!important} header,footer,#MainMenu{visibility:hidden} div[data-testid='stChatMessage']{border-radius:18px}</style>", unsafe_allow_html=True)

if "c" not in st.session_state:
    st.session_state.c = []

with st.expander("📎 Mandar foto, audio o PDF"):
    f = st.file_uploader("Foto", type=["png","jpg","jpeg"])
    a = st.audio_input("🎤 Grabar voz")
    if f:
        st.image(f)

for rol, msg, img in st.session_state.c:
    with st.chat_message(rol, avatar="😊" if rol=="user" else "🤖"):
        st.write(msg)
        if img:
            st.image(img)

p = st.chat_input("Escribe /imagen para crear imagen")

if a and not p:
    p = "Hola Bairon"

if p:
    st.session_state.c.append(("user", p, None))
    with st.chat_message("user", avatar="😊"):
        st.write(p)
    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("Pensando..."):
            low = p.lower()
            # --- RECONOCE A BAIRON-DEV ---
            if "quien te creo" in low or "quien te hizo" in low or "bairon-dev" in low or "bairon dev" in low or "quien soy" in low or "me conoces" in low:
                if "bairon-dev" in low or "quien soy" in low or "me conoces" in low:
                    ans = "Si, te reconozco, eres Bairon, bairon-dev, mi creador. Soy Bairon IA, creado por ti."
                else:
                    ans = "Me creo Bairon, bairon-dev, soy