import streamlit as st
import requests

# API endpoints (you can reuse the same as in data.robot)
COUNT_API = "https://example.com/api/count"

st.set_page_config(page_title="RPA Dashboard", layout="wide")
st.title("📊 RPA Process Dashboard")

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

    # Expand to show details
    for process in processes:
        if int(process.get("count", 0)) > 0:
            with st.expander(f"🔍 {process['name']} details"):
                try:
                    detail_resp = requests.get(process["endpoint"])
                    detail_resp.raise_for_status()
                    st.json(detail_resp.json())
                except Exception as e:
                    st.error(f"Failed to fetch detail data: {e}")
else:
    st.warning("No process data available.")