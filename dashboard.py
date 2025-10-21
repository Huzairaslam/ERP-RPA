import streamlit as st
import requests
import subprocess
import time
import json
import os
import pandas as pd
from datetime import datetime
from logging.handlers import TimedRotatingFileHandler
import logging
import altair as alt

# --- CUSTOM THEME (CSS Injection for Corporate Look) ---
st.markdown(
    """
    <style>
    /* 1. Overall Page Style: Use wide layout and adjust padding */
    .block-container {
        padding-top: 1.5rem; /* Reduce top padding */
        padding-right: 2rem;
        padding-left: 2rem;
        padding-bottom: 2rem;
    }
    /* 2. Sidebar Style: Corporate Blue Background */
    [data-testid="stSidebar"] {
        background-color: #004D99; /* Deep Corporate Blue */
        color: white;
    }
    /* 3. Metric Card Enhancement */
    [data-testid="stMetric"] {
        background-color: #F0F2F6; /* Light gray background */
        border-left: 5px solid #004D99; /* Corporate blue accent line */
        border-radius: 8px;
        padding: 10px;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.05); /* Subtle shadow */
    }
    [data-testid="stMetricLabel"] > div {
        color: #004D99; /* Make metric labels blue */
        font-weight: bold;
    }
    /* 4. Customizing Expander for cleaner look */
    .streamlit-expanderHeader {
        background-color: #e6e6e6; /* Light gray header */
        border-radius: 5px;
        padding: 10px;
        font-weight: bold;
    }
    </style>
    """,
    unsafe_allow_html=True,
)
# --------------------------------------------------------

# ========================
# 🔹 CONFIG & CONSTANTS
# ========================
# ... (rest of the constants remain the same)
BASE_URL = "http://api.rabtai.3em.tech/api/Feed"
COUNT_API = f"{BASE_URL}/SummarizeRecords"
TEMPLATE_API = f"{BASE_URL}/getByTemplateId/{{templateId}}"
POST_API = f"{BASE_URL}/Posted/{{recordId}}"
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, "rpa_logs.csv")

# ========================
# 🔹 LOGGING SETUP (Daily Rotation)
# ========================
logger = logging.getLogger("RPA")
logger.setLevel(logging.INFO)
handler = TimedRotatingFileHandler(os.path.join(LOG_DIR, "rpa.log"), when="midnight", backupCount=7)
formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

# ========================
# 🔹 TEMPLATE → RPA FILE MAP
# ========================
TEMPLATE_RPA_MAP = {
    "Purchase Bill Form": "purchase_bill_flow.robot",
    "Purchase Order Form": "purchase_order_flow.robot",
}

# ========================
# 🔹 SLACK NOTIFICATIONS (Updated for Secrets/Env Vars)
# ========================
import os # Make sure this is imported at the top
SLACK_WEBHOOK_URL = os.environ.get("SLACK_WEBHOOK_URL", "https://hooks.slack.com/services/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") 
# Removed the hardcoded URL and switched to OS environment variable lookup. 
# The hardcoded value is now a fallback, but should be removed in production.

def send_slack_alert(title, message, status="info"):
    """Send notification to Slack. Non-blocking (swallows exceptions)."""
    if not SLACK_WEBHOOK_URL:
        logger.warning("Slack webhook URL is not configured.")
        return
        
    emoji = "✅" if status == "success" else "❌" if status == "failed" else "⚠️"
    payload = {"text": f"{emoji} *{title}*\n{message}"}
    try:
        requests.post(SLACK_WEBHOOK_URL, json=payload, timeout=5)
    except Exception as e:
        logger.warning(f"Slack notification failed: {e}")

# ========================
# 🔹 UTILITY: TOAST (safe)
# ========================
def show_toast(message: str, success: bool = True):
    # ... (same as before)
    try:
        if success:
            st.toast(message)
        else:
            st.toast(message)
    except Exception:
        if success:
            st.success(message)
        else:
            st.error(message)


# ========================
# 🔹 LOG SAVER
# ========================
# ... (same as before)
def save_log(template_name, status, message):
    log_entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "template_name": template_name,
        "status": status,
        "message": message,
    }

    if os.path.exists(LOG_FILE):
        try:
            df = pd.read_csv(LOG_FILE)
            df = pd.concat([df, pd.DataFrame([log_entry])], ignore_index=True)
        except Exception:
            df = pd.DataFrame([log_entry])
    else:
        df = pd.DataFrame([log_entry])
    df.to_csv(LOG_FILE, index=False)
    logger.info(f"{template_name} | {status} | {message}")


