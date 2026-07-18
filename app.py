import streamlit as st, requests, urllib.parse
st.set_page_config(page_title="Bairon-AI", layout="centered")
st.markdown("<style>.stApp{background:#0e0e0e}h1{color:#fff;text-align:center}.msg-u{background:#fff;color:#000;padding:10px 16px;border-radius:18px 18px 2px 18px;float:right;max-width:80%;margin:6px;clear:both}.msg-b{background:#222;color:#fff;padding:12px 16px;border-radius:18px 18px 18px 2px;float:left;max-width:85%;margin:6px;clear:both}</style>",unsafe_allow_html=True)
st.markdown("<h1>Bairon-AI - Garcia NL</h1>",unsafe_allow_html=True)
if "c" not in st.session_state: st.session_state.c=[]
for m in st.session_state.c:
 if m["r"]=="u": st.markdown(f'<div style="display:flex;justify-content:flex-end;width:100%"><div class="msg-u">{m["t"]}</div></div>',unsafe_allow_html=True)
 else:
  if m["y"]=="t": st.markdown(f'<div style="display:flex;width:100%"><div class="msg-b">{m["t"]}</div></div>',unsafe_allow_html=True)
  else: st.image(m["t"])
p=st.chat_input("Escribe algo o /imagen un tesla...")
if p:
 st.session_state.c.append({"r":"u","y":"t","t":p})
 if p.lower().startswith("/imagen"):
  q=p.replace("/imagen","").strip() or "cybertruck"
  u=f"https://image.pollinations.ai/prompt/{urllib.parse.quote(q)}?width=1024&nologo=1"
  st.session_state.c.append({"r":"b","y":"i","t":u})
 else:
  try:
   k=st.secrets["GROQ_API_KEY"]
   r=requests.post("https://api.groq.com/openai/v1/chat/completions",headers={"Authorization":f"Bearer {k}","Content-Type":"application/json"},json={"model":"llama-3.3-70b-versatile","messages":[{"role":"system","content":"Eres Bairon-AI de Garcia NL, creado por Bairon. Responde corto y chido."},{"role":"user","content":p}]},timeout=30)
   a=r.json()["choices"][0]["message"]["content"]
  except Exception as e: a=f"Pon tu GROQ_API_KEY en Settings > Secrets. Error: {e}"
  st.session_state.c.append({"r":"b","y":"t","t":a})
 st.rerun()