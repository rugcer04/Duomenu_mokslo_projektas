import ee
import geemap
import xarray as xr
import dask
import os
import warnings
import numpy as np
from tqdm.dask import TqdmCallback

warnings.filterwarnings('ignore', message=".*cfgrib.*")
warnings.filterwarnings('ignore', message=".*eccodes.*")
warnings.filterwarnings('ignore', message=".*_eccodes.*")

FOLDER  = r'.\sentinel_data\S5P_Aerosol_Index'
CHUNK_SIZE = 500

ee.Initialize(project='data-science-project-490323')

os.makedirs(FOLDER, exist_ok=True)

lithuania = ee.FeatureCollection("FAO/GAUL/2015/level0") \
    .filter(ee.Filter.eq('ADM0_NAME', 'Lithuania'))
lithuania_geometry = lithuania.geometry()

bounds = lithuania_geometry.bounds().getInfo()['coordinates'][0]
lon_min, lat_min = bounds[0]
lon_max, lat_max = bounds[2]
print(f"Lithuania bounds: lon [{lon_min:.2f}, {lon_max:.2f}], lat [{lat_min:.2f}, {lat_max:.2f}]")

collection = ee.ImageCollection("COPERNICUS/S5P/OFFL/L3_AER_AI") \
    .filterDate('2018-07-04', '2026-03-13') \
    .filterBounds(lithuania_geometry) \
    .select('absorbing_aerosol_index')

n_images = collection.size().getInfo()
print(f"Total images: {n_images}")

ds = xr.open_dataset(
    collection,
    engine='ee',
    crs='EPSG:4326',
    scale=0.01,
    geometry=lithuania_geometry,
    chunks={'time': CHUNK_SIZE},
    fast_time_slicing=True
)

print(ds.chunks)
print(ds['absorbing_aerosol_index'].encoding)

n_lon = ds.sizes['lon']
n_lat = ds.sizes['lat']

print(f"Dataset size: {ds.nbytes / 1e9:.1f} GB")
print(f"Chunks: time={CHUNK_SIZE}, lon={n_lon}, lat={n_lat}")
print(ds)

date_start = str(ds.time.min().values)[:10]
date_end   = str(ds.time.max().values)[:10]
output_path = os.path.join(FOLDER, f'lithuania_aerosol_{date_start}_{date_end}.nc')

time_chunk = ds.chunks['time'][0]
lon_chunk  = ds.chunks['lon'][0]
lat_chunk  = ds.chunks['lat'][0]

print(f"Internal chunks — time: {time_chunk}, lon: {lon_chunk}, lat: {lat_chunk}")


with TqdmCallback(desc='Downloading'), dask.config.set(scheduler='synchronous'):
    ds.to_netcdf(
        output_path,
        format='NETCDF4',
        encoding={
            'absorbing_aerosol_index': {
                'zlib': True,
                'complevel': 5,
                'chunksizes': (time_chunk, lon_chunk, lat_chunk)
            }
        },
        compute=True
    )

print(f"Saved {output_path}")