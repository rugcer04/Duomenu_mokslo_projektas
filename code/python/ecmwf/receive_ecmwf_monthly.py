import os
from ecmwfapi import ECMWFDataServer

server = ECMWFDataServer()

years = range(2016, 2024)
months = range(1, 13)

for year in years:
    for month in months:
        target_file = f"lithuania_precip_{year}_{month:02d}.grib"
        
        if os.path.exists(target_file):
            continue
        
        if year == 2016 and month == 12: continue
        if year == 2017 and month in range(2, 11): continue

        start_date = f"{year}-{month:02d}-01"
        end_date = f"{year}-{month:02d}-31"
        if year == 2023 and month == 11: end_date = "2023-11-10"
        
        server.retrieve({
            "class": "ti",
            "dataset": "tigge",
            "date": f"{start_date}/to/{end_date}",
            "expver": "prod",
            "grid": "0.125/0.125",
            "area": "56.5/20.9/53.8/26.9",
            "levtype": "sfc",
            "origin": "ecmf",
            "param": "228228",
            "step": "6/12/18/24",
            "time": "00:00:00",
            "type": "cf",
            "target": target_file
        })