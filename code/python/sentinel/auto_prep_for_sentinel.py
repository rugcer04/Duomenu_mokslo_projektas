from pathlib import Path
import pandas as pd
import xarray as xr
import numpy as np
import os
from concurrent.futures import ProcessPoolExecutor

CSV_OUTPUT = r'sentinel_data\lithuania_cloud_vilnius.csv'
FOLDER_TO_PROCESS = "S5P_Cloud"

base_path = Path(os.getcwd())
FOLDER = os.path.join(base_path, 'sentinel_data', FOLDER_TO_PROCESS)
nc_files = [f for f in os.listdir(FOLDER) if f.endswith('.nc')]

def prepare_dataset(file_path):
    vilnius_lon, vilnius_lat = 25.2797, 54.6872
    full_path = os.path.join(FOLDER, file_path)
    
    try:
        with xr.open_dataset(full_path) as ds:
            
            print(f"[{file_path}]: boxing.")
            ds_box = ds.sel(
                lon=slice(vilnius_lon - 0.25, vilnius_lon + 0.25),
                lat=slice(vilnius_lat - 0.25, vilnius_lat + 0.25))

            # print(f"[{file_path}]: grouping.")
            #ds_box = ds_box.groupby('time').mean()
            ds_regional = ds_box.mean(dim=['lat', 'lon'])
            
            print(f"[{file_path}]: to df.")
            df = ds_regional.to_dataframe()
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