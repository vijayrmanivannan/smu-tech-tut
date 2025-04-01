import streamlit as st
from website.dbconn import dbconn, cursor

st.set_page_config(page_title="Login", layout="centered")

# ---- STYLES ----
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


st.markdown('<h1 class="main-title">Login</h1>', unsafe_allow_html=True)

email = st.text_input("Enter your SMU email address")
password = st.text_input("Enter your password", type="password")

col1, col2 = st.columns([1, 2])
with col1:
    st.markdown("[Forgot password?](#)")

if st.button("Login"):
    if not email or not password:
        st.error("Please fill in both fields.")
    else:
        cursor.execute("SELECT student_id FROM Student WHERE email = %s AND password = %s", (email, password))
        result = cursor.fetchone()
        if result:
            st.session_state.userID = result["student_id"]
            st.success("Login successful!")
            st.switch_page("pages/_Portal.py")
        else:
            st.error("Invalid email or password.")
