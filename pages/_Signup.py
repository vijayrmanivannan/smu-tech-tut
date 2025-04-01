import streamlit as st
from website.dbconn import dbconn, cursor

st.set_page_config(page_title="Sign Up", layout="centered")

# --- STYLES ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;700&display=swap');
    body { background-color: white; }
    .nav-bar {
        background-color: #1A1A70; padding: 1rem 2rem; color: white;
        font-family: 'DM Sans', sans-serif; font-size: 22px;
        display: flex; justify-content: space-between; align-items: center;
    }
    .main-title {
        font-family: 'DM Sans', sans-serif; font-size: 34px;
        font-weight: 700; text-align: center; margin-top: 2rem;
    }
    .stTextInput>div>div>input { font-family: Calibri, sans-serif; }
    .stButton>button {
        font-family: 'DM Sans', sans-serif;
        background-color: #1A1A70; color: white;
        padding: 10px 24px; border-radius: 6px; font-size: 16px;
        border: none; font-weight: 500; margin-top: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# --- NAV BAR ---
nav_col1, nav_col2 = st.columns([6, 1])
with nav_col1:
    st.markdown(
        "<div style='background-color:#1A1A70; padding:1rem 2rem; font-family:DM Sans; font-size:24px; color:white; font-weight:bold;'>"
        "SMU Feedback Hub</div>",
        unsafe_allow_html=True
    )
with nav_col2:
    st.image("assets/smu.png", width=200)


st.markdown('<h1 class="main-title">Create an Account</h1>', unsafe_allow_html=True)

name = st.text_input("Full Name")
email = st.text_input("SMU Email")
password = st.text_input("Password", type="password")
confirm = st.text_input("Confirm Password", type="password")

if st.button("Register"):
    if not name or not email or not password or not confirm:
        st.error("Please fill in all fields.")
    elif password != confirm:
        st.error("Passwords do not match.")
    else:
        cursor.execute("SELECT student_id FROM Student ORDER BY student_id DESC LIMIT 1")
        last = cursor.fetchone()
        new_id = last["student_id"] + 1 if last else 1

        cursor.execute(
            "INSERT INTO Student (student_id, name, email, password) VALUES (%s, %s, %s, %s)",
            (new_id, name, email, password)
        )
        dbconn.commit()
        st.success("Account created! Please log in.")
        st.switch_page("pages/_Login.py")
