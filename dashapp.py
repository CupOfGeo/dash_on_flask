from app import create_app
import os
key = os.environ['GOOGLE_CRED']
with open('google_key.json') as file:
    file.write(key)
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'google_key.json'
server = create_app()