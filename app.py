
    st.set_page_config(
    page_title="Bairon AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.title("🤖 Bairon AI")
st.caption("Tu asistente personal con IA")

with st.sidebar:
    st.header("⚙️ Opciones")

    if st.button("🗑️ Nuevo chat"):
        st.session_state.c = []
        st.rerun()

    st.divider()

    st.write("Modelo")
    st.success("Llama 3.3 70B")

    st.divider()

    st.write("Creado por Bairon 🚀")