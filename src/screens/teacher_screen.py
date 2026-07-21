from PIL import Image
import streamlit as st


from src.component.attendance_result_dilog import attendance_result_dilog
from src.database.config import supabase
from UI.main_style import header_style_teacher, teacher_style
from src.pipelines.face_pipeline import predict_attendance
from src.database.db import create_teacher, check_teacher_exist,teacher_loginn,get_student_subject_t,get_all_record_of_attendace
from src.component.header import header_for_teacher,header_for_teacher_1,header_for_teacher_dashbord
from src.component.create_subject_dilog import Create_subject_dilog
from src.component.subject_card_t import subject_card
from src.component.share_subject_dilog import share_subject_dilog
from src.component.add_photo_dilog import add_photo_dilog
import numpy as np
from datetime import datetime
import pandas as pd
from src.component.voice_attendance_dilog import voice_attendance_dilog

def teacher_auth(username, password, confirm_password, name):
    if check_teacher_exist(username):
        return False, "Username already exists. Please choose a different username."
    if password != confirm_password:
        return False, "Passwords do not match. Please try again."
    try:
        create_teacher(username, password, name)
        return True, "Teacher account created successfully."
    except Exception as e:
        return False,"unexpected error accour"

def tlogin(username,password):
    teacher=teacher_loginn(username,password)
    if teacher:
        st.session_state['teacher'] = teacher
        st.session_state['login'] = 'dashboard'
        st.session_state.user_role='teacher'
        st.session_state.teacher_data=teacher
        st.session_state.is_logged_in=True
    else:
        st.error("Invalid username or password. Please try again.")

def header_tech():
    header_style_teacher()
    header_for_teacher()
    
def header_tech_1():
    header_style_teacher()
    header_for_teacher_1()

def teacher_screen():

    header_tech_1()
    teacher_style()

    st.markdown(
        '<div class="main-title">Teacher Dashboard</div>',
        unsafe_allow_html=True
    )

    

    btn1, btn2 = st.columns(2, gap="large")

   
    with btn1:

        st.markdown("""
        <div class="card-box">
            <div class="card-title">
                Register Teacher Account
            </div>
            <div class="card-text">
                Don't have an account? Register here.
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="register-btn">', unsafe_allow_html=True)

        if st.button("Register", key="register_btn", use_container_width=True):
            st.session_state['login'] = 'register'
            st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

    with btn2:

        st.markdown("""
        <div class="card-box">
            <div class="card-title">
                Login to Teacher Account
            </div>
            <div class="card-text">
                Already have an account? Login here.
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="login-btn">', unsafe_allow_html=True)

        if st.button("Login", key="login_btn", use_container_width=True):
            st.session_state['login'] = 'login'
            st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)




def teacher_login():
    header_tech()
    teacher_style()
    st.subheader("Teacher Login")

    st.write("Please enter your username.")
    username = st.text_input("username", key="teacher_username")

    st.write("Please enter your password.")
    password = st.text_input("Password", type="password", key="teacher_password")

    st.write("Don't have an account? Sign up now!")

    if st.button("Login", key="teacher_login_button",type="tertiary"):
        tlogin(username,password)


def teacher_register():
    header_tech()
    teacher_style()

    st.subheader("Teacher Register")
    name = st.text_input("Full Name", key="teacher_name")

    username = st.text_input("Username", key="teacher_username")

    password = st.text_input(
        "Password",
        type="password",
        key="teacher_register_password"
    )
    confirm_password = st.text_input(
        "Confirm Password",
        type="password",
        key="teacher_confirm_password"
    )

    if st.button("Create Account", key="teacher_register_button",type="tertiary"):
        succes, message = teacher_auth(username, password, confirm_password, name)
        if succes == True:
            st.success(message)
        else:
            st.error(message)   




def teacher_deshborad():
    header_for_teacher_dashbord()
    teacher_style()
    teacher= st.session_state.teacher_data

    st.space()

    if "current_teacher_tab" not in st.session_state:
        st.session_state.current_teacher_tab='start'
    tab1,tab2,tab3 =st.columns(3)

    with tab1:
        type1="secondary" if st.session_state.current_teacher_tab=='take_attendace' else 'tertiary'
        if st.button('Take Attendance',width="stretch",type=type1):
           st.session_state.current_teacher_tab='take_attendace'
           st.rerun()

    with tab2:
        type2="secondary" if st.session_state.current_teacher_tab=='manage_subject' else 'tertiary'
        if st.button('Manage Subject',width="stretch",type=type2):
           st.session_state.current_teacher_tab='manage_subject'
           st.rerun()


    with tab3:
        type3="secondary" if st.session_state.current_teacher_tab=='attendace_record' else 'tertiary'
        if st.button('Attendance Record',width="stretch",type=type3):
           st.session_state.current_teacher_tab='attendace_record'
           st.rerun()

    if st.session_state.current_teacher_tab=='take_attendace':
        teacher_tab_take_attendace()

    if st.session_state.current_teacher_tab=='manage_subject':
        teacher_tab_manage_subject()

    if st.session_state.current_teacher_tab=='attendace_record':
        teacher_tab_manage_attendace()


