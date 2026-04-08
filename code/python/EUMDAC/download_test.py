import eumdac
import datetime
import shutil
import requests
import time
from eumdac.tailor_models import Chain, RegionOfInterest
import json
from unittest.mock import patch

CONSUMER_KEY = open('CONSUMER_KEY.txt').read().strip()
CONSUMER_SECRET = open('CONSUMER_SECRET.txt').read().strip()

bounding_box = '20.96, 53.89, 26.84, 56.45'
roi = RegionOfInterest(NSWE=[56.45, 53.89, 20.96, 26.84])

start = datetime.datetime(2021, 10, 20, 9, 0)
end = datetime.datetime(2021, 11, 1, 9, 0)

credentials = (CONSUMER_KEY, CONSUMER_SECRET)

token = eumdac.AccessToken(credentials)

print(f"This token '{token}' expires {token.expiration}")

datastore = eumdac.DataStore(token)
datatailor = eumdac.DataTailor(token)

selected_collection = datastore.get_collection('EO:EUM:DAT:METOP:GOMEL1')
chain = Chain(
    format='netcdf4',
    projection='geographic',
    roi = roi
)

print("Chain config:", json.dumps(chain.asdict(), indent=2))

products = selected_collection.search(
    bbox=bounding_box,
    dtstart=start, 
    dtend=end)

print(f'Found Datasets: {products.total_results} datasets for the given time range')

for product in products:
    print(str(product))

# product = next(iter(products), None)

# if product is None:
#     print("No products found.")
#     exit()

# print(f"Product ID: {product._id}")
# print(f"Collection ID: {product.collection._id}")

# customization = datatailor.new_customisation(product, chain=chain)
# print(f"Customization {customization._id} started...")
# while customization.status not in ('DONE', 'ERROR', 'KILLED'):
#     time.sleep(5)
#     print(f"Status: {customization.status}")

# for item in customization.outputs:
#     with item.open() as fsrc, open(item.name, mode='wb') as fdst:
#         shutil.copyfileobj(fsrc, fdst)
#         print(f"Downloaded: {item.name}")

# print('All downloads are finished.')
