import streamlit as st

st.set_page_config(page_title="SMU Feedback Hub", layout="centered")

# ---- STYLE ----
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;700&display=swap');

    body {
        background-color: white;
    }

    .nav-bar {
        background-color: #1A1A70;
        padding: 1rem 2rem;
        color: white;
        font-family: 'DM Sans', sans-serif;
        font-size: 22px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .title-text {
        font-family: 'DM Sans', sans-serif;
        font-size: 36px;
        font-weight: 700;
        text-align: center;
        margin-top: 4rem;
    }

    .description {
        font-family: 'DM Sans', sans-serif;
        font-size: 18px;
        font-weight: 400;
        text-align: center;
        max-width: 700px;
        margin: 1.5rem auto;
        color: white;
    }

    .stButton>button {
        background-color: #1A1A70;
        color: white;
        font-family: 'DM Sans', sans-serif;
        font-size: 16px;
        padding: 10px 24px;
        border-radius: 6px;
        border: none;
        display: block;
        margin: 0 auto;
    }
    </style>
""", unsafe_allow_html=True)

# ---- NAV BAR ----
# --- NAV BAR ---
nav_col1, nav_col2 = st.columns([6, 1])
with nav_col1:
    st.markdown(
        "<div style='background-color:#1A1A70; padding:1rem 2rem; font-family:DM Sans; font-size:24px; color:white; font-weight:bold;'>"
        "SMU Feedback Hub</div>",
        unsafe_allow_html=True
    )
with nav_col2:
    st.image("assets/smu.png", width=250)


# ---- MAIN CONTENT ----
st.markdown('<div class="title-text">Welcome to the SMU Feedback Hub</div>', unsafe_allow_html=True)

st.markdown("""
    <div class="description">
        This portal allows students to submit peer evaluations, track assignment progress,
        and contribute to collaborative learning in SMU courses. Use the sidebar to access the login page and get started.
    </div>
""", unsafe_allow_html=True)

# ---- OPTIONAL LOGIN BUTTON ----
if "userID" not in st.session_state or st.session_state.userID is None:
    if st.button("Go to Login"):
        st.switch_page("pages/_Login.py")
else:
    st.success(f"You're logged in as Student ID: {st.session_state.userID}")
    if st.button("Go to Portal"):
        st.switch_page("pages/_Portal.py")

from website.dbconn import dbconn, cursor

st.subheader(" Database Connection Test")

try:
    cursor.execute("SELECT COUNT(*) AS total FROM Student")
    result = cursor.fetchone()
    st.success(f"Connected! Student table has {result['total']} record(s).")
except Exception as e:
    st.error("❌ Database connection failed.")
    st.exception(e)

        