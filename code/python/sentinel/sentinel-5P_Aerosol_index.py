import ee
import geemap
import os

FOLDER_NAME = "S5P_Aerosol_Index"

# ee.Authenticate()  # Run this once to authenticate with Google Earth Engine
ee.Initialize(project='data-science-project-490323')
# ee.Initialize(project='PROJECT_ID')

lithuania = ee.FeatureCollection("FAO/GAUL/2015/level0") \
    .filter(ee.Filter.eq('ADM0_NAME', 'Lithuania'))
lithuania_geometry = lithuania.geometry()

collection  = ee.ImageCollection("COPERNICUS/S5P/OFFL/L3_AER_AI") \
    .filterDate('2018-07-04', '2026-03-13') \
    .filterBounds(lithuania_geometry) \
    .select('absorbing_aerosol_index')

first_image = collection.sort('system:time_start', True).first()
timestamp = first_image.date().format('YYYY-MM-dd').getInfo()
print(f"Visualising first timestamp: {timestamp}")
print(f"Total images in collection: {collection.size().getInfo()}")

output_dir = f'./sentinel_data/{FOLDER_NAME}'
os.makedirs(output_dir, exist_ok=True)

image_list = collection.sort('system:time_start').toList(collection.size())
n_images = image_list.size().getInfo()

print(f"Exporting {n_images} images...")

for i in range(n_images):
    img = ee.Image(image_list.get(i))

    date_str = img.date().format('YYYY-MM-dd_HH-mm-ss').getInfo()
    img_id = str(i).zfill(5)
    filename = f'aerosol_{img_id}_{date_str}.tif'
    output_path = os.path.join(output_dir, filename)

    if os.path.exists(output_path):
        print(f"[{i+1}/{n_images}] Skipping: {filename}")
        continue

    print(f"[{i+1}/{n_images}] Exporting: {filename}")
    geemap.ee_export_image(
        img.clip(lithuania_geometry),
        filename=output_path,
        scale=1113,
        region=lithuania_geometry,
        file_per_band=False
    )

print(f"Done! All files saved to: {output_dir}")