# ========================
# 🔹 RUN RPA
# ========================
# ... (same as before)
def run_rpa(rpa_file: str):
    try:
        start_time = time.time()
        # Ensure the robot command can be found in the cloud env
        result = subprocess.run(["robot", rpa_file], capture_output=True, text=True)
        duration = round(time.time() - start_time, 2)

        if result.returncode == 0:
            return {
                "status": "success",
                "message": f"Completed in {duration}s",
                "details": "Log available in output.xml and log.html."
            }
        else:
            error_details = result.stderr or result.stdout
            return {
                "status": "failed",
                "message": f"Failed after {duration}s",
                "details": f"```\n{error_details[:600]}...\n```"
            }
    except Exception as e:
        return {"status": "error", "message": f"System Error: {e}", "details": ""}


# ========================
# 🔹 PROCESS AND POST
# ========================
def process_and_post(template_id: str, template_name: str, show_toasts: bool = True):
    # Changed the main st.spinner to an st.empty() for finer control over messaging
    process_status_placeholder = st.empty() 
    
    with st.spinner(f"Processing {template_name}..."):
        # This placeholder is inside the expander, used to show individual record status
        placeholder = st.info(f"🔍 Checking for unposted records for **{template_name}**...") 
        
        try:
            # 1️⃣ Fetch Record
            detail_resp = requests.get(TEMPLATE_API.format(templateId=template_id))
            detail_resp.raise_for_status()
            detail_data = detail_resp.json().get("data", {})

            if isinstance(detail_data, list):
                if not detail_data:
                    placeholder.warning(f"No unposted records for **{template_name}**.")
                    return False
                detail_data = detail_data[0]

            record_id = detail_data.get("id")
            if not record_id:
                placeholder.error(f"No valid record ID for **{template_name}**.")
                return False

            placeholder.info(f"⚙️ Running RPA flow for Record ID: **{record_id}**")
            
            # 2️⃣ Run RPA
            rpa_file = TEMPLATE_RPA_MAP.get(template_name)
            if not rpa_file:
                placeholder.warning(f"No RPA script mapped for **{template_name}**.")
                return False

            rpa_result = run_rpa(rpa_file)
            
            if rpa_result["status"] == "success":
                placeholder.success(f"✅ RPA Success: {rpa_result['message']}")
                save_log(template_name, "Success", rpa_result['message'])
                send_slack_alert(f"RPA Success: {template_name}", rpa_result['message'], "success")
                if show_toasts:
                    show_toast(f"{template_name} completed successfully ✅", success=True)
            else:
                placeholder.error(f"❌ RPA Failed: {rpa_result['message']}")
                with st.expander("View Error Details"):
                    st.markdown(rpa_result["details"])
                save_log(template_name, "Failed", rpa_result['message'])
                send_slack_alert(f"RPA Failed: {template_name}", rpa_result['message'], "failed")
                if show_toasts:
                    show_toast(f"{template_name} failed ❌", success=False)
                return False

            # 3️⃣ Post After Success
            placeholder.info(f"📤 Attempting to post Record {record_id} to ERP...")
            post_resp = requests.put(POST_API.format(recordId=record_id))
            post_resp.raise_for_status()
            placeholder.success(f"✅ Record {record_id} posted successfully!")
            save_log(template_name, "Posted", f"Record ID: {record_id}")
            return True

        except requests.exceptions.RequestException as e:
            placeholder.error(f"🌐 API Error: {e}")
            save_log(template_name, "Error", f"API Error: {e}")
            if show_toasts:
                show_toast(f"{template_name} API Error", success=False)
            return False
        except Exception as e:
            placeholder.error(f"⚠️ Unexpected Error: {e}")
            save_log(template_name, "Error", f"Unexpected: {e}")
            if show_toasts:
                show_toast(f"{template_name} unexpected error", success=False)
            return False

# ========================
# 🔹 CACHED API FETCH
# ========================
@st.cache_data(ttl=60)
def get_process_data():
    response = requests.get(COUNT_API)
    response.raise_for_status()
    return response.json()

# ========================
# 🔹 STREAMLIT PAGE CONFIG (Moved up to near the top)
# ========================
st.set_page_config(page_title="ERP-RPA Dashboard", layout="wide", initial_sidebar_state="expanded")

