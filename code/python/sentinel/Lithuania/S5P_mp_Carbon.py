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

# Estimated laikas (KK pc ir wifi): iki 30 min.
FOLDER     = r'.\sentinel_data\S5P_Carbon' # Paskutinę dalį pakeiskit pagal produktą
N_WORKERS  = max(1, os.cpu_count() - 2)

# Taip pat čia reikia atžvelgti į vius šiuos 6 parametrus
DATE_START = '2018-06-28'
DATE_END   = '2026-03-13'
PRODUCT    = "COPERNICUS/S5P/OFFL/L3_CO"
PROJECT_ID = 'data-science-project-490323'
PRODUCT_BANDS = [
    'CO_column_number_density', 
    'H2O_column_number_density'
]
PRODUCT_SHORT = 'carbon'

def check_valid(image, lithuania_geometry):
    count = image.select(PRODUCT_BANDS[0]).reduceRegion(
        reducer=ee.Reducer.count(),
        geometry=lithuania_geometry,
        scale=1000,
        maxPixels=1e9
    ).get(PRODUCT_BANDS[0])
    return image.set('valid_pixel_count', count)

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
        .map(lambda image: check_valid(image, lithuania_geometry)) \
            .filter(ee.Filter.gt('valid_pixel_count', 0)) \
        .select(PRODUCT_BANDS)

    n = collection.size().getInfo()
    if n == 0:
        print(f"[{date_start} → {date_end}] No images, skipping")
        return None
    
    print(f"[{date_start} → {date_end}] Number of valid images: {n}")

    ds = xr.open_dataset(
        collection,
        engine='ee',
        crs='EPSG:4326',
        scale=0.01,
        geometry=lithuania_geometry,
        chunks={'time': 100},
        fast_time_slicing=True
    )

    actual_time = ds.sizes['time']
    actual_lat  = ds.sizes['lat']
    actual_lon  = ds.sizes['lon']

    time_chunk_safe = min(300, actual_time)
    
    lat_chunk_safe = ds.chunks['lat'][0] if ds.chunks and 'lat' in ds.chunks else actual_lat
    lon_chunk_safe = ds.chunks['lon'][0] if ds.chunks and 'lon' in ds.chunks else actual_lon

    lat_chunk_safe = min(lat_chunk_safe, actual_lat)
    lon_chunk_safe = min(lon_chunk_safe, actual_lon)

    dims_order = ds[PRODUCT_BANDS[0]].dims 

    chunk_map = {
        'time': time_chunk_safe,
        'lat': lat_chunk_safe,
        'lon': lon_chunk_safe
    }

    final_chunks = tuple(chunk_map[d] for d in dims_order)

    output_path = os.path.join(FOLDER, f'lithuania_{PRODUCT_SHORT}_{date_start}_{date_end}.nc')

    if os.path.exists(output_path):
        print(f"[{date_start} → {date_end}] Already exists, skipping")
        return output_path

    encoding_config = {
        band: {
            'zlib': True,
            'complevel': 5,
            'chunksizes': final_chunks
        } for band in PRODUCT_BANDS
    }

    with TqdmCallback(
        desc=f'Core {worker_id} [{date_start} → {date_end}]',
        position=worker_id,
        leave=True
    ), dask.config.set(scheduler='synchronous'):
        ds.to_netcdf(
            output_path,
            format='NETCDF4',
            encoding=encoding_config,
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
