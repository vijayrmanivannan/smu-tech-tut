import streamlit as st
from website.dbconn import dbconn, cursor
from datetime import date

st.set_page_config(page_title="Peer Evaluation", layout="wide")

# --- Get assignment data from session ---
assignment_id = st.session_state.get("assignment_id")
course_name = st.session_state.get("course_name")
professor_name = st.session_state.get("professor_name")

if not assignment_id or not course_name or not professor_name:
    st.warning("No assignment selected. Please return to the Portal.")
    st.stop()

# --- Get logged-in user info ---
userID = st.session_state.get("userID", None)
if not userID:
    st.warning("Please log in first.")
    st.stop()

cursor.execute("SELECT name FROM Student WHERE student_id = %s", (userID,))
student_name = cursor.fetchone()["name"]

# --- STYLE ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;700&family=Source+Sans+3:wght@400;700&display=swap');

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

    .form-container {
        border: 1px solid #ccc;
        border-radius: 12px;
        padding: 2rem;
        max-width: 1000px;
        margin: auto;
        background-color: white;
    }

    .form-title {
        font-family: 'DM Sans', sans-serif;
        font-size: 32px;
        font-weight: 700;
        text-align: center;
        margin-bottom: 10px;
    }

    .subtext {
        text-align: center;
        font-family: Calibri, sans-serif;
        font-size: 20px;
        margin-bottom: 2rem;
    }

    .category-label {
        font-family: 'DM Sans', sans-serif;
        font-size: 20px;
        font-weight: 600;
        margin-top: 1rem;
    }

    .stRadio > div { font-family: Calibri, sans-serif; font-size: 15px; }

    .stButton>button {
        background-color: #1A1A70;
        color: white;
        font-family: 'DM Sans', sans-serif;
        font-size: 16px;
        padding: 10px 24px;
        border-radius: 6px;
        margin-top: 1.5rem;
        border: none;
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


# --- FORM HEADER ---
st.markdown('<div class="form-container">', unsafe_allow_html=True)
st.markdown('<div class="form-title">Peer Evaluation Form</div>', unsafe_allow_html=True)
st.markdown(f'<div class="subtext">{course_name}<br>{professor_name}</div>', unsafe_allow_html=True)

# --- Completed By ---
completed_by = st.selectbox("Completed By:", [student_name])

# --- Student Being Evaluated ---
cursor.execute("SELECT student_id, name FROM Student WHERE student_id != %s", (userID,))
peers = cursor.fetchall()
peer_options = {f"{p['name']} (ID {p['student_id']})": p["student_id"] for p in peers}
evaluatee_label = st.selectbox("Student being evaluated:", list(peer_options.keys()))
evaluatee_id = peer_options[evaluatee_label]

# --- Evaluation Criteria ---
categories = {
    "Disciplinary Knowledge": "dk",
    "Multidisciplinary Knowledge": "mk",
    "Innovative/Entrepreneurial Skills": "ies",
    "Collaboration/Leadership": "cl",
    "Communication": "com",
    "Intercultural Understanding/Sensitivity": "ius",
    "Sensitivity Towards Developments in Asia": "asia",
    "Ethical/Social Responsibility": "esr",
    "Self Directedness/Meta–Learning": "meta",
    "Resilience/Positivity": "rp"
}

scale = ["Never", "Sometimes", "Usually", "Regularly", "Always"]
responses = {}

for label, key in categories.items():
    st.markdown(f'<div class="category-label">{label}</div>', unsafe_allow_html=True)
    responses[key] = st.radio("", scale, horizontal=True, key=label)

# --- Submission ---
if st.button("Submit"):
    # Convert scale to numeric
    scale_map = {v: i+1 for i, v in enumerate(scale)}
    numeric_scores = [scale_map[val] for val in responses.values()]
    avg_score = sum(numeric_scores) / len(numeric_scores)

    # Get new evaluation ID
    cursor.execute("SELECT evaluation_id FROM Peer_Evaluation ORDER BY evaluation_id DESC LIMIT 1")
    last = cursor.fetchone()
    evaluation_id = last["evaluation_id"] + 1 if last else 1

    self_eval = (evaluatee_id == userID)

    # Insert into Peer_Evaluation table
    cursor.execute("""
        INSERT INTO Peer_Evaluation (
            evaluation_id, evaluator_id, evaluatee_id, assignment_id,
            date_submitted, self_evaluation
        ) VALUES (%s, %s, %s, %s, %s, %s)
    """, (evaluation_id, userID, evaluatee_id, assignment_id, date.today(), self_eval))

    dbconn.commit()

    # Save summary data for _Confirmation.py
    st.session_state.submission_summary = {
        "evaluator_name": student_name,
        "evaluatee_id": evaluatee_id,
        "assignment_id": assignment_id,
        "avg_score": avg_score,
        "date": date.today().strftime('%Y-%m-%d')
    }

    # Redirect to confirmation page
    st.switch_page("pages/_Confirmation.py")

   

    dbconn.commit()

    # --- Admin View Output ---
    st.success("✅ Evaluation submitted!")

    cursor.execute("SELECT name FROM Student WHERE student_id = %s", (evaluatee_id,))
    evaluatee_name = cursor.fetchone()["name"]

    st.markdown("### 🧾 Submission Summary (Admin View)")
    st.markdown(f"""
    - **Evaluator:** {student_name}  
    - **Evaluatee:** {evaluatee_name}  
    - **Assignment ID:** {assignment_id}  
    - **Average Score:** {avg_score:.2f}  
    - **Date Submitted:** {date.today().strftime('%Y-%m-%d')}
    """)

    st.info("This section is for demo purposes.")


if st.button("Reset"):
    st.rerun()

st.markdown('</div>', unsafe_allow_html=True)
