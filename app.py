 import streamlit as st
import requests, urllib.parse

st.set_page_config(page_title="Bairon-AI",layout="centered")
st.markdown("<style>.stApp{background:#0e0e0e}h1{color:#fff;text-align:center}.u{background:#fff;color:#000;padding:10px 16px;border-radius:18px 18px 2px 18px;float:right;max-width:80%;margin:6px 0;clear:both}.b{background:#2a2a2a;color:#fff;padding:12px 16px;border-radius:18px 18px 18px 2px;float:left;max-width:85%;margin:6px 0;clear:both}</style>",unsafe_allow_html=True)
st.markdown("<h1>Bairon-AI - Garcia NL</h1>",unsafe_allow_html=True)

if "chat" not in st.session_state:
 st.session_state.chat=[]

for m in st.session_state.chat:
 if m["role"]=="user":
  st.markdown(f'<div style="display:flex;justify-content:flex-end;width:100%"><div class="u">{m["content"]}</div></div>',unsafe_allow_html=True)
 else:
  if m["type"]=="text":
   st.markdown(f'<div style="display:flex;width:100%"><div class="b">{m["content"]}</div></div>',unsafe_allow_html=True)
  else:
   st.image(m["content"])

p=st.chat_input("Escribe algo o /imagen un tesla...")
if p:
 st.session_state.chat.append({"role":"user","type":"text","content":p})
 if p.lower().startswith("/imagen"):
  txt=p.replace("/imagen","").strip() or "tesla cybertruck"
  url=f"https://image.pollinations.ai/prompt/{urllib.parse.quote(txt)}?width=1024&height=1024&nologo=1"
  st.session_state.chat.append({"role":"bot","type":"image","content":url})
 else:
  try:
   k=st.secrets["GROQ_API_KEY"]
   h={"Authorization":f"Bearer {k}","Content-Type":"application/json"}
   d={"model":"llama-3.3-70b-versatile","messages":[{"role":"system","content":"Eres Bairon-AI hecha por Bairon en Garcia NL"},{"role":"user","content":p}]}
   r=requests.post("https://api.groq.com/openai/v1/chat/completions",headers=h,json=d,timeout=30)
   ans=r.json()["choices"][0]["message"]["content"]
  except Exception as e:
   ans=f"Pon tu GROQ_API_KEY en Secrets. Error: {e}"
  st.session_state.chat.append({"role":"bot","type":"text","content":ans})
 st.rerun()


