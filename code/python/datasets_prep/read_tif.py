import rasterio
import numpy as np
from rasterio.plot import show
import matplotlib.pyplot as plt

with rasterio.open('sentinel_data\\S5P_Aerosol_Index\\aerosol_00005_2018-07-04_08-51-26.tif') as src:
    data = src.read(1)
    transform = src.transform
    crs = src.crs
    bounds = src.bounds

print(f"Shape: {data.shape}")
print(f"CRS: {crs}")
print(f"Bounds: {bounds}")
print(f"Min: {np.nanmin(data)}, Max: {np.nanmax(data)}")


with rasterio.open('sentinel_data\\S5P_Aerosol_Index\\aerosol_00005_2018-07-04_08-51-26.tif') as src:
    fig, ax = plt.subplots(figsize=(8, 6))
    show(src, ax=ax, cmap='RdYlBu_r', title='Aerosol Index - Lithuania')
    plt.colorbar(ax.images[0], ax=ax, label='Absorbing Aerosol Index')
    plt.show()