import streamlit as st
from UI.main_style import header_style_teacher,header_style_student

def header():
    st.markdown(
        """
        <div style="display:flex; padding: 20px; text-align: center;">
        <h1 style="color: #E0E0E0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: auto;">AMS</h1>
          <style>
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Changa+One:ital@0;1&display=swap" rel="stylesheet">
        h1 {
        font-family: 'Changa One', cursive !important;  
         color: #E0E0E0 !important;
        text-align: center !important;
        margin-bottom: 50px !important;
        margin-top: 0px !important;
        }
    }
        </style>
        """,unsafe_allow_html=True)
    

def header_for_teacher():
    header_style_teacher()
    c1, c2 = st.columns([5, 1])   

    with c1:
        st.markdown("""
        <div style="text-align:left;">
            <h6>Welcome, Teacher!</h6>
            <h2>Class Management</h2>
        </div>

        <style>
            h6 {
                margin-bottom: 0px !important;
                padding: 0px !important;
            }

            h2 {
                margin-top: 0px !important;
                padding: 0px !important;
            }
        </style>
        """, unsafe_allow_html=True)

        
    with c2:

        st.markdown('<div class="home-btn">', unsafe_allow_html=True)

        if st.button("back", use_container_width=True,type="primary"):
          st.session_state['login'] = 'none'
          st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)


def header_for_teacher_1():
    header_style_teacher()
    c1, c2 = st.columns([5, 1])   

    with c1:
        st.markdown("""
        <div style="text-align:left;">
            <h6>Welcome, Teacher!</h6>
            <h2>Class Management</h2>
        </div>

        <style>
            h6 {
                margin-bottom: 0px !important;
                padding: 0px !important;
            }

            h2 {
                margin-top: 0px !important;
                padding: 0px !important;
            }
        </style>
        """, unsafe_allow_html=True)

        
    with c2:

        st.markdown('<div class="home-btn">', unsafe_allow_html=True)

        if st.button("Go to home", use_container_width=True,type="primary"):
          st.session_state['logged_in'] = 'none'
          st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)


def header_for_teacher_dashbord():
    header_style_teacher()
    c1, c2 = st.columns([5, 1])   

    with c1:
        st.markdown("""
        <div style="text-align:left;">
            <h6>Welcome, Teacher!</h6>
            <h2>Class Management</h2>
        </div>

        <style>
            h6 {
                margin-bottom: 0px !important;
                padding: 0px !important;
            }

            h2 {
                margin-top: 0px !important;
                padding: 0px !important;
            }
        </style>
        """, unsafe_allow_html=True)

        
    with c2:

        st.markdown('<div class="home-btn">', unsafe_allow_html=True)

        if st.button("logout", use_container_width=True,type="primary"):
          st.session_state['login'] = 'none'
          del st.session_state.teacher_data
          st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)




def header_for_student():
    header_style_student()
    c1, c2 = st.columns([5, 1])   

    with c1:
        st.markdown("""
        <div style="text-align:left;">
            <h6>Welcome, students!</h6>
            <h2>Class Management</h2>
        </div>

        <style>
            h6 {
                margin-bottom: 0px !important;
                padding: 0px !important;
            }

            h2 {
                margin-top: 0px !important;
                padding: 0px !important;
            }
        </style>
        """, unsafe_allow_html=True)

        
    with c2:

        st.markdown('<div class="home-btn">', unsafe_allow_html=True)

        if st.button("logout", use_container_width=True,type="primary"):
          st.session_state['logged_in'] = 'none'
          del st.session_state.student_data
          st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)