def teacher_tab_take_attendace():
    teacher_id=st.session_state.teacher_data['teacher_id']
    st.header("Take Attendace")
    if 'attendance_image' not in st.session_state:
        st.session_state['attendance_image'] = []

    subjects= get_student_subject_t(teacher_id)
    if not subjects:
        st.warning("No subjects found. Please create a subject first.")
        return
    subject_options = {f"{s['name']} - {s['subject_code']}": s['subject_id'] for s in subjects}
    col1,col2=st.columns([3,1],vertical_alignment="bottom")

    with col1:
        select_subject_label=st.selectbox("Select Subject", options=list(subject_options.keys()), key="selected_subject")

    with col2:
        if st.button('Add photo',type='primary',icon="📸",width="stretch"):
           add_photo_dilog()
    subject_ids=subject_options[select_subject_label]

    st.divider()
    
    if st.session_state.attendance_image:
        st.header('Added Photos')
        gallary_cols=st.columns(4)
        for i,img in enumerate(st.session_state.attendance_image):
            with gallary_cols[i%4]:
                st.image(img,width='stretch',caption=f"Photo {i+1}")

    has_photo=bool(st.session_state.attendance_image)
    c1,c2,c3=st.columns(3)
    with c1:
            if st.button('Clear All photo',width='stretch',type='secondary',icon="🗑️",disabled=not has_photo):
                st.session_state.attendance_image=[]
                st.rerun()
    with c2:
            
            if st.button('Run Face Analysis',width='stretch',type='secondary',icon="🧠",disabled=not has_photo):
               with st.spinner('deep scanning classrom photo...'):
                     all_detected_id={}

                     for idx,img in enumerate(st.session_state.attendance_image):
                         img_np=np.array(img.convert('RGB'))
                         detected, _, _ = predict_attendance(img_np)

                         if detected:
                           for student_id in detected.keys():
                              student_id = int(student_id)
                              all_detected_id.setdefault(student_id, []).append(f"Photo {idx+1}")

                     enrolled_stud=supabase.table('subject_students').select("*,student(*)").eq('subject_id', subject_ids).execute()
                     enrolled_students=enrolled_stud.data

                     if not enrolled_students:
                         st.warning("No students enrolled in this subject.")
                         return
                     else:
                         result,attendace_to_log=[],[]
                         current_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                         

                         for node in enrolled_students:
                             student=node['student']
                             sources=all_detected_id.get(student['student_id'],[])
                             is_present=len(sources)>0
                             result.append({
                                 "Name": student['name'],
                                 "ID": student['student_id'],
                                 "sources": ", ".join(sources) if is_present else "_",
                                 "Status": "Present" if is_present else "Absent"
                             })
                             attendace_to_log.append({
                                 "student_id": student['student_id'],
                                 "subject_id": subject_ids,
                                 "timestamp": current_time,
                                 "is_present":bool(is_present)
                             })

                     attendance_result_dilog(pd.DataFrame(result),attendace_to_log)


    with c3:
        if st.button('Use Voice Analysis',width='stretch',type='secondary',icon="🎤"):
           voice_attendance_dilog(subject_ids)




def teacher_tab_manage_subject():

    teacher_id=st.session_state.teacher_data['teacher_id']
    clm1,clm2 =st.columns(2)

    with clm1:
        st.header("Manage Subject")

    with clm2:
        if st.button('Creat New Subject',type='primary',width="stretch"):
            Create_subject_dilog(teacher_id)


    subject= get_student_subject_t(teacher_id)
    if subject:
        for sub in subject:
            states=[
                ("students",sub['total_student']),
                ("Classes",sub["total_classes"])
            ]
            
            def share_btn():
               if st.button(f"Share Code: {sub['subject_code']}",key=f"share_{sub['name']}",type='secondary'):
                    share_subject_dilog(sub['name'],sub['subject_code'])
               st.space()

            subject_card(
            name=sub['name'],
            code=sub['subject_code'],
            section=sub['section'],
            stats=states,
            footer_callback=None
            )
            share_btn()
    else:
        st.info("No Subject Found, Create One Above")
        



def teacher_tab_manage_attendace():
    st.header("attendace record")

    teacher_id=st.session_state.teacher_data['teacher_id']

    record=get_all_record_of_attendace(teacher_id)
    if not record:
        st.info("No attendance record found.")
        return
    
    data=[]
    for log in record:
        ts=log.get('timestamp')
        data.append({
            "ts_group":ts.split(" ")[0] if ts else None,
            "Time":datetime.fromisoformat(ts).strftime("%Y-%m-%d %I:%M %p") if ts else None,
            "Subject":log['subject']['name'] ,
            "Subject code":log['subject']['subject_code'],
            "is_present":bool(log.get('is_present',False))
        })
        df=pd.DataFrame(data)


    summary=(
        df.groupby(['ts_group','Time','Subject','Subject code'])
        .agg(
            present_count=('is_present', 'sum'),
            total_count=('is_present', 'count')
        ).reset_index()
    )

    summary['Attendance Stats']=(
        summary['present_count'].astype(str) + '/' + summary['total_count'].astype(str)+ 'students'
    )
    display_df=(summary.sort_values(by='ts_group',ascending=False)
                [['Time','Subject','Subject code','Attendance Stats']])
    
    st.dataframe(display_df,width='stretch',hide_index=True)






def teacher_main2():
    if 'login' not in st.session_state:
        st.session_state['login'] = 'none'

    match st.session_state['login']:

        case 'login':
            teacher_login()

        case 'register':
            teacher_register()

        case 'dashboard':
            teacher_deshborad()

        case 'none':
            teacher_screen()  