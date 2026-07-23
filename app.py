import streamlit as st
from src.screens.home_screen import home_screen
from src.screens.student_screen import student_screen
from src.screens.teacher_screen import teacher_main2
from src.component.auto_enroll_dilog import auto_enroll_dilog




def main():
  st.set_page_config(
     page_title='SnapClass-Making Attendance faster using Ai',
     page_icon="UI\images\logo.png"
  )
  if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = 'none'


  join_code=st.query_params.get('join-code')
  if join_code and st.session_state.logged_in == 'none':
        st.session_state.logged_in = 'student'
        st.rerun() 

  match st.session_state['logged_in']:
    case 'teacher':
      placeholder = st.empty()

      with placeholder.container():
            with st.spinner("Loading..."):
              teacher_main2()
    case 'student':
       placeholder = st.empty()

       with placeholder.container():
            with st.spinner("Loading..."):
                student_screen()

    case 'none':
        placeholder = st.empty()

        with placeholder.container():
            with st.spinner("Loading..."):
              home_screen()

  
  if join_code:
    try:
        if (
            st.session_state.get("logged_in")=="student"
            and st.session_state.get("student_data")
        ):
            auto_enroll_dilog(join_code)

    except Exception as e:
        st.error(f"Error: {e}")

main()