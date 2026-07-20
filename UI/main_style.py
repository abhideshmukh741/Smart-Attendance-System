import streamlit as st 

def main_style():
    st.markdown(
         """
        <style>
           .stApp {
                background-color:#0B1120 !important;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                color: #E0E0E0 !important;
            }
             #MAinMenu,footer,header{
                 visibility: hidden;
            }
            
            </style>
            """,
            unsafe_allow_html=True  )  


def style_bag_home():
    st.markdown(
        """
        <style>
            section.main > div {
           padding-top: 1rem;
           }
        .stApp {
            background-color: #0B1120 !important;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            color: #E0E0E0 !important;
            }
        h1 {
            color: #E0E0E0 !important;
            text-align: center !important;
            font-size: 50px !important;
            margin-bottom: 100px !important;
            margin-top: 0px !important;
            }
        img {
            display: block;
            margin-left: auto;
            margin-right: auto;
            width: 50%;
            margin-bottom: 50px !important;
            }

        .stButton > button {
            background-color: #38BDF8;
            color: white;
            border: none;
            padding: 12px 20px;
            font-size: 16px;
            cursor: pointer;
            border-radius: 10px;
            width: 100%;
            transition: 0.3s;
            }
        .stButton > button:hover {
            background-color: #0EA5E9;
            transform: scale(1.03);
            }
        
            #MainMenu,footer,header{
        visibility: hidden;
        }

        .stApp div[data-testid="stColumn"]{
        background-color: #E0E3FF;
        border-radius: 20px;
        padding: 12px 20px;}
            </style>
            """,
            unsafe_allow_html=True)


def teacher_style():

    st.markdown("""
    <style>

    
    .stApp{
        background-color:#EAB308;
        font-family: 'Segoe UI', sans-serif;
    }

    #MainMenu, footer, header{
        visibility:hidden;
    }

  
    .main-title{
        text-align:center;
        font-size:42px;
        font-weight:bold;
        color:white;
        margin-bottom:40px;
    }


    .card-box{
        background-color:#E9E9FF;
        padding:30px;
        border-radius:25px;
        height:250px;
        box-shadow:0px 4px 15px rgba(0,0,0,0.15);
        margin-bottom:15px;
    }

   
    .card-title{
        font-size:32px;
        font-weight:bold;
        color:black;
        line-height:1.4;
        margin-bottom:20px;
    }

    
    .card-text{
        font-size:18px;
        color:#444;
    }

  
    div[data-testid="stButton"] button[kind="secondary"]{
        background-color:#6366F1 !important;
        color:white !important;
        border:none !important;
        border-radius:14px !important;
        height:55px !important;
        font-size:18px !important;
        font-weight:bold !important;
        transition:0.3s !important;
    }

    div[data-testid="stButton"] button[kind="secondary"]:hover{
        background-color:#4F46E5 !important;
        transform:scale(1.02);
    }
   button[kind="tertiary"] {
        background: #06B6D4 !important;
        color: white !important;
        border: none !important;
        border-radius: 14px !important;
        padding: 12px 24px !important;
        font-size: 18px !important;
        font-weight: bold !important;
        height: 55px !important;
        box-shadow: 0px 4px 12px rgba(79, 70, 229, 0.35) !important;
        transition: all 0.3s ease-in-out !important;
}


button[kind="tertiary"]:hover {
    background: linear-gradient(135deg, #4F46E5, #3730A3) !important;
    transform: translateY(-3px) scale(1.02);
    box-shadow: 0px 8px 18px rgba(79, 70, 229, 0.45) !important;
}


button[kind="tertiary"]:active {
    transform: scale(0.98);
}

    </style>
    """, unsafe_allow_html=True)
            
def header_style_teacher():

    st.markdown("""
    <style>

    .home-btn button {

        background-color:#EF4444 !important;
        color:white !important;

        border:none !important;
        border-radius:14px !important;

        padding:12px 24px !important;

        font-size:18px !important;
        font-weight:600 !important;

        height:55px !important;

        box-shadow:0px 4px 10px rgba(0,0,0,0.15) !important;

        transition:0.3s ease-in-out !important;
    }

    .home-btn button:hover {

        background-color:#DC2626 !important;

        transform:scale(1.05);

        box-shadow:0px 6px 14px rgba(0,0,0,0.25) !important;
    }

    </style>
    """, unsafe_allow_html=True)



def header_style_student():

    st.markdown("""
    <style>

    .home-btn button {

        background-color:#EF4444 !important;
        color:white !important;

        border:none !important;
        border-radius:14px !important;

        padding:12px 24px !important;

        font-size:18px !important;
        font-weight:600 !important;

        height:55px !important;

        box-shadow:0px 4px 10px rgba(0,0,0,0.15) !important;

        transition:0.3s ease-in-out !important;
    }

    .home-btn button:hover {

        background-color:#DC2626 !important;

        transform:scale(1.05);

        box-shadow:0px 6px 14px rgba(0,0,0,0.25) !important;
    }

    </style>
    """, unsafe_allow_html=True)


def student_style():
        st.markdown("""
    <style>
        .stApp{
       background-color:#edc5e5 !important;
        font-family: 'Segoe UI', sans-serif;
        color: black !important;
        }   
     #MainMenu, footer, header{
        visibility:hidden;
    }  
    .main-title{
        text-align:center;
        font-size:42px;
        font-weight:bold;
        color:black !important;
        margin-bottom:40px;
    }
    [data-testid="stCameraInput"] button {
    background-color: #06B6D4 !important;
    color: white !important;
    border-radius: 12px !important;
    border: none !important;
    padding: 10px 20px !important;
    font-size: 16px !important;
    font-weight: bold !important;
}
     div[data-testid="stButton"] button[kind="secondary"]{
        background-color:#6366F1 !important;
        color:white !important;
        border:none !important;
        border-radius:14px !important;
        height:55px !important;
        font-size:18px !important;
        font-weight:bold !important;
        transition:0.3s !important;
    }
                    
    div[data-testid="stButton"] button[kind="secondary"]:hover{
        background-color:#4F46E5 !important;
        transform:scale(1.02);
    }

 button[kind="tertiary"] {
        background: #06B6D4 !important;
        color: white !important;
        border: none !important;
        border-radius: 14px !important;
        padding: 12px 24px !important;
        font-size: 18px !important;
        font-weight: bold !important;
        height: 55px !important;
        box-shadow: 0px 4px 12px rgba(79, 70, 229, 0.35) !important;
        transition: all 0.3s ease-in-out !important;
}                    
[data-testid="stCameraInput"] button:hover {
    background-color: #0891B2 !important;
    transform: scale(1.03);
    transition: 0.3s;
}
button[kind="tertiary"]:hover {
    background: linear-gradient(135deg, #4F46E5, #3730A3) !important;
    transform: translateY(-3px) scale(1.02);
    box-shadow: 0px 8px 18px rgba(79, 70, 229, 0.45) !important;
}


button[kind="tertiary"]:active {
    transform: scale(0.98);
}

    </style>
    """, unsafe_allow_html=True)
    