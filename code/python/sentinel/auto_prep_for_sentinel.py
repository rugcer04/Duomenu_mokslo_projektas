from pathlib import Path
import pandas as pd
import xarray as xr
import numpy as np
import os
from concurrent.futures import ProcessPoolExecutor

#PARMAS=============================
# 'aer': "Aerosol_Index"
# 'clo': "Cloud"
# 'nit': "Nitrogen"
# 'oze': "Ozone"
# 'car': "Carbon"
# 'for': "Formaldehyde"
# 'sul': "Sulfur"
# 'met': "Methane"

ID = "clo"
LT_TIME = True

# "Vilnius"
# "Klaipeda"
# "Ryga"
CITY = 'Ryga'
#===================================

ALL_PRODUCTS = {'aer': "Aerosol_Index",
                'clo': "Cloud",
                'nit': "Nitrogen",
                'oze': "Ozone",
                'car': "Carbon",
                'for': "Formaldehyde",
                'sul': "Sulfur",
                'met': "Methane"}
lon_lat_bank = {
        "Vilnius": {"lon": 25.2797, "lat": 54.6872, "file_end": 'vilnius'},
        "Klaipeda": {"lon": 21.1333, "lat": 55.7167, "file_end": 'klaipeda'},
        "Ryga": {"lon": 24.1052, "lat": 56.9496, "file_end": 'ryga'}
    }
COORD = lon_lat_bank[CITY]
PRODUCT_NAME = ALL_PRODUCTS[ID]
CSV_OUTPUT = f'sentinel_data\\lithuania_{PRODUCT_NAME.lower()}_{COORD["file_end"]}.csv'

if CITY == 'Ryga':
    FOLDER_TO_PROCESS = f"S5P_{PRODUCT_NAME}_Ryga"
else:
    FOLDER_TO_PROCESS = f"S5P_{PRODUCT_NAME}"

if CITY == 'Ryga' and ID == 'aer':
    FOLDER_TO_PROCESS = f"S5P_Aerosol_Ryga"

base_path = Path(os.getcwd())
FOLDER = os.path.join(base_path, 'sentinel_data', FOLDER_TO_PROCESS)
nc_files = [f for f in os.listdir(FOLDER) if f.endswith('.nc')]

def prepare_dataset(file_path):
    full_path = os.path.join(FOLDER, file_path)
    
    try:
        with xr.open_dataset(full_path) as ds:
            
            print(f"[{file_path}]: boxing.")
            ds_box = ds.sel(
                lon=slice(COORD["lon"] - 0.25, COORD["lon"] + 0.25),
                lat=slice(COORD["lat"] - 0.25, COORD["lat"] + 0.25))

            # print(f"[{file_path}]: grouping.")
            #ds_box = ds_box.groupby('time').mean()
            ds_regional = ds_box.mean(dim=['lat', 'lon'])
            
            print(f"[{file_path}]: to df.")
            df = ds_regional.to_dataframe()
            
            if LT_TIME:
                if df.index.tz is None:
                    df.index = df.index.tz_localize('UTC')
                df.index = df.index.tz_convert('Europe/Vilnius')

            df_new = df.groupby(df.index.floor('D')).mean().reset_index()
            
            print(f"Finished: {file_path}")
            return df_new
            
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return None

if __name__ == '__main__':
    df_list = []
    
    print(f"Starting parallel processing of {len(nc_files)} files.")
    
    with ProcessPoolExecutor(max_workers=4) as executor:
        results = list(executor.map(prepare_dataset, nc_files))

    df_list = [df for df in results if df is not None]

    if df_list:
        print("Combining results.")
        df_final = pd.concat(df_list, ignore_index=True)

        output_path = os.path.join(base_path, CSV_OUTPUT)
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        df_final.to_csv(output_path, index=False)
        print(f"Saved to {output_path}")