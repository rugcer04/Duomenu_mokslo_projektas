import eumdac

CONSUMER_KEY = open('CONSUMER_KEY.txt').read().strip()
CONSUMER_SECRET = open('CONSUMER_SECRET.txt').read().strip()

credentials = (CONSUMER_KEY, CONSUMER_SECRET)

token = eumdac.AccessToken(credentials)

print(f"This token '{token}' expires {token.expiration}")

datastore = eumdac.DataStore(token)

look = 'EO:EUM:DAT:METOP:GOMEL1'

for collection in datastore.collections:
	print(collection)

collections = [col._id for col in datastore.collections]

if look in collections:
    print(f"Collection '{look}' is available")
