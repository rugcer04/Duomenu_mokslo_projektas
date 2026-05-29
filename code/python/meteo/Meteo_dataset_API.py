import requests
import pandas as pd
import time
from datetime import datetime, timedelta
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# start_date = datetime(2013, 10, 11)
# end_date = datetime(2026, 3, 1)
start_date = datetime(2017, 11, 1)
end_date = datetime(2026, 3, 1)
# station_code = "vilniaus-ams"
station_code = "kauno-ams"

session = requests.Session()
retries = Retry(total=5, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
session.mount('https://', HTTPAdapter(max_retries=retries))

all_observations = []
current_date = start_date

print(f"Pradedamas duomenų rinkimas nuo {start_date.date()} iki {end_date.date()}...")

while current_date <= end_date:
    date_str = current_date.strftime('%Y-%m-%d')
    url = f"https://api.meteo.lt/v1/stations/{station_code}/observations/{date_str}"
    
    try:
        response = session.get(url, timeout=5)
        
        if response.status_code == 200:
            day_data = response.json()
            if 'observations' in day_data:
                all_observations.extend(day_data['observations'])
                print(f"Sėkmingai gauta: {date_str} (Iš viso: {len(all_observations)})")
        elif response.status_code == 404:
            print(f"Duomenų nėra: {date_str}")
        else:
            print(f"Serverio klaida {date_str}: {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"Ryšio klaida ties {date_str}. Bandysime tęsti... Klaida: {e}")
        time.sleep(5)
        continue

    time.sleep(0.5) 
    current_date += timedelta(days=1)

if all_observations:
    df_full = pd.DataFrame(all_observations)
    if 'observationTimeUtc' in df_full.columns:
        df_full['observationTimeUtc'] = pd.to_datetime(df_full['observationTimeUtc'])
    
    filename = f'Kauno_meteo_{start_date.year}_{end_date.year}.csv'
    df_full.to_csv(filename, index=False)
    print(f"\nBaigta! Surinkta eilučių: {len(df_full)}. Failas: {filename}")
else:
    print("\nNepavyko surinkti jokių duomenų.")