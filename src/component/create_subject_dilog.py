import streamlit as st
from src.database.db import student_sub

@st.dialog("Create New Subject")
def Create_subject_dilog(teacher_id):
    st.write("Enter the detils of new Subject")
    Subject_code=st.text_input("Subject Code",placeholder="CSE201")
    Subject_name=st.text_input("Subject Name",placeholder="Mechine Learning")
    Subject_sec=st.text_input("Section",placeholder="Batch A")
    if st.button("Create New Subject",type="primary",width="stretch"):
        if Subject_code and Subject_name and Subject_sec:
            try:
                student_sub(Subject_code,Subject_name,Subject_sec,teacher_id)
                st.toast("New Subject Is Created")
                st.rerun()
            except Exception as e:
                st.error(f"the error is {e}")
        else:
            st.warning("please fill all the details")


