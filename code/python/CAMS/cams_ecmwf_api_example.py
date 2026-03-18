import logging
import os

logging.basicConfig(level="INFO")

from ecmwf.datastores import Client
client = Client()
client.check_authentication()


years = ["2018", "2019", "2020", "2021", "2022", "2023"]
months = [f"{m:02d}" for m in range(1, 13)]

DOWNLOAD_DIR = "CAMS_Downloads\\Dust"
NAME = "dust"

VILNIUS_AREA = [54.95, 25.00, 54.40, 25.55]
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

dataset = "cams-europe-air-quality-reanalyses"


for year in years:
    for month in months:
        file_name = f"cams_{years}_{month}_{NAME}_validated.zip"
        target_path = os.path.join(DOWNLOAD_DIR, file_name)

        if os.path.exists(target_path):
            continue
        
        request = {
            "variable": ["dust"],
            "model": ["ensemble"],
            "level": ["500"],
            "type": ["validated_reanalysis"],
            "year": [year],
            "month": [month],
            "area": VILNIUS_AREA 
        }

        # request = {
        #     "variable": ["ammonia"],
        #     "model": ["ensemble"],
        #     "level": "500",
        #     "type": ["validated_reanalysis"],
        #     "year": [year],
        #     "month": [month],
        #     "time": ["00:00", "06:00", "12:00", "18:00"],
        #     "data_format": "netcdf_zip",
        #     "area": VILNIUS_AREA 
        # }

        try:
            remote = client.submit_and_wait_on_results(dataset, request)
            remote.download(target_path)
        except Exception as e:
            print(f"ERROR on {file_name}: {e}")