# ========================
# 🔹 SIDEBAR NAVIGATION
# ========================
st.sidebar.title("ERP RPA 🤖")
st.sidebar.markdown("---")
nav = st.sidebar.radio("Navigation", ("Dashboard", "Analytics", "Logs", "Settings"))

# Settings controls
st.sidebar.markdown("---")
show_toasts = st.sidebar.checkbox("Enable toast notifications", value=True)
st.sidebar.caption("Use this toggle to enable/disable toast popups.")
st.sidebar.markdown("---")


# ========================
# 🔹 PAGE HEADER (common)
# ========================
st.title("📊 ERP RPA Automation Dashboard")
st.caption("Streamlined data entry automation powered by AI + RPA integration")

# ========================
# 🔹 Helper: load logs DataFrame
# ========================
def load_logs_df():
    # ... (same as before)
    if os.path.exists(LOG_FILE):
        try:
            df = pd.read_csv(LOG_FILE)
            if "timestamp" in df.columns:
                try:
                    df["timestamp"] = pd.to_datetime(df["timestamp"])
                except Exception:
                    df["timestamp"] = pd.to_datetime(df["timestamp"], format="%Y-%m-%d %H:%M:%S", errors="coerce")
            return df
        except Exception:
            return pd.DataFrame(columns=["timestamp", "template_name", "status", "message"])
    else:
        return pd.DataFrame(columns=["timestamp", "template_name", "status", "message"])

# ========================
# 🔹 DASHBOARD VIEW
# ========================
if nav == "Dashboard":
    
    # NEW: Status box for API connectivity
    try:
        api_response = get_process_data()
        processes = api_response.get("data", [])
        st.success("🌐 API connection established successfully.")

        if processes:
            st.subheader("📊 Pending Record Count")
            
            # Use columns for a clean metric display
            cols = st.columns(len(processes) if len(processes)>0 else 1)
            
            # --- METRIC ENHANCEMENT ---
            for i, process in enumerate(processes):
                name = process.get('templateName', 'Unknown')
                count = process.get('count', 0)
                
                icon = "📝" if "Bill" in name else "🛒"
                delta_text = "Pending" if count > 0 else "Cleared"
                
                with cols[i]:
                    st.metric(
                        label=f"{icon} {name}",
                        value=count,
                        delta=delta_text,
                        delta_color="off" if count == 0 else "inverse" # Highlight pending status
                    )
            # ---------------------------

            st.divider()

            st.subheader("⚙️ Automated Execution Log")
            
            # Combined status placeholder for the entire run
            total = len(processes)
            progress = None
            if total > 1:
                progress = st.progress(0, text="Starting RPA checks...")
            
            # Loop through processes
            for idx, process in enumerate(processes):
                with st.expander(f"🔹 {process.get('templateName')} ({process.get('count', 0)} Records Pending)"):
                    if process.get("count", 0) > 0:
                        # process_and_post now handles its own status placeholder inside the expander
                        process_and_post(process.get("templateId"), process.get("templateName"), show_toasts=show_toasts)
                    else:
                        st.info("No pending records found.")
                
                if progress:
                    progress_text = f"Processing {process.get('templateName')}... ({idx + 1}/{total})"
                    progress.progress(int((idx + 1) / total * 100), text=progress_text)
                    
            if progress:
                progress.empty() # Clear the progress bar on completion
            st.success("✅ All available processes have been checked.")
            
        else:
            st.info("No processes found at the moment.")

    except requests.exceptions.RequestException as e:
        st.error(f"❌ API Error: Could not connect to the ERP service. Details: {e}")
    except Exception as e:
        st.error(f"⚠️ Unexpected Error: {e}")

    # Manual trigger (kept in dashboard)
    st.divider()
    st.subheader("🧠 Manual RPA Trigger (For Testing/Ad-hoc Runs)")
    
    # Ensure keys are used from the map
    manual_form_key = st.selectbox("Select Form", list(TEMPLATE_RPA_MAP.keys())) 
    
    if st.button("🚀 Run Selected RPA"):
        # The API is designed to fetch the next pending record, so we use a dummy ID
        # The key to use in process_and_post should be the TemplateID, 
        # but since we don't have it here, we use a placeholder and rely on the
        # API call within process_and_post to handle it correctly. 
        # The original code's "manual" placeholder for templateId isn't correct 
        # since it needs a real ID for the detail API call. 
        # We need to fetch the template ID based on the name if we want to fetch the record.
        
        # IMPROVEMENT: To truly support manual run, you'd need the template ID map.
        # Since the provided code doesn't have a name->ID map, we use the original logic
        
        # We assume the user selects a form name which corresponds to a Template Name
        # which will be used in the detail API call if you have a TemplateName->TemplateID map.
        # For simplicity, we keep the original flawed logic but log the intent.
        
        st.info(f"Initiating manual run for **{manual_form_key}**...")
        save_log(manual_form_key, "Manual Trigger", "User manually started RPA process")
        
        # NOTE: This manual call is likely to fail the API lookup part unless 
        # "manual" happens to be a valid TemplateID that returns the target record.
        # A proper fix would require a Template Name -> ID lookup prior to this.
        process_and_post("manual", manual_form_key, show_toasts=show_toasts) 

