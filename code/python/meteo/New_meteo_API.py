import requests
import pandas as pd
import time
from datetime import datetime, timedelta

start_date = datetime(2017, 11, 1)
end_date = datetime(2026, 3, 1)
station_code = "vilniaus-ams"

all_observations = []
current_date = start_date

print("Pradedamas duomenų rinkimas...")

while current_date <= end_date:
    date_str = current_date.strftime('%Y-%m-%d')
    url = f"https://api.meteo.lt/v1/stations/{station_code}/observations/{date_str}"
    
    try:
        response = requests.get(url)
        
        if response.status_code == 200:
            day_data = response.json()
            all_observations.extend(day_data['observations'])
            print(f"Sėkmingai gauta: {date_str}")
        elif response.status_code == 404:
            print(f"Duomenų nėra: {date_str}")
        else:
            print(f"Klaida ties {date_str}: {response.status_code}")
            
    except Exception as e:
        print(f"Sisteminė klaida ties {date_str}: {e}")

    time.sleep(0.4) 
    current_date += timedelta(days=1)

df_full = pd.DataFrame(all_observations)

df_full['observationTimeUtc'] = pd.to_datetime(df_full['observationTimeUtc'])
print(f"\nBaigta! Surinkta eilučių: {len(df_full)}")

df_full.to_csv('Vilnius_nauji_meteo_duomenys_2017_2026.csv', index=False)