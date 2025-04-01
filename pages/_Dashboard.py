import streamlit as st
from website.dbconn import cursor, dbconn

st.set_page_config(page_title="Dashboard", layout="wide")

# --- STYLES ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;700&display=swap');

    body {
        background-color: #fefbe9;
        font-family: 'DM Sans', sans-serif;
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

    .dashboard-title {
        font-size: 36px;
        font-weight: bold;
        color: white;
        font-family: 'DM Sans', sans-serif;
        margin-top: 2rem;
        margin-left: 2rem;
    }

    .card-title {
        font-size: 20px;
        font-weight: bold;
        color: white;
        margin-bottom: 10px;
        font-family: 'DM Sans', sans-serif;
        background-color: #1A1A70;
        padding: 0.5rem 1rem;
        border-radius: 8px 8px 0 0;
        text-align: center;
    }

    .card-container {
        background-color: #f2e8cf;
        padding: 0;
        border-radius: 12px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.08);
        overflow: hidden;
        height: 100%;
    }

    .progress-labels {
      display: flex;
      justify-content: space-between;
      font-size: 14px;
      color: white;
      font-weight: bold;
      margin-top: 6px;
      padding: 0 1rem;
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
nav_col1, nav_col2 = st.columns([6, 1])
with nav_col1:
    st.markdown(
        "<div style='background-color:#1A1A70; padding:1rem 2rem; font-family:DM Sans; font-size:24px; color:white; font-weight:bold;'>"
        "SMU Feedback Hub</div>",
        unsafe_allow_html=True
    )
with nav_col2:
    st.image("assets/smu.png", width=200)


# --- HEADER ---
st.markdown('<div class="dashboard-title">Student Performance Dashboard</div>', unsafe_allow_html=True)

# --- CHART CARDS ---
chart_cards = [
    ("Average Student Score by Course", "assets/course.png"),
    ("Average Student Score by Group", "assets/barbygroup.png"),
    ("Average Student Score by Evaluation Category", "assets/evaluationcat.png"),
    ("Improvements Over Time", "assets/improvements.svg"),
    ("Peer Comparison", "assets/boxplot.png"),
    ("Total Peer Evaluations", None)  # We'll handle progress bar separately
]

# Rowed layout: 3 cards per row
for i in range(0, len(chart_cards), 3):
    row = chart_cards[i:i+3]
    cols = st.columns(3)
    for col, (title, img_path) in zip(cols, row):
        with col:
            st.markdown('<div class="card-container">', unsafe_allow_html=True)
            st.markdown(f'<div class="card-title">{title}</div>', unsafe_allow_html=True)
            if img_path:
                st.image(img_path, use_container_width=True)
            else:
                # Progress bar card
                st.markdown("<div style='padding: 1rem;'>", unsafe_allow_html=True)
                st.markdown("**5 out of 9 Completed**")
                st.markdown('<div class="progress-labels"><div>Completed</div><div>Incomplete</div></div>', unsafe_allow_html=True)
                st.progress(5 / 9)
                st.markdown("</div>", unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

# --- NAV BUTTONS ---
col_left, col_right = st.columns(2)
with col_left:
    if st.button("Return to Peer Review Portal"):
        st.switch_page("pages/_Portal.py")
with col_right:
    if st.button("Logout"):
        st.session_state.userID = None
        st.switch_page("pages/_Login.py")