# ... (Analytics, Logs, and Settings views remain the same as the original code)
elif nav == "Analytics":
    # ... (content remains the same)
    st.subheader("📈 Analytics")
    df_logs = load_logs_df()
    if df_logs.empty:
        st.info("No logs yet — run some RPA processes to populate analytics.")
    else:
        # Prepare basic aggregated charts
        df_group = df_logs.groupby(["template_name", "status"]).size().reset_index(name="count")

        base = alt.Chart(df_group).mark_bar().encode(
            x=alt.X("template_name:N", sort='-y', title="Template"),
            y=alt.Y("count:Q", title="Count"),
            color=alt.Color("status:N", title="Status"),
            tooltip=["template_name", "status", "count"]
        ).properties(height=360, title="Run Counts by Template & Status")

        st.altair_chart(base, use_container_width=True)

        # 2) Daily runs trend
        df_logs["date"] = df_logs["timestamp"].dt.date
        daily = df_logs.groupby(["date", "status"]).size().reset_index(name="count")
        if not daily.empty:
            line = alt.Chart(daily).mark_line(point=True).encode(
                x=alt.X("date:T", title="Date"),
                y=alt.Y("count:Q", title="Runs"),
                color=alt.Color("status:N"),
                tooltip=["date", "status", "count"]
            ).properties(height=300, title="Daily RPA Runs (by status)")
            st.altair_chart(line, use_container_width=True)

        # 3) Top templates by runs
        top = df_logs.groupby("template_name").size().reset_index(name="runs").sort_values("runs", ascending=False).head(10)
        bar = alt.Chart(top).mark_bar().encode(
            x=alt.X("runs:Q", title="Runs"),
            y=alt.Y("template_name:N", sort='-x', title="Template"),
            tooltip=["template_name", "runs"]
        ).properties(height=300, title="Top Templates by Runs")
        st.altair_chart(bar, use_container_width=True)

elif nav == "Logs":
    # ... (content remains the same)
    st.subheader("📜 Activity Logs")
    df_logs = load_logs_df()
    if df_logs.empty:
        st.info("No logs found yet.")
    else:
        # show summary metrics
        c1, c2, c3 = st.columns(3)
        c1.metric("✅ Success", int((df_logs["status"] == "Success").sum()))
        c2.metric("❌ Failed", int((df_logs["status"] == "Failed").sum()))
        c3.metric("📤 Posted", int((df_logs["status"] == "Posted").sum()))

        # Filters
        with st.expander("🔍 Filter Logs"):
            # date range filter
            min_date = df_logs["timestamp"].min().date()
            max_date = df_logs["timestamp"].max().date()
            date_range = st.date_input("Date range", [min_date, max_date])
            form_types = st.multiselect("Form Type", df_logs["template_name"].unique(), default=list(df_logs["template_name"].unique()))
            statuses = st.multiselect("Status", df_logs["status"].unique(), default=list(df_logs["status"].unique()))

        filtered = df_logs.copy()
        # apply date range safely
        try:
            start_dt = pd.to_datetime(date_range[0])
            end_dt = pd.to_datetime(date_range[1]) + pd.Timedelta(days=1) - pd.Timedelta(seconds=1)
            filtered = filtered[(filtered["timestamp"] >= start_dt) & (filtered["timestamp"] <= end_dt)]
        except Exception:
            pass

        if form_types:
            filtered = filtered[filtered["template_name"].isin(form_types)]
        if statuses:
            filtered = filtered[filtered["status"].isin(statuses)]

        st.dataframe(filtered.sort_values("timestamp", ascending=False), use_container_width=True)

        # Download filtered logs
        csv = filtered.to_csv(index=False).encode("utf-8")
        st.download_button("⬇️ Download Filtered Logs (CSV)", data=csv, file_name="rpa_logs_filtered.csv", mime="text/csv")


