import eumdac

CONSUMER_KEY = open('CONSUMER_KEY.txt').read().strip()
CONSUMER_SECRET = open('CONSUMER_SECRET.txt').read().strip()

credentials = (CONSUMER_KEY, CONSUMER_SECRET)

token = eumdac.AccessToken(credentials)

print(f"This token '{token}' expires {token.expiration}")