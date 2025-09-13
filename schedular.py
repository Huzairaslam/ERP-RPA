import time
import subprocess

DASHBOARD_SCRIPT = "dashboard.py"

def run_dashboard():
    """Run the dashboard script."""
    print("[🚀] Launching dashboard.py...")
    subprocess.run(["streamlit", "run", DASHBOARD_SCRIPT], check=True)

if __name__ == "__main__":
    print("[⏳] Scheduler started. Running dashboard.py every 5 minutes...")
    while True:
        run_dashboard()
        time.sleep(300)  # wait 5 minutes
