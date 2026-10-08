import subprocess
import sys
import time

def run_step(command, step_name, cwd=None):
    print(f"\n[RUNNING] {step_name}...")
    start_time = time.time()
    result = subprocess.run(command, cwd=cwd, shell=True)
    duration = round(time.time() - start_time, 2)
    
    if result.returncode != 0:
        print(f"[FAILED] {step_name} gagal dalam {duration}s!")
        sys.exit(result.returncode)
        
    print(f"[SUCCESS] {step_name} selesai ({duration}s).")

def main():
    print("=== MEMULAI WEATHER ELT PIPELINE ===")
    
    # 1. Extract & Load (Python)
    run_step("python extractors/extract_weather.py", "Extract & Load ke Bronze Layer")

    # 2. Transform & Test (dbt)
    run_step("dbt build", "Transform & Testing (Silver/Gold Layer)", cwd="transform")

    print("\n=== PIPELINE SELESAI DENGAN SUKSES ===")

if __name__ == "__main__":
    main()
