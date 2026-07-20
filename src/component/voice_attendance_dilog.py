import streamlit as st
from src.component.attendance_result_dilog import show_attendance_result
from src.database.config import supabase
from src.pipelines.voice_pipeline import process_bulk_attendance
import pandas as pd
from datetime import datetime

@st.dialog('Voice Attendance')
def voice_attendance_dilog(subject_ids):
    st.write("Record Audio for Attendance,Say 'I am present' to mark your attendance")
    audio_data=None
    audio_data=st.audio_input("Record Audio")
    if st.button("Process Attendance",type='primary',width='stretch'):
        with st.spinner('Processing Audio for Attendance...'):
            enrolled_stud=supabase.table('subject_students').select("*,student(*)").eq('subject_id', subject_ids).execute()
            enrolled_students=enrolled_stud.data

            if not enrolled_students:
                st.warning("No students enrolled in this subject.")
                return
            
            candidates_dir={stud['student']['student_id']:stud['student']['voice_embedding']
                             for stud in enrolled_students if stud['student']['voice_embedding']}
            if not candidates_dir:
                st.error("No voice embeddings found for enrolled students.")
                return
            
            audio_bytes=audio_data.read() if audio_data else None


            st.write("Candidates Directory:", candidates_dir)
            st.write("Number of candidates:", len(candidates_dir))

            detected_sources=process_bulk_attendance(audio_bytes,candidates_dir)
            
            result,attendace_to_log=[],[]
            
            current_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            for node in enrolled_students:
                student=node['student']
                sources=detected_sources.get(student['student_id'],0.0)

                is_present=bool(sources)
                result.append({
                    "Name": student['name'],
                    "ID": student['student_id'],
                    "sources":sources if is_present else "_",
                    "Status": "Present" if is_present else "Absent"
                    })
                attendace_to_log.append({
                    "student_id": student['student_id'],
                    "subject_id": subject_ids,
                    "timestamp": current_time,
                    "is_present":bool(is_present)
                   })
                

            st.session_state.voice_attendance_result=(pd.DataFrame(result),attendace_to_log)

    if st.session_state.get('voice_attendance_result'):
        st.divider()
        df,logs=st.session_state.voice_attendance_result
        show_attendance_result(df,logs)