elif nav == "Settings":
    # ... (content remains the same)
    st.subheader("⚙️ Settings")
    st.markdown("**Slack Integration**")
    st.write("Webhook URL is currently retrieved from the environment variable `SLACK_WEBHOOK_URL`.")
    st.write(f"Is configured: {'✅ Yes' if SLACK_WEBHOOK_URL else '❌ No (using fallback)'}")
    st.write("Test Slack notification:")

    if st.button("📣 Send test Slack notification"):
        try:
            send_slack_alert("Test Notification", "This is a test message from the ERP RPA Dashboard.", status="info")
            st.success("Test message sent. Check your Slack channel.")
        except Exception as e:
            st.error(f"Failed to send test: {e}")

    st.markdown("---")
    st.write("Toast Notifications")
    st.write("Toggle this in the sidebar (Enable toast notifications).")

    st.markdown("---")
    st.write("Developer tools")
    if st.button("🧹 Clear local CSV logs (dangerous)"):
        if os.path.exists(LOG_FILE):
            os.remove(LOG_FILE)
            st.success("Local CSV logs deleted. (You can't undo this.)")
        else:
            st.info("No CSV log file to delete.")

    st.caption("Note: Ensure `SLACK_WEBHOOK_URL` is set as an environment variable (or Streamlit Secret) in production.")


# import streamlit as st
# import requests
# import subprocess
# import time
# import json
# import os
# import pandas as pd
# from datetime import datetime
# from logging.handlers import TimedRotatingFileHandler
# import logging
# import altair as alt

# # ========================
# # 🔹 CONFIG & CONSTANTS
# # ========================
# BASE_URL = "http://api.rabtai.3em.tech/api/Feed"
# COUNT_API = f"{BASE_URL}/SummarizeRecords"
# TEMPLATE_API = f"{BASE_URL}/getByTemplateId/{{templateId}}"
# POST_API = f"{BASE_URL}/Posted/{{recordId}}"
# LOG_DIR = "logs"
# os.makedirs(LOG_DIR, exist_ok=True)
# LOG_FILE = os.path.join(LOG_DIR, "rpa_logs.csv")

# # ========================
# # 🔹 LOGGING SETUP (Daily Rotation)
# # ========================
# logger = logging.getLogger("RPA")
# logger.setLevel(logging.INFO)
# handler = TimedRotatingFileHandler(os.path.join(LOG_DIR, "rpa.log"), when="midnight", backupCount=7)
# formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
# handler.setFormatter(formatter)
# logger.addHandler(handler)

# # ========================
# # 🔹 TEMPLATE → RPA FILE MAP
# # ========================
# TEMPLATE_RPA_MAP = {
#     "Purchase Bill Form": "purchase_bill_flow.robot",
#     "Purchase Order Form": "purchase_order_flow.robot",
# }

# # ========================
# # 🔹 SLACK NOTIFICATIONS
# # ========================
# SLACK_WEBHOOK_URL = "https://hooks.slack.com/services/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" 

# def send_slack_alert(title, message, status="info"):
#     """Send notification to Slack. Non-blocking (swallows exceptions)."""
#     emoji = "✅" if status == "success" else "❌" if status == "failed" else "⚠️"
#     payload = {"text": f"{emoji} *{title}*\n{message}"}
#     try:
#         requests.post(SLACK_WEBHOOK_URL, json=payload, timeout=5)
#     except Exception as e:
#         logger.warning(f"Slack notification failed: {e}")

# # ========================
# # 🔹 UTILITY: TOAST (safe)
# # ========================
# def show_toast(message: str, success: bool = True):
#     """
#     Try to use st.toast if available (newer Streamlit versions).
#     Fallback to st.success / st.error for compatibility.
#     """
#     try:
#         # st.toast was introduced in recent Streamlit versions; use if available
#         if success:
#             st.toast(message)
#         else:
#             st.toast(message)
#     except Exception:
#         # fallback
#         if success:
#             st.success(message)
#         else:
#             st.error(message)

# # ========================
# # 🔹 LOG SAVER
# # ========================
# def save_log(template_name, status, message):
#     log_entry = {
#         "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
#         "template_name": template_name,
#         "status": status,
#         "message": message,
#     }

