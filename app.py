import streamlit as st, requests, urllib.parse
st.set_page_config(page_title="Bairon AI", layout="wide")
if "c" not in st.session_state:
 st.session_state.c=[]
st.markdown("<h3 style='text-align:center'>Bairon AI - by bairon-dev</h3>", unsafe_allow_html=True)
with st.expander("Mandar foto, audio o PDF"):
 foto=st.file_uploader("Foto", type=["png","jpg","jpeg"])
 audio=st.file_uploader("Audio", type=["mp3","wav","m4a","ogg"])
 pdf=st.file_uploader("PDF", type=["pdf"])
for r,m,i in st.session_state.c:
 with st.chat_message(r, avatar="😊" if r=="user" else "🤖"):
  st.write(m)
  if i:
   st.image(i)
p=st.chat_input("Escribe /imagen para crear imagen")
if p:
 img_to_show=foto if foto else None
 st.session_state.c.append(("user",p,img_to_show))
 with st.chat_message("user", avatar="😊"):
  st.write(p)
  if img_to_show:
   st.image(img_to_show, width=250)
  if audio:
   st.audio(audio)
  if pdf:
   st.write(f"PDF recibido: {pdf.name}")
 with st.chat_message("assistant", avatar="🤖"):
  low=p.lower()
  if "bairon-dev" in low or "quien soy" in low or "me conoces" in low:
   ans="Si, te reconozco, eres Bairon, bairon-dev, mi creador. Yo soy Bairon IA creado por ti."
  elif "quien te creo" in low:
   ans="Me creo bairon-dev, soy Bairon IA."
  elif "/imagen" in low or "imagen de" in low or "dibuja" in low:
   clean=p.replace("/imagen","").replace("imagen de","").strip() or "homero simpson"
   q=urllib.parse.quote(clean)
   url=f"https://image.pollinations.ai/prompt/{q}?nologo=true"
   st.image(url)
   st.session_state.c.append(("assistant", f"Imagen: {clean}", url))
   ans=None
  else:
   q=urllib.parse.quote(f"Eres Bairon IA creado por bairon-dev. Responde corto: {p}")
   r=requests.get(f"https://text.pollinations.ai/{q}?model=openai", timeout=30)
   ans=r.text
  if ans:
   st.write(ans)
   st.session_state.c.append(("assistant",ans,None))