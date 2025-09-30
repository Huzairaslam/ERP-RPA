import streamlit as st
import requests
import subprocess
import time
import json

# ========================
# 🔹 API Endpoints
# ========================
BASE_URL = "http://api.rabtai.3em.tech/api/Feed"
COUNT_API = f"{BASE_URL}/SummarizeRecords"
TEMPLATE_API = f"{BASE_URL}/getByTemplateId/{{templateId}}"
POST_API = f"{BASE_URL}/Posted/{{recordId}}"

# ==============================
# 🔹 Template → RPA file mapping
# ==============================
TEMPLATE_RPA_MAP = {
    "Purchase Bill Form": "purchase_bill_flow.robot",
    "Purchase Order Form": "purchase_order_flow.robot",
}

# ========================
# 🔹 Run RPA (Enhanced Output)
# ========================
def run_rpa(rpa_file: str):
    """Runs the Robot Framework file and returns a structured result."""
    try:
        start_time = time.time()
        result = subprocess.run(
            ["robot", rpa_file],
            capture_output=True,
            text=True
        )
        end_time = time.time()
        duration = round(end_time - start_time, 2)

        if result.returncode == 0:
            return {
                "status": "success",
                "message": f"Execution completed in **{duration}s**.",
                "details": f"Robot output log available in **output.xml** and **log.html**."
            }
        else:
            error_details = result.stderr or result.stdout
            return {
                "status": "failed",
                "message": f"Execution failed after **{duration}s**.",
                "details": f"Error Log Snippet:\n```\n{error_details[:800]}...\n```" # Show more context
            }

    except Exception as e:
        return {
            "status": "error",
            "message": f"System Error during RPA launch: {str(e)}",
            "details": ""
        }

# [============================]
# [🔹 Auto Process & Post🔹    ]
# [=========================== ]
def process_and_post(template_id: str, template_name: str):
    placeholder = st.empty() # Placeholder for processing status

    try:
        # 1️⃣ Fetch all records under this template
        placeholder.info(f"🔍 Fetching record details for **{template_name}**...")
        
        detail_resp = requests.get(TEMPLATE_API.format(templateId=template_id))
        detail_resp.raise_for_status()
        detail_data = detail_resp.json().get("data", {})

        # Handle both single record and list of records
        if isinstance(detail_data, list):
            if not detail_data:
                return placeholder.warning(f"⚠️ No unposted record found for **{template_name}**")
            detail_data = detail_data[0]

        if not detail_data:
            return placeholder.warning(f"⚠️ No unposted record found for **{template_name}**")

        # Grab recordId
        record_id = detail_data.get("id")
        
        if not record_id:
            return placeholder.error(f"⚠️ No valid recordId for **{template_name}**")

        placeholder.info(f"🤖 Starting RPA for Record **{record_id}**...")

        # 2️⃣ Run mapped RPA file
        rpa_file = TEMPLATE_RPA_MAP.get(template_name)
        if rpa_file:
            rpa_result = run_rpa(rpa_file)
            
            if rpa_result['status'] == 'success':
                st.success(f"✅ RPA Success for **{template_name}** ({record_id}). {rpa_result['message']}")
            else:
                st.error(f"❌ RPA Failed for **{template_name}** ({record_id}). {rpa_result['message']}")
                with st.expander("Show detailed error log"):
                    st.markdown(rpa_result['details'])
                return f"🛑 RPA failed for **{template_name}**. Posting skipped."
        else:
            return placeholder.warning(f"⚠️ No RPA file mapped for **{template_name}**")

        # 3️⃣ Post the record after RPA
        placeholder.info(f"📤 Posting Record **{record_id}**...")
        post_resp = requests.put(POST_API.format(recordId=record_id))
        post_resp.raise_for_status()
        
        # Final success message replaces the placeholder content
        placeholder.success(f"✅ Record **{record_id}** posted successfully!")
        return True # Return True to signal successful processing

    except requests.exceptions.RequestException as e:
        placeholder.error(f"❌ API Error in processing **{template_name}**: {e}")
        return False
    except json.JSONDecodeError as e:
        placeholder.error(f"❌ JSON Error in processing **{template_name}**: {e}")
        return False
    except Exception as e:
        placeholder.error(f"❌ Unhandled Error in processing **{template_name}**: {e}")
        return False


# ========================
# 🔹 Streamlit Dashboard
# ========================
st.set_page_config(page_title="ERP-RPA Dashboard", layout="wide")
st.title("📊 ERP RPA Dashboard")

try:
    response = requests.get(COUNT_API)
    response.raise_for_status()
    api_response = response.json()

    processes = api_response.get("data", [])

    if processes:
        st.subheader("📌 Process Counts")
        # Use st.dataframe for a nicer look than st.table
        st.dataframe([
            {"Process": p.get("templateName", "Unknown"), "Unposted Count": p.get("count", 0)}
            for p in processes
        ], hide_index=True)
        
        st.subheader("⚙️ Automatic Processing")

        all_successful = True
        
        # Loop and auto-handle processing + posting
        for process in processes:
            template_id = process.get("templateId")
            process_name = process.get("templateName", "Unknown")
            count = int(process.get("count", 0))

            # Display the count for the process currently being handled
            st.metric(label=f"📄 {process_name}", value=count)

            if count > 0:
                result = process_and_post(template_id, process_name)
                if not result:
                    all_successful = False

        # 🔄 Refresh summarize API after all done (Correctly implemented)
        st.divider()
        st.success("✅ All active processes have been checked.")
        
        # Only show the refresh block if there were processes to begin with
        st.subheader("Summary Refresh")
        st.info("🔄 Refreshing summary to reflect posted records...")
        
        refreshed = requests.get(COUNT_API).json()
        st.json(refreshed)
        

    else:
        st.info("No processes found.")

