@echo off
echo ============================================
echo 🤖 ERP RPA Automation Dashboard Starting
echo ============================================
echo.

REM 1️⃣ Activate virtual environment
call venv\Scripts\activate

echo
streamlit run dashboard.py
echo.
pause
