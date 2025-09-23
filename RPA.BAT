@echo off
echo [🚀] Starting RPA Dashboard...
REM Activate your Python environment if you use venv
REM call venv\Scripts\activate

REM Run Streamlit dashboard on all network interfaces
streamlit run dashboard.py --server.address=0.0.0.0 --server.port=8501

pause
