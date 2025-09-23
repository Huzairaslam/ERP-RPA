import streamlit as st
import requests
import subprocess
import time

# ========================
# 🔹 API Endpoints
# ========================
COUNT_API = "http://api.rabtai.3em.tech/api/Feed/SummarizeRecords"
PROCESS_IDS_API = "http://0.0.0.0:8000/processes/{doc_type}/ids"
PROCESS_DETAIL_API = "http://0.0.0.0:8000/processes/{process_id}"

# ========================
# 🔹 RPA Runner
# ========================
def run_rpa(process_type: str):
    try:
        start_time = time.time()
        rpa_file = f"{process_type.lower().replace(' ', '_')}_flow.robot"

        result = subprocess.run(
            ["robot", rpa_file],
            capture_output=True,
            text=True
        )
        end_time = time.time()
        duration = round(end_time - start_time, 2)

        if result.returncode == 0:
            return f"✅ Success in {duration}s"
        else:
            return f"❌ Failed: {result.stderr}"

    except Exception as e:
        return f"⚠️ Error: {str(e)}"


# ========================
# 🔹 Streamlit Dashboard
# ========================
st.set_page_config(page_title="ERP-RPA Dashboard", layout="wide")
st.title("📊 ERP RPA Dashboard")

try:
    response = requests.get(COUNT_API)
    response.raise_for_status()
    api_response = response.json()

    # Extract data list from API response
    processes = api_response.get("data", [])

    if processes:
        st.subheader("📌 Process Counts")
        st.table([{ "Process": p.get("templateName", "Unknown"), 
                    "Count": p.get("count", 0)} for p in processes])

        for process in processes:
            process_name = process.get("templateName", "Unknown")
            count = int(process.get("count", 0))

            st.metric(label=f"📄 {process_name}", value=count)

            if count > 0:
                with st.expander(f"🔍 {process_name} details", expanded=False):
                    try:
                        ids_resp = requests.get(PROCESS_IDS_API.format(doc_type=process_name))
                        ids_resp.raise_for_status()
                        ids = ids_resp.json()
                    except Exception as e:
                        st.error(f"Could not fetch process IDs: {e}")
                        ids = []

                    for proc in ids:
                        process_id = proc.get("id")
                        st.write(f"📌 Process ID: {process_id}")

                        try:
                            detail_resp = requests.get(PROCESS_DETAIL_API.format(process_id=process_id))
                            detail_resp.raise_for_status()
                            data = detail_resp.json()
                            st.json(data)
                        except Exception as e:
                            st.error(f"Could not fetch details: {e}")
                            data = {}

                        if st.button(f"⚡ Run RPA for {process_name} ({process_id})"):
                            result_msg = run_rpa(process_name)
                            st.success(result_msg)

    else:
        st.info("No processes found.")

except requests.exceptions.RequestException as e:
    st.error(f"API Error: {str(e)}")
except Exception as e:
    st.error(f"Unexpected Error: {str(e)}")












# =============================== OLD CODE =========================================
# import streamlit as st
# import requests
# import subprocess
# import time
# import random
# import pandas as pd

# # ----------------- CONFIG -----------------
# COUNT_API = "http://0.0.0.0:8000/processes"
# st.set_page_config(page_title="ERP Forms Automation", layout="wide")

# # ----------------- CUSTOM CSS -----------------
# st.markdown("""
#     <style>
#         .stApp {
#             background: linear-gradient(135deg, #1e1e2f, #2d2d44);
#             font-family: 'Segoe UI', Tahoma, sans-serif;
#             color: #e0e0e0;
#         }
#         h1, h2, h3, h4 {
#             color: #f5f6fa;
#         }
#         /* Sidebar */
#         section[data-testid="stSidebar"] {
#             background-color: #222233;
#         }
#         section[data-testid="stSidebar"] h2 {
#             color: #00c6ff;
#         }
#         /* Hover effects */
#         .stMetric:hover, .stTable:hover, .streamlit-expanderHeader:hover {
#             transform: scale(1.02);
#             transition: all 0.3s ease-in-out;
#             box-shadow: 0 4px 20px rgba(0,0,0,0.5);
#         }
#         /* Expander styling */
#         .streamlit-expanderHeader {
#             background-color: #33334f !important;
#             color: #f5f6fa !important;
#             border-radius: 5px;
#         }
#     </style>
# """, unsafe_allow_html=True)

