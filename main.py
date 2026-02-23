import subprocess
import time

def run_script(script_name):
    print(f"Running {script_name}...")
    result = subprocess.run(["python", script_name], check=True)  
    print(f"{script_name} completed successfully.\n")

if __name__ == "__main__":    
    run_script("scrape.py")
    run_script("videoprocess.py")
    run_script("videocompile.py")
    run_script("ytupload.py")

