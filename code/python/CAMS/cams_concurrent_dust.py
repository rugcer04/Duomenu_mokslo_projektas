import os
import logging
from concurrent.futures import ThreadPoolExecutor
from ecmwf.datastores import Client

logging.basicConfig(level="INFO", format='%(asctime)s - %(levelname)s - %(message)s')
DOWNLOAD_DIR = os.path.join("CAMS_Downloads", "Dust")
DATASET = "cams-europe-air-quality-reanalyses"
VILNIUS_AREA = [54.95, 25.00, 54.40, 25.55]
MAX_WORKERS = 6

os.makedirs(DOWNLOAD_DIR, exist_ok=True)
client = Client()
client.check_authentication()

def download_task(task_info):
    """Function to handle a single request and download."""
    year, month = task_info
    file_name = f"cams_{year}_{month}_dust_validated.zip" # uŽmiršau pakeisti, 2024 ir vėliau nėra validuoti!!!
    target_path = os.path.join(DOWNLOAD_DIR, file_name)

    if os.path.exists(target_path):
        logging.info(f"Skipping {file_name} - already exists.")
        return

    request = {
        "variable": ["dust"],
        "model": ["ensemble"],
        "level": ["500"],
        "type": ["interim_reanalysis"],
        "year": [year],
        "month": [month],
        "area": VILNIUS_AREA 
    }

    try:
        logging.info(f"Starting request for {file_name}")
        remote = client.submit_and_wait_on_results(DATASET, request)
        remote.download(target_path)
        logging.info(f"Successfully downloaded {file_name}")
    except Exception as e:
        logging.error(f"Failed to download {file_name}: {e}")

if __name__ == "__main__":
    years = ["2024", "2025"]
    months = [f"{m:02d}" for m in range(1, 13)]
    
    all_tasks = [(y, m) for y in years for m in months]

    logging.info(f"Starting batch processing with {MAX_WORKERS} workers...")
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        executor.map(download_task, all_tasks)

    logging.info("All tasks completed.")