# # ----------------- SIDEBAR -----------------
# st.sidebar.title("ERP FORMS AUTOMATION")
# menu = st.sidebar.radio("Navigation", ["📊 Dashboard", "📝 Logs"])

# # ----------------- GLOBAL LOGS LIST -----------------
# if "logs" not in st.session_state:
#     st.session_state["logs"] = []

# def add_log(message):
#     st.session_state["logs"].append(message)

# # ----------------- RPA FUNCTION -----------------
# def run_rpa(document_type):
#     """
#     Trigger your Robot Framework RPA script based on the process name.
#     """
#     if document_type.lower() == "grn":
#         robot_file = "grn_flow.robot"
#     elif document_type.lower() == "purchaseorder":
#         robot_file = "purchase_order_flow.robot"
#     elif document_type.lower() == "purchasebill":
#         robot_file = "purchase_bill_flow.robot"
#     else:

#         # st.warning(f"No RPA configured for {document_type}")
#         return None

#     start_time = time.time()
#     add_log(f"🚀 Starting RPA for {document_type}...")

#     try:
#         subprocess.run(["robot", robot_file], check=True)
#         duration = round(time.time() - start_time, 2)
#         msg = f"✅ {document_type} completed in {duration} seconds"
#         st.success(msg)
#         add_log(msg)
#         return duration
#     except subprocess.CalledProcessError as e:
#         duration = round(time.time() - start_time, 2)
#         msg = f"❌ {document_type} failed after {duration} seconds: {e}"
#         st.error(msg)
#         add_log(msg)
#         return None

# # ----------------- DASHBOARD -----------------
# if menu == "📊 Dashboard":
#     st.title("📊 RPA Process Dashboard")

#     try:
#         resp = requests.get(COUNT_API)
#         resp.raise_for_status()
#         processes = resp.json()
#     except Exception as e:
#         st.error(f"Failed to fetch data: {e}")
#         processes = []

#     if processes:
#         st.subheader("📌 Process Counts")
#         st.table(processes)

#         # Metric cards
#         cols = st.columns(len(processes))
#         durations = {}  # store execution times

#         for idx, process in enumerate(processes):
#             document_type = process.get("document_type", "Unknown")
#             count = int(process.get("count", 0))

#             with cols[idx]:
#                 st.metric(label=f"📄 {document_type}", value=count)

#         # Detailed expanders + run automation
#         for process in processes:
#             document_type = process.get("document_type", "Unknown")
#             count = int(process.get("count", 0))

#             if count > 0:
#                 with st.expander(f"🔍 {document_type} details", expanded=False):
#                     detail_resp = requests.get(f"http://0.0.0.0:8000/dummy_invoice")
#                     detail_resp.raise_for_status()
#                     data = detail_resp.json()
#                     st.json(data)

#                 st.info(f"⚡ Running automation for {document_type}...")
#                 duration = run_rpa(document_type)
#                 if duration:
#                     durations[document_type] = duration

#         # Show graph of process durations
#         if durations:
#             st.subheader("⏱️ Process Execution Time")
#             df = pd.DataFrame(list(durations.items()), columns=["Process", "Duration (s)"])
#             st.bar_chart(df.set_index("Process"))
#     else:
#         st.warning("⚠️ No process data available.")

# # ----------------- LOGS TAB -----------------
# elif menu == "📝 Logs":
#     st.title("📝 Automation Logs")
#     if st.session_state["logs"]:
#         for log in st.session_state["logs"][::-1]:
#             st.write(log)
#     else:
#         st.info("No logs available yet.")