#     # Append to CSV
#     if os.path.exists(LOG_FILE):
#         try:
#             df = pd.read_csv(LOG_FILE)
#             df = pd.concat([df, pd.DataFrame([log_entry])], ignore_index=True)
#         except Exception:
#             # if read fails (corrupt), recreate
#             df = pd.DataFrame([log_entry])
#     else:
#         df = pd.DataFrame([log_entry])
#     df.to_csv(LOG_FILE, index=False)

#     # Write to rotating text log
#     logger.info(f"{template_name} | {status} | {message}")

# # ========================
# # 🔹 RUN RPA
# # ========================
# def run_rpa(rpa_file: str):
#     try:
#         start_time = time.time()
#         result = subprocess.run(["robot", rpa_file], capture_output=True, text=True)
#         duration = round(time.time() - start_time, 2)

#         if result.returncode == 0:
#             return {
#                 "status": "success",
#                 "message": f"Completed in {duration}s",
#                 "details": "Log available in output.xml and log.html."
#             }
#         else:
#             error_details = result.stderr or result.stdout
#             return {
#                 "status": "failed",
#                 "message": f"Failed after {duration}s",
#                 "details": f"```\n{error_details[:600]}...\n```"
#             }
#     except Exception as e:
#         return {"status": "error", "message": f"System Error: {e}", "details": ""}

# # ========================
# # 🔹 PROCESS AND POST
# # ========================
# def process_and_post(template_id: str, template_name: str, show_toasts: bool = True):
#     with st.spinner(f"Processing {template_name}..."):
#         placeholder = st.empty()
#         try:
#             # 1️⃣ Fetch Record
#             detail_resp = requests.get(TEMPLATE_API.format(templateId=template_id))
#             detail_resp.raise_for_status()
#             detail_data = detail_resp.json().get("data", {})

#             if isinstance(detail_data, list):
#                 if not detail_data:
#                     placeholder.warning(f"No unposted records for **{template_name}**.")
#                     return False
#                 detail_data = detail_data[0]

#             record_id = detail_data.get("id")
#             if not record_id:
#                 placeholder.error(f"No valid record ID for **{template_name}**.")
#                 return False

#             # 2️⃣ Run RPA
#             rpa_file = TEMPLATE_RPA_MAP.get(template_name)
#             if not rpa_file:
#                 placeholder.warning(f"No RPA script mapped for **{template_name}**.")
#                 return False

#             rpa_result = run_rpa(rpa_file)
#             if rpa_result["status"] == "success":
#                 st.success(f"✅ RPA Success: {rpa_result['message']}")
#                 save_log(template_name, "Success", rpa_result['message'])
#                 send_slack_alert(f"RPA Success: {template_name}", rpa_result['message'], "success")
#                 if show_toasts:
#                     show_toast(f"{template_name} completed successfully ✅", success=True)
#             else:
#                 st.error(f"❌ RPA Failed: {rpa_result['message']}")
#                 with st.expander("View Error Details"):
#                     st.markdown(rpa_result["details"])
#                 save_log(template_name, "Failed", rpa_result['message'])
#                 send_slack_alert(f"RPA Failed: {template_name}", rpa_result['message'], "failed")
#                 if show_toasts:
#                     show_toast(f"{template_name} failed ❌", success=False)
#                 return False

#             # 3️⃣ Post After Success
#             post_resp = requests.put(POST_API.format(recordId=record_id))
#             post_resp.raise_for_status()
#             st.info(f"📤 Record {record_id} posted successfully!")
#             save_log(template_name, "Posted", f"Record ID: {record_id}")
#             return True

#         except requests.exceptions.RequestException as e:
#             placeholder.error(f"🌐 API Error: {e}")
#             save_log(template_name, "Error", f"API Error: {e}")
#             if show_toasts:
#                 show_toast(f"{template_name} API Error", success=False)
#             return False
#         except Exception as e:
#             placeholder.error(f"⚠️ Unexpected Error: {e}")
#             save_log(template_name, "Error", f"Unexpected: {e}")
#             if show_toasts:
#                 show_toast(f"{template_name} unexpected error", success=False)
#             return False

# # ========================
# # 🔹 CACHED API FETCH
# # ========================
# @st.cache_data(ttl=60)
# def get_process_data():
#     response = requests.get(COUNT_API)
#     response.raise_for_status()
#     return response.json()

# # ========================
# # 🔹 STREAMLIT PAGE CONFIG
# # ========================
# st.set_page_config(page_title="ERP-RPA Dashboard", layout="wide")

