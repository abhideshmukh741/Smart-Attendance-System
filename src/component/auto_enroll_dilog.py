import streamlit as st
from src.database.db import enroll_student_to_subject
from src.database.config import supabase
import time



@st.dialog('Quick Enrollment')
def auto_enroll_dilog(join_code):
    student_id=st.session_state.student_data['student_id']
    res=supabase.table('subject').select('subject_id,name').eq('subject_code',join_code).execute()
    if not res.data:
        st.error('subject not found')
        if st.button('Close'):
            st.query_params.clear()
            st.rerun()

        return
    subject=res.data[0]
    check=supabase.table('subject_students').select('*').eq('subject_id',subject['subject_id']).eq('student_id',student_id).execute()
    if check.data:
        st.info('you are alrady enroll')
        if st.button('Got it'):
            st.query_params.clear()
            st.rerun()
        return

    st.markdown(f"Would you like to enroll  **{subject['name']}**?")
    col1,col2=st.columns(2)

    with col1:
        if st.button('NO thanks'):
            st.query_params.clear()
            st.rerun()
    with col2:
        if st.button('Yes enroll Now',type='primary',width='stretch'):
            enroll_student_to_subject(student_id,subject['subject_id'])
            st.success("Join Succesfully")
            st.query_params.clear()
            time.sleep(2)
            st.rerun()

