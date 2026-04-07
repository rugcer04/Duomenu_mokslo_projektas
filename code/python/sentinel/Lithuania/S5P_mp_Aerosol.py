import ee
import xarray as xr
import dask
import os
import warnings
import numpy as np
from tqdm.dask import TqdmCallback
from concurrent.futures import ProcessPoolExecutor, as_completed
from tqdm import tqdm

warnings.filterwarnings('ignore', message=".*cfgrib.*")
warnings.filterwarnings('ignore', message=".*eccodes.*")
warnings.filterwarnings('ignore', message=".*_eccodes.*")

FOLDER     = r'.\sentinel_data\S5P_Aerosol_Index' # Paskutinę dalį pakeiskit pagal produktą
N_WORKERS  = max(1, os.cpu_count() - 2)

# Taip pat čia reikia atžvelgti į vius šiuos 5 parametrus
DATE_START = '2018-07-04' # Taip pat čia reikia atžvelgti,
DATE_END   = '2026-03-13'
PRODUCT    = "COPERNICUS/S5P/OFFL/L3_AER_AI"
PROJECT_ID = 'data-science-project-490323'
PRODUCT_BANDS = ['absorbing_aerosol_index']

def split_date_range(start, end, n):
    start_dt = np.datetime64(start)
    end_dt   = np.datetime64(end)
    delta    = (end_dt - start_dt) / n
    periods  = []
    for i in range(n):
        p_start = str(start_dt + i * delta)[:10]
        p_end   = str(start_dt + (i + 1) * delta)[:10]
        periods.append((p_start, p_end))
    return periods

def download_period(args):
    """Each worker runs this — fully synchronous inside."""
    date_start, date_end, worker_id = args

    warnings.filterwarnings('ignore', message=".*cfgrib.*")
    warnings.filterwarnings('ignore', message=".*eccodes.*")
    warnings.filterwarnings('ignore', message=".*_eccodes.*")
    warnings.filterwarnings('ignore', message=".*separate the stored chunks.*")

    ee.Initialize(project=PROJECT_ID)

    lithuania = ee.FeatureCollection("FAO/GAUL/2015/level0") \
        .filter(ee.Filter.eq('ADM0_NAME', 'Lithuania'))
    lithuania_geometry = lithuania.geometry()

    collection = ee.ImageCollection(PRODUCT) \
        .filterDate(date_start, date_end) \
        .filterBounds(lithuania_geometry) \
        .select(PRODUCT_BANDS)

    n = collection.size().getInfo()
    if n == 0:
        print(f"[{date_start} → {date_end}] No images, skipping")
        return None

    ds = xr.open_dataset(
        collection,
        engine='ee',
        crs='EPSG:4326',
        scale=0.01,
        geometry=lithuania_geometry,
        chunks={'time': 200},
        fast_time_slicing=True
    )

    time_chunk = ds.chunks['time'][0]
    lon_chunk  = ds.chunks['lon'][0]
    lat_chunk  = ds.chunks['lat'][0]

    output_path = os.path.join(FOLDER, f'lithuania_aerosol_{date_start}_{date_end}.nc')

    if os.path.exists(output_path):
        print(f"[{date_start} → {date_end}] Already exists, skipping")
        return output_path

    with TqdmCallback(
        desc=f'Core {worker_id} [{date_start} → {date_end}]',
        position=worker_id,
        leave=True
    ), dask.config.set(scheduler='synchronous'):
        ds.to_netcdf(
            output_path,
            format='NETCDF4',
            encoding={
                PRODUCT_BANDS[0]: {
                    'zlib': True,
                    'complevel': 5,
                    'chunksizes': (time_chunk, lon_chunk, lat_chunk)
                }
            },
            compute=True
        )

    print(f"[{date_start} → {date_end}] Saved → {output_path}")
    return output_path


if __name__ == '__main__':
    os.makedirs(FOLDER, exist_ok=True)

    periods = split_date_range(DATE_START, DATE_END, N_WORKERS)
    print(f"Splitting into {N_WORKERS} periods across {N_WORKERS} cores:")
    for p in periods:
        print(f"  {p[0]} → {p[1]}")

    args = [(s, e, i) for i, (s, e) in enumerate(periods)]

    with ProcessPoolExecutor(max_workers=N_WORKERS) as executor:
        futures = {executor.submit(download_period, arg): arg for arg in args}
        for future in as_completed(futures):
            arg = futures[future]
            try:
                future.result()
            except Exception as ex:
                print(f"[{arg[0]} → {arg[1]}] FAILED: {ex}")
