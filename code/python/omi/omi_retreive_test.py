import ee
from google_crc32c import value

ee.Authenticate()
ee.Initialize(project='data-science-project-490323')

test_point = ee.Geometry.Point([23.9, 55.3])

s5p_data = ee.ImageCollection('TOMS/MERGED') \
    .filterBounds(test_point) \
    .filterDate('2023-01-01', '2023-12-31') \
    .first() \
    .select('ozone')

print(s5p_data)

stats = s5p_data.reduceRegion(
    reducer=ee.Reducer.mean(),
    geometry=test_point,
    scale=1113.2,
).getInfo()

print(stats)