except requests.exceptions.RequestException as e:
    st.error(f"❌ API Error: Failed to connect to or retrieve summary from the API: {str(e)}")
except Exception as e:
    st.error(f"❌ Unexpected Error in Dashboard: {str(e)}")


# import streamlit as st
# import requests
# import subprocess
# import time
# import json

# # ========================
# # 🔹 API Endpoints
# # ========================
# BASE_URL = "http://api.rabtai.3em.tech/api/Feed"
# COUNT_API = f"{BASE_URL}/SummarizeRecords"
# TEMPLATE_API = f"{BASE_URL}/getByTemplateId/{{templateId}}"
# POST_API = f"{BASE_URL}/Posted/{{recordId}}"

# # ==============================
# # 🔹 Template → RPA file mapping
# # ==============================
# TEMPLATE_RPA_MAP = {
#     "Purchase Bill Form": "purchase_bill_flow.robot",
#     "Purchase Order Form": "purchase_order_flow.robot",
# }

# # ========================
# # 🔹 Run RPA
# # ========================
# def run_rpa(rpa_file: str):
#     try:
#         start_time = time.time()
#         # NOTE: Removed 'text=True' for subprocess.run. 
#         # While it often works, for full compatibility with Robot's large output, 
#         # it's better to manage text decoding explicitly if needed, but we'll try to keep it simple.
#         # Keeping it as 'text=True' since that's what was in the original and it simplifies stderr handling.
#         result = subprocess.run(
#             ["robot", rpa_file],
#             capture_output=True,
#             text=True
#         )
#         end_time = time.time()
#         duration = round(end_time - start_time, 2)

#         if result.returncode == 0:
#             return f"✅ Success in {duration}s"
#         else:
#             # Include a snippet of stdout/stderr for debugging context
#             error_details = result.stderr or result.stdout
#             return f"❌ Failed: {error_details[:500]}..." # Show first 500 chars of error

#     except Exception as e:
#         return f"⚠️ Error: {str(e)}"

# # [============================]
# # [🔹 Auto Process & Post🔹    ]
# # [=========================== ]
# def process_and_post(template_id: str, template_name: str):
#     try:
#         # 1️⃣ Fetch all records under this template
#         detail_resp = requests.get(TEMPLATE_API.format(templateId=template_id))
#         detail_resp.raise_for_status()
#         detail_data = detail_resp.json().get("data", {})

#         # Handle both single record and list of records
#         if isinstance(detail_data, list):
#             if not detail_data:
#                 return f"⚠️ No unposted record found for {template_name}"
#             detail_data = detail_data[0]  # Take the first record if list

#         if not detail_data:
#             return f"⚠️ No unposted record found for {template_name}"

#         # Grab recordId and formData
#         record_id = detail_data.get("id")
#         form_data_str = detail_data.get("formData", "{}")
        
#         # NOTE: The robot script will parse this itself, but keeping this for local checks
#         # form_data = json.loads(form_data_str) if form_data_str else {} 

#         if not record_id:
#             return f"⚠️ No valid recordId for {template_name}"

#         st.info(f"🔍 Processing record {record_id} for {template_name}")

#         # 2️⃣ Run mapped RPA file
#         rpa_file = TEMPLATE_RPA_MAP.get(template_name)
#         if rpa_file:
#             rpa_result = run_rpa(rpa_file)
#             st.success(rpa_result)
            
#             # If RPA failed, stop here and do not post.
#             if "❌ Failed" in rpa_result:
#                 return f"🛑 RPA failed for {template_name}. Posting skipped."
#         else:
#             return f"⚠️ No RPA file mapped for {template_name}"

#         # 3️⃣ Post the record after RPA
#         # CRITICAL FIX: Changed 'id' to 'record_id'
#         post_resp = requests.put(POST_API.format(recordId=record_id))
#         post_resp.raise_for_status()
#         return f"📤 Record {record_id} posted successfully ✅"

#     except requests.exceptions.RequestException as e:
#         return f"❌ API Error in processing {template_name}: {e}"
#     except json.JSONDecodeError as e:
#         return f"❌ JSON Error in processing {template_name}: {e}"
#     except Exception as e:
#         return f"❌ Error in processing {template_name}: {e}"
    


# # ========================
# # 🔹 Streamlit Dashboard
# # ========================
# st.set_page_config(page_title="ERP-RPA Dashboard", layout="wide")
# st.title("📊 ERP RPA Dashboard")

# try:
#     response = requests.get(COUNT_API)
#     response.raise_for_status()
#     api_response = response.json()

#     processes = api_response.get("data", [])

#     if processes:
#         st.subheader("📌 Process Counts")
#         st.table([
#             {"Process": p.get("templateName", "Unknown"), "Count": p.get("count", 0)}
#             for p in processes
#         ])

#         # Loop and auto-handle processing + posting
#         for process in processes:
#             template_id = process.get("templateId")
#             process_name = process.get("templateName", "Unknown")
#             count = int(process.get("count", 0))

#             st.metric(label=f"📄 {process_name}", value=count)

#             if count > 0:
#                 msg = process_and_post(template_id, process_name)
#                 st.write(msg)

#         # 🔄 Refresh summarize API after all done
#         st.success("✅ All processes handled. Refreshing summary...")
#         refreshed = requests.get(COUNT_API).json()
#         st.json(refreshed)

#     else:
#         st.info("No processes found.")

# except requests.exceptions.RequestException as e:
#     st.error(f"API Error: {str(e)}")
# except Exception as e:
#     st.error(f"Unexpected Error: {str(e)}")