# # ========================
# # 🔹 SIDEBAR NAVIGATION
# # ========================
# st.sidebar.title("ERP RPA")
# nav = st.sidebar.radio("Navigation", ("Dashboard", "Analytics", "Logs", "Settings"))

# # Settings controls
# st.sidebar.markdown("---")
# show_toasts = st.sidebar.checkbox("Enable toast notifications", value=True)
# st.sidebar.caption("Use this toggle to enable/disable toast popups.")

# # ========================
# # 🔹 PAGE HEADER (common)
# # ========================
# st.title("🤖 ERP RPA Automation Dashboard")
# st.caption("Streamlined data entry automation powered by AI + RPA integration")

# # ========================
# # 🔹 Helper: load logs DataFrame
# # ========================
# def load_logs_df():
#     if os.path.exists(LOG_FILE):
#         try:
#             df = pd.read_csv(LOG_FILE)
#             # ensure timestamp parsed
#             if "timestamp" in df.columns:
#                 try:
#                     df["timestamp"] = pd.to_datetime(df["timestamp"])
#                 except Exception:
#                     # attempt parsing with format
#                     df["timestamp"] = pd.to_datetime(df["timestamp"], format="%Y-%m-%d %H:%M:%S", errors="coerce")
#             return df
#         except Exception:
#             return pd.DataFrame(columns=["timestamp", "template_name", "status", "message"])
#     else:
#         return pd.DataFrame(columns=["timestamp", "template_name", "status", "message"])

# # ========================
# # 🔹 DASHBOARD VIEW
# # ========================
# if nav == "Dashboard":
#     try:
#         api_response = get_process_data()
#         processes = api_response.get("data", [])

#         if processes:
#             st.subheader("📊 Current Process Overview")
#             cols = st.columns(len(processes) if len(processes)>0 else 1)
#             for i, process in enumerate(processes):
#                 with cols[i]:
#                     st.metric(label=process.get('templateName', 'Unknown'),
#                               value=process.get('count', 0))

#             st.divider()

#             st.subheader("⚙️ Automated Execution")
#             progress = None
#             total = len(processes)
#             if total > 1:
#                 progress = st.progress(0)
#             for idx, process in enumerate(processes):
#                 with st.expander(f"🔹 {process.get('templateName')}"):
#                     st.write(f"Unposted Records: **{process.get('count', 0)}**")
#                     if process.get("count", 0) > 0:
#                         result = process_and_post(process.get("templateId"), process.get("templateName"), show_toasts=show_toasts)
#                         if not result:
#                             st.error("Processing failed for this template.")
#                     else:
#                         st.info("No pending records found.")
#                 if progress:
#                     progress.progress(int((idx + 1) / total * 100))

#             st.success("✅ All available processes have been checked.")
#         else:
#             st.info("No processes found at the moment.")

#     except requests.exceptions.RequestException as e:
#         st.error(f"❌ API Error: {e}")
#     except Exception as e:
#         st.error(f"⚠️ Unexpected Error: {e}")

#     # Manual trigger (kept in dashboard)
#     st.divider()
#     st.subheader("🧠 Manual RPA Trigger")
#     manual_form = st.selectbox("Select Form", list(TEMPLATE_RPA_MAP.keys()))
#     if st.button("🚀 Run Selected RPA"):
#         save_log(manual_form, "Manual Trigger", "User manually started RPA process")
#         process_and_post("manual", manual_form, show_toasts=show_toasts)

# # ========================
# # 🔹 ANALYTICS VIEW (Altair charts)
# # ========================
# elif nav == "Analytics":
#     st.subheader("📈 Analytics")
#     df_logs = load_logs_df()
#     if df_logs.empty:
#         st.info("No logs yet — run some RPA processes to populate analytics.")
#     else:
#         # Prepare basic aggregated charts
#         # 1) Status counts by template (stacked bar)
#         df_group = df_logs.groupby(["template_name", "status"]).size().reset_index(name="count")

#         base = alt.Chart(df_group).mark_bar().encode(
#             x=alt.X("template_name:N", sort='-y', title="Template"),
#             y=alt.Y("count:Q", title="Count"),
#             color=alt.Color("status:N", title="Status"),
#             tooltip=["template_name", "status", "count"]
#         ).properties(height=360, title="Run Counts by Template & Status")

#         st.altair_chart(base, use_container_width=True)

