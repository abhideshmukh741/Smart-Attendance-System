import streamlit as st
import segno
import io

@st.dialog("Share Subject Link")
def share_subject_dilog(subject_name,subject_code):
   app_domain="http://localhost:8501"
   join_url=f"{app_domain}/?join-code={subject_code}"

   st.header("scanne to join")

   qr=segno.make(join_url)

   out=io.BytesIO()

   qr.save(out,kind='png',scale=10,border=1)

   clm1,clm2=st.columns(2)

   with clm1:
      st.markdown('### copy Link')
      st.code(join_url,language="text")
      st.code(subject_code,language="text")
      st.info("Copy this link to share on Whatsapp or Email")
   with clm2:
       st.markdown('### Scan to join')
       st.image(out.getvalue(),width="stretch",caption='QRCODE for class joining')
