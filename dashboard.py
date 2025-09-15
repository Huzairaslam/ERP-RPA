import streamlit as st
import requests
import subprocess

# API endpoints
COUNT_API = "http://0.0.0.0:8000/processes"  
st.set_page_config(page_title="RPA Dashboard", layout="wide")
st.title("📊 RPA Process Dashboard")

def run_rpa(document_type):
    """
    Trigger your Robot Framework RPA script based on the process name.
    Adjust the robot file names as per your setup.
    """
    if document_type.lower() == "po":
        robot_file = "po_flow.robot"
    elif document_type.lower() == "purchasebill":
        robot_file = "bill_flow.robot"
    elif document_type.lower() == "GRN":
        robot_file = "grn_flow.robot"
    else:
        st.warning(f"No RPA configured for {document_type}")
        return
    
    st.info(f"🚀 Starting RPA for {document_type}...")
    try:
        subprocess.run(["robot", robot_file], check=True)
        st.success(f"✅ RPA for {document_type} completed successfully!")
    except subprocess.CalledProcessError as e:
        st.error(f"❌ Failed to run RPA for {document_type}: {e}")

# Fetch process counts
try:
    resp = requests.get(COUNT_API)
    resp.raise_for_status()
    processes = resp.json()
except Exception as e:
    st.error(f"Failed to fetch data: {e}")
    processes = []

# Show table of counts
if processes:
    st.subheader("Process Counts")
    st.table(processes)

    for process in processes:
        document_type = process.get("document_type", "Unknown")
        count = int(process.get("count", 0))

        if count > 0:
            with st.expander(f"🔍 {document_type} details"):
                detail_resp = requests.get(f"http://0.0.0.0:8000/dummy_invoice")
                detail_resp.raise_for_status()
                data = detail_resp.json()
                st.json(data)
            st.info(f"⚡ Auto-running RPA for {document_type} (count increases)")
            run_rpa(document_type)
else:
    st.warning("No process data available.")
