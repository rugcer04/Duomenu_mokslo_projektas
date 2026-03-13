import os
from ecmwfapi import ECMWFDataServer

server = ECMWFDataServer()

YEAR = 2016
MONTH = 12

GRID = "0.125/0.125"
ORIGIN = "kwbc"

# FOLDER = "DataGRIB"
FOLDER = "DataGRIB_kwbc"

target_file = os.path.join(FOLDER, f"lithuania_precip_{YEAR}_{MONTH:02d}.grib")
start_date = f"{YEAR}-{MONTH:02d}-01"
end_date = f"{YEAR}-{MONTH:02d}-31"

if not os.path.exists(target_file):
    server.retrieve({
        "class": "ti",
        "dataset": "tigge",
        "date": f"{start_date}/to/{end_date}",
        "expver": "prod",
        "grid": GRID,
        "area": "56.5/20.9/53.8/26.9",
        "levtype": "sfc",
        "origin": ORIGIN,
        "param": "228228/167",
        "step": "6/12/18/24",
        "time": "00:00:00",
        "type": "cf",
        "target": target_file
    })
