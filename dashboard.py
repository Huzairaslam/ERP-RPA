import streamlit as st
import requests
import subprocess

# API endpoints
COUNT_API = "https://example.com/api/count"  # Replace with your actual API

st.set_page_config(page_title="RPA Dashboard", layout="wide")
st.title("📊 RPA Process Dashboard")

def run_rpa(process_name):
    """
    Trigger your Robot Framework RPA script based on the process name.
    Adjust the robot file names as per your setup.
    """
    if process_name.lower() == "po":
        robot_file = "po_flow.robot"
    elif process_name.lower() == "invoice":
        robot_file = "invoice_flow.robot"
    else:
        st.warning(f"No RPA configured for {process_name}")
        return
    
    st.info(f"Starting RPA for {process_name}...")
    try:
        # Run the robot file
        subprocess.run(["robot", robot_file], check=True)
        st.success(f"RPA for {process_name} completed successfully!")
    except subprocess.CalledProcessError as e:
        st.error(f"Failed to run RPA for {process_name}: {e}")

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

    # Check and optionally run RPA
    for process in processes:
        count = int(process.get("count", 0))
        if count > 0:
            with st.expander(f"🔍 {process['name']} details"):
                try:
                    detail_resp = requests.get(process["endpoint"])
                    detail_resp.raise_for_status()
                    data = detail_resp.json()
                    st.json(data)
                    
                    # Button to run RPA for this process
                    if st.button(f"▶ Run RPA for {process['name']}"):
                        run_rpa(process["name"])
                except Exception as e:
                    st.error(f"Failed to fetch detail data: {e}")
else:
    st.warning("No process data available.")