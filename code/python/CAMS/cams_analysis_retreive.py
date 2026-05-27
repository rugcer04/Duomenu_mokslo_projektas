import cdsapi
import os

years = ["2018", "2019", "2020", "2021", "2022", "2023"]
months = [f"{m:02d}" for m in range(1, 13)]

DOWNLOAD_DIR = "CAMS_Downloads\\Ammonia"
NAME = "Ammonia"

VILNIUS_AREA = [25.55, 54.40, 25, 54.95]
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

dataset = "cams-europe-air-quality-reanalyses"
client = cdsapi.Client()

for year in years:
    for month in months:

        file_name = f"cams_{year}_{month}_{NAME}.zip"
        target_path = os.path.join(DOWNLOAD_DIR, file_name)

        if os.path.exists(target_path):
            print(f"Skipping {year}, file already exists.")
            continue

        request = {
            "variable": ["ammonia"],
            "model": ["ensemble"],
            "level": [
                "0",
                "50",
                "250",
                "500"
            ],
            "type": ["validated_reanalysis"],
            "year": [year],
            "month": [month],
            "data_format": "netcdf_zip",
            "area": VILNIUS_AREA
        }

        try:
            client.retrieve(dataset, request, target_path)
        except Exception as e:
            print(f"ERROR on {file_name}: {e}")
