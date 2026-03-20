from pathlib import Path
import pandas as pd
import xarray as xr
import numpy as np
import os
from concurrent.futures import ProcessPoolExecutor

FOLDER_TO_PROCESS = "particulate_matter_10um"
CSV_OUTPUT = f'cams_data\\lithuania_{FOLDER_TO_PROCESS}_vilnius.csv'

base_path = Path(os.getcwd())
FOLDER = os.path.join(base_path, 'CAMS unzip', FOLDER_TO_PROCESS)
nc_files = [f for f in os.listdir(FOLDER) if f.endswith('.nc')]

SHIFT = 2

def prepare_dataset(file_path):
    full_path = os.path.join(FOLDER, file_path)
    
    try:
        with xr.open_dataset(full_path) as ds:
            
            print(f"[{file_path}]: Aggregating.")
            ds_regional = ds.mean(dim=['lat', 'lon', ])

            print(f"[{file_path}]: to df.")
            df = ds_regional.to_dataframe()

            df.index = df.index + pd.Timedelta(hours=SHIFT)

            df_new = df.groupby(df.index.floor('D')).mean().reset_index()
            
            print(f"Finished: {file_path}")
            return df_new
            
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return None

if __name__ == '__main__':
    df_list = []
    
    print(f"Starting parallel processing of {len(nc_files)} files.")
    
    with ProcessPoolExecutor(max_workers=6) as executor:
        results = list(executor.map(prepare_dataset, nc_files))

    df_list = [df for df in results if df is not None]

    if df_list:
        print("Combining results.")
        df_final = pd.concat(df_list, ignore_index=True)

        output_path = os.path.join(base_path, CSV_OUTPUT)
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        df_final.to_csv(output_path, index=False)
        print(f"Saved to {output_path}")