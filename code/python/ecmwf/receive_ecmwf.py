import os
from ecmwfapi import ECMWFDataServer

server = ECMWFDataServer()

years = range(2006, 2024)

for year in years:
    target_file = f"lithuania_precip_{year}.grib"
    
    if os.path.exists(target_file):
        continue
    
    start_date = f"{year}-01-01"
    end_date = f"{year}-12-31"
    if year == 2006: start_date = "2006-11-01"
    if year == 2023: end_date = "2023-11-10"

    server.retrieve({
        "class": "ti",
        "dataset": "tigge",
        "date": f"{start_date}/to/{end_date}",
        "expver": "prod",
        "grid": "0.5/0.5",
        "area": "56.5/20.9/53.8/26.9",
        "levtype": "sfc",
        "origin": "ecmf",
        "param": "228228",
        "step": "6/12/18/24",
        "time": "00:00:00",
        "type": "cf",
        "target": target_file
    })

# server.retrieve({
#     "class": "ti",
#     "dataset": "tigge",
#     "date": "2006-11-01/to/2023-11-10",
#     "expver": "prod",
#     "grid": "0.5/0.5",
#     "area": "56.5/20.9/53.8/26.9",
#     "levtype": "sfc",
#     "origin": "ecmf",
#     "param": "228228",
#     "step": "6/12/18/24",
#     "time": "00:00:00",
#     "type": "cf",
#     "target": "tigge_2006-11-01_to_2023-11-10.grib"
# })