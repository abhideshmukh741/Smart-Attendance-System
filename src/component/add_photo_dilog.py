import streamlit as st
from src.database.db import student_sub
from src.database.config import supabase
import time
from PIL import Image

@st.dialog('capture or upload your photo')
def add_photo_dilog():
    st.write('Add classroom photos to scan for attendance')

    if 'photo_tab' not in st.session_state:
        st.session_state['photo_tab']="camera"

    t1,t2=st.columns(2)

    with t1:
        type_camera="tertiary" if st.session_state.photo_tab=='camera' else 'secondary'
        if st.button('Camera',type=type_camera,width='stretch'):
            st.session_state.photo_tab='camera'
            
            
            

    with t2:
        type_upload="tertiary" if st.session_state.photo_tab=='upload' else 'secondary'
        if st.button('Upload',type=type_upload,width='stretch'):
            st.session_state.photo_tab='upload'
            
            


    if st.session_state.photo_tab=='camera':
        cam_photo=st.camera_input("Take a photo",key="cam_inp")
        if cam_photo:
            st.session_state.attendance_image.append(Image.open(cam_photo))
            st.toast('photo captured')
            st.rerun()
            

    if st.session_state.photo_tab=='upload':
        uploaded_files=st.file_uploader('choose image files',type=['jpg','png','jpeg'],accept_multiple_files=True,key='dilog_update')

        if uploaded_files:
            for f in uploaded_files:
                st.session_state.attendance_image.append(Image.open(f))
            st.toast('photo uploaded successfully')
            st.rerun()
            
    st.divider()
    if st.button('Done',type='primary',width='stretch'):
        st.rerun()


