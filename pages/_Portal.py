import streamlit as st
from website.dbconn import dbconn, cursor

st.set_page_config(page_title="Portal", layout="wide")

# ---- STYLES ----
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;700&display=swap');

    body { background-color: white; }

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

    .page-title {
        font-family: 'DM Sans', sans-serif;
        font-size: 36px;
        font-weight: 700;
        margin-top: 2rem;
        color: #1A1A1A;
    }

    .card {
        background-color: #ffffff;
        border: 1px solid #ccc;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        font-family: 'DM Sans', sans-serif;
        height: 280px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
    }

    .card-title {
        font-weight: bold;
        font-size: 18px;
        color: #1A1A1A;
    }

    .card-sub {
        font-size: 16px;
        color: #333333;
    }

    .card-deadline {
        font-weight: 600;
        color: #555555;
        margin-top: 10px;
    }

    .stButton>button {
        background-color: #1A1A70;
        color: white;
        font-family: 'DM Sans', sans-serif;
        font-size: 16px;
        padding: 8px 24px;
        border-radius: 6px;
        border: none;
        margin-top: 10px;
        transition: background-color 0.3s ease;
    }

    .stButton>button:hover {
        background-color: #2d2db3;
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
    st.image("assets/smu.png", width=200)


# ---- HEADER ----
st.markdown('<div class="page-title">Peer Review Portal</div>', unsafe_allow_html=True)

# ---- Logged-in User Check ----
userID = st.session_state.get("userID", None)

if not userID:
    st.warning("Please log in first.")
    st.stop()

# ---- Get Assignments for Student ----
cursor.execute('''
    SELECT 
        c.course_name, 
        a.assignment_id, 
        a.deadline, 
        co.semester, 
        co.year, 
        p.name AS professor_name
    FROM Course c
    JOIN Course_Offering co ON c.course_id = co.course_id
    JOIN Professor p ON co.professor_id = p.professor_id
    JOIN Assignment a ON co.offering_id = a.offering_id
    WHERE a.student_id = %s
''', (userID,))
assignments = cursor.fetchall()
if not assignments:
    st.info("You currently have no assignments to evaluate.")
    st.stop()

# ---- De-duplicate Cards ----
seen = set()
unique_assignments = []
for row in assignments:
    card_id = (row["course_name"], row["professor_name"], row["semester"], row["year"])
    if card_id not in seen:
        unique_assignments.append(row)
        seen.add(card_id)

# ---- Render Cards ----
cols = st.columns(3)
for i, row in enumerate(unique_assignments):
    with cols[i % 3]:
        st.markdown(f"""
            <div class="card">
                <div class="card-title">Course<br>{row['course_name']}</div>
                <div class="card-sub">{row['professor_name']}<br>{row['semester']} {row['year']}</div>
                <div class="card-deadline">Deadline: {row['deadline'].strftime("%Y-%m-%d %H:%M:%S")}</div>
            </div>
        """, unsafe_allow_html=True)

        if st.button("Go", key=f"go_{row['assignment_id']}_{i}"):
            st.session_state.assignment_id = row["assignment_id"]
            st.session_state.course_name = row["course_name"]
            st.session_state.professor_name = row["professor_name"]
            st.switch_page("pages/_Peer_Evaluation.py")
