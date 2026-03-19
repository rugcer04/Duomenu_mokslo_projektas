import os
import logging
from concurrent.futures import ThreadPoolExecutor
import cdsapi

# Konfigūracija
logging.basicConfig(level="INFO", format='%(asctime)s - %(levelname)s - %(message)s')
DOWNLOAD_DIR = "CAMS_Methane_Data"
DATASET = "cams-global-reanalysis-eac4"
MAX_WORKERS = 3 

os.makedirs(DOWNLOAD_DIR, exist_ok=True)
client = cdsapi.Client()

def download_year(year):
    """Atsiunčia konkrečių metų metano duomenis."""
    file_name = f"cams_methane_{year}.grib"
    target_path = os.path.join(DOWNLOAD_DIR, file_name)

    if os.path.exists(target_path):
        logging.info(f"Praleidžiama: {file_name} jau egzistuoja.")
        return

    # Nustatome datas pagal metus (atsižvelgiant į tavo rėžius)
    start_date = f"{year}-01-01"
    end_date = f"{year}-12-31"
    
    # Korekcija pirmiems ir paskutiniems metams pagal tavo užklausą
    if year == "2017": start_date = "2017-11-01"
    if year == "2025": end_date = "2025-08-31"

    request = {
        "variable": ["methane_chemistry"],
        "model_level": ["60"],
        "date": [f"{start_date}/{end_date}"],
        "time": ["00:00"],
        "data_format": "grib",
        "area": [54.95, 25, 54.4, 25.55]
    }

    try:
        logging.info(f"Paleidžiama užklausa metams: {year}")
        client.retrieve(DATASET, request, target_path)
        logging.info(f"Sėkmingai baigta: {file_name}")
    except Exception as e:
        logging.error(f"Klaida siunčiant {year} metus: {e}")

if __name__ == "__main__":
    # Metų sąrašas pagal tavo nurodytą periodą (2017-2025)
    years = [str(y) for y in range(2017, 2026)]

    logging.info(f"Pradedamas siuntimas naudojant {MAX_WORKERS} gijas...")
    
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        executor.map(download_year, years)

    logging.info("Visi darbai baigti.")

