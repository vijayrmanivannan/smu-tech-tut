import streamlit as st
from website.dbconn import cursor

st.set_page_config(page_title="Confirmation", layout="centered")

# --- STYLES ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;700&display=swap');

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

    .confirm-msg {
        font-family: 'DM Sans', sans-serif;
        font-size: 26px;
        font-weight: 500;
        text-align: center;
        margin-top: 3rem;
    }

    .admin-summary {
        background-color: #f3f3f3;
        border-radius: 12px;
        padding: 1.5rem;
        font-family: Calibri, sans-serif;
        font-size: 17px;
        margin-top: 2rem;
    }

    .stButton>button {
        background-color: #1A1A70;
        color: white;
        font-family: 'DM Sans', sans-serif;
        font-size: 16px;
        padding: 10px 24px;
        border-radius: 6px;
        border: none;
        margin-top: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# --- NAV BAR ---
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

# --- Confirmation Message ---
st.markdown('<div class="confirm-msg">Your peer evaluation has been submitted.</div>', unsafe_allow_html=True)

# --- Admin View Summary ---
summary = st.session_state.get("submission_summary")

if summary:
    cursor.execute("SELECT name FROM Student WHERE student_id = %s", (summary["evaluatee_id"],))
    evaluatee_name = cursor.fetchone()["name"]

    st.markdown("###  Submission Summary")

    st.markdown(f"""
    <div style="
        background-color: #f4f4f4;
        border-radius: 12px;
        padding: 1.5rem 2rem;
        font-family: 'DM Sans', sans-serif;
        font-size: 16px;
        color: #1A1A1A;
        margin-top: 1rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        line-height: 1.7;
    ">
        <strong>Evaluator:</strong> {summary["evaluator_name"]}<br>
        <strong>Evaluatee:</strong> {evaluatee_name}<br>
        <strong>Assignment ID:</strong> {summary["assignment_id"]}<br>
        <strong>Average Score:</strong> {summary["avg_score"]:.2f}<br>
        <strong>Date Submitted:</strong> {summary["date"]}
    </div>
    """, unsafe_allow_html=True)
# --- Buttons ---
col1, col2 = st.columns(2)
with col1:
    if st.button("Return to Portal"):
        st.switch_page("pages/_Portal.py")

with col2:
    if st.button("Log Out"):
        st.session_state.userID = None
        st.success("You have been logged out.")
        st.switch_page("pages/_Login.py")
