# ECMWF Data Retrieval Guide

This folder contains scripts for retrieving meteorological data from the ECMWF (European Centre for Medium-Range Weather Forecasts) using their API. Specifically, these scripts target the **TIGGE** (THORPEX Interactive Grand Global Ensemble) dataset.

## Setup

1. **Install Dependencies**:
   Ensure you have the ECMWF API client installed:
   ```bash
   pip install ecmwf-api-client
   ```

2. **API Key**:
   You need an ECMWF account and an API key. 
   - Register at [ECMWF](https://apps.ecmwf.int/registration/).
   - Get your key from [API Key page](https://api.ecmwf.int/v1/key/).
   - Create a file named `.ecmwfapirc` in your home directory (e.g., `C:\Users\<YourUser>\.ecmwfapirc` on Windows or `~/.ecmwfapirc` on Linux/Mac) with the following content:
     ```json
     {
         "url": "https://api.ecmwf.int/v1",
         "key": "your-api-key-here",
         "email": "your-email@example.com"
     }
     ```

## Retrieval Scripts

- `receive_ecmwf_monthly.py`: Downloads data month-by-month for higher granularity or handling gaps.
- `receive_ecmwf_yearly.py`: Downloads full years of data in single GRIB files.

## Parameter Breakdown

The `server.retrieve({...})` function uses a dictionary of parameters. Here is what they mean:

| Parameter | Current Value | Description | Alternatives / Notes |
| :--- | :--- | :--- | :--- |
| `class` | `ti` | Dataset class. | `ti` stands for TIGGE. |
| `dataset` | `tigge` | The specific dataset name. | `tigge` is the primary one used here. |
| `date` | `YYYY-MM-DD/to/YYYY-MM-DD` | Time period for the data. | Can be a single date or a range. |
| `expver` | `prod` | Experiment version. | `prod` (Production) is standard for historical data. |
| `grid` | `0.125/0.125` | Spatial resolution (Lat/Lon). | `0.25/0.25`, `0.5/0.5`, etc. Smaller is higher resolution. |
| `area` | `56.5/20.9/53.8/26.9` | Bounding box (North/West/South/East). | Current range covers Lithuania. |
| `levtype` | `sfc` | Level type. | `sfc` (Surface), `pl` (Pressure levels). |
| `origin` | `ecmf` | Data provider/model source. | `ecmf` (ECMWF), `kwbc` (NCEP), `rjtd` (JMA), `babj` (CMA). |
| `param` | `228228` | Variable code. | `228228` is Total Precipitation. |
| `step` | `6/12/18/24` | Forecast steps (hours). | Intervals from the base time (e.g., `6/12/18/24/30...`). |
| `time` | `00:00:00` | Base time of the forecast. | `00:00:00` or `12:00:00` are most common. |
| `type` | `cf` | Type of data. | `cf` (Control Forecast), `pf` (Perturbed Forecast). |
| `target` | `filename.grib` | Local output path. | The file will be saved in GRIB format. |

## Common Variable Codes (`param`)

| Code | Variable Name |
| :--- | :--- |
| **228228** | Total Precipitation |
| **167** | 2m Temperature |
| **165** | 10m U wind component |
| **166** | 10m V wind component |
| **134** | Surface pressure |
| **168** | 2m Dewpoint temperature |

## Notes on Usage

- **Gaps**: The scripts include logic to skip existing files and handle specific date ranges where data might be missing or requires special handling (see `receive_ecmwf_monthly.py`).
- **Data Format**: The output is in `.grib` format. You can use libraries like `xarray` with `cfgrib` engine or `pygrib` to read these files in Python.
- **Limits**: ECMWF may have request limits. Downloading by month instead of year can help stay within session limits and allows for easier recovery if a download fails.

---
File created using Gemini CLI 0.32.1 (model: Gemini 3)