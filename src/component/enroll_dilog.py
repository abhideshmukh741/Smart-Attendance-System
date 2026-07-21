import streamlit as st
from src.database.config import supabase
from src.database.db import student_sub,enroll_student_to_subject
import time



@st.dialog('Enroll into The Subject')
def enroll_dilog():
    st.write('Enter the subject code provided by your teacher to enroll')
    join_code=st.text_input('Subject Code',placeholder='CSE210')
    if st.button('Enroll Now',type='primary',width='stretch',key='stundet_enrolll'):
        if join_code:
            res=supabase.table('subject').select('subject_id,name,subject_code').eq('subject_code',join_code).execute()
            if res.data:
                subject=res.data[0]
                student_id= st.session_state.student_data['student_id']


                check=supabase.table('subject_students').select('*').eq('student_id',student_id).eq('subject_id',subject['subject_id']).execute()
                if check.data:
                    st.warning('You are already enroll in this program')
                else:
                    enroll_student_to_subject(student_id,subject['subject_id'])
                    st.success('Sussesfully Enroll')
                    time.sleep(1)
        else:
           st.warning('Please Enter the Subject code') 