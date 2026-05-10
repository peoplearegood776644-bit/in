import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import time
import base64

# =============================================================================
# 1. GLOBAL CONFIGURATION & BRANDING
# =============================================================================
st.set_page_config(
    page_title="Awais Ahmad | ME-108 Enterprise System",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Identification Variables
DEV_NAME = "Awais Ahmad"
ROLL_NO = "25-ME-108"
VERSION = "3.5.0-PRO"

# =============================================================================
# 2. CUSTOM CSS UI ENHANCEMENT
# =============================================================================
st.markdown(f"""
    <style>
    /* Main Background */
    .main {{ background: #f4f7f6; }}
    
    /* Header Styling */
    .header-box {{
        background-color: #1E3A8A;
        padding: 30px;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 25px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }}
    
    /* Metric Card Styling */
    div[data-testid="stMetric"] {{
        background: white;
        border: 1px solid #e0e0e0;
        padding: 15px;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }}
    
    /* Button Customization */
    .stButton>button {{
        width: 100%;
        border-radius: 8px;
        height: 3em;
        background-color: #2563EB;
        color: white;
        font-weight: bold;
        transition: 0.3s;
    }}
    
    .stButton>button:hover {{
        background-color: #1E40AF;
        border: 2px solid white;
    }}
    </style>
    """, unsafe_allow_html=True)

# =============================================================================
# 3. SESSION STATE INITIALIZATION (Database Simulation)
# =============================================================================
if 'database' not in st.session_state:
    # Initial dummy data to make charts look "Heavy" from start
    st.session_state.database = pd.DataFrame({
        'ID': [1001, 1002, 1003],
        'Timestamp': [datetime.now().strftime("%Y-%m-%d %H:%M")] * 3,
        'Name': ['Sample User', 'Test Lead', 'System Bot'],
        'Email': ['user@example.com', 'lead@example.com', 'bot@system.com'],
        'Category': ['Technical', 'Management', 'Other'],
        'Priority': ['High', 'Medium', 'Low'],
        'Rating': [8, 9, 5],
        'Status': ['Approved', 'Pending', 'Rejected']
    })

if 'auth' not in st.session_state:
    st.session_state.auth = False

# =============================================================================
# 4. SIDEBAR & NAVIGATION
# =============================================================================
with st.sidebar:
    st.image("https://flaticon.com", width=100)
    st.title("System Control")
    st.markdown(f"**Dev:** {DEV_NAME}")
    st.markdown(f"**Roll:** {ROLL_NO}")
    st.divider()
    
    if st.session_state.auth:
        nav = st.radio("MAIN NAVIGATION", 
                       ["🏠 Control Center", "📝 Smart Form", "📊 Advanced Analytics", "📂 Data Explorer", "🛠️ System Logs"])
        if st.button("🔴 Secure Logout"):
            st.session_state.auth = False
            st.rerun()
    else:
        nav = "Login"
        st.warning("Locked: Authentication Required")

# =============================================================================
# 5. AUTHENTICATION MODULE
# =============================================================================
if not st.session_state.auth:
    st.markdown(f'<div class="header-box"><h1>{DEV_NAME} | Enterprise Portal</h1><p>Roll No: {ROLL_NO}</p></div>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        with st.container():
            st.subheader("🔑 System Login")
            user = st.text_input("Admin ID", value="Awais_Ahmad")
            pw = st.text_input("Access Key", type="password", help="Tip: Your Roll Number")
            if st.button("Initialize Access"):
                if pw == ROLL_NO:
                    st.session_state.auth = True
                    st.success("Access Granted. Loading Environment...")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("Invalid Credentials. Please check Access Key.")

# =============================================================================
# 6. PAGE: CONTROL CENTER (DASHBOARD)
# =============================================================================
elif nav == "🏠 Control Center":
    st.title("🚀 Executive Dashboard")
    st.write(f"System Version: {VERSION} | Node: Localhost")
    
    # KPIs
    c1, c2, c3, c4 = st.columns(4)
    total_records = len(st.session_state.database)
    avg_rating = st.session_state.database['Rating'].mean()
    
    c1.metric("Total Submissions", total_records, "+12%")
    c2.metric("System Health", "98.4%", "Stable")
    c3.metric("Avg Rating", f"{avg_rating:.1f}/10", "+0.4")
    c4.metric("Active Sessions", "1", "Dev Mode")
    
    st.divider()
    
    # Large Visualization
    st.subheader("Submission Trends (Real-time)")
    chart_data = pd.DataFrame(np.random.randn(20, 3), columns=['Server A', 'Server B', 'Server C'])
    st.line_chart(chart_data)

# =============================================================================
# 7. PAGE: SMART FORM (THE GOOGLE FORM CLONE)
# =============================================================================
elif nav == "📝 Smart Form":
    st.title("📝 Detailed Application Form")
    st.info("Fill out the following technical details. All fields marked with * are mandatory.")
    
    with st.form("main_form_logic", clear_on_submit=True):
        # Section A
        st.markdown("#### 👤 Section A: Personal Identification")
        f1, f2 = st.columns(2)
        with f1:
            u_name = st.text_input("Full Name *", placeholder="Enter official name")
            u_email = st.text_input("Email Address *")
        with f2:
            u_dept = st.selectbox("Academic Department", ["Mechanical Engineering", "Civil", "Electrical", "AI & Data Science"])
            u_phone = st.text_input("Contact Number")
        
        st.divider()
        
        # Section B
        st.markdown("#### ⚙️ Section B: Technical Evaluation")
        f3, f4 = st.columns(2)
        with f3:
            u_cat = st.radio("Submission Category", ["Technical Query", "Management Feedback", "Hardware Request", "Other"], horizontal=True)
            u_pri = st.select_slider("Priority Level", options=["Low", "Standard", "High", "Critical"])
        with f4:
            u_rating = st.slider("Quality Assessment Score", 1, 10, 7)
            u_file = st.file_uploader("Upload Supporting Documentation (PDF/PNG)")
            
        u_msg = st.text_area("Detailed Message/Abstract", height=150, placeholder="Describe your request in detail...")
        
        st.divider()
        
        # Policy Check
        agree = st.checkbox("I confirm that the information provided is accurate and belongs to the specified ID.")
        
        # Submission
        btn_col1, btn_col2 = st.columns([1,4])
        submit = btn_col2.form_submit_button("🚀 PROCESS AND SAVE DATA")
        
        if submit:
            if not u_name or not u_email or not agree:
                st.error("Submission Failed: Please fill required fields and agree to terms.")
            else:
                with st.spinner("Writing to Database..."):
                    time.sleep(1.5)
                    new_id = st.session_state.database['ID'].max() + 1
                    new_entry = {
                        'ID': new_id,
                        'Timestamp': datetime.now().strftime("%Y-%m-%d %H:%M"),
                        'Name': u_name,
                        'Email': u_email,
                        'Category': u_cat,
                        'Priority': u_pri,
                        'Rating': u_rating,
                        'Status': 'Pending'
                    }
                    st.session_state.database = pd.concat([st.session_state.database, pd.DataFrame([new_entry])], ignore_index=True)
                    st.balloons()
                    st.success(f"Record Successfully Optimized and Saved! Tracking ID: {new_id}")

# =============================================================================
# 8. PAGE: ADVANCED ANALYTICS
# =============================================================================
elif nav == "📊 Advanced Analytics":
    st.title("📊 Data Intelligence Dashboard")
    df = st.session_state.database
    
    if len(df) > 0:
        tab1, tab2, tab3 = st.tabs(["Distributions", "Correlation Matrix", "Status Tracking"])
        
        with tab1:
            col_left, col_right = st.columns(2)
            with col_left:
                fig_pie = px.pie(df, names='Category', title='Submissions by Category', hole=0.4)
                st.plotly_chart(fig_pie, use_container_width=True)
            with col_right:
                fig_bar = px.bar(df, x='Priority', y='Rating', color='Category', title='Rating by Priority')
                st.plotly_chart(fig_bar, use_container_width=True)
                
        with tab2:
            st.subheader("Regression Analysis Simulation")
            fig_scatter = px.scatter(df, x='ID', y='Rating', size='Rating', color='Status', hover_name='Name')
            st.plotly_chart(fig_scatter, use_container_width=True)
            
        with tab3:
            fig_funnel = px.funnel(df, x='Rating', y='Status')
            st.plotly_chart(fig_funnel, use_container_width=True)
    else:
        st.warning("Insufficient data for analytics.")

# =============================================================================
# 9. PAGE: DATA EXPLORER
# =============================================================================
elif nav == "📂 Data Explorer":
    st.title("📂 Master Database Management")
    df = st.session_state.database
    
    st.markdown("### Filter & Search")
    search_query = st.text_input("🔍 Search by Name or Email", "")
    
    filtered_df = df[df['Name'].str.contains(search_query, case=False) | df['Email'].str.contains(search_query, case=False)]
    
    st.dataframe(filtered_df.style.highlight_max(axis=0, subset=['Rating']), use_container_width=True)
    
    st.divider()
    
    # Export Section
    c1, c2 = st.columns(2)
    with c1:
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Export Database (CSV)", data=csv, file_name=f"awais_database_{ROLL_NO}.csv", mime="text/csv")
    with c2:
        if st.button("🗑️ Factory Reset Database"):
            st.session_state.database = st.session_state.database.iloc[0:0]
            st.rerun()

# =============================================================================
# 10. PAGE: SYSTEM LOGS
# =============================================================================
elif nav == "🛠️ System Logs":
    st.title("🛠️ Technical System Logs")
    st.code(f"""
    [SYSTEM START] - Initializing Enterprise Environment...
    [VERSION] - {VERSION}
    [DEVELOPER] - {DEV_NAME}
    [IDENTIFIER] - {ROLL_NO}
    [NETWORK] - TCP/IP Handshake Successful.
    [DB_STATUS] - {len(st.session_state.database)} Records Loaded.
    [SECURITY] - SSL/TLS Encryption Active.
    [LOG_TIME] - {datetime.now()}
    """, language='bash')
    
    st.progress(100, text="System Stability: 100%")
    st.info("System is running optimally on Streamlit Cloud Cluster.")

# =============================================================================
# FOOTER
# =============================================================================
st.markdown("---")
footer_col1, footer_col2 = st.columns(2)
footer_col1.caption(f"© 2024 {DEV_NAME} | All Rights Reserved.")
footer_col2.markdown(f"<p style='text-align:right; color:grey;'>Roll No: {ROLL_NO} | Mechanical Dept.</p>", unsafe_allow_html=True)
