import time
from PIL import Image
from src.pipelines.voice_pipeline import get_voice_embedding
from src.pipelines.voice_pipeline import get_voice_embedding
from src.pipelines.face_pipeline import get_face_embedding, predict_attendance, train_classifier
from src.database.db import get_all_students, create_student,get_student__subjects,get_student_attendace
import streamlit as st
import numpy as np
from src.component.subject_card import subject_card
from UI.main_style import header_style_student,student_style
from src.component.header import header_for_student,header_for_student_1
from src.component.enroll_dilog import enroll_dilog
from src.database.db import unenroll_student_to_subject


def header_tech_1():
    header_style_student()
    header_for_student()
  
    
def student_dashbord():
    student_data=st.session_state.student_data
    student_id=student_data['student_id']
    st.markdown(
        f'<div class="welcome-message">Welcome back, {st.session_state.student_data["name"]}!</div>',
        unsafe_allow_html=True
    )


    st.space()

    c1,c2=st.columns(2)
    with c1:
        st.header("Your Enrolled Subject")

    with c2:
        if st.button('Enroll in Subject',type='tertiary',width='stretch',key='student_en'):
            enroll_dilog()
      


    st.divider()

    with st.spinner('loading your enrollment subject...'):
        subjects=get_student__subjects(student_id)
        logs=get_student_attendace(student_id)

    stats_map={}

    for log in logs:
        sid=log['subject_id']
        if sid not in stats_map:
            stats_map[sid]={'total':0,'attendace':0}

        stats_map[sid]['total']+=1
        if log['is_present']:
            stats_map[sid]['attendace']+=1


    st.space()

    clm=st.columns(2)
    for i ,sub_node in enumerate(subjects):
            sub=sub_node["subject"]
            sid=sub["subject_id"]


            stats=stats_map.get(sid,{"total":0,"attendace":0})
            def uneroll_button():
                if st.button('Uneroll from this course',type='secondary',width='stretch',key=f"unenroll_{sub['subject_id']}"):
                    unenroll_student_to_subject(student_id,sid)
                    st.toast(f"Unrolled from {sub['name']} successfully!")
                    st.rerun()

            with clm[ i%2 ]:
                subject_card(
                    name=sub['name'],
                    code=sub['subject_code'],
                    section=sub['section'],
                    stats=[
                        {'Total :',stats['total']},
                        {'Attended :',stats['attendace']}
                       ],
                    footer_callback=uneroll_button()
                )
        



def student_screen():
    header_tech_1() 
    student_style()

    
    if "student_data" in st.session_state:
        student_dashbord()
        return

    st.markdown(
        '<div class="main-title">Student Dashboard</div>',
        unsafe_allow_html=True
    )
    if "show_registration" not in st.session_state:
        st.session_state.show_registration = False

    img = st.camera_input("Take a picture of your face to mark attendance")
    if img:
        st.session_state.last_img = img
        img_array = np.array(Image.open(img))
        

        with st.spinner("Processing your attendance..."):
            detected_students,all_ids,num_face = predict_attendance(img_array)
            st.write(f"Faces: {num_face} | Detected: {detected_students} | Total students: {len(all_ids)}")
        if num_face == 0:
            st.error("No face detected. Please try again.")
            st.session_state.show_registration = False
        elif num_face > 1:
            st.warning("Multiple faces detected. Please ensure only your face is visible.")
            st.session_state.show_registration = False
        else:
            if detected_students:
                student_id=list(detected_students.keys())[0]
                all_ids=get_all_students()
                student_info=next((s for s in all_ids if s['student_id']==student_id),None)

                if student_info:
                    st.session_state.logged_in='student'
                    st.session_state.is_logged_in=True
                    st.session_state.user_role='student'
                    st.session_state.student_data=student_info
                    st.session_state.show_registration = False
                    st.toast(f"Welcome {student_info['name']}! Your attendance has been marked.")
                    time.sleep(1)
                    st.rerun()
            else: 
                st.info("Face not recognised ! you might be new student .")
                st.session_state.show_registration = True 

    if img:
        st.session_state.last_img = img
    if st.session_state.show_registration and "last_img" in st.session_state:
            with st.container(border=True):
                new_name=st.text_input("Enter your name to register")
                st.subheader("Optional :voice sample for better recognition in future")
                st.info("Please record a short voice sample (5-10 seconds) saying your name clearly.")

                audo_data=None
                try:
                    audo_data=st.audio_input("Record your voice")
                except Exception as e:
                    st.error(f"Audio input not supported: {e}")

                if st.button("Create Profile"):
                    if new_name:
                     with st.spinner("Creating your profile..."):
                        image = np.array(Image.open(st.session_state.last_img))
                        face_embedding=get_face_embedding(image)
                        if face_embedding:
                            face_embedding=face_embedding[0].tolist()
                            voice_embedding=None
                            if audo_data:
                              voice_embedding=get_voice_embedding(audo_data)
                            response=create_student(new_name,face_embedding,voice_embedding)
                            if response:
                              train_classifier()
                              st.session_state.logged_in='student'
                              st.session_state.is_logged_in=True
                              st.session_state.user_role='student'
                              st.session_state.student_data=response[0]
                              st.session_state.show_registration = False
                              st.toast(f"Welcome {response[0]['name']}! Your Profile is created.")
                              time.sleep(1)
                              st.rerun()
                        else:
                            st.error("Could not capture your facial features.")

                    else:
                       st.error("Name is required to create a profile.")
                