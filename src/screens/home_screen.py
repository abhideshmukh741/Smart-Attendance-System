import streamlit as st
from UI.main_style import style_bag_home
from src.component.header import header





def home_screen():
    style_bag_home()
    st.markdown("<h1>Welcome to Attendance Management System</h1>", unsafe_allow_html=True)
    st.image("C:\\Users\\Mayur\\OneDrive\\Desktop\\addendence system\\UI\\images\\image.png")
    btn1, btn2 = st.columns(2, gap="large")
    with btn1:
        st.header("i am a Teacher")
        st.image("C:\\Users\\Mayur\\OneDrive\\Desktop\\addendence system\\UI\\images\\teacher.png", width=110)
        if st.button("Login as Teacher",width=200):
            st.session_state['logged_in'] = 'teacher'
            st.rerun()
    with btn2:
        st.header("i am a Student")
        st.image("C:\\Users\\Mayur\\OneDrive\\Desktop\\addendence system\\UI\\images\\student.png", width=150)
        if st.button("Login as Student",width=200):
            st.session_state['logged_in'] = 'student'
            st.rerun()

    st.markdown("""
         
                <style>h2{
        color: black !important; 
            }
            </style>    """, unsafe_allow_html=True 
    
    )