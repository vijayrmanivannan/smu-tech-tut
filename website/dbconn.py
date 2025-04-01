import pymysql
import streamlit as st

try:
    dbconn = pymysql.connect(
        host=st.secrets["db_host"],
        port=int(st.secrets.get("db_port", 3306)),
        user=st.secrets["db_user"],
        password=st.secrets["db_pass"],
        database=st.secrets["db_name"],
        cursorclass=pymysql.cursors.DictCursor
    )
    cursor = dbconn.cursor()
except Exception as e:
    st.error("❌ Could not connect to the database.")
    st.stop()
    
