from src.database.config import supabase
import bcrypt

def hash_pass(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def check_pass(password,hashed):
    return bcrypt.checkpw(password.encode(), hashed.encode())

def check_teacher_exist(username):
    response=supabase.table('teacher').select('username').eq('username',username).execute()
    return len(response.data)>0

def create_teacher(username,password,name):
    if check_teacher_exist(username):
        return False, "Username already exists. Please choose a different username."
    data={
        "username":username,
        "password":hash_pass(password),
        "name":name
    }
    response=supabase.table('teacher').insert(data).execute()
    return response.data

def teacher_loginn(username,password):
    response=supabase.table('teacher').select('*').eq('username',username).execute()
    if response.data:
        teacher=response.data[0]
        if check_pass(password,teacher['password']):
            return teacher 
    return None

def get_all_students():
    response=supabase.table('student').select('*').execute()
    return response.data

def create_student(name,face_embedding,voice_embedding):
    data={
        "name":name,
        "face_embedding":face_embedding,
        "voice_embedding":voice_embedding
    }
    response=supabase.table('student').insert(data).execute()
    return response.data

def student_sub(Subject_code,Subject_name,Subject_sec,teacher_id):
    data={"subject_code":Subject_code,"name":Subject_name,"section":Subject_sec,"teacher_id":teacher_id}
    response=supabase.table('subject').insert(data).execute()
    return response.data

def get_student_subject_t(teacher_id):
    respose=supabase.table('subject').select("*,subject_students(count),attendace_logs(timestamp)").eq("teacher_id",teacher_id).execute()
    subject = respose.data
    
    for sub in subject:
        sub['total_student']=sub.get("subject_students",[{}])[0].get('count',0) if sub.get('subject_students') else 0
        attendance=sub.get("attendace_logs",[])
        unique_section=len(set(log['timestamp'] for log in attendance))
        sub["total_classes"]=unique_section
        sub.pop('subject_students',None)
        sub.pop('attendance_logs',None)

    return subject

def enroll_student_to_subject(student_id,subject_id):
    data={
        'student_id':student_id,'subject_id':subject_id
    }
    responce=supabase.table('subject_students').insert(data).execute()
    return responce.data

def unenroll_student_to_subject(student_id,subject_id):
    responce=supabase.table('subject_students').delete().eq('student_id',student_id).eq('subject_id',subject_id).execute()
    return responce.data


def get_student__subjects(student_id):
    responce=supabase.table('subject_students').select('*,subject(*)').eq('student_id',student_id).execute()
    return responce.data



def get_student_attendace(student_id):
     responce=supabase.table('attendace_logs').select('*,subject(*)').eq('student_id',student_id).execute()
     return responce.data

def create_attendance(attendance_data):
    response=supabase.table('attendace_logs').insert(attendance_data).execute()
    return response.data

def get_all_record_of_attendace(teacher_id):
    response=supabase.table('attendace_logs').select("*,subject!inner(*)").eq('subject.teacher_id',teacher_id).execute()
    return response.data