import streamlit as st
from src.database.config import supabase
from src.database.db import create_attendance

@st.dialog("Capture or update photos")
def show_attendance_result(df,logs):
        
        st.write("please review attendance befor confirming")
        st.dataframe(df,hide_index=True,width="stretch")

        col1,col2=st.columns(2)

        with col1:
            if st.button('Discard',type='tertiary',width='stretch'):
              st.session_state.voice_attendance_result=None
              st.session_state.attendance_image=[]
              st.rerun()

        with col2:
            if st.button('Confirm & save',width='stretch',type='secondary'):
                try:
                    create_attendance(logs)
                    st.toast("Attendance saved successfully")
                    st.session_state.attendance_image=[]
                    st.session_state.voice_attendance_result=None
                    st.rerun()
                except Exception as e:
                    st.error(f"Error saving attendance: {e}")
    

@st.dialog('Attendance Result')
def attendance_result_dilog(df,logs):
    st.write("Attendance Result")
    show_attendance_result(df,logs)

                
