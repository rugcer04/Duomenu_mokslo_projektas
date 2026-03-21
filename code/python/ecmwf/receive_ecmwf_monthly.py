import os
from ecmwfapi import ECMWFDataServer

server = ECMWFDataServer()

years = range(2017, 2027)
months = range(1, 13)

for year in years:
    for month in months:
        target_file = os.path.join("DataGRIB", f"lithuania_precip_{year}_{month:02d}.grib")
        
        if os.path.exists(target_file):
            continue
        
        if year == 2006 and month < 11: continue
        if year == 2016 and month == 12: continue
        if year == 2017 and month in range(1, 11): continue
        if year == 2026 and month > 2: continue

        start_date = f"{year}-{month:02d}-01"
        end_date = f"{year}-{month:02d}-31"
        
        server.retrieve({
            "class": "ti",
            "dataset": "tigge",
            "date": f"{start_date}/to/{end_date}",
            "expver": "prod",
            "grid": "0.125/0.125",
            "area": "56.5/20.9/53.8/26.9",
            "levtype": "sfc",
            "origin": "ecmf",
            "param": "228228/167",
            "step": "24/30/36/42/48",
            "time": "00:00:00",
            "type": "cf",
            "target": target_file
        })
