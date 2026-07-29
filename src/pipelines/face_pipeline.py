import numpy as np
import streamlit as st

try:
    import dlib
    import face_recognition_models
    from sklearn.svm import SVC
except Exception:  # pragma: no cover - optional dependency fallback
    dlib = None
    face_recognition_models = None
    SVC = None

from src.database.db import get_all_students


@st.cache_resource
def load_dlib_models():
    if dlib is None or face_recognition_models is None:
        raise RuntimeError("Face recognition dependencies are not installed.")

    detecter = dlib.get_frontal_face_detector()
    sp = dlib.shape_predictor(face_recognition_models.pose_predictor_model_location())
    facerec = dlib.face_recognition_model_v1(face_recognition_models.face_recognition_model_location())
    return detecter, sp, facerec


def get_face_embedding(image):
    detecter, sp, facerec = load_dlib_models()

    embedding = []
    faces = detecter(image, 1)

    for face in faces:
        shape = sp(image, face)
        face_descriptor = facerec.compute_face_descriptor(image, shape, 1)
        embedding.append(np.array(face_descriptor))
    return embedding


def gate_trained_model():
    if SVC is None:
        return None

    x = []
    y = []

    students = get_all_students()
    if not students:
        return None
    for student in students:
        embedding = student.get('face_embedding')
        if embedding:
            x.append(np.array(embedding))
            y.append(student.get('student_id'))
    if len(x) == 0:
        return None

    clf = SVC(kernel='linear', probability=True, class_weight='balanced')
    try:
        clf.fit(x, y)
    except ValueError:
        pass
    return {'clf': clf, 'x': x, 'y': y}


def train_classifier():
    model_data = gate_trained_model()
    return bool(model_data)


def predict_attendance(group_image):
    try:
        encoding = get_face_embedding(group_image)
    except Exception as exc:
        st.warning(f"Face attendance disabled: {exc}")
        return {}, [], 0

    detected_student = {}
    model_dta = gate_trained_model()
    if model_dta is None:
        return detected_student, [], len(encoding)

    clf = model_dta['clf']
    x_train = model_dta['x']
    y_train = model_dta['y']

    all_students = sorted(list(set(y_train)))
    for enc in encoding:
        if len(all_students) >= 2:
            predict_id = clf.predict([enc])[0]
        else:
            predict_id = y_train[0]

        student_embedding = x_train[y_train.index(predict_id)]

        best_match_score = np.linalg.norm(student_embedding - enc)
        if best_match_score < 0.6:
            detected_student[predict_id] = True

    return detected_student, all_students, len(encoding)


            
   

    