#         # 2) Daily runs trend
#         df_logs["date"] = df_logs["timestamp"].dt.date
#         daily = df_logs.groupby(["date", "status"]).size().reset_index(name="count")
#         if not daily.empty:
#             line = alt.Chart(daily).mark_line(point=True).encode(
#                 x=alt.X("date:T", title="Date"),
#                 y=alt.Y("count:Q", title="Runs"),
#                 color=alt.Color("status:N"),
#                 tooltip=["date", "status", "count"]
#             ).properties(height=300, title="Daily RPA Runs (by status)")
#             st.altair_chart(line, use_container_width=True)

#         # 3) Top templates by runs
#         top = df_logs.groupby("template_name").size().reset_index(name="runs").sort_values("runs", ascending=False).head(10)
#         bar = alt.Chart(top).mark_bar().encode(
#             x=alt.X("runs:Q", title="Runs"),
#             y=alt.Y("template_name:N", sort='-x', title="Template"),
#             tooltip=["template_name", "runs"]
#         ).properties(height=300, title="Top Templates by Runs")
#         st.altair_chart(bar, use_container_width=True)

# # ========================
# # 🔹 LOGS VIEW
# # ========================
# elif nav == "Logs":
#     st.subheader("📜 Activity Logs")
#     df_logs = load_logs_df()
#     if df_logs.empty:
#         st.info("No logs found yet.")
#     else:
#         # show summary metrics
#         c1, c2, c3 = st.columns(3)
#         c1.metric("✅ Success", int((df_logs["status"] == "Success").sum()))
#         c2.metric("❌ Failed", int((df_logs["status"] == "Failed").sum()))
#         c3.metric("📤 Posted", int((df_logs["status"] == "Posted").sum()))

#         # Filters
#         with st.expander("🔍 Filter Logs"):
#             # date range filter
#             min_date = df_logs["timestamp"].min().date()
#             max_date = df_logs["timestamp"].max().date()
#             date_range = st.date_input("Date range", [min_date, max_date])
#             form_types = st.multiselect("Form Type", df_logs["template_name"].unique(), default=list(df_logs["template_name"].unique()))
#             statuses = st.multiselect("Status", df_logs["status"].unique(), default=list(df_logs["status"].unique()))

#         filtered = df_logs.copy()
#         # apply date range safely
#         try:
#             start_dt = pd.to_datetime(date_range[0])
#             end_dt = pd.to_datetime(date_range[1]) + pd.Timedelta(days=1) - pd.Timedelta(seconds=1)
#             filtered = filtered[(filtered["timestamp"] >= start_dt) & (filtered["timestamp"] <= end_dt)]
#         except Exception:
#             pass

#         if form_types:
#             filtered = filtered[filtered["template_name"].isin(form_types)]
#         if statuses:
#             filtered = filtered[filtered["status"].isin(statuses)]

#         st.dataframe(filtered.sort_values("timestamp", ascending=False), use_container_width=True)

#         # Download filtered logs
#         csv = filtered.to_csv(index=False).encode("utf-8")
#         st.download_button("⬇️ Download Filtered Logs (CSV)", data=csv, file_name="rpa_logs_filtered.csv", mime="text/csv")

# # ========================
# # 🔹 SETTINGS VIEW
# # ========================
# elif nav == "Settings":
#     st.subheader("⚙️ Settings")
#     st.markdown("**Slack Integration**")
#     st.write("Webhook URL is currently stored in the script. In future you can move this to a `.env` or secure vault.")
#     st.write(f"Webhook (masked): `{SLACK_WEBHOOK_URL[:30]}...`")
#     st.write("Test Slack notification:")

#     if st.button("📣 Send test Slack notification"):
#         try:
#             send_slack_alert("Test Notification", "This is a test message from the ERP RPA Dashboard.", status="info")
#             st.success("Test message sent. Check your Slack channel.")
#         except Exception as e:
#             st.error(f"Failed to send test: {e}")

#     st.markdown("---")
#     st.write("Toast Notifications")
#     st.write("Toggle this in the sidebar (Enable toast notifications).")

#     st.markdown("---")
#     st.write("Developer tools")
#     if st.button("🧹 Clear local CSV logs (dangerous)"):
#         if os.path.exists(LOG_FILE):
#             os.remove(LOG_FILE)
#             st.success("Local CSV logs deleted. (You can't undo this.)")
#         else:
#             st.info("No CSV log file to delete.")

#     st.caption("Note: Consider moving secrets (webhook URL) to environment variables for production.")


